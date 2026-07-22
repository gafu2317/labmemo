from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT.parent / "shared"
sys.path.insert(0, str(ROOT / "src"))

from dialogue_runner import run_dialogue
from landlord_agent import (
    build_system_prompt,
    fallback_landlord_reply,
    opening_action,
    select_landlord_action,
    validate_landlord_reply,
    validate_landlord_scenario,
)
from models import Case, LandlordAction, Property, Turn, TurnPlan
from passion_evidence import parse_passion_evidence
from planner import _apply_plan_constraints, _fallback_plan, build_dialogue_state
from verifier import _remove_forbidden_sentences


class HybridLandlordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.property_path = SHARED / "data" / "properties" / "property01_kuwana.yaml"
        cls.case_path = SHARED / "data" / "eval_cases" / "case01_ceramic_atelier.yaml"

    def test_property_scenario_is_loaded_in_fixed_order(self) -> None:
        prop = Property.from_yaml(self.property_path)

        self.assertEqual(opening_action(prop).act, "ask_usage")
        self.assertEqual(
            [select_landlord_action(prop, i).act for i in range(1, 5)],
            ["ask_operation", "raise_concern", "ask_operation", "close"],
        )
        self.assertEqual(select_landlord_action(prop, 2).topic, "noise_and_smoke")

    def test_landlord_prompt_contains_facts_and_only_current_action(self) -> None:
        prop = Property.from_yaml(self.property_path)
        action = select_landlord_action(prop, 2)

        prompt = build_system_prompt(prop, action)

        self.assertIn("act: raise_concern", prompt)
        self.assertIn("topic: noise_and_smoke", prompt)
        self.assertIn("kiln_space", prompt)
        self.assertNotIn("{landlord_action}", prompt)
        self.assertNotIn("{property_facts}", prompt)

    def test_controlled_scenario_requires_matching_turn_count(self) -> None:
        prop = Property.from_yaml(self.property_path)

        validate_landlord_scenario(prop, 4)
        with self.assertRaisesRegex(ValueError, "max_turns=3"):
            validate_landlord_scenario(prop, 3)

    def test_landlord_reply_validation_enforces_action_shape(self) -> None:
        concern = LandlordAction("raise_concern", "noise", "懸念を伝える")
        close = LandlordAction("close", "end", "閉じる")
        question = LandlordAction("ask_operation", "usage", "尋ねる")

        self.assertTrue(validate_landlord_reply(concern, "音はどうですか？"))
        self.assertTrue(validate_landlord_reply(close, "内見に来てください。"))
        self.assertTrue(validate_landlord_reply(question, "分かりました。"))
        self.assertEqual(validate_landlord_reply(concern, "周辺への影響が心配です。"), [])
        self.assertEqual(validate_landlord_reply(close, fallback_landlord_reply(close)), [])
        kiln_question = fallback_landlord_reply(
            LandlordAction("ask_operation", "kiln_and_workflow", "制作方法を尋ねる")
        )
        self.assertIn("ガス窯", kiln_question)
        self.assertEqual(validate_landlord_reply(question, kiln_question), [])
        storage = LandlordAction("ask_operation", "storage_and_shipping", "保管を尋ねる")
        self.assertTrue(
            validate_landlord_reply(storage, "梱包材はどのくらいの量が必要ですか？")
        )
        self.assertEqual(
            validate_landlord_reply(storage, fallback_landlord_reply(storage)),
            [],
        )

    def test_verifier_removes_next_action_sentences_deterministically(self) -> None:
        text = "梱包スペースが必要です。実際にお会いして物件を見たいです。作品制作を続けたいです。"
        self.assertEqual(
            _remove_forbidden_sentences(text),
            "梱包スペースが必要です。作品制作を続けたいです。",
        )

    def test_planner_state_tracks_landlord_action_moves_and_remaining_turns(self) -> None:
        history = [
            Turn(
                role="landlord",
                content="どのように使いますか？",
                landlord_action=LandlordAction("ask_usage", "intended_use", "使い方を尋ねる"),
            ),
            Turn(
                role="borrower",
                content="陶芸の制作に使いたいです。",
                plan=TurnPlan(
                    turn_goal="appeal",
                    evidence_summary="陶芸制作",
                    ask_slot=None,
                    owner_concern="unknown",
                    move="identity_value",
                    response_strategy="answer_first",
                    evidence_quote="納得できる作品を追求したい",
                    key_message="納得できる作品を追求したい",
                ),
            ),
            Turn(
                role="landlord",
                content="音や煙が心配です。",
                landlord_action=LandlordAction("raise_concern", "noise_and_smoke", "懸念を伝える"),
            ),
        ]

        state = build_dialogue_state(history, turn_number=2, max_turns=4)

        self.assertEqual(state["remaining_turns_including_current"], 3)
        self.assertEqual(state["last_landlord_action"]["act"], "raise_concern")
        self.assertEqual(state["used_moves"], ["identity_value"])
        self.assertEqual(
            state["conveyed_key_messages"],
            ["納得できる作品を追求したい"],
        )

    def test_planner_fallback_respects_concern_and_final_turn(self) -> None:
        concern_state = {
            "current_turn": 3,
            "remaining_turns_including_current": 2,
            "last_landlord_action": {"act": "raise_concern"},
        }
        final_state = {
            "current_turn": 4,
            "remaining_turns_including_current": 1,
            "last_landlord_action": {"act": "ask_operation"},
        }

        inventory = {
            "concern_aligned_commitment": [
                {"quote": "地域に恩返ししたい", "summary": "協力者や地域に報いたい"}
            ],
            "future_continuity": [
                {"quote": "制作を続けたい", "summary": "制作を継続したい"}
            ],
        }
        concern_plan = _fallback_plan("proposed", concern_state, inventory)
        final_plan = _fallback_plan("proposed", final_state, inventory)
        self.assertEqual(concern_plan.move, "concern_aligned_commitment")
        self.assertEqual(concern_plan.response_strategy, "acknowledge_concern")
        self.assertEqual(final_plan.move, "future_continuity")
        self.assertEqual(final_plan.response_strategy, "close")
        self.assertEqual(_fallback_plan("baseline", final_state).phase, "closing")

        unconstrained = TurnPlan(
            turn_goal="answer",
            evidence_summary="",
            ask_slot="storage",
            owner_concern="unknown",
            move="identity_value",
            response_strategy="answer_first",
        )
        constrained = _apply_plan_constraints(unconstrained, "proposed", final_state)
        self.assertEqual(constrained.response_strategy, "close")
        self.assertEqual(constrained.turn_goal, "close")
        self.assertIsNone(constrained.ask_slot)

    def test_dialogue_logs_controlled_landlord_actions(self) -> None:
        case = Case.from_yaml(self.case_path)
        prop = Property.from_yaml(self.property_path)
        plan = TurnPlan(
            turn_goal="appeal",
            evidence_summary="記事の根拠",
            ask_slot=None,
            owner_concern="unknown",
            move="identity_value",
            response_strategy="answer_first",
            key_message="作品制作を続けたい",
        )
        landlord_prompts: list[str] = []

        def fake_call(system_prompt, history, caller_role, temperature=0):
            if caller_role == "landlord":
                landlord_prompts.append(system_prompt)
                if "topic: kiln_and_workflow" in system_prompt:
                    return "ガス窯を含め、どのように作品を制作したいですか？"
                if "topic: storage_and_shipping" in system_prompt:
                    return "制作以外に、梱包材の保管や発送に必要なスペースはありますか？"
                return "大家の制御済み応答です。"
            return "借り手の応答です。"

        with (
            patch("dialogue_runner.plan_turn", return_value=plan),
            patch("dialogue_runner.extract_passion_evidence", return_value={}),
            patch("dialogue_runner.call_llm", side_effect=fake_call),
            patch("dialogue_runner.verify_utterance", side_effect=lambda text, *args, **kwargs: text),
            patch("dialogue_runner.get_model", return_value="test-model"),
            patch("dialogue_runner._save"),
            patch("dialogue_runner._print_turn"),
            patch("dialogue_runner._print_plan"),
            patch("dialogue_runner._print_landlord_action"),
        ):
            result = run_dialogue(case, prop, condition="proposed", max_turns=4)

        actions = [
            turn.landlord_action.act
            for turn in result.turns
            if turn.role == "landlord" and turn.landlord_action
        ]
        self.assertEqual(
            actions,
            ["ask_usage", "ask_operation", "raise_concern", "ask_operation", "close"],
        )
        self.assertEqual(len(landlord_prompts), 4)
        self.assertIn("act: close", landlord_prompts[-1])
        serialized = result.to_dict()
        self.assertEqual(serialized["turns"][-1]["landlord_action"]["act"], "close")

    def test_passion_evidence_parser_drops_quotes_not_in_article(self) -> None:
        article = "陶芸を一年間\n学びました。試行錯誤しながら制作しています。"
        raw = """{
          "personal_origin": [],
          "identity_value": [],
          "enacted_commitment": [
            {"quote": "陶芸を一年間 学びました。", "summary": "陶芸を一年学んだ"},
            {"quote": "十年間学びました。", "summary": "十年学んだ"}
          ],
          "persistence": [],
          "concrete_episode": [],
          "concern_aligned_commitment": [],
          "future_continuity": []
        }"""

        inventory = parse_passion_evidence(raw, article)

        self.assertEqual(len(inventory["enacted_commitment"]), 1)
        self.assertEqual(
            inventory["enacted_commitment"][0],
            {
                "quote": "陶芸を一年間 学びました。",
                "summary": "陶芸を一年間 学びました。",
            },
        )


if __name__ == "__main__":
    unittest.main()
