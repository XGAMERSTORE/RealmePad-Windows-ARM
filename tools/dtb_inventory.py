#!/usr/bin/env python3
"""Inventory DTB names from upstream kernel build config; no device access."""
import json
import re
import urllib.request

URL = "https://raw.githubusercontent.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/arrow-13.1/build.config.RMP6768"

def parse(text):
    return sorted(set(re.findall(r"arch/arm64/boot/dts/mediatek/([A-Za-z0-9_\-]+\.dtb)", text)))

def main():
    request = urllib.request.Request(URL, headers={"User-Agent": "RealmePad-Windows-ARM"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read().decode("utf-8")
    names = parse(data)
    if not names:
        raise SystemExit("No DTBs found; upstream format may have changed")
    print(json.dumps({"device_family": "RMP6768", "source": URL, "dtbs": names, "flashable": False}, indent=2))

if __name__ == "__main__":
    main()
