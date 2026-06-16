from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

from borrower_policy import build_system_prompt as build_realizer_prompt
from landlord_agent import build_system_prompt as landlord_prompt
from llm_client import call_llm, get_model
from models import Case, Property, RunResult, Turn
from planner import plan_turn
from verifier import verify_utterance

RUNS_DIR = Path(__file__).parent.parent / "runs"
RUNS_HTML_DIR = RUNS_DIR / "html"

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Hiragino Sans", "Meiryo", sans-serif; background: #f0f2f5; color: #333; }
header {
  background: #06c755; color: white; padding: 12px 20px;
  display: flex; align-items: center; gap: 12px;
  position: sticky; top: 0; z-index: 10;
}
.header-title { font-size: 16px; font-weight: bold; }
.header-meta  { font-size: 12px; opacity: 0.85; margin-top: 2px; }
.badge {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 12px; font-weight: bold;
}
.badge-baseline  { background: #fff3e0; color: #e65100; }
.badge-proposed  { background: #e3f2fd; color: #1565c0; }
.chat-area {
  padding: 16px; display: flex; flex-direction: column;
  gap: 12px; background: #e5ddd5; min-height: 100vh;
}
.turn-label {
  text-align: center; font-size: 11px; color: #888;
  background: rgba(255,255,255,0.6); border-radius: 10px;
  padding: 3px 12px; align-self: center;
}
.msg-row { display: flex; align-items: flex-end; gap: 8px; }
.msg-row.landlord { flex-direction: row; }
.msg-row.borrower { flex-direction: row-reverse; }
.avatar {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0;
}
.avatar-landlord { background: #bdbdbd; }
.avatar-borrower { background: #a5d6a7; }
.bubble-group { display: flex; flex-direction: column; max-width: 65%; }
.msg-row.borrower .bubble-group { align-items: flex-end; }
.msg-row.landlord .bubble-group { align-items: flex-start; }
.speaker-name { font-size: 11px; color: #666; margin-bottom: 3px; padding: 0 4px; }
.bubble {
  padding: 10px 14px; border-radius: 18px; font-size: 14px;
  line-height: 1.6; white-space: pre-wrap; word-break: break-word;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.bubble-landlord { background: white; border-top-left-radius: 4px; }
.bubble-borrower { background: #dcf8c6; border-top-right-radius: 4px; }
.plan-chip {
  font-size: 11px; color: #666; background: rgba(255,255,255,0.7);
  border-radius: 8px; padding: 3px 8px; margin-bottom: 4px;
  align-self: flex-end;
}
"""


def run_dialogue(
    case: Case,
    prop: Property,
    condition: str,
    max_turns: int = 4,
    temperature: float = 0,
) -> RunResult:
    l_system = landlord_prompt(prop)
    model = get_model()
    history: list[Turn] = []

    history.append(Turn(role="landlord", content=prop.opening))
    _print_turn("大家", 0, prop.opening)

    for t in range(1, max_turns + 1):
        plan = plan_turn(case, history, temperature=temperature)
        _print_plan(t, plan)

        b_system = build_realizer_prompt(case, condition, plan)
        b_reply = call_llm(b_system, history, caller_role="borrower", temperature=temperature)
        b_reply = verify_utterance(b_reply, case, temperature=temperature)

        history.append(Turn(role="borrower", content=b_reply, plan=plan))
        _print_turn("借り手", t, b_reply)

        l_reply = call_llm(l_system, history, caller_role="landlord", temperature=temperature)
        history.append(Turn(role="landlord", content=l_reply))
        _print_turn("大家", t, l_reply)

    result = RunResult(
        case_id=case.id, property_id=prop.id, condition=condition,
        model_borrower=model, model_landlord=model,
        temperature=temperature, max_turns=max_turns, turns=history,
    )
    _save(result)
    return result


def _print_turn(speaker: str, turn_num: int, content: str) -> None:
    label = f"[{speaker} {'opening' if turn_num == 0 else f'ターン{turn_num}'}]"
    print(f"\n{label}\n{content}")


def _print_plan(turn_num: int, plan) -> None:
    print(f"\n[計画 ターン{turn_num}] goal={plan.turn_goal} phase={plan.phase} ask={plan.ask_slot}")


def _save(result: RunResult) -> None:
    RUNS_DIR.mkdir(exist_ok=True)
    RUNS_HTML_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"{result.case_id}_{result.condition}_{result.property_id}_{ts}"

    json_path = RUNS_DIR / f"{stem}.json"
    json_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    html_path = RUNS_HTML_DIR / f"{stem}.html"
    html_path.write_text(_to_html(result, ts), encoding="utf-8")

    print(f"\n✅ {json_path.name}")
    print(f"🌐 {html_path.name}")


def _fmt_plan_chip(plan) -> str:
    parts = [plan.turn_goal, f"phase={plan.phase}"]
    if plan.ask_slot:
        parts.append(f"ask={plan.ask_slot}")
    if plan.owner_concern not in (None, "unknown"):
        parts.append(f"concern={plan.owner_concern}")
    return " · ".join(parts)


def _to_html(result: RunResult, ts: str) -> str:
    cond = result.condition
    date = f"{ts[:4]}/{ts[4:6]}/{ts[6:8]} {ts[9:11]}:{ts[11:13]}"
    meta = f"{result.model_borrower} | temp={result.temperature} | {result.max_turns}ターン | {date}"

    turns_html: list[str] = []
    borrower_n = landlord_n = 0

    for turn in result.turns:
        c = html.escape(turn.content)
        if turn.role == "landlord":
            label = "大家 opening" if landlord_n == 0 else f"ターン {landlord_n}"
            turns_html.append(f'<div class="turn-label">{label}</div>')
            turns_html.append(f'''
<div class="msg-row landlord">
  <div class="avatar avatar-landlord">🏠</div>
  <div class="bubble-group">
    <div class="speaker-name">大家</div>
    <div class="bubble bubble-landlord">{c}</div>
  </div>
</div>''')
            landlord_n += 1
        else:
            borrower_n += 1
            turns_html.append(f'<div class="turn-label">ターン {borrower_n}</div>')
            plan_chip = ""
            if turn.plan:
                plan_chip = f'<div class="plan-chip">📋 {html.escape(_fmt_plan_chip(turn.plan))}</div>'
            turns_html.append(f'''
<div class="msg-row borrower">
  <div class="avatar avatar-borrower">👤</div>
  <div class="bubble-group">
    <div class="speaker-name">借り手</div>
    {plan_chip}
    <div class="bubble bubble-borrower">{c}</div>
  </div>
</div>''')

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{result.case_id} / {cond}</title>
  <style>{_CSS}</style>
</head>
<body>
  <header>
    <div>
      <div class="header-title">
        {html.escape(result.case_id)}
        <span class="badge badge-{cond}">{cond}</span>
      </div>
      <div class="header-meta">{html.escape(meta)}</div>
    </div>
  </header>
  <div class="chat-area">
    {"".join(turns_html)}
  </div>
</body>
</html>"""
