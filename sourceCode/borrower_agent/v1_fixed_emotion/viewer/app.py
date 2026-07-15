from __future__ import annotations

import json
import re
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)

RUNS_DIR = Path(__file__).parent.parent / "runs"


def _load_log(filename: str) -> dict:
    with open(RUNS_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def _ts_key(path: Path) -> str:
    m = re.search(r"(\d{8}_\d{6})", path.name)
    return m.group(1) if m else ""


def _all_logs() -> list[dict]:
    logs = []
    for path in sorted(RUNS_DIR.glob("*.json"), key=_ts_key, reverse=True):
        try:
            data = _load_log(path.name)
            ts = _ts_key(path)
            logs.append({
                "filename": path.name,
                "case_id": data.get("case_id", ""),
                "property_id": data.get("property_id", ""),
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
    case_latest: dict[str, str] = {}
    for log in logs:
        cid = log["case_id"]
        grouped.setdefault(cid, []).append(log)
        if cid not in case_latest:
            case_latest[cid] = log["timestamp"]
    grouped = dict(sorted(grouped.items(), key=lambda kv: case_latest.get(kv[0], ""), reverse=True))
    return render_template("index.html", grouped=grouped)


@app.route("/log/<filename>")
def detail(filename: str):
    data = _load_log(filename)
    m = re.search(r"(\d{8}_\d{6})", filename)
    timestamp = m.group(1) if m else ""
    return render_template("detail.html", data=data, filename=filename, timestamp=timestamp)


@app.route("/log/<filename>/print")
def print_view(filename: str):
    data = _load_log(filename)
    m = re.search(r"(\d{8}_\d{6})", filename)
    timestamp = m.group(1) if m else ""
    return render_template("print.html", data=data, filename=filename, timestamp=timestamp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
