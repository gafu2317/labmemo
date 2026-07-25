from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SCENARIOS_DIR = Path(__file__).parent.parent / "scenarios"

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


@dataclass
class MethodSlot:
    """話法の1構成要素と、それを支える記事原文。"""

    quote: str = ""
    purpose: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"quote": self.quote, "purpose": self.purpose}


@dataclass
class MethodAudit:
    """最終発話に対する話法再現監査。効果評価とは分離する。"""

    slot_realized: dict[str, bool] = field(default_factory=dict)
    ordered: bool = False
    grounded: bool = False
    available_slots_realized: bool = False
    canonical_method_complete: bool | None = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot_realized": self.slot_realized,
            "ordered": self.ordered,
            "grounded": self.grounded,
            "available_slots_realized": self.available_slots_realized,
            "canonical_method_complete": self.canonical_method_complete,
            "notes": self.notes,
        }


@dataclass
class TurnPlan:
    """V3の各借り手ターンで生成する話法計画。"""

    turn_goal: str
    evidence_summary: str
    ask_slot: str | None
    owner_concern: str
    method: str = "plain"
    response_strategy: str = "answer_first"
    apply_method: bool = False
    method_slots: dict[str, MethodSlot] = field(default_factory=dict)
    missing_slots: list[str] = field(default_factory=list)
    # V2由来のログとの互換性を保つ任意フィールド。
    phase: str | None = None
    move: str | None = None
    evidence_quote: str | None = None
    key_message: str | None = None

    def selected_evidence_quotes(self) -> list[str]:
        return [
            slot.quote
            for slot in self.method_slots.values()
            if slot.quote
        ]

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "turn_goal": self.turn_goal,
            "evidence_summary": self.evidence_summary,
            "ask_slot": self.ask_slot,
            "owner_concern": self.owner_concern,
            "method": self.method,
            "response_strategy": self.response_strategy,
            "apply_method": self.apply_method,
            "method_slots": {
                name: slot.to_dict() for name, slot in self.method_slots.items()
            },
            "missing_slots": self.missing_slots,
            "selected_evidence_quotes": self.selected_evidence_quotes(),
        }
        if self.phase is not None:
            data["phase"] = self.phase
        if self.move is not None:
            data["move"] = self.move
        if self.evidence_quote is not None:
            data["evidence_quote"] = self.evidence_quote
        if self.key_message is not None:
            data["key_message"] = self.key_message
        return data


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
    role: str
    content: str
    plan: TurnPlan | None = None
    method_audit: MethodAudit | None = None
    landlord_action: LandlordAction | None = None


@dataclass
class RunResult:
    case_id: str
    property_id: str
    condition: str
    method: str
    information_level: str
    model_borrower: str
    model_landlord: str
    temperature: float
    max_turns: int
    turns: list[Turn]
    passion_evidence_inventory: dict[str, list[dict[str, str]]]
    evidence_inventory_id: str
    evidence_inventory_sha256: str
    batch_id: str
    replicate_index: int
    execution_index: int
    order_seed: int
    design_version: str = "v3.1"

    def to_dict(self) -> dict[str, Any]:
        return {
            "design_version": self.design_version,
            "case_id": self.case_id,
            "property_id": self.property_id,
            "condition": self.condition,
            "method": self.method,
            "information_level": self.information_level,
            "model_borrower": self.model_borrower,
            "model_landlord": self.model_landlord,
            "temperature": self.temperature,
            "max_turns": self.max_turns,
            "evidence_inventory_id": self.evidence_inventory_id,
            "evidence_inventory_sha256": self.evidence_inventory_sha256,
            "batch_id": self.batch_id,
            "replicate_index": self.replicate_index,
            "execution_index": self.execution_index,
            "order_seed": self.order_seed,
            "passion_evidence_inventory": self.passion_evidence_inventory,
            "turns": [
                {
                    "role": turn.role,
                    "content": turn.content,
                    **({"plan": turn.plan.to_dict()} if turn.plan else {}),
                    **(
                        {"method_audit": turn.method_audit.to_dict()}
                        if turn.method_audit
                        else {}
                    ),
                    **(
                        {"landlord_action": turn.landlord_action.to_dict()}
                        if turn.landlord_action
                        else {}
                    ),
                }
                for turn in self.turns
            ],
        }
