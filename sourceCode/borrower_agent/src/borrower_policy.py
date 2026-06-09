from __future__ import annotations

from pathlib import Path

from models import Case

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def build_system_prompt(case: Case, condition: str) -> str:
    common = _load("borrower_common.txt")

    if condition == "baseline":
        template = _load("borrower_baseline.txt")
        return template.format(common_rules=common, article=case.article)

    if condition == "proposed":
        template = _load("borrower_proposed.txt")
        return template.format(common_rules=common, article=case.article)

    raise ValueError(f"未知の条件: {condition!r}  使用可能: baseline / proposed")
