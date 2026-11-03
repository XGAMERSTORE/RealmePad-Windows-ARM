#!/usr/bin/env python3
"""Compare Android boot image headers with upstream RMP6768 board parameters.

Read-only. The results are Android compatibility hints, not Windows boot proof.
"""
import argparse
import json
import struct
from pathlib import Path

def compare(header, board):
    if len(header) < 48 or header[:8] != b"ANDROID!":
        raise ValueError("Missing or truncated Android boot header")
    boot = board["android_boot"]
    version = struct.unpack_from("<I", header, 40)[0]
    if version not in (0, 1, 2):
        raise ValueError("Unsupported Android boot header version (v3+ uses a different layout)")
    if version == 1 and len(header) < 1648:\n        raise ValueError("Truncated v1 Android boot header")\n    if version == 2 and len(header) < 1660:\n        raise ValueError("Truncated v2 Android boot header")\n    page_size = struct.unpack_from("<I", header, 36)[0]
    kernel_addr = struct.unpack_from("<I", header, 12)[0]
    ramdisk_addr = struct.unpack_from("<I", header, 20)[0]
    tags_addr = struct.unpack_from("<I", header, 32)[0]
    base = int(boot["kernel_base"], 16)
    expected = {
        "kernel_addr": base + int(boot["kernel_offset"], 16),
        "ramdisk_addr": base + int(boot["ramdisk_offset"], 16),
        "tags_addr": base + int(boot["tags_offset"], 16),
    }
    observed = {"kernel_addr": kernel_addr, "ramdisk_addr": ramdisk_addr, "tags_addr": tags_addr}
    matches = {key: observed[key] == value for key, value in expected.items()}
    matches["header_version"] = version == boot["header_version"]
    matches["page_size"] = page_size == boot["page_size"]
    return {"board": board["board"], "observed": {k: hex(v) for k, v in observed.items()},
            "checks": matches, "matches_upstream_config": all(matches.values()),
            "windows_boot_ready": False, "safe_to_flash": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--board", type=Path, default=Path(__file__).resolve().parents[1] / "research/upstream-boardconfig.json")
    args = parser.parse_args()
    board = json.loads(args.board.read_text(encoding="utf-8"))
    with args.image.open("rb") as stream:
        header = stream.read(4096)
    print(json.dumps(compare(header, board), indent=2))

if __name__ == "__main__":
    main()
