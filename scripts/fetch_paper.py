#!/usr/bin/env python3
"""
論文PDFをダウンロードし、引用論文を芋蔓式に追加するスクリプト。

使い方:
  # URLから論文を取得（引用論文も一覧表示）
  python scripts/fetch_paper.py https://arxiv.org/abs/2506.16383

  # キーワードで論文を検索（上位20件表示）
  python scripts/fetch_paper.py --search "argument mining"

  # サーベイ論文に絞って検索（◆マーク付き）
  python scripts/fetch_paper.py --search "argument mining" --survey
"""

import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

RAW_PAPERS_DIR = Path(__file__).parent.parent / "raw" / "papers"
SS_API = "https://api.semanticscholar.org/graph/v1"
ARXIV_API = "http://export.arxiv.org/api/query"
FIELDS = "title,year,authors,externalIds,openAccessPdf,referenceCount"
SURVEY_WORDS = {"survey", "review", "overview", "tutorial", "サーベイ"}
ARXIV_NS = "http://www.w3.org/2005/Atom"


# ── API ──────────────────────────────────────────────────────────────────────

def ss_get(path: str, params: dict = {}) -> dict | None:
    """Semantic Scholar APIを呼ぶ（APIキーがあれば使用、なければフォールバック）"""
    import os
    api_key = os.environ.get("SEMANTICSCHOLAR_API_KEY")
    headers = {"x-api-key": api_key} if api_key else {}
    time.sleep(1)
    for wait in [0, 15, 30, 60]:
        if wait:
            print(f"レート制限: {wait}秒待機中...")
            time.sleep(wait)
        resp = requests.get(f"{SS_API}{path}", params=params, headers=headers, timeout=15)
        if resp.status_code != 429:
            break
    if not resp.ok:
        return None
    return resp.json()


# ── arXiv API ────────────────────────────────────────────────────────────────

def arxiv_search(query: str, limit: int = 20) -> list[dict]:
    """arXiv APIで論文を検索してリストを返す（CS分野に限定）"""
    time.sleep(1)
    # cs.CL / cs.AI / cs.IR に限定して無関係な分野を除外
    search_query = f"all:{query} AND (cat:cs.CL OR cat:cs.AI OR cat:cs.IR OR cat:cs.HC)"
    resp = requests.get(ARXIV_API, params={
        "search_query": search_query,
        "max_results": limit,
        "sortBy": "relevance",
    }, timeout=15)
    if not resp.ok:
        return []

    root = ET.fromstring(resp.text)
    papers = []
    for entry in root.findall(f"{{{ARXIV_NS}}}entry"):
        # arXiv ID
        id_url = entry.findtext(f"{{{ARXIV_NS}}}id", "")
        arxiv_id = id_url.split("/abs/")[-1].split("v")[0]

        # PDF link
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        # authors
        authors = [
            a.findtext(f"{{{ARXIV_NS}}}name", "")
            for a in entry.findall(f"{{{ARXIV_NS}}}author")
        ]

        # year from published date
        published = entry.findtext(f"{{{ARXIV_NS}}}published", "")
        year = int(published[:4]) if published else None

        papers.append({
            "title": entry.findtext(f"{{{ARXIV_NS}}}title", "").strip().replace("\n", " "),
            "year": year,
            "authors": [{"name": a} for a in authors],
            "externalIds": {"ArXiv": arxiv_id},
            "openAccessPdf": {"url": pdf_url},
            "referenceCount": None,
            "_source": "arxiv",
        })
    return papers


# ── 検索モード ────────────────────────────────────────────────────────────────

def is_survey(paper: dict) -> bool:
    title = paper.get("title", "").lower()
    return any(w in title for w in SURVEY_WORDS)


