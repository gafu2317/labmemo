from pathlib import Path
import sys
import unittest


SRC_DIR = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from models import TurnPlan
from planner import _apply_plan_constraints, _fallback_plan


INVENTORY = {
    "identity_value": [
        {
            "quote": "地域に恩返しをしたい",
            "summary": "活動を通して地域に恩返ししたい",
        }
    ],
    "enacted_commitment": [
        {
            "quote": "急須作りを教わり、制作もしています",
            "summary": "急須作りを学び、制作している",
        }
    ],
}


def _state(*, remaining=2, last_act="raise_concern"):
    return {
        "current_turn": 3,
        "remaining_turns_including_current": remaining,
        "last_landlord_action": {
            "act": last_act,
            "topic": "noise_and_smoke",
            "instruction": "音と煙の懸念を伝える",
        },
        "used_evidence_quotes": [],
    }


class PlannerConstraintTests(unittest.TestCase):
    def test_no_supported_signal_does_not_get_replaced_from_inventory(self):
        plan = TurnPlan(
            turn_goal="answer",
            move="no_supported_signal",
            response_strategy="acknowledge_concern",
            evidence_quote="",
            key_message="",
            evidence_summary="",
            ask_slot=None,
            owner_concern="other",
        )

        constrained = _apply_plan_constraints(
            plan,
            "proposed",
            _state(),
            INVENTORY,
        )

        self.assertEqual(constrained.move, "no_supported_signal")
        self.assertIsNone(constrained.evidence_quote)
        self.assertEqual(constrained.key_message, "")
        self.assertEqual(constrained.evidence_summary, "")

    def test_invalid_evidence_is_removed_instead_of_replaced(self):
        plan = TurnPlan(
            turn_goal="appeal",
            move="identity_value",
            response_strategy="acknowledge_concern",
            evidence_quote="在庫にない引用",
            key_message="地域への思い",
            evidence_summary="地域への思い",
            ask_slot=None,
            owner_concern="other",
        )

        constrained = _apply_plan_constraints(
            plan,
            "proposed",
            _state(),
            INVENTORY,
        )

        self.assertEqual(constrained.move, "no_supported_signal")
        self.assertIsNone(constrained.evidence_quote)
        self.assertEqual(constrained.key_message, "")
        self.assertEqual(constrained.evidence_summary, "")

    def test_fallback_uses_no_evidence_when_relevance_cannot_be_judged(self):
        fallback = _fallback_plan("proposed", _state(), INVENTORY)

        self.assertEqual(fallback.response_strategy, "acknowledge_concern")
        self.assertEqual(fallback.move, "no_supported_signal")
        self.assertIsNone(fallback.evidence_quote)
        self.assertEqual(fallback.key_message, "")


if __name__ == "__main__":
    unittest.main()
