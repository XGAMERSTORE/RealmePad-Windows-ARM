#!/usr/bin/env python3
"""Read-only, reproducible audit of upstream RMP6768 board sources."""
import json
import re
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/Realme-Pad-Dev"
SOURCES = {
    "board_config": ("android_device_realme_RMP6768", "lineage-20.0", "BoardConfig.mk"),
    "kernel_build": ("android_kernel_realme_RMP6768", "arrow-13.1", "build.config.RMP6768"),
}
PATTERNS = {
    "board_config": ["TARGET_BOARD_PLATFORM", "BOARD_BOOT_HEADER_VERSION", "BOARD_BOOTIMG_HEADER_VERSION", "BOARD_KERNEL_PAGESIZE", "BOARD_KERNEL_BASE", "TARGET_KERNEL_CONFIG", "TARGET_PREBUILT_DTB", "BOARD_INCLUDE_DTB_IN_BOOTIMG"],
    "kernel_build": ["ARCH", "DEFCONFIG", "KERNEL_DIR", "FILES"],
}
def read_source(repo, branch, path):
    url = f"{BASE}/{repo}/{branch}/{path}"
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "RMP6768-research"}), timeout=30) as res:
        return res.read().decode("utf-8", errors="replace"), url
def audit():
    result = {"board": "RMP6768", "purpose": "research only; never flash", "sources": {}}
    for name, (repo, branch, path) in SOURCES.items():
        content, url = read_source(repo, branch, path)
        lines = content.splitlines()
        matches = {key: [line.strip() for line in lines if re.match(r"^\s*" + re.escape(key) + r"\s*[:?+]?=", line)] for key in PATTERNS[name]}
        result["sources"][name] = {"url": url, "matched_properties": matches}
    return result
if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
