from __future__ import annotations

import json
import re
from pathlib import Path

from llm_client import call_llm_single
from models import MOVES, Case, Turn, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

_FALLBACK_BASELINE = TurnPlan(
    turn_goal="ask_fit_question",
    phase="middle",
    evidence_summary="",
    ask_slot=None,
    owner_concern="unknown",
)

_FALLBACK_PROPOSED = TurnPlan(
    turn_goal="appeal",
    move="elevator_hook",
    key_message="",
    evidence_summary="",
    ask_slot=None,
    owner_concern="unknown",
)


def plan_turn(
    case: Case,
    history: list[Turn],
    condition: str = "proposed",
    temperature: float = 0,
) -> TurnPlan:
    """条件に応じて Baseline（固定感情）または Proposed（修辞ムーブ）の計画を生成する。"""
    if condition == "baseline":
        prompt_name = "planner_baseline.txt"
        fallback = _FALLBACK_BASELINE
    elif condition == "proposed":
        prompt_name = "planner_proposed.txt"
        fallback = _FALLBACK_PROPOSED
    else:
        raise ValueError(f"未知の条件: {condition!r}  使用可能: baseline / proposed")

    system = (PROMPTS_DIR / prompt_name).read_text(encoding="utf-8").replace("{article}", case.article)
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
        return fallback
    try:
        d = json.loads(m.group())
        if condition == "baseline":
            return TurnPlan(
                turn_goal=d.get("turn_goal", "ask_fit_question"),
                phase=d.get("phase", "middle"),
                evidence_summary=d.get("evidence_summary", ""),
                ask_slot=d.get("ask_slot"),
                owner_concern=d.get("owner_concern", "unknown"),
            )
        move = d.get("move", "elevator_hook")
        if move not in MOVES:
            move = "elevator_hook"
        return TurnPlan(
            turn_goal=d.get("turn_goal", "appeal"),
            move=move,
            key_message=d.get("key_message") or d.get("evidence_summary", ""),
            evidence_summary=d.get("evidence_summary", ""),
            ask_slot=d.get("ask_slot"),
            owner_concern=d.get("owner_concern", "unknown"),
        )
    except (json.JSONDecodeError, KeyError, TypeError):
        return fallback
