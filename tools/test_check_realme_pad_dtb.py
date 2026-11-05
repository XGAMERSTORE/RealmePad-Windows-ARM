"""Isolated regression tests: no board access or DT compiler required."""
import pathlib
import subprocess
import unittest
from unittest.mock import patch

import check_realme_pad_dtb as checker


class RealmePadDtbTests(unittest.TestCase):
    def setUp(self):
        self.props = {
            ("/", "model"): checker.EXPECTED_MODEL,
            ("/", "compatible"): "realme,rmp6768 mediatek,mt6768",
        }
        self.memory = "0 0 0 0\n"
        self.root_nodes = "chosen memory soc\n"
        self.dump = '/ { model = "realme Pad"; };'

    def run_fake(self, args, **kwargs):
        if args[0] == "fdtget":
            if args[1] == "-l":
                return subprocess.CompletedProcess(args, 0, self.root_nodes, "")
            if args[2] == "x":
                return subprocess.CompletedProcess(args, 0, self.memory, "")
            value = self.props.get((args[4], args[5]))
            return subprocess.CompletedProcess(args, 0 if value is not None else 1,
                                               value or "", "")
        if args[0] == "dtc":
            return subprocess.CompletedProcess(args, 0, self.dump, "")
        raise AssertionError(f"Unexpected subprocess: {args}")

    def check(self):
        with patch.object(checker.subprocess, "run", side_effect=self.run_fake):
            checker.validate(pathlib.Path("fixture.dtb"))

    def test_valid_skeleton(self):
        self.check()

    def test_reject_wrong_model(self):
        self.props[("/", "model")] = "Xiaomi Redmi 9"
        with self.assertRaisesRegex(ValueError, "Not the experimental"):
            self.check()

    def test_reject_xiaomi_compatible(self):
        self.props[("/", "compatible")] += " xiaomi,lancelot"
        with self.assertRaisesRegex(ValueError, "Xiaomi"):
            self.check()

    def test_reject_missing_realme_compatible(self):
        self.props[("/", "compatible")] = "mediatek,mt6768"
        with self.assertRaisesRegex(ValueError, "compatible missing"):
            self.check()

    def test_reject_hardcoded_dram(self):
        self.memory = "0 40000000 0 80000000"
        with self.assertRaisesRegex(ValueError, "memory placeholder"):
            self.check()

    def test_reject_separate_memory_bank(self):
        self.root_nodes += "memory@40000000\n"
        with self.assertRaisesRegex(ValueError, "Unverified memory@ bank"):
            self.check()

    def test_reject_reserved_memory_node(self):
        self.root_nodes += "reserved-memory\\n"
        with self.assertRaisesRegex(ValueError, "reserved-memory layout"):
            self.check()

    def test_reject_memreserve_header(self):
        self.dump = "/memreserve/ 0x40000000 0x100000;\\n/ { }; "
        with self.assertRaisesRegex(ValueError, "memreserve entry"):
            self.check()

    def test_reject_bootargs(self):
        self.props[("/chosen", "bootargs")] = "console=ttyS0"
        with self.assertRaisesRegex(ValueError, "boot arguments"):
            self.check()

    def test_reject_inherited_framebuffer(self):
        self.dump = 'compatible = "simple-framebuffer";'
        with self.assertRaisesRegex(ValueError, "simple-framebuffer"):
            self.check()

    def test_reject_xiaomi_framebuffer_address(self):
        self.dump = 'reg = <0x7d9b0000>;'
        with self.assertRaisesRegex(ValueError, "Xiaomi reference"):
            self.check()


if __name__ == "__main__":
    unittest.main()
