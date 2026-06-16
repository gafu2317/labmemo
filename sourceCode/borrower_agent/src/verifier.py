from __future__ import annotations

from pathlib import Path

from llm_client import call_llm_single
from models import Case

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def verify_utterance(utterance: str, case: Case, temperature: float = 0) -> str:
    """
    生成された借り手の発話を検証し、プロファイルに根拠のない主張を除去する。
    BaselineとProposed両条件で共通して使用する。
    """
    system = _load("verifier.txt").replace("{article}", case.article)
    verified = call_llm_single(
        system_prompt=system,
        user_message=f"以下の発話を検証してください。\n\n{utterance}",
        temperature=temperature,
    )
    return verified.strip()
