#!/usr/bin/env python3
"""Offline unit tests for ARM64 Image validation; no device or flash access."""
import pathlib
import struct
import tempfile
import unittest

from check_arm64_image import inspect_image, MAGIC


class ImageHeaderTests(unittest.TestCase):
    def make_image(self, *, magic=MAGIC, image_size=128, reserved=0, length=128):
        data = bytearray(length)
        if length >= 64:
            struct.pack_into("<QQQ", data, 8, 0x80000, image_size, 0)
            struct.pack_into("<II", data, 56, magic, reserved)
        return bytes(data)

    def check(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "u-boot.bin"
            path.write_bytes(data)
            return inspect_image(path)

    def test_valid_header(self):
        result = self.check(self.make_image())
        self.assertEqual(result["image_size"], 128)
        self.assertEqual(result["text_offset"], 0x80000)
        self.assertEqual(len(result["sha256"]), 64)

    def test_short_file_rejected(self):
        with self.assertRaisesRegex(ValueError, "shorter"):
            self.check(b"short")

    def test_wrong_magic_rejected(self):
        with self.assertRaisesRegex(ValueError, "magic"):
            self.check(self.make_image(magic=0))

    def test_reserved_word_rejected(self):
        with self.assertRaisesRegex(ValueError, "reserved"):
            self.check(self.make_image(reserved=1))

    def test_declared_size_overrun_rejected(self):
        with self.assertRaisesRegex(ValueError, "exceeds"):
            self.check(self.make_image(image_size=4096))


if __name__ == "__main__":
    unittest.main()
