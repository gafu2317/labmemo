from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from llm_client import call_llm_single
from models import Case, MOVES

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
EVIDENCE_TYPES = tuple(move for move in MOVES if move != "no_supported_signal")


def extract_passion_evidence(
    case: Case,
    temperature: float = 0,
) -> dict[str, list[dict[str, str]]]:
    """記事から熱意証拠を抽出し、原文に存在する引用だけを採用する。"""
    system = (PROMPTS_DIR / "passion_evidence_extractor.txt").read_text(
        encoding="utf-8"
    ).replace("{article}", case.article)
    raw = call_llm_single(
        system_prompt=system,
        user_message="記事を分析し、指定形式のJSONだけを出力してください。",
        temperature=temperature,
        max_tokens=2048,
    )
    return parse_passion_evidence(raw, case.article)


def parse_passion_evidence(
    raw: str,
    article: str,
) -> dict[str, list[dict[str, str]]]:
    """LLM出力を検証する。記事にない quote は決定的に除外する。"""
    inventory = {evidence_type: [] for evidence_type in EVIDENCE_TYPES}
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return inventory
    try:
        data = json.loads(match.group())
    except (json.JSONDecodeError, TypeError):
        return inventory

    for evidence_type in EVIDENCE_TYPES:
        items = data.get(evidence_type, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            quote = item.get("quote")
            summary = item.get("summary")
            if not isinstance(quote, str) or not isinstance(summary, str):
                continue
            quote = quote.strip()
            summary = summary.strip()
            if quote and summary and _normalized(quote) in _normalized(article):
                # LLM要約が引用より強い意味を持つ事故を避けるため、
                # Plannerへ渡す核は検証済み原文そのものに固定する。
                inventory[evidence_type].append({"quote": quote, "summary": quote})
    return inventory


def _normalized(text: str) -> str:
    """原文の内容を変えず、Unicode表記と空白・改行差だけを吸収する。"""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))
