from __future__ import annotations

import json
import re
from pathlib import Path

from llm_client import call_llm_single
from models import MOVES, RESPONSE_STRATEGIES, Case, Turn, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def plan_turn(
    case: Case,
    history: list[Turn],
    condition: str = "proposed",
    turn_number: int | None = None,
    max_turns: int = 4,
    temperature: float = 0,
    passion_evidence_inventory: dict[str, list[dict[str, str]]] | None = None,
) -> TurnPlan:
    """Baselineの中立計画またはProposedの熱意証拠計画を生成する。"""
    if condition == "baseline":
        prompt_name = "planner_baseline.txt"
    elif condition == "proposed":
        prompt_name = "planner_proposed.txt"
    else:
        raise ValueError(f"未知の条件: {condition!r}  使用可能: baseline / proposed")

    system = (PROMPTS_DIR / prompt_name).read_text(encoding="utf-8").replace("{article}", case.article)
    inventory = passion_evidence_inventory or {}
    system = system.replace(
        "{passion_evidence_inventory}",
        json.dumps(inventory, ensure_ascii=False, indent=2),
    )
    history_text = "\n".join(_format_history_turn(t) for t in history)
    state = build_dialogue_state(history, turn_number=turn_number, max_turns=max_turns)
    fallback = _fallback_plan(condition, state, inventory)
    state_text = json.dumps(state, ensure_ascii=False, indent=2)
    raw = call_llm_single(
        system,
        (
            f"## これまでの対話\n\n{history_text}\n\n"
            f"## 現在の対話状態\n\n```json\n{state_text}\n```\n\n"
            "対話履歴と現在の対話状態の両方を使い、"
            "今ターンの計画をJSONで出力してください。"
        ),
        temperature,
    )
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        return fallback
    try:
        d = json.loads(m.group())
        if condition == "baseline":
            plan = TurnPlan(
                turn_goal=d.get("turn_goal", "ask_fit_question"),
                phase=d.get("phase", "middle"),
                evidence_summary=d.get("evidence_summary", ""),
                ask_slot=d.get("ask_slot"),
                owner_concern=d.get("owner_concern", "unknown"),
            )
            return _apply_plan_constraints(plan, condition, state, inventory)
        move = d.get("move", "no_supported_signal")
        if move not in MOVES:
            move = "no_supported_signal"
        response_strategy = d.get("response_strategy", "answer_first")
        if response_strategy not in RESPONSE_STRATEGIES:
            response_strategy = "answer_first"
        plan = TurnPlan(
            turn_goal=d.get("turn_goal", "appeal"),
            move=move,
            response_strategy=response_strategy,
            evidence_quote=d.get("evidence_quote"),
            key_message=d.get("key_message") or d.get("evidence_summary", ""),
            evidence_summary=d.get("evidence_summary", ""),
            ask_slot=d.get("ask_slot"),
            owner_concern=d.get("owner_concern", "unknown"),
        )
        return _apply_plan_constraints(plan, condition, state, inventory)
    except (json.JSONDecodeError, KeyError, TypeError):
        return fallback


def _format_history_turn(turn: Turn) -> str:
    speaker = "大家" if turn.role == "landlord" else "借り手"
    action = ""
    if turn.landlord_action:
        action = f" [act={turn.landlord_action.act}, topic={turn.landlord_action.topic}]"
    return f"{speaker}{action}: {turn.content}"


