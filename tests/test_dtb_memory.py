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

    def test_invalid(self):
        with self.assertRaises(ValueError): inspect(b"invalid")
