"""Offline host-only regression tests for the MT6768 source prerequisite gate."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_mt6768_uboot_source.py'
spec = importlib.util.spec_from_file_location('mt6768_gate', SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class SourceGateTests(unittest.TestCase):
    def run_gate(self, root):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = gate.check(root)
        return status, output.getvalue()

    def test_non_source_tree_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            status, output = self.run_gate(Path(tmp))
            self.assertEqual(status, 2)
            self.assertIn('not a recognizable U-Boot source tree', output)

    def test_missing_prerequisites_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'Makefile').touch()
            (root / 'configs').mkdir()
            status, output = self.run_gate(root)
            self.assertEqual(status, 1)
            self.assertIn('MISSING: configs/mt6768_defconfig', output)
            self.assertIn('MISSING: board/mediatek/mt6768', output)
            self.assertIn('NOT verified', output)

    def test_present_prerequisites_are_not_boot_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'Makefile').touch()
            (root / 'configs').mkdir()
            (root / 'configs' / 'mt6768_defconfig').touch()
            (root / 'board' / 'mediatek' / 'mt6768').mkdir(parents=True)
            status, output = self.run_gate(root)
            self.assertEqual(status, 0)
            self.assertIn('SOURCE GATE ONLY', output)
            self.assertIn('build and tablet boot NOT verified', output)

    def test_partial_prerequisites_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'Makefile').touch()
            (root / 'configs').mkdir()
            (root / 'configs' / 'mt6768_defconfig').touch()
            status, output = self.run_gate(root)
            self.assertEqual(status, 1)
            self.assertIn('PRESENT: configs/mt6768_defconfig', output)
            self.assertIn('MISSING: board/mediatek/mt6768', output)


if __name__ == '__main__':
    unittest.main()
