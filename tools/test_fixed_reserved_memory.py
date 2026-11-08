"""Verify fixed reserved-memory nodes are surfaced, not mistaken for free RAM."""
import struct
import unittest
from dtb_memory import inspect


def dtb_with_reserved_node(overlap=False):
    be = lambda x: struct.pack(">I", x)
    def node(name):
        raw = name.encode() + b"\0"
        return be(1) + raw + b"\0" * ((-len(raw)) % 4)
    def prop(value):
        return be(3) + be(len(value)) + be(0) + value + b"\0" * ((-len(value)) % 4)
    region = struct.pack(">3I", 0, 0x70000000, 0x100000)
    second = (node("other@70080000") + prop(struct.pack(">3I", 0, 0x70080000, 0x100000)) + be(2)) if overlap else b""
    structure = (node("") + node("reserved-memory") + node("firmware@70000000")
                 + prop(region) + be(2) + second + be(2) + be(2) + be(9))
    strings = b"reg\0"
    offset = 56
    header = struct.pack(">10I", 0xd00dfeed, offset + len(structure) + len(strings),
                         offset, offset + len(structure), 40, 17, 16, 0,
                         len(strings), len(structure))
    return header + b"\0" * 16 + structure + strings


class FixedReservationTests(unittest.TestCase):
    def test_reports_fixed_reservation(self):
        rows = inspect(dtb_with_reserved_node())
        self.assertIn(("RESERVED_NODE", "base=0x70000000 size=0x100000"), rows)
        self.assertFalse(any(key == "RAM" for key, _ in rows))

    def test_rejects_overlapping_fixed_reservations(self):
        with self.assertRaisesRegex(ValueError, "overlapping fixed reserved-memory"):
            inspect(dtb_with_reserved_node(overlap=True))


if __name__ == "__main__":
    unittest.main()
