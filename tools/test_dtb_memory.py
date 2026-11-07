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

    def test_report_firmware_reservation(self):
        reg = struct.pack(">3I", 0, 0x40000000, 0x10000000)
        blob = bytearray(fixture(reg))
        # Insert one reservation before the mandatory zero terminator.
        blob[40:40] = struct.pack(">QQ", 0x41000000, 0x1000)
        struct.pack_into(">I", blob, 4, len(blob))
        struct.pack_into(">I", blob, 8, 72)
        struct.pack_into(">I", blob, 12, struct.unpack_from(">I", blob, 12)[0] + 16)
        rows = inspect(bytes(blob))
        self.assertIn(("RESERVED", "base=0x41000000 size=0x1000"), rows)

    def test_reject_overlapping_firmware_reservations(self):
        blob = bytearray(fixture(struct.pack(">3I", 0, 0x40000000, 0x10000000)))
        blob[40:40] = (struct.pack(">QQ", 0x41000000, 0x2000)
                       + struct.pack(">QQ", 0x41001000, 0x1000))
        struct.pack_into(">I", blob, 4, len(blob))
        struct.pack_into(">I", blob, 8, 88)
        struct.pack_into(">I", blob, 12, struct.unpack_from(">I", blob, 12)[0] + 32)
        with self.assertRaisesRegex(ValueError, "overlapping FDT memreserve"):
            inspect(bytes(blob))

    def test_reject_unterminated_reservation_table(self):
        blob = bytearray(fixture(struct.pack(">3I", 0, 0x40000000, 0x10000000)))
        blob[40:56] = struct.pack(">QQ", 0x41000000, 0x1000)
        with self.assertRaisesRegex(ValueError, "memreserve"):
            inspect(bytes(blob))

    def test_reject_terminator_overlapping_structure(self):
        blob = bytearray(fixture(struct.pack(">3I", 0, 0x40000000, 0x10000000)))
        # A zero-only memreserve table starts eight bytes before the structure.
        # The terminator must be included in the overlap check.
        struct.pack_into(">I", blob, 16, 48)
        blob[48:64] = b"\\0" * 16
        with self.assertRaisesRegex(ValueError, "memreserve overlaps"):
            inspect(bytes(blob))

    def test_reject_truncated_node_name_padding(self):
        blob = bytearray(fixture(struct.pack(">3I", 0, 0x40000000, 0x1000)))
        # Structure ends immediately after the node NUL, before required padding.
        structure = struct.pack(">I", 1) + b"a\\0"
        strings = b"reg\\0"
        struct_offset = 56
        strings_offset = struct_offset + len(structure)
        header = struct.pack(">10I", 0xd00dfeed, strings_offset + len(strings),
                             struct_offset, strings_offset, 40, 17, 16, 0,
                             len(strings), len(structure))
        malformed = header + b"\\0" * 16 + structure + strings
        with self.assertRaisesRegex(ValueError, "node name padding"):
            inspect(malformed)

    def test_reject_zero_sized_ram(self):
        reg = struct.pack(">3I", 0, 0x40000000, 0)
        with self.assertRaisesRegex(ValueError, "invalid RAM range"):
            inspect(fixture(reg))


if __name__ == "__main__":
    unittest.main()
