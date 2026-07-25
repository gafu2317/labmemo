"""V3: 既存話法 × 記事情報豊富度の要因実験。

例:
  python scripts/run_experiment.py \
    --cases case01_ceramic_atelier \
    --methods plain,prep,star,aida \
    --information-levels small,medium,large

手法再現監査を省いて試走する場合:
  python scripts/run_experiment.py \
    --cases case01_ceramic_atelier \
    --methods prep \
    --information-levels small \
    --no-method-audit
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
SHARED = ROOT.parent / "shared"
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from article_variants import load_case_with_information_level
from dialogue_runner import run_dialogue
from evidence_cache import load_or_create_evidence_inventory
from methods import INFORMATION_LEVELS, get_method_spec
from models import Property

PROPERTIES_DIR = SHARED / "data" / "properties"
DEFAULT_CASES_DIR = SHARED / "data" / "eval_cases"
BATCHES_DIR = ROOT / "runs" / "batches"


def get_all_case_ids(cases_dir: Path) -> list[str]:
    return [path.stem for path in sorted(cases_dir.glob("*.yaml"))]


def build_case_to_property_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for prop_path in sorted(PROPERTIES_DIR.glob("*.yaml")):
        with open(prop_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        target = data.get("meta", {}).get("target_case")
        if target:
            mapping[target] = data["id"]
        elif data["id"] == "property01_kuwana":
            mapping["case01_ceramic_atelier"] = data["id"]
    return mapping


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def build_jobs(
    prepared: list[dict],
    methods: list[str],
    repetitions: int,
    order_seed: int,
) -> list[dict]:
    jobs: list[dict] = []
    for item in prepared:
        for replicate_index in range(1, repetitions + 1):
            for method in methods:
                jobs.append(
                    {
                        **item,
                        "method": method,
                        "replicate_index": replicate_index,
                    }
                )
    random.Random(order_seed).shuffle(jobs)
    return jobs


def build_batch_manifest(
    jobs: list[dict],
    batch_id: str,
    order_seed: int,
    repetitions: int,
    max_turns: int,
    temperature: float,
) -> dict:
    return {
        "design_version": "v3.1",
        "batch_id": batch_id,
        "order_seed": order_seed,
        "repetitions": repetitions,
        "max_turns": max_turns,
        "temperature": temperature,
        "planned_dialogues": len(jobs),
        "execution_order": [
            {
                "execution_index": index,
                "replicate_index": job["replicate_index"],
                "case_id": job["case"].id,
                "property_id": job["property"].id,
                "information_level": job["level"],
                "method": job["method"],
                "evidence_inventory_id": job["evidence"].inventory_id,
                "evidence_inventory_sha256": (
                    job["evidence"].inventory_sha256
                ),
            }
            for index, job in enumerate(jobs, start=1)
        ],
    }


def save_batch_manifest(manifest: dict) -> Path:
    BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    path = BATCHES_DIR / f"{manifest['batch_id']}.json"
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="V3 既存話法 × 記事情報豊富度 実験"
    )
    parser.add_argument("--property", default=None)
    parser.add_argument("--cases-dir", default="eval_cases")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--random-cases", action="store_true")
    group.add_argument("--cases", help="ケースID（カンマ区切り）")
    group.add_argument("--all-cases", action="store_true")
    parser.add_argument("--n", type=int, default=3)

    parser.add_argument(
        "--methods",
        default="plain,prep,star,aida",
        help="話法（plain,prep,star,aida のカンマ区切り）",
    )
    parser.add_argument(
        "--information-levels",
        default="small,medium,large",
        help="記事情報豊富度（small,medium,large のカンマ区切り）",
    )
    parser.add_argument("--max-turns", type=int, default=4)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--repetitions",
        type=int,
        default=1,
        help="各条件の反復数（デフォルト: 1）",
    )
    parser.add_argument(
        "--order-seed",
        type=int,
        default=0,
        help="条件順ランダム化のseed（デフォルト: 0）",
    )
    parser.add_argument(
        "--refresh-evidence-cache",
        action="store_true",
        help="固定済み証拠在庫を明示的に再抽出する",
    )
    parser.add_argument(
        "--no-method-audit",
        action="store_true",
        help="各発話後のLLM話法再現監査を省く",
    )
    args = parser.parse_args()

    methods = _csv(args.methods)
    levels = _csv(args.information_levels)
    for method in methods:
        get_method_spec(method)
    invalid_levels = [level for level in levels if level not in INFORMATION_LEVELS]
    if invalid_levels:
        raise ValueError(
            f"未知の情報量: {invalid_levels}  使用可能: {INFORMATION_LEVELS}"
        )
    if args.repetitions < 1:
        raise ValueError("--repetitions は1以上にしてください。")

    cases_dir = SHARED / "data" / args.cases_dir
    if args.all_cases:
        case_ids = get_all_case_ids(cases_dir)
    elif args.random_cases:
        all_ids = get_all_case_ids(cases_dir)
        case_ids = random.Random(args.order_seed).sample(
            all_ids,
            min(args.n, len(all_ids)),
        )
    else:
        case_ids = _csv(args.cases)

    mapping = build_case_to_property_map() if args.property is None else {}
    total = (
        len(case_ids)
        * len(levels)
        * len(methods)
        * args.repetitions
    )
    print(
        f"\nV3 実験: {len(case_ids)}ケース × {len(levels)}情報条件 "
        f"× {len(methods)}話法 × {args.repetitions}反復 = {total}対話"
    )
    print(f"話法: {methods}")
    print(f"情報量: {levels}")
    print(f"話法監査: {not args.no_method_audit}")
    print(f"条件順seed: {args.order_seed}")

    prepared: list[dict] = []
    for case_id in case_ids:
        case_path = cases_dir / f"{case_id}.yaml"
        if not case_path.exists():
            print(f"❌ ケースファイルが見つかりません: {case_path}")
            continue

        property_id = args.property or mapping.get(case_id)
        if not property_id:
            print(f"⚠️ {case_id} に対応する物件がないためスキップします。")
            continue
        property_path = PROPERTIES_DIR / f"{property_id}.yaml"
        if not property_path.exists():
            print(f"❌ 物件ファイルが見つかりません: {property_path}")
            continue
        prop = Property.from_yaml(property_path)

        for level in levels:
            try:
                case = load_case_with_information_level(case_path, level)
            except (FileNotFoundError, ValueError) as exc:
                print(f"⚠️ {exc}")
                continue
            evidence = load_or_create_evidence_inventory(
                case,
                level,
                temperature=args.temperature,
                refresh=args.refresh_evidence_cache,
            )
            print(
                f"証拠在庫: {evidence.path.name} "
                f"({evidence.inventory_sha256[:12]})"
            )
            prepared.append(
                {
                    "case": case,
                    "property": prop,
                    "level": level,
                    "evidence": evidence,
                }
            )

    jobs = build_jobs(
        prepared,
        methods,
        args.repetitions,
        args.order_seed,
    )
    batch_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    manifest = build_batch_manifest(
        jobs,
        batch_id=batch_id,
        order_seed=args.order_seed,
        repetitions=args.repetitions,
        max_turns=args.max_turns,
        temperature=args.temperature,
    )
    manifest_path = save_batch_manifest(manifest)
    print(f"\n実行バッチ: {batch_id} / 実行可能対話数: {len(jobs)}")
    print(f"実行順マニフェスト: {manifest_path}")

    for execution_index, job in enumerate(jobs, start=1):
        case = job["case"]
        prop = job["property"]
        level = job["level"]
        method = job["method"]
        evidence = job["evidence"]
        replicate_index = job["replicate_index"]
        print("\n" + "=" * 72)
        print(
            f"実行順={execution_index}/{len(jobs)} / 反復={replicate_index} / "
            f"借り手={case.id} / 物件={prop.id} / "
            f"情報量={level} / 話法={method}"
        )
        print("=" * 72)
        run_dialogue(
            case=case,
            prop=prop,
            condition=method,
            information_level=level,
            passion_evidence_inventory=evidence.inventory,
            evidence_inventory_id=evidence.inventory_id,
            evidence_inventory_sha256=evidence.inventory_sha256,
            batch_id=batch_id,
            replicate_index=replicate_index,
            execution_index=execution_index,
            order_seed=args.order_seed,
            max_turns=args.max_turns,
            temperature=args.temperature,
            audit_method=not args.no_method_audit,
        )


if __name__ == "__main__":
    main()
