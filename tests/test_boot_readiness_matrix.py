"""Exhaustive fail-closed checks for the two supported Realme Pad variants."""
import unittest

from tools.boot_readiness import REQUIRED, evaluate


class BootReadinessMatrixTests(unittest.TestCase):
    def test_each_missing_requirement_blocks_each_variant(self):
        for model in ("RMP2102", "RMP2103"):
            required = (*REQUIRED, "windows_wifi_driver")
            if model == "RMP2102":
                required += ("windows_lte_driver",)
            for missing_key in required:
                with self.subTest(model=model, missing=missing_key):
                    evidence = {key: True for key in required}
                    del evidence[missing_key]
                    result = evaluate(model, evidence)
                    self.assertFalse(result["boot_ready"])
                    self.assertEqual(result["missing"], [missing_key])
                    self.assertIs(result["flash_authorized"], False)

    def test_truthy_values_do_not_count_as_verified_evidence(self):
        for model in ("RMP2102", "RMP2103"):
            required = (*REQUIRED, "windows_wifi_driver")
            if model == "RMP2102":
                required += ("windows_lte_driver",)
            for key in required:
                for invalid in (1, "true", "verified", [True], {"verified": True}):
                    with self.subTest(model=model, key=key, invalid=repr(invalid)):
                        evidence = {name: True for name in required}
                        evidence[key] = invalid
                        result = evaluate(model, evidence)
                        self.assertFalse(result["boot_ready"])
                        self.assertIn(key, result["missing"])
                        self.assertIs(result["flash_authorized"], False)

    def test_full_boolean_matrix_never_authorizes_flash(self):
        for model in ("RMP2102", "RMP2103"):
            evidence = {key: True for key in REQUIRED}
            evidence["windows_wifi_driver"] = True
            if model == "RMP2102":
                evidence["windows_lte_driver"] = True
            result = evaluate(model, evidence)
            self.assertTrue(result["boot_ready"])
            self.assertEqual(result["missing"], [])
            self.assertIs(result["flash_authorized"], False)


if __name__ == "__main__":
    unittest.main()
