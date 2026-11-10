"""No-hardware tests for candidate LK load-range analysis."""
import unittest
from unittest.mock import patch

from check_lk_load_range import assess


class CandidateRangeTests(unittest.TestCase):
    def check(self, rows, address, size):
        with patch("check_lk_load_range.inspect", return_value=[("compatible", "realme,rmp6768, mediatek,mt6768")] + rows):
            return assess(b"offline fixture", address, size)

    def test_unreserved_region_is_not_boot_authorized(self):
        report = self.check([("RAM", "base=0x40000000 size=0x100000")], 0x40010000, 0x1000)
        self.assertTrue(report["offline_layout_consistent"])
        self.assertFalse(report["safe_to_boot"])
        self.assertFalse(report["lk_handoff_verified"])

    def test_reject_unrelated_board_even_when_memory_fits(self):
        rows = [("compatible", "xiaomi,lancelot"),
                ("RAM", "base=0x40000000 size=0x100000")]
        with patch("check_lk_load_range.inspect", return_value=rows):
            report = assess(b"offline fixture", 0x40010000, 0x1000)
        self.assertFalse(report["realme_pad_compatible_found"])
        self.assertFalse(report["offline_layout_consistent"])

    def test_reject_outside_ram(self):
        report = self.check([("RAM", "base=0x40000000 size=0x100000")], 0x50000000, 0x1000)
        self.assertFalse(report["offline_layout_consistent"])

    def test_reject_memreserve_collision(self):
        report = self.check([("RAM", "base=0x40000000 size=0x100000"),
                             ("RESERVED", "base=0x40010000 size=0x1000")], 0x40010800, 0x1000)
        self.assertFalse(report["offline_layout_consistent"])
        self.assertEqual(report["reservation_collisions"][0]["type"], "RESERVED")

    def test_reject_reserved_memory_node_collision(self):
        report = self.check([("RAM", "base=0x40000000 size=0x100000"),
                             ("RESERVED_NODE", "base=0x40010000 size=0x1000")], 0x40010000, 0x100)
        self.assertFalse(report["offline_layout_consistent"])

    def test_reject_range_crossing_ram_boundary(self):
        report = self.check([("RAM", "base=0x40000000 size=0x1000")], 0x40000f00, 0x200)
        self.assertFalse(report["offline_layout_consistent"])

    def test_reject_overflow(self):
        with self.assertRaisesRegex(ValueError, "Invalid candidate"):
            self.check([], (1 << 64) - 8, 16)

    def test_reject_zero_size(self):
        with self.assertRaisesRegex(ValueError, "Invalid candidate"):
            self.check([], 0x40000000, 0)


if __name__ == "__main__":
    unittest.main()
