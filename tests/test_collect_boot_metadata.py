import unittest
from unittest.mock import patch
from tools.collect_boot_metadata import collect

class BootMetadataTests(unittest.TestCase):
    @patch("tools.collect_boot_metadata.adb")
    def test_detects_wifi_variant(self, mock_adb):
        values = {"ro.product.model": "RMP2103", "ro.product.device": "RMP6768"}
        mock_adb.side_effect = lambda serial, *args: values.get(args[-1], "")
        report = collect()
        self.assertEqual(report["model_family_hint"], "RMP6768")
        self.assertTrue(report["no_flash_operations"])
        self.assertEqual(mock_adb.call_count, len(report["properties"]))
        for call in mock_adb.call_args_list:
            self.assertEqual(call.args[1], "shell")
            self.assertEqual(call.args[2], "getprop")

    @patch("tools.collect_boot_metadata.adb")
    def test_unknown_model_not_trusted(self, mock_adb):
        mock_adb.return_value = "unknown"
        self.assertEqual(collect()["model_family_hint"], "unverified")

if __name__ == "__main__":
    unittest.main()
