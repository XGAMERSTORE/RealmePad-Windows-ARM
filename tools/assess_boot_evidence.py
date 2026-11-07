#!/usr/bin/env python3
"""Read-only RMP6768 boot evidence gate.

Accepts the JSON produced by collect_boot_metadata.py. It never unlocks,
boots, flashes, or claims the device can run Windows.
"""
import argparse
import json
from pathlib import Path

MODELS = {"rmp2102": "LTE", "rmp2103": "Wi-Fi"}

def analyze(report):
    props = report.get("properties")
    if not isinstance(props, dict):
        raise ValueError("Missing Android properties")
    model = str(props.get("ro.product.model", "")).strip().lower()
    device = str(props.get("ro.product.device", "")).strip().lower()
    candidates = [k for k in MODELS if k in model]
    variant = MODELS[candidates[0]] if len(candidates) == 1 else "unconfirmed"
    boot_state = str(props.get("ro.boot.verifiedbootstate", "")).lower()
    device_state = str(props.get("ro.boot.vbmeta.device_state", "")).lower()
    # Device codename alone is not proof of the exact retail variant.
    warnings = []
    if variant == "unconfirmed":
        warnings.append("Exact model not confirmed; do not attempt device-specific boot images")
    family_confirmed = "rmp6768" in device or len(candidates) == 1
    if not family_confirmed:
        warnings.append("RMP6768 board family not confirmed")
    if boot_state not in ("green", "yellow", "orange", "red"):
        warnings.append("Verified boot state unavailable or unexpected")
    if device_state not in ("locked", "unlocked"):
        warnings.append("VBMeta device lock state unavailable")
    warnings.append("Windows-compatible EDK2 firmware and boot-critical drivers not established")
    return {
        "model": model or "unknown",
        "variant": variant,
        "android_verified_boot_state": boot_state or "unknown",
        "android_device_state": device_state or "unknown",
        "boot_research_possible": family_confirmed,
        "windows_boot_ready": False,
        "safe_to_flash": False,
        "warnings": warnings,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(json.loads(args.metadata.read_text(encoding="utf-8"))), indent=2))

if __name__ == "__main__":
    main()
