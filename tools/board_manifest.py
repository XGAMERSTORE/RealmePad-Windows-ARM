#!/usr/bin/env python3
"""Generate a non-flashable, machine-readable board research manifest."""
import json
from pathlib import Path

board = {
    "project": "RealmePad-Windows-ARM",
    "codename": "RMP6768",
    "models": {"RMP2102": "LTE", "RMP2103": "Wi-Fi"},
    "soc": "MediaTek Helio G80",
    "cpu_architecture": "aarch64",
    "gpu": "Mali-G52 MC2",
    "display": {"width": 1200, "height": 2000},
    "boot_status": "not demonstrated",
    "windows_status": "not demonstrated",
    "uefi_status": "not demonstrated",
    "safe_to_flash": False,
    "note": "Research metadata only. NOT a firmware image or Windows driver.",
}
if __name__ == "__main__":
    print(json.dumps(board, indent=2, ensure_ascii=False, sort_keys=True))
