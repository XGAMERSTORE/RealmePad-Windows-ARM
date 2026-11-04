import gzip
import unittest
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


if __name__ == '__main__':
    unittest.main()
