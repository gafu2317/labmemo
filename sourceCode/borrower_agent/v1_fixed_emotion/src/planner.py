from __future__ import annotations

import json
import re
from pathlib import Path

from llm_client import call_llm_single
from models import Case, Turn, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

_FALLBACK = TurnPlan(turn_goal="ask_fit_question", phase="middle",
                     evidence_summary="", ask_slot=None, owner_concern="unknown")


def plan_turn(case: Case, history: list[Turn], temperature: float = 0) -> TurnPlan:
    system = (PROMPTS_DIR / "planner.txt").read_text(encoding="utf-8").replace("{article}", case.article)
    history_text = "\n".join(
        f"{'大家' if t.role == 'landlord' else '借り手'}: {t.content}" for t in history
    )
    raw = call_llm_single(
        system,
        f"## これまでの対話\n\n{history_text}\n\n今ターンの計画をJSONで出力してください。",
        temperature,
    )
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        return _FALLBACK
    try:
        d = json.loads(m.group())
        return TurnPlan(
            turn_goal=d.get("turn_goal", "ask_fit_question"),
            phase=d.get("phase", "middle"),
            evidence_summary=d.get("evidence_summary", ""),
            ask_slot=d.get("ask_slot"),
            owner_concern=d.get("owner_concern", "unknown"),
        )
    except (json.JSONDecodeError, KeyError):
        return _FALLBACK