def search_papers(query: str, limit: int = 20, survey_only: bool = False) -> None:
    """キーワードで論文を検索し、選択してダウンロード"""
    q = query + (" survey" if survey_only else "")
    print(f"検索中: 「{q}」（上位{limit}件）\n")

    # Semantic Scholar → 失敗したらarXivにフォールバック
    data = ss_get("/paper/search", {"query": q, "limit": limit, "fields": FIELDS})
    if data and data.get("data"):
        papers = data["data"]
        source = "Semantic Scholar"
    else:
        print("Semantic Scholar不可 → arXiv APIで検索中...")
        papers = arxiv_search(q, limit)
        source = "arXiv"
        if not papers:
            print("結果が見つかりませんでした。")
            return

    print(f"({source})")

    # survey_onlyのときはサーベイ論文を上に並び替え
    if survey_only:
        papers = sorted(papers, key=lambda p: (not is_survey(p),))

    print(f"検索結果 ({len(papers)}件, ★=PDF入手可, ◆=サーベイ):\n")
    for i, p in enumerate(papers, 1):
        pdf_mark = "★" if has_pdf(p) else " "
        survey_mark = "◆" if is_survey(p) else " "
        authors = ", ".join(a["name"] for a in p.get("authors", [])[:2])
        suffix = " et al." if len(p.get("authors", [])) > 2 else ""
        title = p.get("title", "(タイトル不明)")[:65]
        year = p.get("year", "?")
        refs = p.get("referenceCount")
        refs_str = f" [{refs}refs]" if refs else ""
        print(f"  [{i:2}] {pdf_mark}{survey_mark} {title} ({year}){refs_str}")
        print(f"        {authors}{suffix}")

    print("\nダウンロードする番号を入力 (例: 1,3 / 1-5 / all / Enterでスキップ): ", end="")
    choice = input().strip()
    if not choice:
        print("スキップしました。")
        return

    selected = parse_selection(choice, len(papers))
    print(f"\n{len(selected)}件をダウンロードします...\n")

    ok, ng = 0, 0
    for i in selected:
        p = papers[i]
        print(f"[{i+1}] {p.get('title', '')[:60]}")
        if not has_pdf(p):
            print("  PDF非公開のためスキップ")
            ng += 1
            continue
        path = download_pdf(p)
        if path:
            ok += 1
        else:
            ng += 1

    print(f"\n完了: {ok}件ダウンロード, {ng}件スキップ")
    if ok:
        print("次のステップ: Claude Codeに「raw/papers/ の新しいPDFをwiki記事にして」と依頼してください。")


# ── URL解決 ───────────────────────────────────────────────────────────────────

def resolve_paper(query: str) -> dict | None:
    """URLまたはタイトルからSemantic Scholar論文メタデータを返す"""

    # arXiv abs / pdf URL
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s/?#]+)", query)
    if m:
        arxiv_id = m.group(1).rstrip(".pdf")
        data = ss_get(f"/paper/arXiv:{arxiv_id}", {"fields": FIELDS})
        if data:
            return data

    # ACL Anthology URL → defuddleでタイトル取得してフォールバック
    if "aclanthology.org" in query:
        try:
            import subprocess
            result = subprocess.run(
                ["defuddle", "parse", query, "-p", "title"],
                capture_output=True, text=True, timeout=15
            )
            title = result.stdout.strip()
            if title:
                query = title
                print(f"タイトルを取得: {title}")
        except Exception:
            pass

    # タイトル検索（候補が複数なら選ばせる）
    data = ss_get("/paper/search", {"query": query, "limit": 5, "fields": FIELDS})
    if not data or not data.get("data"):
        return None

    papers = data["data"]
    if len(papers) == 1:
        return papers[0]

    print("\n候補が複数あります:")
    for i, p in enumerate(papers):
        authors = ", ".join(a["name"] for a in p.get("authors", [])[:2])
        print(f"  [{i+1}] {p['title']} ({p.get('year', '?')}) — {authors}")
    choice = input("番号を選択 [1]: ").strip() or "1"
    return papers[int(choice) - 1]


# ── PDF ───────────────────────────────────────────────────────────────────────

def has_pdf(paper: dict) -> bool:
    oa = paper.get("openAccessPdf") or {}
    if oa.get("url"):
        return True
    return bool((paper.get("externalIds") or {}).get("ArXiv"))


def get_pdf_url(paper: dict) -> str | None:
    oa = paper.get("openAccessPdf") or {}
    if oa.get("url"):
        return oa["url"]
    arxiv_id = (paper.get("externalIds") or {}).get("ArXiv")
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}"
    return None


