#!/usr/bin/env python3
"""
さかさま不動産 /lessee/ の全記事を取得してmdファイルに保存するスクリプト
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BASE_URL = "https://sakasama-fudosan.com/lessee/"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data/cases")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research bot)"}
SLEEP_SEC = 1.0  # サーバー負荷軽減のため各リクエスト間に待機


def get_article_urls(max_pages=50):
    """全ページから記事URLを収集する"""
    urls = []
    page = 1
    while page <= max_pages:
        if page == 1:
            page_url = BASE_URL
        else:
            page_url = f"{BASE_URL}page/{page}/"

        print(f"ページ {page} を取得中: {page_url}")
        resp = requests.get(page_url, headers=HEADERS, timeout=15)
        if resp.status_code == 404:
            print(f"  → ページ {page} が見つかりません。終了。")
            break
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        # 記事リンクを抽出（/lessee/スラッグ/ の形式、ページネーション等を除外）
        found = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.match(r"https://sakasama-fudosan\.com/lessee/[^/]+/$", href):
                if "/page/" not in href:
                    found.add(href)

        if not found:
            print(f"  → 記事URLが見つかりません。終了。")
            break

        new_urls = [u for u in found if u not in urls]
        print(f"  → {len(new_urls)} 件の新規記事URL")
        urls.extend(new_urls)
        page += 1
        time.sleep(SLEEP_SEC)

    return urls


def slug_from_url(url):
    """URLからスラッグを取得する"""
    parts = url.rstrip("/").split("/")
    return parts[-1]


def parse_article(url, html):
    """記事HTMLをパースしてmarkdown文字列を生成する"""
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main", class_="p_lesseeSingle")
    if not main:
        return None

    # タイトル
    title_el = main.find("h1", class_="p_lesseeSingleHeader_title")
    title = title_el.get_text(strip=True) if title_el else "（タイトルなし）"

    # 更新日
    date_el = main.find("time", class_="p_lesseeSingleHeader_date")
    date = date_el.get_text(strip=True).replace("更新日 : ", "") if date_el else ""

    # 掲載者名・氏名
    roll_el = main.find("p", class_="p_lesseeSingleHeaderText_roll")
    roll = roll_el.get_text(strip=True) if roll_el else ""
    name_el = main.find("h2", class_="p_lesseeSingleHeaderText_name")
    name = name_el.get_text(strip=True) if name_el else ""

    # 一言プロフィール
    short_profile_el = main.find("p", class_="p_lesseeSingleHeaderText_profile")
    short_profile = short_profile_el.get_text(separator="\n", strip=True) if short_profile_el else ""

    # 物件を探している地域
    area_section = main.find("div", class_="p_lesseeSingleArea")
    area_lines = []
    if area_section:
        for area_list in area_section.find_all("div", class_="p_lesseeSingleAreaList"):
            pref = area_list.find("h4")
            pref_name = pref.get_text(strip=True) if pref else ""
            cities = [li.get_text(strip=True) for li in area_list.find_all("li")]
            area_lines.append(f"- **{pref_name}:** {', '.join(cities)}")

    # 本文セクション（やりたいこと / やりたい理由 / 希望物件の基本情報 など）
    content_sections = []
    # h2タグを基準にセクション分割
    for h2 in main.find_all("h2"):
        section_title = h2.get_text(strip=True)
        if section_title in ("掲載者情報", "掲載者を検索", "SEARCH", "PROFILE"):
            continue
        # h2の次の兄弟要素をすべて取得（次のh2まで）
        body_parts = []
        for sib in h2.find_next_siblings():
            if sib.name == "h2":
                break
            if sib.name in ("p", "ul", "ol", "h3", "h4", "table"):
                text = sib.get_text(separator="\n", strip=True)
                if text:
                    if sib.name in ("ul", "ol"):
                        items = [f"- {li.get_text(strip=True)}" for li in sib.find_all("li")]
                        body_parts.append("\n".join(items))
                    else:
                        body_parts.append(text)
        if body_parts:
            content_sections.append((section_title, "\n\n".join(body_parts)))

    # プロフィールセクション（h2「掲載者情報」以降）
    profile_sections = []
    profile_h2 = main.find("h2", string=lambda s: s and "掲載者情報" in s)
    if profile_h2:
        for h3 in profile_h2.find_all_next("h3"):
            # サイドバーや検索エリアより前のものに限定
            search_h2 = main.find("h2", string=lambda s: s and "掲載者を検索" in s)
            if search_h2 and h3.find_previous("h2") == search_h2:
                break
            section_title = h3.get_text(strip=True)
            body_parts = []
            for sib in h3.find_next_siblings():
                if sib.name in ("h2", "h3"):
                    break
                if sib.name in ("p", "ul", "ol", "h4"):
                    text = sib.get_text(separator="\n", strip=True)
                    if text:
                        if sib.name in ("ul", "ol"):
                            items = [f"- {li.get_text(strip=True)}" for li in sib.find_all("li")]
                            body_parts.append("\n".join(items))
                        else:
                            body_parts.append(text)
            if body_parts:
                profile_sections.append((section_title, "\n\n".join(body_parts)))

    # ステータス（物件が見つかりました 等）
    status_el = main.find("div", class_="p_lesseeSingleStatus") or main.find("p", class_=lambda c: c and "status" in c.lower())
    status = status_el.get_text(strip=True) if status_el else ""

    # Markdown組み立て
    lines = [f"# {title}", ""]
    if roll:
        lines.append(f"**掲載者:** {roll}  ")
    if name:
        lines.append(f"**氏名:** {name}  ")
    if date:
        lines.append(f"**更新日:** {date}  ")
    lines.append(f"**URL:** {url}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for section_title, body in content_sections:
        lines.append(f"## {section_title}")
        lines.append("")
        lines.append(body)
        lines.append("")

    if area_lines:
        lines.append("### 物件を探している地域")
        lines.append("")
        lines.extend(area_lines)
        lines.append("")

    if profile_sections:
        lines.append("---")
        lines.append("")
        lines.append("## プロフィール")
        lines.append("")
        for section_title, body in profile_sections:
            lines.append(f"### {section_title}")
            lines.append("")
            lines.append(body)
            lines.append("")

    if status:
        lines.append("---")
        lines.append("")
        lines.append(f"**ステータス:** {status}")
        lines.append("")

    return "\n".join(lines)


def scrape_and_save(url, output_dir, skip_existing=True):
    """1記事を取得してmdファイルに保存する"""
    slug = slug_from_url(url)
    # URLエンコードされたスラッグをデコード
    from urllib.parse import unquote
    slug = unquote(slug)
    # ファイル名に使えない文字を除去
    safe_slug = re.sub(r'[\\/:*?"<>|]', '_', slug)
    filepath = os.path.join(output_dir, f"{safe_slug}.md")

    if skip_existing and os.path.exists(filepath):
        print(f"  スキップ（既存）: {safe_slug}.md")
        return False

    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"

    md = parse_article(url, resp.text)
    if md is None:
        print(f"  パース失敗: {url}")
        return False

    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="さかさま不動産 lessee 記事を一括md化")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="既存のmdファイルをスキップ（デフォルト: True）")
    parser.add_argument("--no-skip", dest="skip_existing", action="store_false",
                        help="既存ファイルも上書き")
    parser.add_argument("--dry-run", action="store_true",
                        help="URLを列挙するだけで保存しない")
    parser.add_argument("--limit", type=int, default=0,
                        help="取得する記事数の上限（0=無制限）")
    args = parser.parse_args()

    print("=== 記事URL収集 ===")
    article_urls = get_article_urls()
    print(f"\n合計 {len(article_urls)} 件の記事URLを収集しました\n")

    if args.dry_run:
        for u in article_urls:
            print(u)
        return

    targets = article_urls[:args.limit] if args.limit > 0 else article_urls
    saved = 0
    skipped = 0
    failed = 0

    print("=== 記事保存 ===")
    for i, url in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] {url}")
        try:
            result = scrape_and_save(url, OUTPUT_DIR, skip_existing=args.skip_existing)
            if result:
                saved += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  エラー: {e}")
            failed += 1
        time.sleep(SLEEP_SEC)

    print(f"\n完了: 保存 {saved} 件 / スキップ {skipped} 件 / 失敗 {failed} 件")
    print(f"出力先: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
