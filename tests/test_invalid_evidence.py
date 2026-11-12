"""Reject malformed readiness evidence without ever treating it as verified."""
import unittest
from tools.boot_readiness import evaluate


class InvalidEvidenceTests(unittest.TestCase):
    def test_non_mapping_evidence_is_rejected(self):
        for model in ("RMP2102", "RMP2103"):
            for evidence in (None, True, False, [], ["board_uefi"], "verified", 1):
                with self.subTest(model=model, evidence=repr(evidence)):
                    with self.assertRaisesRegex(ValueError, "Evidence must be"):
                        evaluate(model, evidence)

    def test_empty_evidence_remains_fail_closed(self):
        for model in ("RMP2102", "RMP2103"):
            with self.subTest(model=model):
                result = evaluate(model, {})
                self.assertFalse(result["boot_ready"])
                self.assertFalse(result["flash_authorized"])


if __name__ == "__main__":
    unittest.main()
