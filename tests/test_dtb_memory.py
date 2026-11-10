import struct
import unittest
from tools.dtb_memory import inspect

def dtb():
    u = lambda n: struct.pack(">I", n)
    pad = lambda b: b + b"\0"*((-len(b))%4)
    node = lambda s: u(1) + pad(s.encode()+b"\0")
    prop = lambda offset, data: u(3)+u(len(data))+u(offset)+pad(data)
    names = b"#address-cells\0#size-cells\0reg\0compatible\0"
    offsets = [names.index(s) for s in (b"#address-cells",b"#size-cells",b"reg",b"compatible")]
    body = node("")+prop(offsets[0],u(2))+prop(offsets[1],u(2))+prop(offsets[3],b"realme,rmp6768\0")+node("memory@40000000")+prop(offsets[2],u(0)+u(0x40000000)+u(0)+u(0x80000000))+u(2)+u(2)+u(9)
    total = 56+len(body)+len(names)
    return struct.pack(">10I",0xd00dfeed,total,56,56+len(body),40,17,16,0,len(names),len(body))+b"\0"*16+body+names

class DtbTests(unittest.TestCase):
    def test_ram(self):
        self.assertIn(("RAM","base=0x40000000 size=0x80000000"),inspect(dtb()))
    def test_model(self):
        self.assertIn(("compatible","realme,rmp6768"),inspect(dtb()))
    def test_truncated(self):
        with self.assertRaises(ValueError): inspect(dtb()[:-1])
    def test_header_overlapping_blocks(self):
        blob = bytearray(dtb())
        struct.pack_into(">I", blob, 8, 0)
        with self.assertRaises(ValueError): inspect(bytes(blob))

    def test_memory_controller_is_not_ram(self):
        blob = dtb()
        self.assertTrue(any(k == "RAM" for k, _ in inspect(blob)))
        # The parser must not infer RAM from memory-controller nodes.
        modified = blob.replace(b"memory@40000000", b"memory-ctrl0000")
        self.assertFalse(any(k == "RAM" for k, _ in inspect(modified)))

    def test_overlapping_fdt_blocks(self):
        blob = bytearray(dtb())
        # Place strings block inside the structure block.
        struct.pack_into(">I", blob, 12, 60)
        with self.assertRaisesRegex(ValueError, "overlap"):
            inspect(bytes(blob))


    def test_fdt_end_requires_closed_nodes(self):
        blob = bytearray(dtb())
        offset = struct.unpack_from(">I", blob, 8)[0]
        size = struct.unpack_from(">I", blob, 36)[0]
        # Replace the final FDT_END_NODE with FDT_END, leaving root open.
        struct.pack_into(">I", blob, offset + size - 8, 9)
        with self.assertRaisesRegex(ValueError, "closing all nodes"):
            inspect(bytes(blob))

    def test_properties_outside_nodes_rejected(self):
        blob = bytearray(dtb())
        offset = struct.unpack_from(">I", blob, 8)[0]
        # FDT_PROP token before the first FDT_BEGIN_NODE.
        struct.pack_into(">I", blob, offset, 3)
        with self.assertRaises(ValueError):
            inspect(bytes(blob))

    def test_invalid(self):
        with self.assertRaises(ValueError): inspect(b"invalid")

    def test_zero_length_ram_rejected(self):
        blob = bytearray(dtb())
        signature = struct.pack(">4I", 0, 0x40000000, 0, 0x80000000)
        index = blob.find(signature)
        self.assertGreaterEqual(index, 0)
        struct.pack_into(">I", blob, index + 12, 0)
        with self.assertRaisesRegex(ValueError, "invalid RAM range"):
            inspect(bytes(blob))

    def test_overflowing_ram_range_rejected(self):
        blob = bytearray(dtb())
        signature = struct.pack(">4I", 0, 0x40000000, 0, 0x80000000)
        index = blob.find(signature)
        self.assertGreaterEqual(index, 0)
        struct.pack_into(">4I", blob, index, 0xffffffff, 0xfffffff0, 0, 0x100)
        with self.assertRaisesRegex(ValueError, "invalid RAM range"):
            inspect(bytes(blob))


    def test_addressed_reserved_memory_is_not_lost(self):
        blob = bytearray(dtb())
        u = lambda n: struct.pack(">I", n)
        pad = lambda b: b + b"\0" * ((-len(b)) % 4)
        # /reserved-memory@0/region@41000000 with fixed reg and
        # inherited root 2-address/2-size cell encoding.
        new_node = (u(1) + pad(b"reserved-memory@0\0") +
                    u(1) + pad(b"region@41000000\0") +
                    u(3) + u(16) + u(27) +
                    u(0) + u(0x41000000) + u(0) + u(0x1000) +
                    u(2) + u(2))
        offset = struct.unpack_from(">I", blob, 8)[0]
        size = struct.unpack_from(">I", blob, 36)[0]
        blob[offset + size - 8:offset + size - 8] = new_node
        struct.pack_into(">I", blob, 4, len(blob))
        struct.pack_into(">I", blob, 12, struct.unpack_from(">I", blob, 12)[0] + len(new_node))
        struct.pack_into(">I", blob, 36, size + len(new_node))
        rows = inspect(bytes(blob))
        self.assertIn(("RESERVED_NODE", "base=0x41000000 size=0x1000"), rows)

    def test_overlapping_ram_banks_rejected(self):
        blob = bytearray(dtb())
        structure_offset = struct.unpack_from(">I", blob, 8)[0]
        structure_size = struct.unpack_from(">I", blob, 36)[0]
        # Insert a second memory node immediately before root's END_NODE.
        def u(n):
            return struct.pack(">I", n)
        def pad(data):
            return data + b"\0" * ((-len(data)) % 4)
        new_node = (u(1) + pad(b"memory@50000000\0") +
                    u(3) + u(16) + u(27) +
                    u(0) + u(0x50000000) + u(0) + u(0x10000000) +
                    u(2))
        insertion = structure_offset + structure_size - 8
        blob[insertion:insertion] = new_node
        struct.pack_into(">I", blob, 4, len(blob))
        struct.pack_into(">I", blob, 12, struct.unpack_from(">I", blob, 12)[0] + len(new_node))
        struct.pack_into(">I", blob, 36, structure_size + len(new_node))
        with self.assertRaisesRegex(ValueError, "overlapping RAM"):
            inspect(bytes(blob))

    def test_parent_cells_after_memory_node(self):
        blob = dtb()
        u = lambda n: struct.pack(">I", n)
        pad = lambda b: b + b"\0" * ((-len(b)) % 4)
        # Root defaults are 2 address cells and 1 size cell, but the
        # actual root properties (2/2) occur after the memory node.
        root = u(1) + pad(b"\0")
        address = u(3) + u(4) + u(0) + u(2)
        size = u(3) + u(4) + u(15) + u(2)
        memory = (u(1) + pad(b"memory@40000000\0") +
                  u(3) + u(16) + u(27) +
                  u(0) + u(0x40000000) + u(0) + u(0x80000000) + u(2))
        body = root + memory + address + size + u(2) + u(9)
        names = b"#address-cells\0#size-cells\0reg\0compatible\0"
        header = struct.pack(">10I", 0xd00dfeed, 56 + len(body) + len(names),
                             56, 56 + len(body), 40, 17, 16, 0,
                             len(names), len(body))
        rows = inspect(header + b"\0" * 16 + body + names)
        self.assertIn(("RAM", "base=0x40000000 size=0x80000000"), rows)
