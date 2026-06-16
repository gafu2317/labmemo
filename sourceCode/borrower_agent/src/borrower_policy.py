from __future__ import annotations

import json
from pathlib import Path

from models import Case, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def build_system_prompt(case: Case, condition: str, plan: TurnPlan | None = None) -> str:
    """
    Realizerのsystem promptを構築する。
    planが与えられた場合はプロンプトに埋め込む（毎ターン更新）。
    planがない場合は計画フィールドを空にする。
    """
    plan_json = json.dumps(plan.to_dict(), ensure_ascii=False, indent=2) if plan else "{}"

    if condition == "baseline":
        return _load("realizer_baseline.txt").replace("{article}", case.article).replace("{plan_json}", plan_json)

    if condition == "proposed":
        return _load("realizer_proposed.txt").replace("{article}", case.article).replace("{plan_json}", plan_json)

    raise ValueError(f"未知の条件: {condition!r}  使用可能: baseline / proposed")
