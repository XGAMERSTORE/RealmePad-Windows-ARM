import struct
import unittest
from tools.inspect_boot_image import inspect

class BootHeaderTests(unittest.TestCase):
    def test_v3(self):
        data = bytearray(1580)
        data[:8] = b"ANDROID!"
        struct.pack_into("<4I", data, 8, 12345, 678, 0, 1580)
        struct.pack_into("<I", data, 40, 3)
        self.assertEqual(inspect(data)["header_version"], 3)

    def test_v4(self):
        data = bytearray(1584)
        data[:8] = b"ANDROID!"
        struct.pack_into("<4I", data, 8, 12345, 678, 0, 1584)
        struct.pack_into("<I", data, 40, 4)
        self.assertEqual(inspect(data)["header_version"], 4)

    def test_legacy(self):
        data = bytearray(64)
        data[:8] = b"ANDROID!"
        struct.pack_into("<I", data, 36, 4096)
        self.assertEqual(inspect(data)["page_size"], 4096)

    def test_bad_magic(self):
        with self.assertRaises(ValueError):
            inspect(bytes(100))

    def test_bad_version(self):
        data = bytearray(64)
        data[:8] = b"ANDROID!"
        struct.pack_into("<I", data, 40, 99)
        with self.assertRaises(ValueError):
            inspect(data)

if __name__ == "__main__":
    unittest.main()
