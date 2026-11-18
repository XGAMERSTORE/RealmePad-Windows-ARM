"""Offline regression tests for the host-only U-Boot defconfig probe."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'probe_mt6768_defconfig.py'
spec = importlib.util.spec_from_file_location('probe_mt6768_defconfig', SCRIPT)
probe_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe_module)


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'uboot'
        self.root.mkdir()
        self.out = Path(self.tmp.name) / 'report'

    def valid_tree(self):
        (self.root / 'Makefile').write_text('all:\n\t@true\n')
        (self.root / 'configs').mkdir()
        (self.root / 'configs' / 'mt6768_defconfig').write_text('CONFIG_ARM=y\n')

    def test_rejects_non_uboot_tree_without_running_commands(self):
        with patch.object(probe_module.subprocess, 'run') as run:
            self.assertEqual(probe_module.probe(self.root, self.out), 2)
            run.assert_not_called()
        self.assertFalse(self.out.exists())

    def test_missing_defconfig_is_reported_without_make(self):
        self.valid_tree()
        (self.root / 'configs' / 'mt6768_defconfig').unlink()
        with patch.object(probe_module.subprocess, 'run',
                          return_value=subprocess.CompletedProcess([], 0, 'sha')) as run:
            self.assertEqual(probe_module.probe(self.root, self.out), 1)
        report = json.loads((self.out / 'mt6768_defconfig_probe.json').read_text())
        self.assertIn('missing or empty', report['make_dry_run']['error'])
        self.assertIsNone(report['make_dry_run']['command'])
        self.assertEqual(run.call_count, 1)

    def test_empty_defconfig_is_reported_without_make(self):
        self.valid_tree()
        (self.root / 'configs' / 'mt6768_defconfig').write_text('  ')
        with patch.object(probe_module.subprocess, 'run',
                          return_value=subprocess.CompletedProcess([], 0, 'sha')) as run:
            self.assertEqual(probe_module.probe(self.root, self.out), 1)
        self.assertEqual(run.call_count, 1)

    def test_failed_defconfig_is_reported_not_hidden(self):
        self.valid_tree()
        results = [subprocess.CompletedProcess([], 0, 'deadbeef\n'),
                   subprocess.CompletedProcess([], 2, 'No rule to make target mt6768_defconfig')]
        with patch.object(probe_module.subprocess, 'run', side_effect=results) as run:
            self.assertEqual(probe_module.probe(self.root, self.out), 1)
        report = json.loads((self.out / 'mt6768_defconfig_probe.json').read_text())
        self.assertEqual(report['make_dry_run']['exit_code'], 2)
        self.assertIn('No rule', report['make_dry_run']['output'])
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[1].args[0][0:2], ['make', '-n'])

    def test_success_is_only_dry_run_not_boot(self):
        self.valid_tree()
        with patch.object(probe_module.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'ok')):
            self.assertEqual(probe_module.probe(self.root, self.out), 0)
        report = json.loads((self.out / 'mt6768_defconfig_probe.json').read_text())
        self.assertIn('NOT a build or boot test', report['kind'])

    def test_timeout_is_recorded_as_failure(self):
        self.valid_tree()
        with patch.object(probe_module.subprocess, 'run', side_effect=[
            subprocess.CompletedProcess([], 0, 'sha'),
            subprocess.TimeoutExpired(['make'], 1)]):
            self.assertEqual(probe_module.probe(self.root, self.out), 1)
        report = json.loads((self.out / 'mt6768_defconfig_probe.json').read_text())
        self.assertIsNone(report['make_dry_run']['exit_code'])
        self.assertIn('error', report['make_dry_run'])


if __name__ == '__main__':
    unittest.main()
