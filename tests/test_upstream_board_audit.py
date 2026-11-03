import unittest
from unittest.mock import patch
from tools.upstream_board_audit import audit

class UpstreamBoardAuditTests(unittest.TestCase):
    @patch("tools.upstream_board_audit.read_source")
    def test_makefile_assignments(self, read):
        def fake(repo, branch, path):
            if path == "BoardConfig.mk":
                return " TARGET_BOARD_PLATFORM := mt6768\nBOARD_KERNEL_PAGESIZE := 2048\n", "fixture://board"
            return "ARCH=arm64\nDEFCONFIG=RMP6768_defconfig\nFILES=\"\n", "fixture://kernel"
        read.side_effect = fake
        result = audit()["sources"]
        self.assertEqual(result["board_config"]["matched_properties"]["TARGET_BOARD_PLATFORM"], ["TARGET_BOARD_PLATFORM := mt6768"])
        self.assertEqual(result["kernel_build"]["matched_properties"]["DEFCONFIG"], ["DEFCONFIG=RMP6768_defconfig"])

if __name__ == "__main__":
    unittest.main()
