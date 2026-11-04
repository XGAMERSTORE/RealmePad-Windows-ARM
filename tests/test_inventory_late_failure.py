"""Ensure ADB inventory stops after late-stage command failures (mocked ADB only)."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"
PROPS = (
    "ro.product.model", "ro.product.device", "ro.product.board",
    "ro.hardware", "ro.board.platform", "ro.build.version.release",
    "ro.build.version.sdk", "ro.boot.slot_suffix", "ro.boot.verifiedbootstate",
)

class InventoryLateFailureTests(unittest.TestCase):
    def test_uname_failure_never_reads_partitions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mock = root / "adb"
            log = root / "commands.txt"
            mock.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'case "$*" in\n'
                '  "get-state") echo device ;;\n'
                '  "shell getprop "*) echo mock-value ;;\n'
                '  "shell uname -a") exit 27 ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ.get("PATH", ""),
                       ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(log.read_text().splitlines(),
                             ["get-state"] + ["shell getprop " + p for p in PROPS] + ["shell uname -a"])
            self.assertNotIn("Partition names", result.stdout)

if __name__ == "__main__":
    unittest.main()
