#!/usr/bin/env python3
"""Check PE/COFF header of an ARM64 EFI application, without executing it."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

def inspect(data):
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("Not an MZ executable")
    pe_offset = struct.unpack_from("<I", data, 0x3c)[0]
    if pe_offset + 26 > len(data) or data[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise ValueError("Invalid PE header")
    machine = struct.unpack_from("<H", data, pe_offset + 4)[0]
    optional_offset = pe_offset + 24
    magic = struct.unpack_from("<H", data, optional_offset)[0]
    subsystem = struct.unpack_from("<H", data, optional_offset + 68)[0]
    if machine != 0xaa64:
        raise ValueError(f"Expected ARM64 (0xaa64), got {machine:#x}")
    if magic != 0x20b:
        raise ValueError(f"Expected PE32+, got {magic:#x}")
    if subsystem != 10:
        raise ValueError(f"Expected EFI application subsystem (10), got {subsystem}")
    return {"machine": "ARM64", "format": "PE32+", "subsystem": "EFI_APPLICATION", "flashable": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("efi", type=Path)
    args = parser.parse_args()
    data = args.efi.read_bytes()
    report = inspect(data)
    report["sha256"] = hashlib.sha256(data).hexdigest()
    report["bytes"] = len(data)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
