import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tpta import evaluate_case, validate_case  # noqa: E402


def base_case():
    return {
        "id": "T-001",
        "condition": "Test condition",
        "purpose": "Test purpose",
        "evidence": [{"id": "E1", "statement": "Observed fact", "status": "SUPPORTED"}],
        "gates": [{"id": "G1", "required": True, "status": "PASS", "reason": "ok"}],
        "comparative_result": "Option B",
        "human_decision": None,
    }


class TestTPTA(unittest.TestCase):
    def test_all_required_pass_is_ready_for_human_decision(self):
        result = evaluate_case(base_case())
        self.assertEqual(result["system_posture"], "READY_FOR_HUMAN_DECISION")
        self.assertIsNone(result["human_decision"])

    def test_required_fail_forces_hold_despite_comparative_winner(self):
        case = base_case()
        case["gates"].append({"id": "G2", "required": True, "status": "FAIL", "reason": "blocking"})
        result = evaluate_case(case)
        self.assertEqual(result["comparative_result"], "Option B")
        self.assertEqual(result["system_posture"], "HOLD")
        self.assertIn("G2", result["controlling_issues"]["failed_gates"])

    def test_required_unknown_propagates(self):
        case = base_case(); case["gates"][0]["status"] = "UNKNOWN"
        self.assertEqual(evaluate_case(case)["system_posture"], "INSUFFICIENT_EVIDENCE")

    def test_fail_precedes_unknown(self):
        case = base_case()
        case["gates"] = [
            {"id": "GF", "required": True, "status": "FAIL"},
            {"id": "GU", "required": True, "status": "UNKNOWN"},
        ]
        result = evaluate_case(case)
        self.assertEqual(result["system_posture"], "HOLD")
        self.assertEqual(result["controlling_issues"]["unknown_gates"], ["GU"])

    def test_optional_fail_does_not_control_posture(self):
        case = base_case(); case["gates"].append({"id":"G2","required":False,"status":"FAIL"})
        self.assertEqual(evaluate_case(case)["system_posture"], "READY_FOR_HUMAN_DECISION")

    def test_zero_required_gates_is_invalid(self):
        case = base_case(); case["gates"][0]["required"] = False
        self.assertIn("at least one gate must be required", validate_case(case))

    def test_empty_gates_must_not_earn_readiness(self):
        case = base_case()
        case["gates"] = []
        self.assertIn("at least one gate must be required", validate_case(case))
        with self.assertRaisesRegex(ValueError, "at least one gate must be required"):
            evaluate_case(case)

    def test_missing_gates_must_not_earn_readiness(self):
        case = base_case()
        case.pop("gates")
        self.assertIn("missing required field: gates", validate_case(case))
        with self.assertRaises(ValueError):
            evaluate_case(case)

    def test_optional_only_gates_must_not_earn_readiness(self):
        case = base_case()
        case["gates"][0]["required"] = False
        with self.assertRaisesRegex(ValueError, "at least one gate must be required"):
            evaluate_case(case)

    def test_required_must_be_boolean(self):
        case = base_case(); case["gates"][0]["required"] = "yes"
        self.assertTrue(any("required must be boolean" in e for e in validate_case(case)))

    def test_inversion_requires_evidence(self):
        case = base_case(); case["inversion"] = {"prior_frame":"A","proposed_frame":"B","evidence_ids":[],"counterevidence_ids":[],"falsification_test":"X","status":"PROPOSED"}
        self.assertTrue(any("inversion requires at least one evidence reference" in e for e in validate_case(case)))

    def test_supported_inversion_requires_supported_evidence(self):
        case = base_case(); case["evidence"][0]["status"] = "UNKNOWN"
        case["inversion"] = {"prior_frame":"A","proposed_frame":"B","evidence_ids":["E1"],"counterevidence_ids":[],"falsification_test":"X","status":"SUPPORTED"}
        self.assertTrue(any("SUPPORTED inversion requires" in e for e in validate_case(case)))

    def test_validation_non_unknown_requires_evidence(self):
        case = base_case(); case["validations"] = [{"id":"V1","status":"PASS","evidence_ids":[]}]
        self.assertTrue(any("status PASS requires evidence references" in e for e in validate_case(case)))

    def test_unknown_validation_may_have_no_evidence(self):
        case = base_case(); case["validations"] = [{"id":"V1","status":"UNKNOWN","evidence_ids":[]}]
        self.assertEqual(validate_case(case), [])

    def test_evaluator_never_invents_human_decision(self):
        self.assertIsNone(evaluate_case(base_case())["human_decision"])

    def test_recorded_human_decision_is_preserved_not_generated(self):
        case = base_case(); case["human_decision"] = "HOLD pending independent review"
        self.assertEqual(evaluate_case(case)["human_decision"], "HOLD pending independent review")


if __name__ == "__main__":
    unittest.main()
