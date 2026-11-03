import json
import struct
import unittest
from pathlib import Path
from tools.compare_boot_layout import compare

BOARD = json.loads((Path(__file__).resolve().parents[1] / "research/upstream-boardconfig.json").read_text())

class BootLayoutTests(unittest.TestCase):
    def header(self, offset=0):
        data = bytearray(1660)
        data[:8] = b"ANDROID!"
        boot = BOARD["android_boot"]
        base = int(boot["kernel_base"], 16)
        for position, key in ((12, "kernel_offset"), (20, "ramdisk_offset"), (32, "tags_offset")):
            struct.pack_into("<I", data, position, base + int(boot[key], 16) + offset)
        struct.pack_into("<I", data, 36, boot["page_size"])
        struct.pack_into("<I", data, 40, boot["header_version"])
        return data

    def test_expected_layout(self):
        result = compare(self.header(), BOARD)
        self.assertTrue(result["matches_upstream_config"])
        self.assertFalse(result["windows_boot_ready"])
        self.assertFalse(result["safe_to_flash"])

    def test_mismatched_layout(self):
        self.assertFalse(compare(self.header(4096), BOARD)["matches_upstream_config"])

    def test_rejects_modern_header_versions(self):
        for version in (3, 4, 0xffffffff):
            with self.subTest(version=version):
                data = self.header()
                struct.pack_into("<I", data, 40, version)
                with self.assertRaisesRegex(ValueError, "Unsupported Android boot header"):
                    compare(data, BOARD)

    def test_rejects_truncated_v2(self):
        with self.assertRaises(ValueError):
            compare(self.header()[:1659], BOARD)

    def test_rejects_unsupported_version(self):
        header = self.header()
        struct.pack_into("<I", header, 40, 0xffffffff)
        with self.assertRaises(ValueError):
            compare(header, BOARD)

    def test_rejects_truncated_v0(self):
        header = self.header()
        struct.pack_into("<I", header, 40, 0)
        with self.assertRaisesRegex(ValueError, "Truncated v0"):
            compare(header[:1631], BOARD)

    def test_rejects_truncated_v1(self):
        header = self.header()
        struct.pack_into("<I", header, 40, 1)
        with self.assertRaises(ValueError):
            compare(header[:1647], BOARD)

    def test_truncated(self):
        with self.assertRaises(ValueError):
            compare(b"ANDROID!", BOARD)

if __name__ == "__main__":
    unittest.main()
