from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Proposed 条件で使う修辞ムーブ（面接・プレゼン由来）
MOVES = (
    "elevator_hook",
    "concrete_scene",
    "answer_first",
    "acknowledge_reframe",
    "ask_with_image",
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
    # Proposed（修辞ムーブ）用。Baseline では null 可
    move: str | None = None
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
    meta: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: Path) -> Property:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(
            id=data["id"],
            title=data["title"],
            property_facts=data.get("property_facts", {}),
            opening=data["opening"],
            meta=data.get("meta", {}),
        )


@dataclass
class Turn:
    role: str     # "borrower" | "landlord"
    content: str
    plan: TurnPlan | None = None  # 借り手ターンのみ。Plannerが生成した計画


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

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "property_id": self.property_id,
            "condition": self.condition,
            "model_borrower": self.model_borrower,
            "model_landlord": self.model_landlord,
            "temperature": self.temperature,
            "max_turns": self.max_turns,
            "turns": [
                {"role": t.role, "content": t.content, **({"plan": t.plan.to_dict()} if t.plan else {})}
                for t in self.turns
            ],
        }
