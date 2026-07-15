"""既存の runs/*.json を runs/html/*.html に一括変換する。

新規実行分は dialogue_runner が自動生成するため不要。
過去ログを遡って変換したいときに使う。

使い方:
  python scripts/to_html.py          # 全ファイル
  python scripts/to_html.py --latest # 最新1件だけ
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dialogue_runner import RUNS_DIR, RUNS_HTML_DIR, _CSS, _fmt_plan_chip

OUT_DIR = RUNS_HTML_DIR


def _fmt_plan_chip_dict(plan: dict) -> str:
    parts = [plan.get("turn_goal", "?"), f"phase={plan.get('phase', '?')}"]
    if plan.get("ask_slot"):
        parts.append(f"ask={plan['ask_slot']}")
    if plan.get("owner_concern") not in (None, "unknown"):
        parts.append(f"concern={plan['owner_concern']}")
    return " · ".join(parts)


def convert(path: Path) -> Path:
    data = json.loads(path.read_text(encoding="utf-8"))
    m = re.search(r"(\d{8}_\d{6})", path.name)
    ts = m.group(1) if m else "00000000_000000"
    date = f"{ts[:4]}/{ts[4:6]}/{ts[6:8]} {ts[9:11]}:{ts[11:13]}"

    cond = data.get("condition", "?")
    meta = f"{data.get('model_borrower','?')} | temp={data.get('temperature','?')} | {data.get('max_turns','?')}ターン | {date}"
    case_id = data.get("case_id", "?")

    turns_html: list[str] = []
    borrower_n = landlord_n = 0

    for turn in data.get("turns", []):
        c = html_mod.escape(turn["content"])
        if turn["role"] == "landlord":
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
            if plan := turn.get("plan"):
                plan_chip = f'<div class="plan-chip">📋 {html_mod.escape(_fmt_plan_chip_dict(plan))}</div>'
            turns_html.append(f'''
<div class="msg-row borrower">
  <div class="avatar avatar-borrower">👤</div>
  <div class="bubble-group">
    <div class="speaker-name">借り手</div>
    {plan_chip}
    <div class="bubble bubble-borrower">{c}</div>
  </div>
</div>''')

    body = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{case_id} / {cond}</title>
  <style>{_CSS}</style>
</head>
<body>
  <header>
    <div>
      <div class="header-title">
        {html_mod.escape(case_id)}
        <span class="badge badge-{cond}">{cond}</span>
      </div>
      <div class="header-meta">{html_mod.escape(meta)}</div>
    </div>
  </header>
  <div class="chat-area">
    {"".join(turns_html)}
  </div>
</body>
</html>"""

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / path.with_suffix(".html").name
    out.write_text(body, encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--latest", action="store_true")
    args = parser.parse_args()

    paths = sorted(RUNS_DIR.glob("*.json"))
    if not paths:
        print("runs/ に JSON ファイルがありません")
        return
    for p in ([paths[-1]] if args.latest else paths):
        print(f"🌐 {convert(p).name}")


if __name__ == "__main__":
    main()
