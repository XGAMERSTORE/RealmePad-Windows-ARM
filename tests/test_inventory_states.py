"""Reject non-authorized ADB states before issuing any shell commands."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"


class InventoryStateTests(unittest.TestCase):
    def test_non_device_states_never_read_properties(self):
        for state in ("offline", "recovery", "unauthorized", "sideload", "bootloader", ""):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as directory:
                mock = Path(directory) / "adb"
                log = Path(directory) / "commands.txt"
                mock.write_text(
                    '#!/bin/sh\n'
                    'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                    'if [ "$*" = "get-state" ]; then printf "%s\\n" "$ADB_TEST_STATE"; exit 0; fi\n'
                    'exit 42\n'
                )
                mock.chmod(0o755)
                env = dict(os.environ, PATH=directory + os.pathsep + os.environ.get("PATH", ""),
                           ADB_TEST_LOG=str(log), ADB_TEST_STATE=state)
                result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertEqual(log.read_text().splitlines(), ["get-state"])
                self.assertNotIn("Read-only system properties", result.stdout)


if __name__ == "__main__":
    unittest.main()
