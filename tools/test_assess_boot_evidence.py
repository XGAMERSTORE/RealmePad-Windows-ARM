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

    def test_exact_variant_allows_research_only(self):
        result = analyze({"properties": {"ro.product.model": "RMP2102", "ro.product.device": "RMP6768"}})
        self.assertTrue(result["boot_research_possible"])
        self.assertEqual(result["variant"], "LTE")
        self.assertFalse(result["windows_boot_ready"])

    def test_missing_properties_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing Android properties"):
            analyze({})


if __name__ == "__main__":
    unittest.main()
