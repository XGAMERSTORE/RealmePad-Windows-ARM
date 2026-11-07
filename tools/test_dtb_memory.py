"""Offline DTB regression tests; no tablet, flash tools, or dtc required."""
import struct
import unittest

from dtb_memory import inspect


def fixture(reg):
    be = lambda n: struct.pack(">I", n)
    node = lambda name: be(1) + (name.encode() + b"\0").ljust((len(name) + 4) & ~3, b"\0")
    prop = lambda value: be(3) + be(len(value)) + be(0) + value.ljust((len(value) + 3) & ~3, b"\0")
    structure = node("") + node("memory@40000000") + prop(reg) + be(2) + be(2) + be(9)
    strings = b"reg\0"
    # Standard FDT header; empty memreserve table terminator precedes structure.
    offset_struct = 40 + 16
    offset_strings = offset_struct + len(structure)
    total = offset_strings + len(strings)
    header = struct.pack(">10I", 0xd00dfeed, total, offset_struct, offset_strings,
                         40, 17, 16, 0, len(strings), len(structure))
    return header + b"\0" * 16 + structure + strings


class DtbMemoryTests(unittest.TestCase):
    def test_reject_empty_ram_reg(self):
        with self.assertRaisesRegex(ValueError, "empty RAM reg"):
            inspect(fixture(b""))

    def test_valid_ram_range_is_only_reported(self):
        # Two address cells + one size cell.
        reg = struct.pack(">3I", 0, 0x40000000, 0x10000000)
        rows = inspect(fixture(reg))
        self.assertIn(("RAM", "base=0x40000000 size=0x10000000"), rows)

    def test_reject_zero_sized_ram(self):
        reg = struct.pack(">3I", 0, 0x40000000, 0)
        with self.assertRaisesRegex(ValueError, "invalid RAM range"):
            inspect(fixture(reg))


if __name__ == "__main__":
    unittest.main()
