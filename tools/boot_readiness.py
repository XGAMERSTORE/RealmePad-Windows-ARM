#!/usr/bin/env python3
"""Fail-closed Windows ARM boot readiness gate for RMP2102/RMP2103."""
import json
import sys

MODELS = {"RMP2102": "LTE", "RMP2103": "Wi-Fi"}
REQUIRED = (
    "recoverable_boot_path",
    "board_uefi",
    "acpi_tables",
    "windows_storage_driver",
    "windows_display_driver",
    "windows_touch_driver",
)

def evaluate(model, evidence):
    if model not in MODELS:
        raise ValueError("Unsupported or unverified Realme Pad model")
    missing = [key for key in REQUIRED if evidence.get(key) is not True]
    if model == "RMP2102" and evidence.get("windows_lte_driver") is not True:
        missing.append("windows_lte_driver")
    if evidence.get("windows_wifi_driver") is not True:
        missing.append("windows_wifi_driver")
    return {"model": model, "variant": MODELS[model], "boot_ready": not missing,
            "missing": missing, "flash_authorized": False}

if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "RMP2103"
    report = evaluate(model, {})
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["boot_ready"] else 2)
