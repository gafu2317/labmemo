from __future__ import annotations

import re
from pathlib import Path

from models import LandlordAction, Property

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def _fmt_facts(facts: dict[str, str]) -> str:
    return "\n".join(f"- {k}: {v}" for k, v in facts.items())


_DEFAULT_RESPONSE_ACTIONS = (
    LandlordAction(
        act="ask_operation",
        topic="concrete_usage",
        instruction="借り手の活動内容や使い方を具体化する質問を1つする。",
    ),
    LandlordAction(
        act="raise_concern",
        topic="property_impact",
        instruction="借り手の使い方が建物や近隣に与える影響について、現実的な懸念を1つ短く伝える。",
    ),
    LandlordAction(
        act="ask_consideration",
        topic="response_to_concern",
        instruction="直前に示した懸念にどのように配慮するか、質問を1つする。",
    ),
    LandlordAction(
        act="close",
        topic="end_conversation",
        instruction="新しい質問や次アクションを出さず、話を聞いたことだけを中立的に短く伝えて終える。",
    ),
)


def _action_from_dict(data: dict, fallback: LandlordAction) -> LandlordAction:
    return LandlordAction(
        act=str(data.get("act", fallback.act)),
        topic=str(data.get("topic", fallback.topic)),
        instruction=str(data.get("instruction", fallback.instruction)),
    )


def opening_action(prop: Property) -> LandlordAction:
    fallback = LandlordAction(
        act="ask_usage",
        topic="intended_use",
        instruction="借り手がどのように物件を使いたいか、質問を1つする。",
    )
    data = prop.landlord_scenario.get("opening_action", {})
    return _action_from_dict(data, fallback) if isinstance(data, dict) else fallback


def select_landlord_action(prop: Property, response_turn: int) -> LandlordAction:
    """1始まりの大家応答番号に対応する制御済み対話行為を返す。"""
    fallback_index = min(max(response_turn - 1, 0), len(_DEFAULT_RESPONSE_ACTIONS) - 1)
    fallback = _DEFAULT_RESPONSE_ACTIONS[fallback_index]
    steps = prop.landlord_scenario.get("response_steps", [])
    if not isinstance(steps, list) or response_turn > len(steps):
        return fallback
    data = steps[response_turn - 1]
    return _action_from_dict(data, fallback) if isinstance(data, dict) else fallback


def validate_landlord_scenario(prop: Property, max_turns: int) -> None:
    """明示シナリオではターン数と行為数を一致させ、条件間の刺激を保つ。"""
    steps = prop.landlord_scenario.get("response_steps")
    if not isinstance(steps, list) or not steps:
        return
    if len(steps) != max_turns:
        raise ValueError(
            f"{prop.id} の landlord_scenario.response_steps は {len(steps)} 件ですが、"
            f"max_turns={max_turns} です。制御シナリオでは一致させてください。"
        )


def build_system_prompt(prop: Property, action: LandlordAction) -> str:
    action_text = (
        f"- act: {action.act}\n"
        f"- topic: {action.topic}\n"
        f"- instruction: {action.instruction}"
    )
    return (
        _load("landlord.txt")
        .replace("{property_facts}", _fmt_facts(prop.property_facts))
        .replace("{landlord_action}", action_text)
    )


_PRAISE_PATTERNS = (
    "素敵",
    "素晴ら",
    "感動",
    "好印象",
    "魅力的",
    "そういう姿勢は大切",
    "そういう姿勢は大事",
    "姿勢は大切",
    "姿勢は大事",
    "熱意が伝わ",
)
_NEXT_ACTION_PATTERNS = (
    "内見",
    "見学",
    "訪問",
    "現地",
    "お会い",
    "実際に会って",
    "日程",
    "あらためて確認",
)


def validate_landlord_reply(action: LandlordAction, reply: str) -> list[str]:
    """指定した大家行為に対する形式違反を返す。空リストなら有効。"""
    violations: list[str] = []
    has_question = "？" in reply or "?" in reply
    sentence_count = len(
        [part for part in re.findall(r"[^。！？!?]+[。！？!?]?", reply) if part.strip()]
    )

    if action.act.startswith("ask_") and not has_question:
        violations.append("指定行為は質問なのに疑問文がない")
    if action.act in {"raise_concern", "close"} and has_question:
        violations.append("質問禁止の行為で疑問文を出した")
    if sentence_count > 2:
        violations.append(f"{sentence_count}文あり、最大2文を超えた")
    if any(pattern in reply for pattern in _PRAISE_PATTERNS):
        violations.append("借り手への賞賛・評価を含む")
    if any(pattern in reply for pattern in _NEXT_ACTION_PATTERNS):
        violations.append("内見・対面・日程などの次アクションを含む")
    if action.topic == "kiln_and_workflow" and not (
        "ガス窯" in reply and ("制作" in reply or "作品" in reply)
    ):
        violations.append("指定topicのガス窯と制作工程を尋ねていない")
    if action.topic == "storage_and_shipping":
        if not any(word in reply for word in ("保管", "梱包", "発送", "配送")):
            violations.append("指定topicの保管・梱包・発送を尋ねていない")
        if any(word in reply for word in ("どのくらい", "量", "頻度", "月に", "週に", "何回")):
            violations.append("記事で答えられない量・頻度まで尋ねている")
    return violations


def fallback_landlord_reply(action: LandlordAction) -> str:
    """2回生成しても制約違反した場合の決定的な代替発話。"""
    if action.act == "close":
        return "お考えは分かりました。お話しいただき、ありがとうございました。"
    if action.act == "raise_concern":
        if action.topic == "noise_and_smoke":
            return "周辺が住宅街なので、ガス窯の音や煙が近隣に影響しないか心配しています。"
        return "その使い方について、物件や周辺への影響が気になっています。"
    topic_questions = {
        "kiln_and_workflow": "ガス窯を含め、この物件でどのように作品を制作したいですか？",
        "storage_and_shipping": "制作以外に、作品の保管や発送に必要なスペースはありますか？",
        "concrete_usage": "この物件での具体的な使い方を教えていただけますか？",
        "response_to_concern": "その懸念には、どのように配慮するお考えですか？",
    }
    if action.topic in topic_questions:
        return topic_questions[action.topic]
    return "その点について、もう少し具体的に教えていただけますか？"
