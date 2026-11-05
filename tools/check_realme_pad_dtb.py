#!/usr/bin/env python3
"""Fail-closed checks for the experimental Realme Pad DTB (not a bootability test)."""
import argparse
import pathlib
import subprocess

EXPECTED_MODEL = "realme Pad (RMP2102/RMP2103) - experimental"


def get_property(dtb: pathlib.Path, node: str, prop: str):
    result = subprocess.run(
        ["fdtget", "-t", "s", str(dtb), node, prop],
        text=True, capture_output=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def validate(dtb: pathlib.Path):
    if get_property(dtb, "/", "model") != EXPECTED_MODEL:
        raise ValueError("Not the experimental Realme Pad device tree")
    compatible = get_property(dtb, "/", "compatible") or ""
    if "realme,rmp6768" not in compatible.split():
        raise ValueError("Realme Pad compatible missing")
    if any(name in compatible.lower() for name in ("xiaomi", "lancelot", "merlin")):
        raise ValueError("Xiaomi identity found in experimental tree")
    # A skeleton-only /memory placeholder must not be mistaken for real DRAM.
    memory = subprocess.run(["fdtget", "-t", "x", str(dtb), "/memory", "reg"],
                            text=True, capture_output=True, check=False)
    if memory.returncode != 0 or any(int(v, 16) for v in memory.stdout.split()):
        raise ValueError("Experimental DTB must retain an unconfigured /memory placeholder")
    if get_property(dtb, "/chosen", "bootargs") is not None:
        raise ValueError("Unexpected hard-coded boot arguments")
    # Check entire flattened tree, not only a guessed /framebuffer node.
    dump = subprocess.run(["dtc", "-I", "dtb", "-O", "dts", str(dtb)],
                          capture_output=True, text=True, check=True)
    if "simple-framebuffer" in dump.stdout:
        raise ValueError("Unverified simple-framebuffer is enabled/present")
    if "0x7d9b0000" in dump.stdout.lower():
        raise ValueError("Xiaomi reference framebuffer address present")
    print("Experimental Realme Pad DTB checks passed; NOT boot-tested or flashable.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dtb", type=pathlib.Path)
    validate(parser.parse_args().dtb)
