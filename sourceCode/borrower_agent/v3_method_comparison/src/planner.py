from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from llm_client import call_llm_single
from methods import get_method_spec
from models import Case, MethodSlot, Turn, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
RESPONSE_STRATEGIES = ("answer_first", "acknowledge_concern", "close")


def plan_turn(
    case: Case,
    history: list[Turn],
    condition: str = "plain",
    turn_number: int | None = None,
    max_turns: int = 4,
    temperature: float = 0,
    passion_evidence_inventory: dict[str, list[dict[str, str]]] | None = None,
) -> TurnPlan:
    """指定話法の構成要素へ、記事中の根拠を割り当てる。"""
    spec = get_method_spec(condition)
    inventory = passion_evidence_inventory or {}
    state = build_dialogue_state(
        history,
        turn_number=turn_number,
        max_turns=max_turns,
    )
    system = _build_planner_prompt(case, spec, inventory)
    history_text = "\n".join(_format_history_turn(turn) for turn in history)
    raw = call_llm_single(
        system_prompt=system,
        user_message=(
            f"## これまでの対話\n\n{history_text}\n\n"
            "## 現在の対話状態\n\n"
            f"```json\n{json.dumps(state, ensure_ascii=False, indent=2)}\n```\n\n"
            "指定形式の計画JSONだけを出力してください。"
        ),
        temperature=temperature,
        max_tokens=2048,
    )
    parsed = parse_method_plan(
        raw,
        case,
        condition,
        state,
        passion_evidence_inventory=inventory,
    )
    return parsed if parsed is not None else fallback_plan(condition, state)


def _build_planner_prompt(case, spec, inventory) -> str:
    slots = "\n".join(
        f"- `{name}`: {spec.slot_instructions[name]}" for name in spec.slots
    )
    return (
        (PROMPTS_DIR / "method_planner.txt")
        .read_text(encoding="utf-8")
        .replace("{article}", case.article)
        .replace(
            "{passion_evidence_inventory}",
            json.dumps(inventory, ensure_ascii=False, indent=2),
        )
        .replace("{method_id}", spec.id)
        .replace("{method_name}", spec.name)
        .replace("{method_domain}", spec.domain)
        .replace("{method_description}", spec.description)
        .replace("{method_slots}", slots)
    )


