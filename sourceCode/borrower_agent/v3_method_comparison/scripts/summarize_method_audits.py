"""V3ログの話法再現監査を、話法 × 情報豊富度ごとに集計する。"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
RUNS_DIR = ROOT / "runs"


def summarize(paths: list[Path]) -> list[dict]:
    groups: dict[tuple[str, str], dict] = defaultdict(
        lambda: {
            "dialogues": 0,
            "borrower_turns": 0,
            "method_applied_turns": 0,
            "audited_turns": 0,
            "audited_applied_turns": 0,
            "available_slots_realized": 0,
            "canonical_method_complete": 0,
            "canonical_audited_turns": 0,
            "ordered": 0,
            "grounded": 0,
            "missing_slots": Counter(),
        }
    )
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        method = data.get("method", data.get("condition", "unknown"))
        level = data.get("information_level", "unknown")
        group = groups[(method, level)]
        group["dialogues"] += 1
        for turn in data.get("turns", []):
            if turn.get("role") != "borrower":
                continue
            group["borrower_turns"] += 1
            plan = turn.get("plan", {})
            if plan.get("apply_method"):
                group["method_applied_turns"] += 1
            group["missing_slots"].update(plan.get("missing_slots", []))

            audit = turn.get("method_audit")
            if not isinstance(audit, dict):
                continue
            group["audited_turns"] += 1
            group["grounded"] += bool(audit.get("grounded"))
            if plan.get("apply_method"):
                group["audited_applied_turns"] += 1
                group["available_slots_realized"] += bool(
                    audit.get("available_slots_realized")
                )
                group["ordered"] += bool(audit.get("ordered"))
                canonical = audit.get("canonical_method_complete")
                if canonical is not None:
                    group["canonical_audited_turns"] += 1
                    group["canonical_method_complete"] += bool(canonical)

    rows: list[dict] = []
    for (method, level), group in sorted(groups.items()):
        turns = group["borrower_turns"]
        audited = group["audited_turns"]
        audited_applied = group["audited_applied_turns"]
        canonical_audited = group["canonical_audited_turns"]
        rows.append(
            {
                "method": method,
                "information_level": level,
                "dialogues": group["dialogues"],
                "borrower_turns": turns,
                "method_application_rate": _rate(
                    group["method_applied_turns"], turns
                ),
                "audited_turns": audited,
                "audited_applied_turns": audited_applied,
                "available_slots_realized_rate": _rate(
                    group["available_slots_realized"], audited_applied
                ),
                "canonical_audited_turns": canonical_audited,
                "canonical_method_complete_rate": _rate(
                    group["canonical_method_complete"], canonical_audited
                ),
                "ordered_rate": _rate(group["ordered"], audited_applied),
                "grounded_rate": _rate(group["grounded"], audited),
                "missing_slots": ";".join(
                    f"{name}:{count}"
                    for name, count in group["missing_slots"].most_common()
                ),
            }
        )
    return rows


def _rate(numerator: int, denominator: int) -> str:
    return f"{numerator / denominator:.3f}" if denominator else ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="CSV保存先。省略時は標準出力",
    )
    args = parser.parse_args()
    rows = summarize(sorted(RUNS_DIR.glob("*.json")))
    fieldnames = [
        "method",
        "information_level",
        "dialogues",
        "borrower_turns",
        "method_application_rate",
        "audited_turns",
        "audited_applied_turns",
        "available_slots_realized_rate",
        "canonical_audited_turns",
        "canonical_method_complete_rate",
        "ordered_rate",
        "grounded_rate",
        "missing_slots",
    ]
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(args.output)
        return

    writer = csv.DictWriter(__import__("sys").stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
