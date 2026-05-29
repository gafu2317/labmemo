"""
借り手AIエージェント実験スクリプト

使い方:
  python scripts/run_experiment.py --case case01_ceramic_atelier --conditions baseline,structured
  python scripts/run_experiment.py --case case01_ceramic_atelier --conditions baseline
  python scripts/run_experiment.py --all-cases --conditions baseline,structured
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from models import Case
from dialogue_runner import run_dialogue

CASES_DIR = ROOT / "data" / "cases"


def get_all_case_ids() -> list[str]:
    return [p.stem for p in sorted(CASES_DIR.glob("*.yaml"))]


def main() -> None:
    parser = argparse.ArgumentParser(description="借り手AIエージェント実験")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--case", help="ケースID（例: case01_ceramic_atelier）")
    group.add_argument("--all-cases", action="store_true", help="data/cases/ 以下の全YAMLを対象にする")
    parser.add_argument("--conditions", default="baseline,structured", help="実行する条件（カンマ区切り）")
    parser.add_argument("--max-turns", type=int, default=6, help="最大ターン数（デフォルト: 6）")
    parser.add_argument("--temperature", type=float, default=0.0, help="temperature（デフォルト: 0）")
    args = parser.parse_args()

    case_ids = get_all_case_ids() if args.all_cases else [args.case]
    conditions = [c.strip() for c in args.conditions.split(",")]

    for case_id in case_ids:
        yaml_path = CASES_DIR / f"{case_id}.yaml"
        if not yaml_path.exists():
            print(f"❌ ケースファイルが見つかりません: {yaml_path}")
            continue

        case = Case.from_yaml(yaml_path)
        print(f"\n{'='*60}")
        print(f"📋 ケース: {case.id}  {case.title}")
        print(f"🔧 条件: {conditions}  ターン数: {args.max_turns}")
        print("=" * 60)

        for condition in conditions:
            print(f"\n▶ 条件: {condition.upper()}")
            print("-" * 40)
            run_dialogue(
                case=case,
                condition=condition,
                max_turns=args.max_turns,
                temperature=args.temperature,
            )


if __name__ == "__main__":
    main()
