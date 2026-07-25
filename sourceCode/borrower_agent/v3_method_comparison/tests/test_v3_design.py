from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT.parent / "shared"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from article_variants import load_case_with_information_level
from dialogue_runner import run_dialogue
from evidence_cache import load_or_create_evidence_inventory
from method_auditor import parse_method_audit
from methods import METHOD_IDS, get_method_spec
from models import Case, MethodSlot, Property, TurnPlan
from planner import fallback_plan, parse_method_plan
from run_experiment import build_batch_manifest, build_jobs
from summarize_method_audits import summarize


class V3DesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case_path = (
            SHARED / "data" / "eval_cases" / "case01_ceramic_atelier.yaml"
        )
        cls.property_path = (
            SHARED / "data" / "properties" / "property01_kuwana.yaml"
        )

    def test_four_method_conditions_have_explicit_slots(self) -> None:
        self.assertEqual(METHOD_IDS, ("plain", "prep", "star", "aida"))
        self.assertEqual(
            get_method_spec("prep").slots,
            ("point", "reason", "example", "point_restated"),
        )
        self.assertEqual(
            get_method_spec("star").slots,
            ("situation", "task", "action", "result"),
        )
        self.assertTrue(get_method_spec("aida").allows_call_to_action)

    def test_information_variants_are_fixed_and_increase_in_richness(self) -> None:
        small = load_case_with_information_level(self.case_path, "small")
        medium = load_case_with_information_level(self.case_path, "medium")
        large = load_case_with_information_level(self.case_path, "large")

        self.assertEqual(small.meta["information_level"], "small")
        self.assertEqual(medium.meta["information_level"], "medium")
        self.assertEqual(large.meta["information_level"], "large")
        self.assertLess(len(small.article), len(medium.article))
        self.assertLess(len(medium.article), len(large.article))
        self.assertNotIn("常滑市", small.article)
        self.assertIn("常滑市", medium.article)
        self.assertIn("大学では森林資源", large.article)

    def test_missing_variant_does_not_fall_back_to_automatic_summary(self) -> None:
        missing_case = (
            SHARED / "data" / "eval_cases" / "kanda-wanpaku-club.yaml"
        )
        with self.assertRaisesRegex(FileNotFoundError, "自動生成へフォールバック"):
            load_case_with_information_level(missing_case, "small")

    def test_method_plan_removes_quotes_not_found_in_article(self) -> None:
        case = Case(
            id="test",
            title="test",
            article="陶芸を学びました。作品制作を続けたいです。",
        )
        raw = json.dumps(
            {
                "turn_goal": "appeal",
                "response_strategy": "answer_first",
                "apply_method": True,
                "method_slots": {
                    "situation": {
                        "quote": "陶芸を学びました。",
                        "purpose": "学習背景",
                    },
                    "task": {
                        "quote": "記事にない課題です。",
                        "purpose": "架空の課題",
                    },
                    "action": {
                        "quote": "陶芸を学びました。",
                        "purpose": "重複引用",
                    },
                    "result": {
                        "quote": "記事にない成果です。",
                        "purpose": "架空の成果",
                    },
                },
                "missing_slots": [],
                "ask_slot": None,
                "owner_concern": "unknown",
            },
            ensure_ascii=False,
        )
        state = {
            "remaining_turns_including_current": 4,
            "last_landlord_action": {"act": "ask_usage"},
            "used_evidence_quotes": [],
        }

        plan = parse_method_plan(raw, case, "star", state)

        self.assertIsNotNone(plan)
        self.assertFalse(plan.apply_method)
        self.assertEqual(plan.method_slots["situation"].quote, "陶芸を学びました。")
        self.assertEqual(plan.method_slots["task"].quote, "")
        self.assertEqual(plan.method_slots["action"].quote, "")
        self.assertEqual(plan.method_slots["result"].quote, "")
        self.assertEqual(
            plan.missing_slots,
            ["task", "action", "result"],
        )

    def test_aida_action_is_not_emitted_without_grounded_content(self) -> None:
        case = Case(id="test", title="test", article="陶芸をしています。")
        raw = json.dumps(
            {
                "turn_goal": "appeal",
                "response_strategy": "answer_first",
                "apply_method": True,
                "method_slots": {
                    "attention": {
                        "quote": "陶芸をしています。",
                        "purpose": "活動",
                    },
                    "interest": {"quote": "", "purpose": ""},
                    "desire": {"quote": "", "purpose": ""},
                    "action": {
                        "quote": "",
                        "purpose": "さらに話を聞くことを検討してもらう",
                    },
                },
                "missing_slots": ["interest", "desire"],
                "ask_slot": None,
                "owner_concern": "unknown",
            },
            ensure_ascii=False,
        )
        state = {
            "remaining_turns_including_current": 4,
            "last_landlord_action": {"act": "ask_usage"},
            "used_evidence_quotes": [],
        }

        plan = parse_method_plan(raw, case, "aida", state)

        self.assertFalse(plan.apply_method)

    def test_final_turn_disables_aida_action(self) -> None:
        case = Case(
            id="test",
            title="test",
            article="陶芸をしています。制作が好きです。制作を続けたいです。",
        )
        raw = json.dumps(
            {
                "turn_goal": "appeal",
                "response_strategy": "answer_first",
                "apply_method": True,
                "method_slots": {
                    "attention": {"quote": "陶芸をしています。", "purpose": ""},
                    "interest": {"quote": "制作が好きです。", "purpose": ""},
                    "desire": {"quote": "制作を続けたいです。", "purpose": ""},
                    "action": {
                        "quote": "",
                        "purpose": "さらに話を聞くことを検討してもらう",
                    },
                },
                "missing_slots": [],
                "ask_slot": None,
                "owner_concern": "unknown",
            },
            ensure_ascii=False,
        )
        state = {
            "remaining_turns_including_current": 1,
            "last_landlord_action": {"act": "ask_operation"},
            "used_evidence_quotes": [],
        }

        plan = parse_method_plan(raw, case, "aida", state)

        self.assertFalse(plan.apply_method)
        self.assertEqual(plan.response_strategy, "close")
        self.assertEqual(plan.method_slots["action"].purpose, "")
        self.assertIn("action", plan.missing_slots)

    def test_prep_point_restated_can_reuse_point_quote(self) -> None:
        case = Case(
            id="test",
            title="test",
            article="制作を続けたいです。制作が好きです。陶芸を学びました。",
        )
        raw = json.dumps(
            {
                "turn_goal": "appeal",
                "response_strategy": "answer_first",
                "apply_method": True,
                "method_slots": {
                    "point": {"quote": "制作を続けたいです。", "purpose": ""},
                    "reason": {"quote": "制作が好きです。", "purpose": ""},
                    "example": {"quote": "陶芸を学びました。", "purpose": ""},
                    "point_restated": {
                        "quote": "制作を続けたいです。",
                        "purpose": "",
                    },
                },
                "missing_slots": [],
                "ask_slot": None,
                "owner_concern": "unknown",
            },
            ensure_ascii=False,
        )
        state = {
            "remaining_turns_including_current": 3,
            "last_landlord_action": {"act": "ask_usage"},
            "used_evidence_quotes": [],
        }

        plan = parse_method_plan(raw, case, "prep", state)

        self.assertTrue(plan.apply_method)
        self.assertEqual(plan.missing_slots, [])
        self.assertEqual(
            plan.method_slots["point_restated"].quote,
            plan.method_slots["point"].quote,
        )

    def test_actual_planner_is_limited_to_shared_evidence_inventory(self) -> None:
        case = Case(
            id="test",
            title="test",
            article="陶芸を学びました。作品制作を続けたいです。",
        )
        raw = json.dumps(
            {
                "turn_goal": "appeal",
                "response_strategy": "answer_first",
                "apply_method": True,
                "method_slots": {
                    "evidence": {
                        "quote": "作品制作を続けたいです。",
                        "purpose": "継続意思",
                    }
                },
                "missing_slots": [],
                "ask_slot": None,
                "owner_concern": "unknown",
            },
            ensure_ascii=False,
        )
        state = {
            "remaining_turns_including_current": 4,
            "last_landlord_action": {"act": "ask_usage"},
            "used_evidence_quotes": [],
        }
        inventory = {
            "enacted_commitment": [
                {"quote": "陶芸を学びました。", "summary": "陶芸を学びました。"}
            ]
        }

        plan = parse_method_plan(
            raw,
            case,
            "plain",
            state,
            passion_evidence_inventory=inventory,
        )

        self.assertFalse(plan.apply_method)
        self.assertEqual(plan.method_slots["evidence"].quote, "")
        self.assertEqual(plan.missing_slots, ["evidence"])

    def test_fallback_records_all_slots_as_missing(self) -> None:
        state = {
            "remaining_turns_including_current": 2,
            "last_landlord_action": {"act": "raise_concern"},
        }
        plan = fallback_plan("prep", state)
        self.assertFalse(plan.apply_method)
        self.assertEqual(plan.response_strategy, "acknowledge_concern")
        self.assertEqual(
            plan.missing_slots,
            ["point", "reason", "example", "point_restated"],
        )

    def test_audit_separates_available_realization_from_canonical_completion(self) -> None:
        plan = TurnPlan(
            turn_goal="appeal",
            evidence_summary="",
            ask_slot=None,
            owner_concern="unknown",
            method="star",
            response_strategy="answer_first",
            apply_method=True,
            method_slots={
                "situation": MethodSlot("背景です。", "背景です。"),
                "task": MethodSlot("課題です。", "課題です。"),
                "action": MethodSlot("行動しました。", "行動しました。"),
                "result": MethodSlot(),
            },
            missing_slots=["result"],
        )
        raw = json.dumps(
            {
                "slot_realized": {
                    "situation": True,
                    "task": True,
                    "action": True,
                    "result": False,
                },
                "ordered": True,
                "grounded": True,
                "available_slots_realized": True,
                "canonical_method_complete": True,
                "notes": "",
            }
        )

        audit = parse_method_audit(raw, plan)

        self.assertTrue(audit.available_slots_realized)
        self.assertFalse(audit.canonical_method_complete)

    def test_run_result_records_both_experimental_factors(self) -> None:
        case = load_case_with_information_level(self.case_path, "small")
        prop = Property.from_yaml(self.property_path)
        plan = TurnPlan(
            turn_goal="answer",
            evidence_summary="",
            ask_slot=None,
            owner_concern="unknown",
            method="prep",
            response_strategy="answer_first",
            apply_method=False,
            method_slots={
                name: MethodSlot() for name in get_method_spec("prep").slots
            },
            missing_slots=list(get_method_spec("prep").slots),
        )

        def fake_call(system_prompt, history, caller_role, temperature=0):
            if caller_role == "borrower":
                return "陶作家として、アトリエ兼住居に使いたいです。"
            if "topic: kiln_and_workflow" in system_prompt:
                return "ガス窯を含め、どのように作品を制作したいですか？"
            if "topic: noise_and_smoke" in system_prompt:
                return "周辺が住宅街なので、音や煙が心配です。"
            if "topic: storage_and_shipping" in system_prompt:
                return "作品の保管や発送に必要なスペースはありますか？"
            return "お考えは分かりました。ありがとうございました。"

        with (
            patch("dialogue_runner.plan_turn", return_value=plan),
            patch("dialogue_runner.call_llm", side_effect=fake_call),
            patch(
                "dialogue_runner.verify_utterance",
                side_effect=lambda text, *args, **kwargs: text,
            ),
            patch("dialogue_runner.get_model", return_value="test-model"),
            patch("dialogue_runner._save"),
            patch("dialogue_runner._print_turn"),
            patch("dialogue_runner._print_plan"),
            patch("dialogue_runner._print_landlord_action"),
        ):
            result = run_dialogue(
                case,
                prop,
                condition="prep",
                information_level="small",
                passion_evidence_inventory={"future_continuity": []},
                evidence_inventory_id="test:small:inventory",
                evidence_inventory_sha256="abc123",
                batch_id="batch-test",
                replicate_index=2,
                execution_index=7,
                order_seed=42,
                max_turns=4,
                audit_method=False,
            )

        serialized = result.to_dict()
        self.assertEqual(serialized["method"], "prep")
        self.assertEqual(serialized["information_level"], "small")
        self.assertEqual(serialized["condition"], "prep")
        self.assertEqual(serialized["design_version"], "v3.1")
        self.assertEqual(serialized["evidence_inventory_id"], "test:small:inventory")
        self.assertEqual(serialized["replicate_index"], 2)
        self.assertEqual(serialized["execution_index"], 7)
        self.assertEqual(serialized["order_seed"], 42)

    def test_method_audit_summary_groups_method_and_information_level(self) -> None:
        data = {
            "method": "star",
            "information_level": "medium",
            "turns": [
                {
                    "role": "borrower",
                    "plan": {
                        "apply_method": True,
                        "missing_slots": ["result"],
                    },
                    "method_audit": {
                        "available_slots_realized": True,
                        "canonical_method_complete": False,
                        "ordered": True,
                        "grounded": True,
                    },
                },
                {"role": "landlord", "content": "質問"},
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "run.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            rows = summarize([path])

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["method"], "star")
        self.assertEqual(rows[0]["information_level"], "medium")
        self.assertEqual(rows[0]["method_application_rate"], "1.000")
        self.assertEqual(rows[0]["available_slots_realized_rate"], "1.000")
        self.assertEqual(rows[0]["canonical_method_complete_rate"], "0.000")
        self.assertEqual(rows[0]["grounded_rate"], "1.000")
        self.assertEqual(rows[0]["missing_slots"], "result:1")

    def test_evidence_inventory_is_created_once_and_reused(self) -> None:
        case = Case(
            id="test",
            title="test",
            article="陶芸を学び、制作を続けたいです。",
        )
        inventory = {
            "enacted_commitment": [
                {
                    "quote": "陶芸を学び",
                    "summary": "陶芸を学び",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir)
            with (
                patch(
                    "evidence_cache.extract_passion_evidence",
                    return_value=inventory,
                ) as extractor,
                patch("evidence_cache.get_model", return_value="test-model"),
            ):
                first = load_or_create_evidence_inventory(
                    case,
                    "small",
                    cache_dir=cache_dir,
                )
                second = load_or_create_evidence_inventory(
                    case,
                    "small",
                    cache_dir=cache_dir,
                )

        extractor.assert_called_once()
        self.assertEqual(first.inventory_id, second.inventory_id)
        self.assertEqual(first.inventory_sha256, second.inventory_sha256)
        self.assertEqual(first.inventory, second.inventory)

    def test_jobs_are_repeated_and_randomized_reproducibly(self) -> None:
        prepared = [
            {"case": "case", "property": "prop", "level": "small"},
            {"case": "case", "property": "prop", "level": "large"},
        ]
        methods = ["plain", "prep", "star", "aida"]
        first = build_jobs(prepared, methods, repetitions=2, order_seed=17)
        second = build_jobs(prepared, methods, repetitions=2, order_seed=17)
        different = build_jobs(prepared, methods, repetitions=2, order_seed=18)

        self.assertEqual(first, second)
        self.assertNotEqual(first, different)
        self.assertEqual(len(first), 16)
        self.assertEqual(
            sorted(job["replicate_index"] for job in first),
            [1] * 8 + [2] * 8,
        )

    def test_batch_manifest_preserves_planned_execution_order(self) -> None:
        jobs = [
            {
                "case": SimpleNamespace(id="case01"),
                "property": SimpleNamespace(id="property01"),
                "level": "medium",
                "method": "star",
                "replicate_index": 2,
                "evidence": SimpleNamespace(
                    inventory_id="inventory-1",
                    inventory_sha256="sha-1",
                ),
            },
            {
                "case": SimpleNamespace(id="case01"),
                "property": SimpleNamespace(id="property01"),
                "level": "small",
                "method": "plain",
                "replicate_index": 1,
                "evidence": SimpleNamespace(
                    inventory_id="inventory-2",
                    inventory_sha256="sha-2",
                ),
            },
        ]

        manifest = build_batch_manifest(
            jobs,
            batch_id="batch-test",
            order_seed=42,
            repetitions=2,
            max_turns=4,
            temperature=0,
        )

        self.assertEqual(manifest["planned_dialogues"], 2)
        self.assertEqual(
            [item["execution_index"] for item in manifest["execution_order"]],
            [1, 2],
        )
        self.assertEqual(
            manifest["execution_order"][0]["evidence_inventory_id"],
            "inventory-1",
        )


if __name__ == "__main__":
    unittest.main()
