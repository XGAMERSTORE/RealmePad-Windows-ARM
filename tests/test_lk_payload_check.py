import gzip
import unittest
from unittest.mock import patch
from tools.lk_payload_check import inspect


class TestLkPayloadCheck(unittest.TestCase):
    def test_valid_gzip_arm64(self):
        image = bytearray(128)
        image[0x38:0x3c] = b'ARM\x64'
        ok, msg = inspect(gzip.compress(bytes(image)))
        self.assertTrue(ok, msg)

    def test_raw_arm64_rejected(self):
        image = bytearray(128)
        image[0x38:0x3c] = b'ARM\x64'
        self.assertFalse(inspect(bytes(image))[0])

    def test_bad_gzip_rejected(self):
        self.assertFalse(inspect(b'\x1f\x8bgarbage')[0])

    def test_gzip_non_arm64_rejected(self):
        self.assertFalse(inspect(gzip.compress(b'not an image'))[0])

    def test_oversized_gzip_rejected_without_unbounded_decompression(self):
        image = bytearray(4096)
        image[0x38:0x3c] = b'ARM\x64'
        with patch('tools.lk_payload_check.MAX_DECOMPRESSED_BYTES', 1024):
            ok, message = inspect(gzip.compress(bytes(image)))
        self.assertFalse(ok)
        self.assertIn('inspection limit', message)

    def test_payload_exactly_at_limit_accepted(self):
        image = bytearray(128)
        image[0x38:0x3c] = b'ARM\x64'
        with patch('tools.lk_payload_check.MAX_DECOMPRESSED_BYTES', 128):
            self.assertTrue(inspect(gzip.compress(bytes(image)))[0])


if __name__ == '__main__':
    unittest.main()
