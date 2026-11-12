import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
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
    def test_software_claims_cannot_replace_hardware_proof(self):
        evidence = {name: True for name in REQUIRED}
        evidence["windows_wifi_driver"] = True
        evidence["stock_restore_verified_on_device"] = False
        evidence["non_destructive_uefi_entry_verified_on_device"] = False
        report = evaluate("RMP2103", evidence)
        self.assertFalse(report["boot_ready"])
        self.assertIn("stock_restore_verified_on_device", report["missing"])
        self.assertIn("non_destructive_uefi_entry_verified_on_device", report["missing"])
        self.assertFalse(report["flash_authorized"])

    def test_cli_evidence_file_is_read_and_never_authorizes_flash(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "evidence.json"
            path.write_text(json.dumps({"board_uefi": True}), encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "tools.boot_readiness", "RMP2103",
                                  "--evidence-file", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            report = json.loads(run.stdout)
            self.assertNotIn("board_uefi", report["missing"])
            self.assertFalse(report["flash_authorized"])

    def test_cli_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text("{bad", encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "tools.boot_readiness", "RMP2102",
                                  "--evidence-file", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("Evidence error:", run.stderr)
            self.assertFalse(run.stdout.strip())

    def test_cli_rejects_duplicate_top_level_evidence_keys(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.json"
            path.write_text('{"board_uefi": true, "board_uefi": false}', encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "tools.boot_readiness", "RMP2103",
                                  "--evidence-file", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("Duplicate evidence key: board_uefi", run.stderr)
            self.assertFalse(run.stdout.strip())

    def test_cli_rejects_nested_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "nested.json"
            path.write_text('{"nested": {"x": 1, "x": 2}}', encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "tools.boot_readiness", "RMP2102",
                                  "--evidence-file", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("Duplicate evidence key: x", run.stderr)
            self.assertFalse(run.stdout.strip())

    def test_unknown_model_rejected(self):
        with self.assertRaises(ValueError):
            evaluate("RMP9999", {})
    def test_no_flash_authorization_even_when_ready(self):
        evidence = {name: True for name in REQUIRED}
        evidence["windows_wifi_driver"] = True
        self.assertFalse(evaluate("RMP2103", evidence)["flash_authorized"])

if __name__ == "__main__":
    unittest.main()
