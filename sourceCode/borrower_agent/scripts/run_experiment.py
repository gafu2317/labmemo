"""
借り手AIエージェント実験スクリプト

使い方:
  # ランダムに5人の借り手を選んで実行（デフォルト）
  python scripts/run_experiment.py \
    --property property01_kuwana \
    --random-cases \
    --conditions baseline,structured

  # ランダム人数を指定
  python scripts/run_experiment.py \
    --property property01_kuwana \
    --random-cases --n 3 \
    --conditions baseline,structured

  # 借り手を手動指定
  python scripts/run_experiment.py \
    --property property01_kuwana \
    --cases case01_ceramic_atelier,case02_xxx \
    --conditions baseline,structured

  # 全ケース
  python scripts/run_experiment.py \
    --property property01_kuwana \
    --all-cases \
    --conditions baseline,structured
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from models import Case, Property
from dialogue_runner import run_dialogue

CASES_DIR = ROOT / "data" / "cases"
PROPERTIES_DIR = ROOT / "data" / "properties"


def get_all_case_ids() -> list[str]:
    return [p.stem for p in sorted(CASES_DIR.glob("*.yaml"))]


def main() -> None:
    parser = argparse.ArgumentParser(description="借り手AIエージェント実験")

    parser.add_argument("--property", required=True, help="物件ID（例: property01_kuwana）")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--random-cases", action="store_true", help="ランダムにN人の借り手を選ぶ（デフォルト5人）")
    group.add_argument("--cases", help="ケースID（カンマ区切り、例: case01,case02）")
    group.add_argument("--all-cases", action="store_true", help="data/cases/ 以下の全YAMLを対象にする")
    parser.add_argument("--n", type=int, default=5, help="--random-cases のときの借り手人数（デフォルト: 5）")

    parser.add_argument("--conditions", default="baseline,structured", help="実行する条件（カンマ区切り）")
    parser.add_argument("--max-turns", type=int, default=6, help="最大ターン数（デフォルト: 6）")
    parser.add_argument("--temperature", type=float, default=0.0, help="temperature（デフォルト: 0）")
    args = parser.parse_args()

    # 物件読み込み
    property_path = PROPERTIES_DIR / f"{args.property}.yaml"
    if not property_path.exists():
        print(f"❌ 物件ファイルが見つかりません: {property_path}")
        sys.exit(1)
    prop = Property.from_yaml(property_path)

    # ケースID一覧
    if args.all_cases:
        case_ids = get_all_case_ids()
    elif args.random_cases:
        all_ids = get_all_case_ids()
        n = min(args.n, len(all_ids))
        case_ids = random.sample(all_ids, n)
        print(f"\n🎲 ランダム選出（{n}人）: {case_ids}")
    else:
        case_ids = [c.strip() for c in args.cases.split(",")]

    conditions = [c.strip() for c in args.conditions.split(",")]

    print(f"\n🏠 物件: {prop.id}  {prop.title}")
    print(f"📋 ケース数: {len(case_ids)}  条件: {conditions}  ターン数: {args.max_turns}")

    for case_id in case_ids:
        yaml_path = CASES_DIR / f"{case_id}.yaml"
        if not yaml_path.exists():
            print(f"❌ ケースファイルが見つかりません: {yaml_path}")
            continue

        case = Case.from_yaml(yaml_path)
        print(f"\n{'='*60}")
        print(f"👤 借り手: {case.id}  {case.title}")
        print("=" * 60)

        for condition in conditions:
            print(f"\n▶ 条件: {condition.upper()}")
            print("-" * 40)
            run_dialogue(
                case=case,
                prop=prop,
                condition=condition,
                max_turns=args.max_turns,
                temperature=args.temperature,
            )


if __name__ == "__main__":
    main()
