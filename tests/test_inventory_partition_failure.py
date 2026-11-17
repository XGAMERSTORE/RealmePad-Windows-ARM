"""Offline regression: missing partition-name metadata is nonfatal and read-only."""
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"


class PartitionFailureTests(unittest.TestCase):
    def test_partition_listing_failure_warns_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            mock = pathlib.Path(directory) / "adb"
            log = pathlib.Path(directory) / "commands.txt"
            mock.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'case "$*" in\n'
                '  "get-state") echo device ;;\n'
                '  "shell getprop "*) echo test-value ;;\n'
                '  "shell uname -r") echo test-kernel ;;\n'
                '  "shell uname -m") echo aarch64 ;;\n'
                '  "shell ls /dev/block/by-name") exit 13 ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            commands = log.read_text().splitlines()
            self.assertEqual(commands[-3:], ["shell uname -r", "shell uname -m", "shell ls /dev/block/by-name"])
            self.assertEqual(len(commands), 13)
            self.assertIn("Partition-name metadata unavailable", result.stderr)
            self.assertIn("Do NOT publish serial numbers", result.stdout)


if __name__ == "__main__":
    unittest.main()
