import unittest
from tools.dtb_inventory import parse

class TestDtbInventory(unittest.TestCase):
    def test_extract_and_deduplicate(self):
        sample = 'FILES="arch/arm64/boot/dts/mediatek/mt6768.dtb arch/arm64/boot/dts/mediatek/oppo8786_wlan.dtb arch/arm64/boot/dts/mediatek/mt6768.dtb"'
        self.assertEqual(parse(sample), ["mt6768.dtb", "oppo8786_wlan.dtb"])

    def test_empty(self):
        self.assertEqual(parse("ARCH=arm64"), [])

if __name__ == "__main__":
    unittest.main()
