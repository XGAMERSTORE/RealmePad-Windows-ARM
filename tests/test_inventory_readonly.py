"""Offline contract checks for the read-only Linux ADB inventory script."""
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"
PROPERTIES = (
    "ro.product.model", "ro.product.device", "ro.product.board",
    "ro.hardware", "ro.board.platform", "ro.build.version.release",
    "ro.build.version.sdk", "ro.boot.slot_suffix", "ro.boot.verifiedbootstate",
)


class InventoryTests(unittest.TestCase):
    def test_read_only_commands_and_no_identifiers(self):
        with tempfile.TemporaryDirectory() as directory:
            mock = pathlib.Path(directory) / "adb"
            log = pathlib.Path(directory) / "commands.txt"
            mock.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'case "$*" in\n'
                '  "get-state") echo device ;;\n'
                '  "shell getprop "*) echo test-value ;;\n'
                '  "shell uname -a") echo test-kernel ;;\n'
                '  "shell ls /dev/block/by-name 2>/dev/null || true") echo boot ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            commands = log.read_text().splitlines()
            expected = ["get-state"] + ["shell getprop " + p for p in PROPERTIES] + [
                "shell uname -a", "shell ls /dev/block/by-name 2>/dev/null || true"
            ]
            self.assertEqual(commands, expected)
            self.assertIn("ro.product.model: test-value", result.stdout)
            self.assertIn("partition names (metadata only):", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
