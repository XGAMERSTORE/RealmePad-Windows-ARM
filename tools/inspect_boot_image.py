#!/usr/bin/env python3
"""Inspect an Android boot image locally without extracting or flashing it."""
import argparse
import json
import struct
from pathlib import Path

MAGIC = b"ANDROID!"

def inspect(data):
    if len(data) < 44 or data[:8] != MAGIC:
        raise ValueError("Not an Android boot image")
    # v3/v4 have header_version at offset 40 and header_size at offset 20.
    version = struct.unpack_from("<I", data, 40)[0]
    if version in (3, 4):
        kernel_size, ramdisk_size, os_version, header_size = struct.unpack_from("<4I", data, 8)
        expected_size = 1580 if version == 3 else 1584
        if header_size != expected_size:
            raise ValueError("Invalid v3/v4 boot header size")
        if len(data) < header_size:
            raise ValueError("Truncated v3/v4 boot header")
        return {"format": "android_boot", "header_version": version,
                "kernel_size": kernel_size, "ramdisk_size": ramdisk_size,
                "header_size": header_size, "flashable": False}
    # Legacy v0/v1/v2: page_size at 36, header_version at 40.
    if version not in (0, 1, 2):
        raise ValueError(f"Unknown boot header version: {version}")
    if len(data) < 48:
        raise ValueError("Truncated legacy boot header")
    kernel_size = struct.unpack_from("<I", data, 8)[0]
    ramdisk_size = struct.unpack_from("<I", data, 16)[0]
    page_size = struct.unpack_from("<I", data, 36)[0]
    if page_size not in (2048, 4096, 8192, 16384):
        raise ValueError("Unexpected boot page size")
    return {"format": "android_boot", "header_version": version,
            "kernel_size": kernel_size, "ramdisk_size": ramdisk_size,
            "page_size": page_size, "flashable": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Local boot.img (read-only)")
    args = parser.parse_args()
    with args.image.open("rb") as stream:
        header = stream.read(65536)
    print(json.dumps(inspect(header), indent=2))

if __name__ == "__main__":
    main()
