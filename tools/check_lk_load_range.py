#!/usr/bin/env python3
"""Offline fail-closed candidate load-range check against a supplied runtime DTB.

This is NOT authorization to boot or flash. A DTB alone cannot prove that
LK, TrustZone, or other firmware has released a physical memory range.
"""
import argparse
import json
from pathlib import Path

from dtb_memory import inspect


def parse_ranges(rows):
    result = {"RAM": [], "RESERVED": [], "RESERVED_NODE": []}
    for kind, value in rows:
        if kind not in result:
            continue
        fields = dict(part.split("=", 1) for part in value.split())
        start, size = int(fields["base"], 16), int(fields["size"], 16)
        result[kind].append((start, start + size))
    return result


def assess(blob, address, size):
    if address < 0 or size <= 0 or address + size > 1 << 64:
        raise ValueError("Invalid candidate physical address or size")
    ranges = parse_ranges(inspect(blob))
    end = address + size
    within_ram = any(start <= address and end <= stop for start, stop in ranges["RAM"])
    collisions = [
        {"type": kind, "base": hex(start), "size": hex(stop - start)}
        for kind in ("RESERVED", "RESERVED_NODE")
        for start, stop in ranges[kind]
        if address < stop and start < end
    ]
    return {
        "candidate_base": hex(address),
        "candidate_size": hex(size),
        "within_reported_ram": within_ram,
        "reservation_collisions": collisions,
        "offline_layout_consistent": within_ram and not collisions,
        "lk_handoff_verified": False,
        "safe_to_boot": False,
        "safe_to_flash": False,
        "note": "DTB evidence alone cannot establish LK/firmware ownership or a safe boot address.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime_dtb", type=Path, help="Offline copy of DTB; no device commands")
    parser.add_argument("--address", type=lambda s: int(s, 0), required=True)
    parser.add_argument("--size", type=lambda s: int(s, 0), required=True)
    args = parser.parse_args()
    try:
        result = assess(args.runtime_dtb.read_bytes(), args.address, args.size)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if result["offline_layout_consistent"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
