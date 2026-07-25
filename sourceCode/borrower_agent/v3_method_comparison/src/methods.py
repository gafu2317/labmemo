from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MethodSpec:
    """V3で比較する既存話法の操作的定義。"""

    id: str
    name: str
    domain: str
    slots: tuple[str, ...]
    description: str
    slot_instructions: dict[str, str]
    allows_call_to_action: bool = False


METHOD_SPECS: dict[str, MethodSpec] = {
    "plain": MethodSpec(
        id="plain",
        name="Plain（構造指定なし）",
        domain="control",
        slots=("evidence",),
        description=(
            "大家の質問へ直接答え、関連する記事上の根拠があれば自然に添える。"
            "PREP・STAR・AIDAの順序や構成は指定しない。"
        ),
        slot_instructions={
            "evidence": "直前の問いに関連する、記事上の判断材料",
        },
    ),
    "prep": MethodSpec(
        id="prep",
        name="PREP",
        domain="presentation / interview",
        slots=("point", "reason", "example", "point_restated"),
        description="Point → Reason → Example → Point の順で、主張を簡潔に根拠づける。",
        slot_instructions={
            "point": "最初に伝える結論または用途",
            "reason": "その結論を支える本人の動機・理由・価値",
            "example": "記事にある具体的な経験・行動・出来事",
            "point_restated": "同じ主張を繰り返さず、目的または継続意思として短く結ぶ",
        },
    ),
    "star": MethodSpec(
        id="star",
        name="STAR",
        domain="employment interview",
        slots=("situation", "task", "action", "result"),
        description="Situation → Task → Action → Result の順で、過去の行動を具体化する。",
        slot_instructions={
            "situation": "活動の背景・置かれていた状況",
            "task": "本人が達成しようとしたこと、または向き合った課題",
            "action": "本人が実際に行った学習・制作・活動",
            "result": "記事に明記された結果・変化・反応。推測した成果は禁止",
        },
    ),
    "aida": MethodSpec(
        id="aida",
        name="AIDA",
        domain="sales / marketing communication",
        slots=("attention", "interest", "desire", "action"),
        description=(
            "Attention → Interest → Desire → Action の順で関心を形成する。"
            "V3では条件交渉をせず、Actionは本人からさらに話を聞くことを"
            "低圧に検討してもらう一文に限定する。"
        ),
        slot_instructions={
            "attention": "本人固有の活動・経験を示す、記事中の具体的な事実",
            "interest": "なぜその活動をしているか、本人にとっての意味",
            "desire": "その物件で継続したい活動や将来像。大家の利益を創作しない",
            "action": (
                "面談・内見・契約を迫らず、関心があれば本人からさらに話を聞くことを"
                "検討してもらう低圧な呼びかけ。記事引用は不要"
            ),
        },
        allows_call_to_action=True,
    ),
}

METHOD_IDS = tuple(METHOD_SPECS)
INFORMATION_LEVELS = ("small", "medium", "large")


def get_method_spec(method: str) -> MethodSpec:
    try:
        return METHOD_SPECS[method]
    except KeyError as exc:
        available = ", ".join(METHOD_IDS)
        raise ValueError(f"未知の手法: {method!r}  使用可能: {available}") from exc

