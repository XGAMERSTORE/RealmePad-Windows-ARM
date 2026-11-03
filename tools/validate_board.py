#!/usr/bin/env python3
"""Offline checks for public board metadata; never communicates with a tablet."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
board = json.loads(subprocess.check_output([sys.executable, str(root / "tools" / "board_manifest.py")], text=True))
assert board["codename"] == "RMP6768"
assert board["models"] == {"RMP2102": "LTE", "RMP2103": "Wi-Fi"}
assert board["cpu_architecture"] == "aarch64"
assert board["safe_to_flash"] is False
assert board["windows_status"] == "not demonstrated"
print("Board research manifest validated; no device firmware produced.")