def _fallback_plan(
    condition: str,
    state: dict,
    inventory: dict[str, list[dict[str, str]]] | None = None,
) -> TurnPlan:
    current_turn = state["current_turn"]
    remaining = state["remaining_turns_including_current"]
    last_action = (state.get("last_landlord_action") or {}).get("act")

    if condition == "baseline":
        phase = "opening" if current_turn == 1 else "closing" if remaining == 1 else "middle"
        return TurnPlan(
            turn_goal="close" if phase == "closing" else "appeal",
            phase=phase,
            evidence_summary="",
            ask_slot=None,
            owner_concern="unknown",
        )

    if remaining == 1:
        response_strategy = "close"
    elif last_action == "raise_concern":
        response_strategy = "acknowledge_concern"
    else:
        response_strategy = "answer_first"

    # LLM出力を解析できない場合、対話との関連性をコードだけでは判定できない。
    # 無関係な証拠を自動挿入するより、事実回答だけにフォールバックする。
    return TurnPlan(
        turn_goal="close" if response_strategy == "close" else "appeal",
        move="no_supported_signal",
        response_strategy=response_strategy,
        evidence_quote=None,
        key_message="",
        evidence_summary="",
        ask_slot=None,
        owner_concern="unknown",
    )


def _apply_plan_constraints(
    plan: TurnPlan,
    condition: str,
    state: dict,
    inventory: dict[str, list[dict[str, str]]] | None = None,
) -> TurnPlan:
    """LLMが選択ルールを外しても、実験上必須の順序はコードで保証する。"""
    current_turn = state["current_turn"]
    remaining = state["remaining_turns_including_current"]
    last_action = (state.get("last_landlord_action") or {}).get("act")

    if condition == "baseline":
        plan.phase = "opening" if current_turn == 1 else "closing" if remaining == 1 else "middle"
        if remaining == 1:
            plan.turn_goal = "close"
            plan.ask_slot = None
        return plan

    if remaining == 1:
        plan.response_strategy = "close"
        plan.turn_goal = "close"
        plan.ask_slot = None
    elif last_action == "raise_concern":
        plan.response_strategy = "acknowledge_concern"
        plan.ask_slot = None
    elif plan.response_strategy not in RESPONSE_STRATEGIES:
        plan.response_strategy = "answer_first"

    if inventory is not None:
        # no_supported_signal は「関連する証拠を使わない」というPlannerの判断。
        # 在庫が残っていても別の証拠を自動補充しない。
        if plan.move == "no_supported_signal":
            evidence = None
        else:
            evidence = _find_inventory_evidence(plan.move, plan.evidence_quote, inventory)
        if evidence:
            plan.evidence_quote = evidence["quote"]
            plan.evidence_summary = evidence["summary"]
            plan.key_message = evidence["summary"]
        else:
            plan.move = "no_supported_signal"
            plan.evidence_quote = None
            plan.evidence_summary = ""
            plan.key_message = ""
    return plan


def _find_inventory_evidence(
    move: str | None,
    quote: str | None,
    inventory: dict[str, list[dict[str, str]]],
) -> dict[str, str] | None:
    if not move or move == "no_supported_signal":
        return None
    for item in inventory.get(move, []):
        if quote == item.get("quote"):
            return item
    return None


def build_dialogue_state(
    history: list[Turn],
    turn_number: int | None = None,
    max_turns: int = 4,
) -> dict:
    """Plannerに明示する、条件間で共通の観測可能な対話状態。"""
    borrower_turns = [t for t in history if t.role == "borrower"]
    current_turn = turn_number if turn_number is not None else len(borrower_turns) + 1
    last_landlord = next((t for t in reversed(history) if t.role == "landlord"), None)

    return {
        "current_turn": current_turn,
        "max_turns": max_turns,
        "remaining_turns_including_current": max(max_turns - current_turn + 1, 0),
        "last_landlord_action": (
            last_landlord.landlord_action.to_dict()
            if last_landlord and last_landlord.landlord_action
            else None
        ),
        "used_moves": [t.plan.move for t in borrower_turns if t.plan and t.plan.move],
        "used_phases": [t.plan.phase for t in borrower_turns if t.plan and t.plan.phase],
        "conveyed_key_messages": [
            t.plan.key_message
            for t in borrower_turns
            if t.plan and t.plan.key_message
        ],
        "used_evidence_quotes": [
            t.plan.evidence_quote
            for t in borrower_turns
            if t.plan and t.plan.evidence_quote
        ],
        "asked_slots": [t.plan.ask_slot for t in borrower_turns if t.plan and t.plan.ask_slot],
    }
