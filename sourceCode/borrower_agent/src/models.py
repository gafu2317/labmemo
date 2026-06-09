from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


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
    role: str  # "borrower" | "landlord"
    content: str


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
            "turns": [{"role": t.role, "content": t.content} for t in self.turns],
        }
