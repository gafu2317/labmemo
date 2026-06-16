"""
借り手AIエージェント実験スクリプト

使い方:
  # 全ケース（各ケースに対応した専用物件を自動マッチ）
  python scripts/run_experiment.py \
    --all-cases \
    --conditions baseline,proposed

  # ランダムにN人の借り手を選んで実行（デフォルト3人）
  python scripts/run_experiment.py \
    --random-cases --n 3 \
    --conditions baseline,proposed

  # ケースを手動指定
  python scripts/run_experiment.py \
    --cases case01_ceramic_atelier,light_to_flowre \
    --conditions baseline,proposed

  # 物件を手動指定する場合（全ケースに同じ物件を使う）
  python scripts/run_experiment.py \
    --property property01_kuwana \
    --all-cases \
    --conditions baseline,proposed
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

import yaml
from models import Case, Property
from dialogue_runner import run_dialogue

PROPERTIES_DIR = ROOT / "data" / "properties"
DEFAULT_CASES_DIR = ROOT / "data" / "eval_cases"


def get_all_case_ids(cases_dir: Path) -> list[str]:
    return [p.stem for p in sorted(cases_dir.glob("*.yaml"))]


def build_case_to_property_map() -> dict[str, str]:
    """物件YAMLのtarget_caseフィールドからケース→物件IDのマッピングを構築する。"""
    mapping: dict[str, str] = {}
    for prop_path in sorted(PROPERTIES_DIR.glob("*.yaml")):
        with open(prop_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        target = data.get("meta", {}).get("target_case")
        if target:
            mapping[target] = data["id"]
        # property01_kuwana はnotesのみ → case01_ceramic_atelier を直接登録
        elif data["id"] == "property01_kuwana":
            mapping["case01_ceramic_atelier"] = data["id"]
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="借り手AIエージェント実験")

    parser.add_argument(
        "--property",
        default=None,
        help="物件IDを手動指定（省略時は各ケースの専用物件を自動マッチ）",
    )
    parser.add_argument(
        "--cases-dir",
        default="eval_cases",
        help="ケースYAMLが格納されたフォルダ名（data/ 以下、デフォルト: eval_cases）",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--random-cases", action="store_true", help="ランダムにN人の借り手を選ぶ（デフォルト3人）")
    group.add_argument("--cases", help="ケースID（カンマ区切り）")
    group.add_argument("--all-cases", action="store_true", help="--cases-dir 以下の全YAMLを対象にする")
    parser.add_argument("--n", type=int, default=3, help="--random-cases のときの借り手人数（デフォルト: 3）")

    parser.add_argument("--conditions", default="baseline,proposed", help="実行する条件（カンマ区切り）")
    parser.add_argument("--max-turns", type=int, default=4, help="最大ターン数（デフォルト: 4）")
    parser.add_argument("--temperature", type=float, default=0.0, help="temperature（デフォルト: 0）")
    args = parser.parse_args()

    cases_dir = ROOT / "data" / args.cases_dir

    # ケースID一覧
    if args.all_cases:
        case_ids = get_all_case_ids(cases_dir)
    elif args.random_cases:
        all_ids = get_all_case_ids(cases_dir)
        n = min(args.n, len(all_ids))
        case_ids = random.sample(all_ids, n)
        print(f"\n🎲 ランダム選出（{n}人）: {case_ids}")
    else:
        case_ids = [c.strip() for c in args.cases.split(",")]

    conditions = [c.strip() for c in args.conditions.split(",")]

    # ケース→物件マッピング（手動指定がない場合のみ使用）
    case_property_map = build_case_to_property_map() if args.property is None else {}

    print(f"\n📁 ケースフォルダ: {cases_dir.name}")
    print(f"📋 ケース数: {len(case_ids)}  条件: {conditions}  ターン数: {args.max_turns}")
    if args.property:
        print(f"🏠 物件（全ケース共通）: {args.property}")

    for case_id in case_ids:
        yaml_path = cases_dir / f"{case_id}.yaml"
        if not yaml_path.exists():
            print(f"❌ ケースファイルが見つかりません: {yaml_path}")
            continue

        # 物件を決定
        if args.property:
            property_id = args.property
        else:
            property_id = case_property_map.get(case_id)
            if not property_id:
                print(f"⚠️  {case_id} に対応する物件が見つかりません。スキップします。")
                continue

        property_path = PROPERTIES_DIR / f"{property_id}.yaml"
        if not property_path.exists():
            print(f"❌ 物件ファイルが見つかりません: {property_path}")
            continue

        case = Case.from_yaml(yaml_path)
        prop = Property.from_yaml(property_path)

        print(f"\n{'='*60}")
        print(f"👤 借り手: {case.id}  {case.title}")
        print(f"🏠 物件: {prop.id}  {prop.title}")
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
