"""Offline regression: kernel metadata failure must stop before partition listing."""
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "inventory.sh"


class KernelFailureTests(unittest.TestCase):
    def test_failed_uname_does_not_list_partitions(self):
        with tempfile.TemporaryDirectory() as directory:
            mock = pathlib.Path(directory) / "adb"
            log = pathlib.Path(directory) / "commands.txt"
            mock.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$ADB_TEST_LOG"\n'
                'case "$*" in\n'
                '  "get-state") echo device ;;\n'
                '  "shell getprop "*) echo test-value ;;\n'
                '  "shell uname -r") exit 23 ;;\n'
                '  *) exit 42 ;;\n'
                'esac\n'
            )
            mock.chmod(0o755)
            env = dict(os.environ, PATH=directory + os.pathsep + os.environ["PATH"], ADB_TEST_LOG=str(log))
            result = subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            commands = log.read_text().splitlines()
            self.assertEqual(commands[-1], "shell uname -r")
            self.assertNotIn("shell uname -m", commands)
            self.assertFalse(any("/dev/block" in command for command in commands))
            self.assertIn("ADB kernel metadata read failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
