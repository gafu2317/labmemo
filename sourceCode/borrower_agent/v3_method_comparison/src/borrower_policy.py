from __future__ import annotations

import json
from pathlib import Path

from methods import get_method_spec
from models import Case, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_system_prompt(
    case: Case,
    condition: str,
    plan: TurnPlan | None = None,
) -> str:
    spec = get_method_spec(condition)
    plan_json = (
        json.dumps(plan.to_dict(), ensure_ascii=False, indent=2)
        if plan
        else "{}"
    )
    return (
        (PROMPTS_DIR / "method_realizer.txt")
        .read_text(encoding="utf-8")
        .replace("{article}", case.article)
        .replace("{method_id}", spec.id)
        .replace("{method_name}", spec.name)
        .replace("{method_description}", spec.description)
        .replace("{plan_json}", plan_json)
    )
