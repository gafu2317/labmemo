from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SCENARIOS_DIR = Path(__file__).parent.parent / "scenarios"

# Proposed 条件で使う、記事から観測可能な「熱意の証拠」の種類。
# no_supported_signal は、該当する根拠が記事にないときに捏造を避けるために使う。
MOVES = (
    "personal_origin",
    "identity_value",
    "enacted_commitment",
    "persistence",
    "concrete_episode",
    "concern_aligned_commitment",
    "future_continuity",
    "no_supported_signal",
)

RESPONSE_STRATEGIES = (
    "answer_first",
    "acknowledge_concern",
    "ask_fit_question",
    "close",
)


@dataclass
class TurnPlan:
    """Plannerが各ターン前に生成する計画。"""
    turn_goal: str   # "appeal" | "ask_fit_question" | "empathize" | "reassure" | "close" | "answer"
    evidence_summary: str  # 使用する借り手情報の要約
    ask_slot: str | None   # 今ターンで聞く物件情報のキーワード
    owner_concern: str     # "unknown" | "cost" | "renovation" | "duration" | "other"
    # Baseline（固定感情）用。Proposed では null 可
    phase: str | None = None  # "opening" | "middle" | "closing"
    # Proposed（熱意証拠）用。Baseline では null 可
    move: str | None = None
    response_strategy: str | None = None
    evidence_quote: str | None = None  # 抽出済み在庫から選んだ記事原文
    key_message: str | None = None  # 今ターンで伝える核（1文）

    def to_dict(self) -> dict:
        d: dict[str, Any] = {
            "turn_goal": self.turn_goal,
            "evidence_summary": self.evidence_summary,
            "ask_slot": self.ask_slot,
            "owner_concern": self.owner_concern,
        }
        if self.phase is not None:
            d["phase"] = self.phase
        if self.move is not None:
            d["move"] = self.move
        if self.response_strategy is not None:
            d["response_strategy"] = self.response_strategy
        if self.evidence_quote is not None:
            d["evidence_quote"] = self.evidence_quote
        if self.key_message is not None:
            d["key_message"] = self.key_message
        return d


@dataclass
class Case:
    id: str
    title: str
    article: str
    meta: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: Path) -> Case:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(
            id=data["id"],
            title=data["title"],
            article=data["article"],
            meta=data.get("meta", {}),
        )


@dataclass
class Property:
    id: str
    title: str
    property_facts: dict[str, str]
    opening: str
    landlord_scenario: dict[str, Any] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: Path) -> Property:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        scenario_path = SCENARIOS_DIR / f"{data['id']}.yaml"
        scenario_data: dict[str, Any] = {}
        if scenario_path.exists():
            with open(scenario_path, encoding="utf-8") as f:
                scenario_data = yaml.safe_load(f) or {}
            scenario_property_id = scenario_data.get("property_id")
            if scenario_property_id not in (None, data["id"]):
                raise ValueError(
                    f"{scenario_path.name} の property_id={scenario_property_id!r} が "
                    f"物件ID={data['id']!r} と一致しません。"
                )

        return cls(
            id=data["id"],
            title=data["title"],
            property_facts=data.get("property_facts", {}),
            opening=data["opening"],
            landlord_scenario=scenario_data.get(
                "landlord_scenario",
                data.get("landlord_scenario", {}),
            ),
            meta=data.get("meta", {}),
        )


@dataclass
class LandlordAction:
    """実験側が制御する大家の対話行為。LLMはこの行為を自由に変更しない。"""
    act: str
    topic: str
    instruction: str

    def to_dict(self) -> dict[str, str]:
        return {
            "act": self.act,
            "topic": self.topic,
            "instruction": self.instruction,
        }


@dataclass
class Turn:
    role: str     # "borrower" | "landlord"
    content: str
    plan: TurnPlan | None = None  # 借り手ターンのみ。Plannerが生成した計画
    landlord_action: LandlordAction | None = None  # 大家ターンのみ


@dataclass
class RunResult:
    case_id: str
    property_id: str
    condition: str
    model_borrower: str
    model_landlord: str
    temperature: float
    max_turns: int
    turns: list[Turn]
    passion_evidence_inventory: dict[str, list[dict[str, str]]] | None = None

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "property_id": self.property_id,
            "condition": self.condition,
            "model_borrower": self.model_borrower,
            "model_landlord": self.model_landlord,
            "temperature": self.temperature,
            "max_turns": self.max_turns,
            **(
                {"passion_evidence_inventory": self.passion_evidence_inventory}
                if self.passion_evidence_inventory is not None
                else {}
            ),
            "turns": [
                {
                    "role": t.role,
                    "content": t.content,
                    **({"plan": t.plan.to_dict()} if t.plan else {}),
                    **(
                        {"landlord_action": t.landlord_action.to_dict()}
                        if t.landlord_action
                        else {}
                    ),
                }
                for t in self.turns
            ],
        }
