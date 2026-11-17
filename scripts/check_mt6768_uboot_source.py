#!/usr/bin/env python3
"""Host-only MT6768 U-Boot source gate; never accesses a device."""
import argparse
from pathlib import Path

REQUIRED = ('configs/mt6768_defconfig', 'board/mediatek/mt6768')


def check(root: Path) -> int:
    if not (root / 'Makefile').is_file() or not (root / 'configs').is_dir():
        print('ERROR: not a recognizable U-Boot source tree')
        return 2
    missing = [name for name in REQUIRED if not (root / name).exists()]
    for name in REQUIRED:
        print(f'{"MISSING" if name in missing else "PRESENT"}: {name}')
    if missing:
        print('BLOCKED: source prerequisites missing; build and tablet boot NOT verified')
        return 1
    print('SOURCE GATE ONLY: prerequisites present; build and tablet boot NOT verified')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('uboot_tree', type=Path)
    args = parser.parse_args()
    raise SystemExit(check(args.uboot_tree))
