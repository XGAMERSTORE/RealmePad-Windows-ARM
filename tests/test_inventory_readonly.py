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
                '  "shell ls /dev/block/by-name") echo boot ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            commands = log.read_text().splitlines()
            expected = ["get-state"] + ["shell getprop " + p for p in PROPERTIES] + [
                "shell uname -a", "shell ls /dev/block/by-name"
            ]
            self.assertEqual(commands, expected)
            self.assertIn("ro.product.model: test-value", result.stdout)
            self.assertIn("partition names (metadata only):", result.stdout.lower())


    def test_adb_disconnected_fails_before_property_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            mock = pathlib.Path(directory) / "adb"
            log = pathlib.Path(directory) / "commands.txt"
            mock.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'if [ "$*" = "get-state" ]; then echo offline >&2; exit 1; fi\n'
                'exit 42\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(log.read_text().splitlines(), ["get-state"])
            self.assertNotIn("Read-only system properties", result.stdout)

    def test_failed_property_read_stops_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            mock = pathlib.Path(directory) / "adb"
            log = pathlib.Path(directory) / "commands.txt"
            mock.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'case "$*" in\n'
                '  "get-state") echo device ;;\n'
                '  "shell getprop ro.product.model") exit 23 ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(log.read_text().splitlines(), ["get-state", "shell getprop ro.product.model"])
            self.assertNotIn("Kernel:", result.stdout)

if __name__ == "__main__":
    unittest.main()
