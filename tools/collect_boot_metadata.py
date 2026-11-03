#!/usr/bin/env python3
"""Collect non-destructive boot metadata from an authorized Android tablet via adb.

No root, unlock, reboot, flashing, partition reading, or raw image extraction.
"""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROPERTIES = (
    "ro.product.model",
    "ro.product.device",
    "ro.product.board",
    "ro.board.platform",
    "ro.hardware",
    "ro.boot.hardware",
    "ro.boot.bootloader",
    "ro.boot.verifiedbootstate",
    "ro.boot.vbmeta.device_state",
    "ro.build.version.release",
    "ro.build.fingerprint",
    "ro.boot.slot_suffix",
)

def adb(serial, *args):
    command = ["adb"]
    if serial:
        command.extend(["-s", serial])
    command.extend(args)
    return subprocess.run(command, capture_output=True, text=True,
                          check=True, timeout=15).stdout.strip()

def collect(serial=None):
    props = {}
    for prop in PROPERTIES:
        props[prop] = adb(serial, "shell", "getprop", prop)
    # Read-only command; the kernel command line can contain device identifiers.
    # Deliberately do not collect serial, IMEI, MAC addresses, or cmdline.
    model = props.get("ro.product.model", "")
    device = props.get("ro.product.device", "")
    known = ("RMP2102", "RMP2103", "RMP6768")
    family_match = any(x.lower() in (model + " " + device).lower() for x in known)
    return {
        "schema": 1,
        "purpose": "boot-chain research only",
        "collected_utc": datetime.now(timezone.utc).isoformat(),
        "model_family_hint": "RMP6768" if family_match else "unverified",
        "properties": props,
        "no_flash_operations": True,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial", help="adb device selector; never included in output")
    parser.add_argument("--output", type=Path, default=Path("rmp-boot-metadata.json"))
    args = parser.parse_args()
    report = collect(args.serial)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Saved metadata to {args.output}. Review before sharing: build fingerprint may identify firmware.")

if __name__ == "__main__":
    main()
