from __future__ import annotations

import json
import re
from pathlib import Path

import yaml
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

RUNS_DIR = Path(__file__).parent.parent / "runs"
CASES_DIR = Path(__file__).parent.parent / "data" / "cases"


def _load_log(filename: str) -> dict:
    with open(RUNS_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def _load_slots_desc(case_id: str) -> dict[str, str]:
    """YAMLケースファイルからslotの説明文を取得する"""
    yaml_path = CASES_DIR / f"{case_id}.yaml"
    if not yaml_path.exists():
        return {}
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {s["id"]: s.get("description", "") for s in data.get("slots", [])}


def _all_logs() -> list[dict]:
    logs = []
    for path in sorted(RUNS_DIR.glob("*.json"), reverse=True):
        try:
            data = _load_log(path.name)
            m = re.search(r"(\d{8}_\d{6})", path.name)
            ts = m.group(1) if m else ""
            logs.append({
                "filename": path.name,
                "case_id": data.get("case_id", ""),
                "condition": data.get("condition", ""),
                "model": data.get("model_borrower", ""),
                "timestamp": ts,
                "turn_count": len([t for t in data.get("turns", []) if t["role"] == "borrower"]),
            })
        except Exception:
            continue
    return logs


@app.route("/")
def index():
    logs = _all_logs()
    grouped: dict[str, list] = {}
    for log in logs:
        grouped.setdefault(log["case_id"], []).append(log)
    return render_template("index.html", grouped=grouped)


@app.route("/log/<filename>")
def detail(filename: str):
    data = _load_log(filename)
    m = re.search(r"(\d{8}_\d{6})", filename)
    timestamp = m.group(1) if m else ""
    slots_desc = _load_slots_desc(data.get("case_id", ""))
    return render_template("detail.html", data=data, filename=filename,
                           timestamp=timestamp, slots_desc=slots_desc)


@app.route("/log/<filename>/save", methods=["POST"])
def save(filename: str):
    data = _load_log(filename)
    form = request.form

    for slot_id in data["slots_checklist"]:
        mentioned = form.get(f"mentioned_{slot_id}") == "on"
        evidence = form.get(f"evidence_{slot_id}", "").strip()
        data["slots_checklist"][slot_id]["mentioned"] = mentioned
        data["slots_checklist"][slot_id]["evidence_turn"] = int(evidence) if evidence.isdigit() else None

    with open(RUNS_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return redirect(url_for("detail", filename=filename))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
