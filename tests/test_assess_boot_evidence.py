import unittest
from tools.assess_boot_evidence import analyze

class BootEvidenceTests(unittest.TestCase):
    def test_wifi_locked(self):
        report = {"properties": {"ro.product.model": "RMP2103",
            "ro.product.device": "RMP6768",
            "ro.boot.verifiedbootstate": "green",
            "ro.boot.vbmeta.device_state": "locked"}}
        result = analyze(report)
        self.assertEqual(result["variant"], "Wi-Fi")
        self.assertFalse(result["safe_to_flash"])
        self.assertFalse(result["windows_boot_ready"])

    def test_lte(self):
        result = analyze({"properties": {"ro.product.model": "RMP2102"}})
        self.assertEqual(result["variant"], "LTE")

    def test_unknown(self):
        result = analyze({"properties": {}})
        self.assertEqual(result["variant"], "unconfirmed")
        self.assertTrue(result["warnings"])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            analyze({"properties": None})

if __name__ == "__main__":
    unittest.main()
