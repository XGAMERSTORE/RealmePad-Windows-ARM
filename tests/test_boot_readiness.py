import unittest
from tools.boot_readiness import evaluate, REQUIRED

class BootReadinessTests(unittest.TestCase):
    def test_wifi_blocked_without_drivers(self):
        report = evaluate("RMP2103", {})
        self.assertFalse(report["boot_ready"])
        self.assertIn("board_uefi", report["missing"])
    def test_lte_requires_modem(self):
        evidence = {name: True for name in REQUIRED}
        evidence["windows_wifi_driver"] = True
        report = evaluate("RMP2102", evidence)
        self.assertEqual(report["missing"], ["windows_lte_driver"])
    def test_unknown_model_rejected(self):
        with self.assertRaises(ValueError):
            evaluate("RMP9999", {})
    def test_no_flash_authorization_even_when_ready(self):
        evidence = {name: True for name in REQUIRED}
        evidence["windows_wifi_driver"] = True
        self.assertFalse(evaluate("RMP2103", evidence)["flash_authorized"])

if __name__ == "__main__":
    unittest.main()
