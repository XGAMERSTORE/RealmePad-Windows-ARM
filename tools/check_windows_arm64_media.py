#!/usr/bin/env python3
"""Offline preflight of an extracted, user-supplied Windows ARM64 installation ISO.

This is NOT a bootability test, UEFI implementation, ISO builder or flash tool.
Only examines files; never executes payloads or writes to the source tree.
"""
import argparse
from pathlib import Path
import sys

def inspect(root: Path) -> list[str]:
    errors = []
    if not root.is_dir():
        return ["Source must be an extracted ISO directory."]
    efi = root / "efi" / "boot" / "bootaa64.efi"
    if not efi.is_file():
        errors.append("Missing efi/boot/bootaa64.efi (ARM64 removable-media EFI loader).")
    else:
        try:
            with efi.open("rb") as f:
                header = f.read(4096)
            if header[:2] != b"MZ":
                errors.append("EFI loader does not have a DOS MZ header.")
            elif len(header) < 0x40:
                errors.append("EFI loader header is truncated.")
            else:
                pe_offset = int.from_bytes(header[0x3c:0x40], "little")
                if pe_offset > len(header) - 26 or header[pe_offset:pe_offset+4] != b"PE\\0\\0":
                    errors.append("EFI loader has no valid PE signature in first 4096 bytes.")
                elif int.from_bytes(header[pe_offset+4:pe_offset+6], "little") != 0xAA64:
                    errors.append("EFI loader PE machine is not ARM64 (0xAA64).")
        except OSError as exc:
            errors.append(f"Cannot read EFI loader: {exc}")
    if not any((root / "sources" / name).is_file()
               for name in ("install.wim", "install.esd", "install.swm")):
        errors.append("Missing sources/install.wim, install.esd or install.swm.")
    if not (root / "sources" / "boot.wim").is_file():
        errors.append("Missing sources/boot.wim.")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_iso", type=Path)
    args = parser.parse_args()
    errors = inspect(args.extracted_iso)
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    if errors:
        return 1
    print("PASS: basic ARM64 Windows installation-media file checks.")
    print("NOT VERIFIED: ISO boot catalog, firmware compatibility, MT6768 UEFI, drivers, or Windows boot.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
