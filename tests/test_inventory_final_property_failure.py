"""Regression: a failure on the final property must prevent kernel/partition reads."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"

class InventoryFinalPropertyFailure(unittest.TestCase):
    def test_final_property_failure_aborts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mock = root / "adb"
            log = root / "commands.txt"
            mock.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'case "$*" in\n'
                '  "get-state") echo device ;;\n'
                '  "shell getprop ro.boot.verifiedbootstate") exit 29 ;;\n'
                '  "shell getprop "*) echo mock-value ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ.get("PATH", ""),
                       ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            commands = log.read_text().splitlines()
            self.assertEqual(commands[-1], "shell getprop ro.boot.verifiedbootstate")
            self.assertEqual(len(commands), 10)
            self.assertNotIn("shell uname -a", commands)
            self.assertNotIn("Partition names", result.stdout)

if __name__ == "__main__":
    unittest.main()
