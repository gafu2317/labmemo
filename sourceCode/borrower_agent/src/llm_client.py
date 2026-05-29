from __future__ import annotations

import os

import anthropic

from models import Turn

_client: anthropic.Anthropic | None = None

DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def get_model() -> str:
    return os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)


def call_llm(
    system_prompt: str,
    history: list[Turn],
    caller_role: str,
    temperature: float = 0,
) -> str:
    """
    caller_role（"borrower" または "landlord"）を自分として、
    history を Anthropic messages 形式に変換して API を呼び出す。

    - 自分（caller_role）の過去発話 → "assistant"
    - 相手の発話              → "user"
    """
    messages = []
    for turn in history:
        api_role = "assistant" if turn.role == caller_role else "user"
        messages.append({"role": api_role, "content": turn.content})

    # Anthropic API は最初のメッセージが user である必要がある
    # opening（大家の0ターン目）が先頭に来る場合、大家視点では assistant になるが
    # 借り手視点では user になるので問題なし。
    # 大家視点で最初の turn が大家（=assistant）になるケースを除去する。
    if messages and messages[0]["role"] == "assistant":
        messages = messages[1:]

    response = _get_client().messages.create(
        model=get_model(),
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
        temperature=temperature,
    )
    return response.content[0].text