def parse_method_plan(
    raw: str,
    case: Case,
    method: str,
    state: dict,
    passion_evidence_inventory: dict[str, list[dict[str, str]]] | None = None,
) -> TurnPlan | None:
    """LLM計画を解析し、記事に存在しない引用を決定的に除去する。"""
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return None
    try:
        data = json.loads(match.group())
    except (json.JSONDecodeError, TypeError):
        return None

    spec = get_method_spec(method)
    raw_slots = data.get("method_slots", {})
    if not isinstance(raw_slots, dict):
        raw_slots = {}

    slots: dict[str, MethodSlot] = {}
    missing: list[str] = []
    used_quotes: set[str] = set()
    allowed_quotes = (
        {
            _normalized(item["quote"])
            for items in passion_evidence_inventory.values()
            for item in items
            if isinstance(item, dict) and isinstance(item.get("quote"), str)
        }
        if passion_evidence_inventory is not None
        else None
    )
    for name in spec.slots:
        raw_slot = raw_slots.get(name, {})
        if not isinstance(raw_slot, dict):
            raw_slot = {}
        quote = raw_slot.get("quote", "")
        purpose = raw_slot.get("purpose", "")
        quote = quote.strip() if isinstance(quote, str) else ""
        purpose = purpose.strip() if isinstance(purpose, str) else ""

        is_prep_restatement = (
            method == "prep"
            and name == "point_restated"
            and bool(quote)
            and bool(slots.get("point"))
            and _normalized(quote) == _normalized(slots["point"].quote)
        )
        quote_allowed = (
            bool(quote)
            and _normalized(quote) in _normalized(case.article)
            and (
                _normalized(quote) not in used_quotes
                or is_prep_restatement
            )
            and (
                allowed_quotes is None
                or _normalized(quote) in allowed_quotes
            )
        )
        if quote_allowed:
            used_quotes.add(_normalized(quote))
            # LLMがpurposeへ引用以上の因果や成果を書き込む経路を閉じる。
            # Realizerへ渡す意味内容は、検証済み原文そのものに固定する。
            slots[name] = MethodSlot(quote=quote, purpose=quote)
        elif method == "aida" and name == "action":
            # Actionは記事上の事実ではなく発話行為。ただし内容はRealizer側で限定する。
            slots[name] = MethodSlot(quote="", purpose=purpose)
            if not purpose:
                missing.append(name)
        else:
            slots[name] = MethodSlot()
            missing.append(name)

    missing = list(dict.fromkeys(missing))
    response_strategy = data.get("response_strategy", "answer_first")
    if response_strategy not in RESPONSE_STRATEGIES:
        response_strategy = "answer_first"

    remaining = state["remaining_turns_including_current"]
    last_action = (state.get("last_landlord_action") or {}).get("act")
    if remaining == 1:
        response_strategy = "close"
    elif last_action == "raise_concern":
        response_strategy = "acknowledge_concern"

    apply_method = bool(data.get("apply_method", False))
    grounded_slot_count = sum(bool(slot.quote) for slot in slots.values())
    if method == "plain":
        apply_method = apply_method and grounded_slot_count >= 1
    elif method == "aida":
        # Attention/Interest/Desireのうち最低2要素がなければ、CTAだけを出さない。
        apply_method = apply_method and grounded_slot_count >= 2
    else:
        # PREP/STARを1要素だけで装うことを避ける。
        apply_method = apply_method and grounded_slot_count >= 2

    if remaining == 1 and method == "aida":
        # 最終ターンは全条件で次アクションを増やさない。
        # Actionを除いたAIDをAIDA完全再現として数えないため、手法適用自体を止める。
        apply_method = False
        slots["action"] = MethodSlot()
        if "action" not in missing:
            missing.append("action")

    used_before = set(state.get("used_evidence_quotes", []))
    if any(slot.quote in used_before for slot in slots.values() if slot.quote):
        apply_method = False

    evidence_summary = " / ".join(
        slot.purpose or slot.quote for slot in slots.values() if slot.quote
    )
    return TurnPlan(
        turn_goal="close" if remaining == 1 else data.get("turn_goal", "appeal"),
        evidence_summary=evidence_summary,
        ask_slot=None if remaining == 1 else data.get("ask_slot"),
        owner_concern=data.get("owner_concern", "unknown"),
        method=method,
        response_strategy=response_strategy,
        apply_method=apply_method,
        method_slots=slots,
        missing_slots=missing,
    )


def fallback_plan(method: str, state: dict) -> TurnPlan:
    spec = get_method_spec(method)
    remaining = state["remaining_turns_including_current"]
    last_action = (state.get("last_landlord_action") or {}).get("act")
    if remaining == 1:
        strategy = "close"
    elif last_action == "raise_concern":
        strategy = "acknowledge_concern"
    else:
        strategy = "answer_first"
    return TurnPlan(
        turn_goal="close" if remaining == 1 else "answer",
        evidence_summary="",
        ask_slot=None,
        owner_concern="unknown",
        method=method,
        response_strategy=strategy,
        apply_method=False,
        method_slots={name: MethodSlot() for name in spec.slots},
        missing_slots=list(spec.slots),
    )


def build_dialogue_state(
    history: list[Turn],
    turn_number: int | None = None,
    max_turns: int = 4,
) -> dict:
    borrower_turns = [turn for turn in history if turn.role == "borrower"]
    current_turn = (
        turn_number if turn_number is not None else len(borrower_turns) + 1
    )
    last_landlord = next(
        (turn for turn in reversed(history) if turn.role == "landlord"),
        None,
    )
    used_quotes = [
        quote
        for turn in borrower_turns
        if turn.plan
        for quote in turn.plan.selected_evidence_quotes()
    ]
    return {
        "current_turn": current_turn,
        "max_turns": max_turns,
        "remaining_turns_including_current": max(
            max_turns - current_turn + 1,
            0,
        ),
        "last_landlord_action": (
            last_landlord.landlord_action.to_dict()
            if last_landlord and last_landlord.landlord_action
            else None
        ),
        "used_evidence_quotes": used_quotes,
        "applied_method_turns": [
            index + 1
            for index, turn in enumerate(borrower_turns)
            if turn.plan and turn.plan.apply_method
        ],
    }


def _format_history_turn(turn: Turn) -> str:
    speaker = "大家" if turn.role == "landlord" else "借り手"
    action = ""
    if turn.landlord_action:
        action = (
            f" [act={turn.landlord_action.act}, "
            f"topic={turn.landlord_action.topic}]"
        )
    return f"{speaker}{action}: {turn.content}"


def _normalized(text: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))
