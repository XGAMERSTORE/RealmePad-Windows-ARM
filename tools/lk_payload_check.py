#!/usr/bin/env python3
"""Inspect an extracted LK kernel payload; never flash or modify it.

The gzip rule comes from MT6768-family community experiments on Xiaomi;
its applicability to Realme Pad RMP2102/RMP2103 remains UNVERIFIED.
"""
import argparse
import gzip
import io
from pathlib import Path

ARM64_MAGIC = b'ARM\x64'  # Linux arm64 Image header at offset 0x38
MAX_DECOMPRESSED_BYTES = 64 * 1024 * 1024  # Offline inspection resource limit, not a board memory map


def inspect(data: bytes) -> tuple[bool, str]:
    if len(data) < 2 or data[:2] != b'\x1f\x8b':
        return False, 'Payload is not gzip; the Xiaomi LK handoff requires gzip (Realme Pad unverified).'
    try:
        # gzip.decompress() expands the entire input, even for a tiny compressed bomb.
        # Read one byte past the limit to detect oversize images without unbounded allocation.
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
            image = stream.read(MAX_DECOMPRESSED_BYTES + 1)
    except (OSError, EOFError, ValueError) as exc:
        return False, f'Invalid gzip payload: {exc}'
    if len(image) > MAX_DECOMPRESSED_BYTES:
        return False, f'Decompressed payload exceeds offline inspection limit ({MAX_DECOMPRESSED_BYTES} bytes).'
    if len(image) < 0x40 or image[0x38:0x3c] != ARM64_MAGIC:
        return False, 'Decompressed payload lacks the ARM64 Linux Image header magic at offset 0x38.'
    return True, 'Gzip payload contains ARM64 Linux Image header. This does NOT prove Realme Pad bootability.'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('payload', type=Path, help='Extracted kernel payload; NOT a complete Android boot.img')
    args = parser.parse_args()
    try:
        data = args.payload.read_bytes()
    except OSError as exc:
        parser.error(str(exc))
    ok, message = inspect(data)
    print(('PASS: ' if ok else 'FAIL: ') + message)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
