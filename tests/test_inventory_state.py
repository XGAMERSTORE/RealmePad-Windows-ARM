"""Reject ADB states that exit successfully but are not authorized Android devices."""
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"

class StateTests(unittest.TestCase):
    def test_rejects_successful_but_non_device_state(self):
        for state in ("offline", "recovery", "unauthorized", ""):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as d:
                adb = pathlib.Path(d) / "adb"
                log = pathlib.Path(d) / "commands"
                adb.write_text(
                    '#!/bin/sh\n'
                    'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                    'if [ "$*" = get-state ]; then printf "%s\\n" "$ADB_TEST_STATE"; exit 0; fi\n'
                    'exit 42\n'
                )
                adb.chmod(0o755)
                env = dict(os.environ, PATH=d + os.pathsep + os.environ["PATH"],
                           ADB_TEST_LOG=str(log), ADB_TEST_STATE=state)
                result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(log.read_text().splitlines(), ["get-state"])
                self.assertNotIn("Read-only system properties", result.stdout)

if __name__ == "__main__":
    unittest.main()
