from __future__ import annotations

import json
import re
from pathlib import Path

from llm_client import call_llm_single
from methods import get_method_spec
from models import Case, MethodAudit, Turn, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def audit_method_reproduction(
    utterance: str,
    case: Case,
    history: list[Turn],
    plan: TurnPlan,
    temperature: float = 0,
) -> MethodAudit:
    spec = get_method_spec(plan.method)
    system = (
        (PROMPTS_DIR / "method_auditor.txt")
        .read_text(encoding="utf-8")
        .replace("{article}", case.article)
        .replace("{method_id}", spec.id)
        .replace("{method_name}", spec.name)
        .replace("{method_description}", spec.description)
        .replace(
            "{plan_json}",
            json.dumps(plan.to_dict(), ensure_ascii=False, indent=2),
        )
    )
    history_text = "\n".join(
        f"{'大家' if turn.role == 'landlord' else '借り手'}: {turn.content}"
        for turn in history
    )
    raw = call_llm_single(
        system_prompt=system,
        user_message=(
            f"## 対話履歴\n\n{history_text}\n\n"
            f"## 最終的な借り手発話\n\n{utterance}\n\n"
            "指定形式の監査JSONだけを出力してください。"
        ),
        temperature=temperature,
    )
    return parse_method_audit(raw, plan)


def parse_method_audit(raw: str, plan: TurnPlan) -> MethodAudit:
    expected = list(plan.method_slots)
    fallback_slots = {slot: False for slot in expected}
    fallback_canonical = None if plan.method == "plain" else False
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return MethodAudit(
            slot_realized=fallback_slots,
            canonical_method_complete=fallback_canonical,
            notes="監査JSONを解析できない",
        )
    try:
        data = json.loads(match.group())
    except (json.JSONDecodeError, TypeError):
        return MethodAudit(
            slot_realized=fallback_slots,
            canonical_method_complete=fallback_canonical,
            notes="監査JSONを解析できない",
        )

    raw_realized = data.get("slot_realized", {})
    if not isinstance(raw_realized, dict):
        raw_realized = {}
    realized = {slot: bool(raw_realized.get(slot, False)) for slot in expected}
    ordered = bool(data.get("ordered", False))
    available_slots = [
        name
        for name, slot in plan.method_slots.items()
        if slot.quote or slot.purpose
    ]
    available_slots_realized = (
        bool(available_slots)
        and all(realized[name] for name in available_slots)
    )
    canonical_method_complete = (
        None
        if plan.method == "plain"
        else (
            available_slots_realized
            and ordered
            and not plan.missing_slots
            and all(name in available_slots for name in expected)
        )
    )
    return MethodAudit(
        slot_realized=realized,
        ordered=ordered,
        grounded=bool(data.get("grounded", False)),
        available_slots_realized=available_slots_realized,
        canonical_method_complete=canonical_method_complete,
        notes=str(data.get("notes", "")),
    )
