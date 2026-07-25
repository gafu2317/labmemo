from __future__ import annotations

import re
import json
from pathlib import Path

from llm_client import call_llm_single
from models import Case, Turn, TurnPlan

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

_FORBIDDEN_NEXT_ACTIONS = (
    "見学",
    "内見",
    "訪問",
    "現地を見",
    "物件を見",
    "見させていただ",
    "お会い",
    "実際に会",
    "実際にお会い",
    "日程",
)


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def verify_utterance(
    utterance: str,
    case: Case,
    history: list[Turn] | None = None,
    plan: TurnPlan | None = None,
    temperature: float = 0,
) -> str:
    """
    生成された借り手の発話を検証し、プロファイルに根拠のない主張を除去する。
    BaselineとProposed両条件で共通して使用する。
    """
    system = _load("verifier.txt").replace("{article}", case.article)
    history_text = "\n".join(
        f"{'大家' if turn.role == 'landlord' else '借り手'}: {turn.content}"
        for turn in (history or [])
    )
    plan_text = json.dumps(plan.to_dict(), ensure_ascii=False, indent=2) if plan else "（なし）"
    selected_quotes = plan.selected_evidence_quotes() if plan else []
    evidence_instruction = ""
    if selected_quotes:
        evidence_instruction = (
            "\n\n## 今ターンで保持する検証済み証拠\n"
            + "\n".join(f"- 記事原文: {quote}" for quote in selected_quotes)
            + "\n候補発話に計画上必要な証拠の意味が現れていなければ、"
            "記事原文の意味を変えない短い表現を自然に補う。"
            "欠落扱いの話法要素は創作せず、誇張もしない。"
        )
    if plan and plan.method == "aida" and plan.apply_method:
        evidence_instruction += (
            "\nAIDAのActionとして、面談・内見・契約・日程を求めず、"
            "「関心があれば本人からさらに話を聞くことを検討してほしい」"
            "という低圧な発話行為だけは記事外の事実とは扱わない。"
        )
    verified = call_llm_single(
        system_prompt=system + evidence_instruction,
        user_message=(
            f"## これまでの対話\n\n{history_text or '（履歴なし）'}\n\n"
            f"## 今ターンの計画\n\n{plan_text}\n\n"
            f"## 検証対象の借り手発話\n\n{utterance}"
        ),
        temperature=temperature,
    )
    verified = verified.strip()
    required_evidence_audit = "".join(
        f"検証済み証拠「{quote}」の意味は、計画上使用する場合に保持する。"
        for quote in selected_quotes
    )
    verified = call_llm_single(
        system_prompt=(
            system
            + "\n\n## 最終監査（最優先）\n"
            "候補発話の全ての事実・因果関係・作業手順・数量・頻度が、"
            "記事または大家の発話から直接言い換えできるか再確認する。"
            "記事に別々に書かれた事実を新しい理由・目的・配慮で結びつけない。"
            "設備を希望している記載を、その設備の現在の使用経験へ変えない。"
            "陶芸の一般知識や尤もらしい推測は使わない。"
            + required_evidence_audit
            +
            "根拠のない部分を削除し、修正後の借り手発話のみ出力する。"
        ),
        user_message=(
            f"## 対話履歴\n\n{history_text or '（履歴なし）'}\n\n"
            f"## 今ターンの計画\n\n{plan_text}\n\n"
            f"## 候補発話\n\n{verified}"
        ),
        temperature=temperature,
    ).strip()
    forbidden = [phrase for phrase in _FORBIDDEN_NEXT_ACTIONS if phrase in verified]
    if forbidden:
        verified = call_llm_single(
            system_prompt=system,
            user_message=(
                f"## これまでの対話\n\n{history_text or '（履歴なし）'}\n\n"
                f"## 再修正対象\n\n{verified}\n\n"
                "## 必須の修正\n\n"
                f"次アクションの提案（{', '.join(forbidden)}）を含む文を削除し、"
                "それ以外は変えずに発話のみ出力してください。"
            ),
            temperature=temperature,
        ).strip()
    return _remove_forbidden_sentences(verified)


def _remove_forbidden_sentences(text: str) -> str:
    """LLMの再修正後にも残った次アクション文を決定的に除去する。"""
    sentences = re.split(r"(?<=[。！？!?])", text)
    kept = [
        sentence
        for sentence in sentences
        if sentence.strip() and not any(phrase in sentence for phrase in _FORBIDDEN_NEXT_ACTIONS)
    ]
    return "".join(kept).strip()
