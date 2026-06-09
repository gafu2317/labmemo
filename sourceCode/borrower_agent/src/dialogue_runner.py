from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from borrower_policy import build_system_prompt as borrower_prompt
from landlord_agent import build_system_prompt as landlord_prompt
from llm_client import call_llm, get_model
from models import Case, Property, RunResult, Turn

RUNS_DIR = Path(__file__).parent.parent / "runs"


def run_dialogue(
    case: Case,
    prop: Property,
    condition: str,
    max_turns: int = 6,
    temperature: float = 0,
) -> RunResult:
    b_system = borrower_prompt(case, condition)
    l_system = landlord_prompt(prop)
    model = get_model()

    history: list[Turn] = []

    history.append(Turn(role="landlord", content=prop.opening))
    _print_turn("大家", 0, prop.opening)

    for t in range(1, max_turns + 1):
        b_reply = call_llm(b_system, history, caller_role="borrower", temperature=temperature)
        history.append(Turn(role="borrower", content=b_reply))
        _print_turn("借り手", t, b_reply)

        l_reply = call_llm(l_system, history, caller_role="landlord", temperature=temperature)
        history.append(Turn(role="landlord", content=l_reply))
        _print_turn("大家", t, l_reply)

    result = RunResult(
        case_id=case.id,
        property_id=prop.id,
        condition=condition,
        model_borrower=model,
        model_landlord=model,
        temperature=temperature,
        max_turns=max_turns,
        turns=history,
    )

    _save(result)
    return result


def _print_turn(speaker: str, turn_num: int, content: str) -> None:
    label = f"[{speaker} {'opening' if turn_num == 0 else f'ターン{turn_num}'}]"
    print(f"\n{label}\n{content}")


def _save(result: RunResult) -> None:
    RUNS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RUNS_DIR / f"{result.case_id}_{result.property_id}_{result.condition}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"\n✅ ログ保存: {path.name}")
