#!/usr/bin/env python3
"""Package the read-only TWRP device identity check. Not a Windows installer."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo
import hashlib

root = Path(__file__).resolve().parents[1]
src = root / "recovery" / "twrp-check"
out = root / "dist" / "RMP6768-TWRP-READONLY-CHECK.zip"
out.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(out, "w") as z:
    for file in sorted(src.rglob("*")):
        if not file.is_file():
            continue
        rel = file.relative_to(src).as_posix()
        info = ZipInfo(rel, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = (0o755 if rel.endswith("update-binary") else 0o644) << 16
        z.writestr(info, file.read_bytes())
print(out)
print("SHA256", hashlib.sha256(out.read_bytes()).hexdigest())
