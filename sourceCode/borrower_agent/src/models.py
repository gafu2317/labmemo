from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Profile:
    purpose: str
    wishes: list[str]
    constraints: list[str]
    questions: list[str]


@dataclass
class Slot:
    id: str
    description: str


@dataclass
class Case:
    id: str
    title: str
    article: str
    profile: Profile
    property_facts: dict[str, str]
    opening: str
    slots: list[Slot]
    meta: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: Path) -> Case:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        pd = data.get("profile", {})
        profile = Profile(
            purpose=pd.get("purpose", ""),
            wishes=pd.get("wishes", []),
            constraints=pd.get("constraints", []),
            questions=pd.get("questions", []),
        )
        slots = [Slot(id=s["id"], description=s["description"]) for s in data.get("slots", [])]

        return cls(
            id=data["id"],
            title=data["title"],
            article=data["article"],
            profile=profile,
            property_facts=data.get("property_facts", {}),
            opening=data["opening"],
            slots=slots,
            meta=data.get("meta", {}),
        )


@dataclass
class Turn:
    role: str  # "borrower" | "landlord"
    content: str


@dataclass
class RunResult:
    case_id: str
    condition: str
    model_borrower: str
    model_landlord: str
    temperature: float
    max_turns: int
    turns: list[Turn]
    slots_checklist: dict[str, dict]

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "condition": self.condition,
            "model_borrower": self.model_borrower,
            "model_landlord": self.model_landlord,
            "temperature": self.temperature,
            "max_turns": self.max_turns,
            "turns": [{"role": t.role, "content": t.content} for t in self.turns],
            "slots_checklist": self.slots_checklist,
        }
