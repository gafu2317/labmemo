"""
MDファイルをYAMLケースファイルに一括変換するスクリプト

処理内容:
1. data/cases/*.md を読み込む
2. Anthropic API で profile / slots を生成
3. data/cases/{slug}.yaml に保存
4. 元のMDファイルを data/cases_raw/ に移動

使い方:
  python scripts/convert_md_to_yaml.py              # 全件変換
  python scripts/convert_md_to_yaml.py --limit 5    # 最初の5件のみ（テスト用）
  python scripts/convert_md_to_yaml.py --skip-existing  # 既存YAMLはスキップ
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

import anthropic
import yaml

CASES_DIR = ROOT / "data" / "cases"
CASES_RAW_DIR = ROOT / "data" / "cases_raw"

SYSTEM_PROMPT = """\
あなたは不動産研究者のアシスタントです。
借り手の記事を読み、以下のJSON形式でプロファイルとスロットを生成してください。
必ず valid JSON のみを返してください（コードブロック・説明文は不要）。

{
  "title": "記事タイトル（簡潔に）",
  "profile": {
    "purpose": "この借り手が物件で実現したいことを1〜2文で",
    "wishes": ["希望条件1", "希望条件2", ...],
    "constraints": ["記事に書かれていないが誤って言いやすい項目（家族構成・収入・詳細予算など）"],
    "questions": ["大家に確認すべき重要な質問1", "質問2", ...]
  },
  "slots": [
    {"id": "slot_id_snake_case", "description": "借り手が大家から引き出すべき重要情報の説明"},
    ...
  ]
}

ルール:
- wishes は記事から読み取れる希望を3〜6項目
- constraints は「記事に書かれていないため言わない」べき情報を2〜4項目
- questions は借り手が大家に聞くべき重要質問を3〜5項目
- slots は questions に対応した評価項目を3〜5項目（id は英語snake_case）
"""


def slugify(filename: str) -> str:
    """ファイル名からYAML用のIDを生成"""
    stem = Path(filename).stem
    # 日本語・特殊文字をハイフンに（ハイフンはそのまま）
    slug = re.sub(r"[^\w\-]", "_", stem)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug


def extract_url(text: str) -> str:
    m = re.search(r"\*\*URL:\*\*\s*(https?://\S+)", text)
    return m.group(1) if m else ""


def generate_profile_and_slots(client: anthropic.Anthropic, article: str) -> dict:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": article}],
    )
    raw = response.content[0].text.strip()
    # コードブロックが含まれる場合は除去
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def convert_one(md_path: Path, client: anthropic.Anthropic, skip_existing: bool) -> bool:
    slug = slugify(md_path.name)
    yaml_path = CASES_DIR / f"{slug}.yaml"

    if skip_existing and yaml_path.exists():
        print(f"  ⏭ スキップ（既存）: {yaml_path.name}")
        return False

    article = md_path.read_text(encoding="utf-8")
    url = extract_url(article)

    try:
        result = generate_profile_and_slots(client, article)
    except Exception as e:
        print(f"  ❌ LLM生成失敗: {md_path.name} → {e}")
        return False

    profile = result.get("profile", {})
    slots_raw = result.get("slots", [])
    title = result.get("title", slug)

    data = {
        "id": slug,
        "title": title,
        "article": article,
        "profile": {
            "purpose": profile.get("purpose", ""),
            "wishes": profile.get("wishes", []),
            "constraints": profile.get("constraints", []),
            "questions": profile.get("questions", []),
        },
        "slots": [{"id": s["id"], "description": s["description"]} for s in slots_raw],
        "meta": {
            "source_url": url,
            "profile_created_by": "llm_assisted",
        },
    }

    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False,
                  sort_keys=False, width=120)

    print(f"  ✅ 生成: {yaml_path.name}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="MD→YAML一括変換")
    parser.add_argument("--limit", type=int, default=None, help="変換件数の上限（テスト用）")
    parser.add_argument("--skip-existing", action="store_true", help="既存YAMLはスキップ")
    parser.add_argument("--move", action="store_true", help="変換後にMDをcases_rawに移動")
    args = parser.parse_args()

    import os
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    CASES_RAW_DIR.mkdir(exist_ok=True)

    md_files = sorted(CASES_DIR.glob("*.md"))
    if args.limit:
        md_files = md_files[:args.limit]

    print(f"対象: {len(md_files)} 件")

    converted = 0
    for i, md_path in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] {md_path.name}")
        ok = convert_one(md_path, client, args.skip_existing)
        if ok:
            converted += 1
            if args.move:
                shutil.move(str(md_path), str(CASES_RAW_DIR / md_path.name))
        time.sleep(0.3)  # レート制限対策

    print(f"\n完了: {converted} 件変換")

    # --move なしでも既存MDをまとめて移動する確認
    remaining_md = list(CASES_DIR.glob("*.md"))
    if remaining_md and not args.move:
        print(f"\n📁 cases/ に {len(remaining_md)} 件のMDが残っています。")
        print("   移動するには: python scripts/convert_md_to_yaml.py --move --skip-existing")


if __name__ == "__main__":
    main()
