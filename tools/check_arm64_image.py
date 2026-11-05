#!/usr/bin/env python3
"""Validate a compiled ARM64 U-Boot Linux Image wrapper; never proves device compatibility."""
import argparse
import hashlib
import pathlib
import struct

MAGIC = 0x644D5241  # bytes b'ARM\\x64' at offset 56
HEADER_SIZE = 64


def inspect_image(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    if len(data) < HEADER_SIZE:
        raise ValueError("ARM64 Image is shorter than its 64-byte header")
    text_offset, image_size, flags = struct.unpack_from("<QQQ", data, 8)
    magic, reserved = struct.unpack_from("<II", data, 56)
    if magic != MAGIC:
        raise ValueError(f"Bad ARM64 Image magic: 0x{magic:08x}")
    if reserved != 0:
        raise ValueError("ARM64 Image header reserved word is not zero")
    if image_size and image_size > len(data):
        raise ValueError("Declared ARM64 Image size exceeds file size")
    return {
        "file_size": len(data),
        "image_size": image_size,
        "text_offset": text_offset,
        "flags": flags,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=pathlib.Path)
    args = parser.parse_args()
    result = inspect_image(args.image)
    for key, value in result.items():
        print(f"{key}: {value}")
    print("ARM64 header validation passed. Hardware compatibility NOT established.")


if __name__ == "__main__":
    main()
