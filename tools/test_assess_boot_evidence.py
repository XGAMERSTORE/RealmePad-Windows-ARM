"""Regression tests for offline Realme Pad boot-evidence classification."""
import unittest

from assess_boot_evidence import analyze


class BootEvidenceTests(unittest.TestCase):
    def test_unknown_device_cannot_be_marked_research_ready(self):
        result = analyze({"properties": {"ro.product.model": "Other Tablet", "ro.product.device": "unknown"}})
        self.assertFalse(result["boot_research_possible"])
        self.assertFalse(result["windows_boot_ready"])
        self.assertFalse(result["safe_to_flash"])

    def test_family_codename_allows_research_but_not_flashing(self):
        result = analyze({"properties": {"ro.product.model": "realme Pad", "ro.product.device": "RMP6768"}})
        self.assertTrue(result["boot_research_possible"])
        self.assertEqual(result["variant"], "unconfirmed")
        self.assertFalse(result["safe_to_flash"])

    def test_reject_embedded_family_codename(self):
        for device in ("not-rmp6768", "rmp6768_clone", "xrmp6768"):
            with self.subTest(device=device):
                result = analyze({"properties": {"ro.product.model": "Other Tablet",
                                                  "ro.product.device": device}})
                self.assertFalse(result["boot_research_possible"])
                self.assertFalse(result["safe_to_flash"])

    def test_accept_codename_separated_by_spaces(self):
        result = analyze({"properties": {"ro.product.model": "realme Pad",
                                          "ro.product.device": "realme RMP6768"}})
        self.assertTrue(result["boot_research_possible"])
        self.assertEqual(result["variant"], "unconfirmed")

    def test_exact_variant_allows_research_only(self):
        result = analyze({"properties": {"ro.product.model": "RMP2102", "ro.product.device": "RMP6768"}})
        self.assertTrue(result["boot_research_possible"])
        self.assertEqual(result["variant"], "LTE")
        self.assertFalse(result["windows_boot_ready"])

    def test_reject_model_substring_in_other_identifier(self):
        result = analyze({"properties": {"ro.product.model": "not-rmp2102", "ro.product.device": "unknown"}})
        self.assertEqual(result["variant"], "unconfirmed")
        self.assertFalse(result["boot_research_possible"])

    def test_accept_model_with_separating_spaces(self):
        result = analyze({"properties": {"ro.product.model": "realme Pad RMP2103", "ro.product.device": "unknown"}})
        self.assertEqual(result["variant"], "Wi-Fi")
        self.assertTrue(result["boot_research_possible"])

    def test_reject_conflicting_model_and_device_variant(self):
        report = {"properties": {"ro.product.model": "RMP2102", "ro.product.device": "RMP2103"}}
        result = analyze(report)
        self.assertEqual(result["variant"], "unconfirmed")
        self.assertFalse(result["boot_research_possible"])
        self.assertTrue(any("Conflicting" in warning for warning in result["warnings"]))

    def test_reject_both_variants_in_model(self):
        report = {"properties": {"ro.product.model": "RMP2102 RMP2103", "ro.product.device": "RMP6768"}}
        result = analyze(report)
        self.assertEqual(result["variant"], "unconfirmed")
        self.assertFalse(result["boot_research_possible"])

    def test_reject_both_variants_in_device(self):
        report = {"properties": {"ro.product.model": "RMP2102", "ro.product.device": "RMP2102 RMP2103"}}
        result = analyze(report)
        self.assertFalse(result["boot_research_possible"])

    def test_missing_properties_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing Android properties"):
            analyze({})


if __name__ == "__main__":
    unittest.main()
