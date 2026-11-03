import struct
import unittest
from tools.verify_efi import inspect

def fixture(machine=0xaa64, subsystem=10, magic=0x20b):
    data = bytearray(256)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3c, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<H", data, 0x84, machine)
    struct.pack_into("<H", data, 0x98, magic)
    struct.pack_into("<H", data, 0x98 + 68, subsystem)
    return bytes(data)

class VerifyEfiTests(unittest.TestCase):
    def test_arm64_efi(self):
        self.assertEqual(inspect(fixture())["machine"], "ARM64")
    def test_wrong_machine(self):
        with self.assertRaises(ValueError):
            inspect(fixture(machine=0x8664))
    def test_wrong_subsystem(self):
        with self.assertRaises(ValueError):
            inspect(fixture(subsystem=3))
    def test_invalid_header(self):
        with self.assertRaises(ValueError):
            inspect(b"not an executable")

if __name__ == "__main__":
    unittest.main()
