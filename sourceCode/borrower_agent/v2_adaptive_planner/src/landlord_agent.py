from __future__ import annotations

from pathlib import Path

from models import Property

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def _fmt_facts(facts: dict[str, str]) -> str:
    return "\n".join(f"- {k}: {v}" for k, v in facts.items())


def build_system_prompt(prop: Property) -> str:
    return _load("landlord.txt").replace("{property_facts}", _fmt_facts(prop.property_facts))
