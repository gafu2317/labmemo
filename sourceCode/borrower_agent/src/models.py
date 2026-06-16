from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class TurnPlan:
    """Plannerが各ターン前に生成する計画。BaselineとProposed両条件で共有する。"""
    turn_goal: str   # "appeal" | "ask_fit_question" | "empathize" | "reassure" | "close"
    phase: str       # "opening" | "middle" | "closing"
    evidence_summary: str  # 使用する借り手情報の要約
    ask_slot: str | None   # 今ターンで聞く物件情報のキーワード
    owner_concern: str     # "unknown" | "cost" | "renovation" | "duration" | "other"

    def to_dict(self) -> dict:
        return {
            "turn_goal": self.turn_goal,
            "phase": self.phase,
            "evidence_summary": self.evidence_summary,
            "ask_slot": self.ask_slot,
            "owner_concern": self.owner_concern,
        }


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
