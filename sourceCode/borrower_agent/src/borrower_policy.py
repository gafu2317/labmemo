from __future__ import annotations

from pathlib import Path

from models import Case

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def _fmt_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def build_system_prompt(case: Case, condition: str) -> str:
    common = _load("borrower_common.txt")

    if condition == "baseline":
        template = _load("borrower_baseline.txt")
        return template.format(
            common_rules=common,
            article=case.article,
        )

    if condition == "structured":
        template = _load("borrower_structured.txt")
        return template.format(
            common_rules=common,
            purpose=case.profile.purpose,
            wishes=_fmt_list(case.profile.wishes),
            constraints=_fmt_list(case.profile.constraints),
            questions=_fmt_list(case.profile.questions),
        )

    raise ValueError(f"未知の条件: {condition}")
