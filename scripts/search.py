#!/usr/bin/env python3
"""
wiki検索エンジン — CLI経由でLLMにツールとして渡せる。
使い方:
  python search.py "議論マイニング"
  python search.py "topic shift" --top 5
  python search.py "仮説1" --dir wiki/concepts
"""

import os
import re
import sys
import argparse
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
RAW_ROOT = Path(__file__).parent.parent / "raw"


def search_files(query: str, root: Path, top_n: int = 10) -> list[dict]:
    results = []
    terms = query.lower().split()

    for md_file in root.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        text_lower = text.lower()
        score = sum(text_lower.count(t) for t in terms)
        if score == 0:
            continue

        # タイトル行を抽出
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1) if title_match else md_file.stem

        # 最初のマッチ周辺のスニペット
        first_match_pos = min(
            (text_lower.find(t) for t in terms if t in text_lower),
            default=0
        )
        start = max(0, first_match_pos - 80)
        end = min(len(text), first_match_pos + 160)
        snippet = text[start:end].replace("\n", " ").strip()

        rel_path = md_file.relative_to(root.parent)
        results.append({
            "score": score,
            "path": str(rel_path),
            "title": title,
            "snippet": snippet,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


def main():
    parser = argparse.ArgumentParser(description="Wiki検索エンジン")
    parser.add_argument("query", help="検索クエリ")
    parser.add_argument("--top", type=int, default=5, help="表示件数 (default: 5)")
    parser.add_argument("--dir", choices=["wiki", "raw", "all"], default="all",
                        help="検索対象ディレクトリ")
    args = parser.parse_args()

    roots = []
    if args.dir in ("wiki", "all"):
        roots.append(WIKI_ROOT)
    if args.dir in ("raw", "all"):
        roots.append(RAW_ROOT)

    all_results = []
    for root in roots:
        if root.exists():
            all_results.extend(search_files(args.query, root, args.top))

    all_results.sort(key=lambda x: x["score"], reverse=True)
    all_results = all_results[:args.top]

    if not all_results:
        print(f"「{args.query}」に一致するドキュメントが見つかりませんでした。")
        return

    print(f"=== 検索結果: 「{args.query}」 ({len(all_results)}件) ===\n")
    for i, r in enumerate(all_results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    パス: {r['path']}")
        print(f"    スコア: {r['score']}")
        print(f"    ...{r['snippet']}...")
        print()


if __name__ == "__main__":
    main()