def download_pdf(paper: dict) -> Path | None:
    pdf_url = get_pdf_url(paper)
    if not pdf_url:
        return None

    arxiv_id = (paper.get("externalIds") or {}).get("ArXiv")
    if arxiv_id:
        filename = f"{arxiv_id}.pdf"
    else:
        slug = re.sub(r"[^\w\s-]", "", paper["title"].lower())
        slug = re.sub(r"[\s_]+", "-", slug)[:60]
        filename = f"{slug}.pdf"

    out_path = RAW_PAPERS_DIR / filename
    if out_path.exists():
        print(f"  既存: {out_path.name}")
        return out_path

    print(f"  ダウンロード中: {pdf_url}")
    resp = requests.get(pdf_url, timeout=30, allow_redirects=True)
    if not resp.ok or "application/pdf" not in resp.headers.get("content-type", ""):
        print(f"  PDFの取得に失敗しました (HTTP {resp.status_code})")
        return None

    out_path.write_bytes(resp.content)
    print(f"  ✓ 保存: {out_path.name} ({len(resp.content) // 1024} KB)")
    return out_path


# ── 引用論文 ─────────────────────────────────────────────────────────────────

def get_references(paper_id: str) -> list[dict]:
    refs = []
    offset = 0
    limit = 100
    ref_fields = "title,year,authors,externalIds,openAccessPdf"

    while True:
        data = ss_get(
            f"/paper/{paper_id}/references",
            {"fields": ref_fields, "limit": limit, "offset": offset}
        )
        if not data:
            break
        batch = [r["citedPaper"] for r in data.get("data", []) if r.get("citedPaper")]
        refs.extend(batch)
        if "next" not in data or len(batch) < limit:
            break
        offset = data["next"]

    return refs


def display_references(refs: list[dict]) -> None:
    print(f"\n引用論文一覧 ({len(refs)}件, ★=PDF入手可, ◆=サーベイ):\n")
    for i, p in enumerate(refs, 1):
        pdf_mark = "★" if has_pdf(p) else " "
        survey_mark = "◆" if is_survey(p) else " "
        authors = ", ".join(a["name"] for a in p.get("authors", [])[:2])
        suffix = " et al." if len(p.get("authors", [])) > 2 else ""
        title = p.get("title", "(タイトル不明)")[:70]
        year = p.get("year", "?")
        print(f"  [{i:3}] {pdf_mark}{survey_mark} {title} ({year}) — {authors}{suffix}")


def parse_selection(s: str, total: int) -> list[int]:
    s = s.strip().lower()
    if s == "all":
        return list(range(total))
    indices = set()
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            indices.update(range(int(a) - 1, int(b)))
        elif part.isdigit():
            indices.add(int(part) - 1)
    return sorted(i for i in indices if 0 <= i < total)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    # --search モード
    if "--search" in args:
        args.remove("--search")
        survey_only = "--survey" in args
        if survey_only:
            args.remove("--survey")
        query = " ".join(args)
        if not query:
            print("検索クエリを指定してください。")
            sys.exit(1)
        search_papers(query, limit=20, survey_only=survey_only)
        return

    # URL / タイトル解決モード
    query = " ".join(args)
    RAW_PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"論文を解決中: {query}")
    paper = resolve_paper(query)
    if not paper:
        print("論文が見つかりませんでした。")
        sys.exit(1)

    authors = ", ".join(a["name"] for a in paper.get("authors", [])[:3])
    print(f"\n論文: {paper['title']}")
    print(f"著者: {authors} ({paper.get('year', '?')})")
    print(f"引用数: {paper.get('referenceCount', '?')}件\n")

    download_pdf(paper)

    ref_count = paper.get("referenceCount", 0)
    if ref_count == 0:
        print("引用論文なし。終了します。")
        return

    print(f"\n引用論文を取得中 ({ref_count}件)...")
    refs = get_references(paper["paperId"])

    if not refs:
        print("引用論文を取得できませんでした。")
        return

    display_references(refs)

    print("\n追加する番号を入力 (例: 1,3,5 / 1-10 / all / Enterでスキップ): ", end="")
    choice = input().strip()
    if not choice:
        print("スキップしました。")
        return

    selected = parse_selection(choice, len(refs))
    print(f"\n{len(selected)}件をダウンロードします...\n")

    ok, ng = 0, 0
    for i in selected:
        p = refs[i]
        print(f"[{i+1}] {p.get('title', '')[:60]}")
        if not has_pdf(p):
            print("  PDF非公開のためスキップ")
            ng += 1
            continue
        path = download_pdf(p)
        if path:
            ok += 1
        else:
            ng += 1

    print(f"\n完了: {ok}件ダウンロード, {ng}件スキップ")
    if ok:
        print("次のステップ: Claude Codeに「raw/papers/ の新しいPDFをwiki記事にして」と依頼してください。")


if __name__ == "__main__":
    main()
