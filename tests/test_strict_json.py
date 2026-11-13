"""Reject Python's nonstandard JSON number constants in offline evidence."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class StrictEvidenceJsonTests(unittest.TestCase):
    def test_nonfinite_constants_rejected_for_both_models(self):
        for model in ("RMP2102", "RMP2103"):
            for constant in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(model=model, constant=constant), tempfile.TemporaryDirectory() as folder:
                    path = Path(folder) / "evidence.json"
                    path.write_text('{"metadata": ' + constant + "}", encoding="utf-8")
                    run = subprocess.run(
                        [sys.executable, "-m", "tools.boot_readiness", model, "--evidence-file", str(path)],
                        capture_output=True, text=True,
                    )
                    self.assertEqual(run.returncode, 2)
                    self.assertIn("Non-standard JSON constant:", run.stderr)
                    self.assertEqual(run.stdout, "")


if __name__ == "__main__":
    unittest.main()
