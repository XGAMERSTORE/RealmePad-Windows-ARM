#!/usr/bin/env python3
"""Host-only MT6768 U-Boot source gate; never accesses a device."""
import argparse
from pathlib import Path

CONFIG = 'configs/mt6768_defconfig'
BOARD = 'board/mediatek/mt6768'


def check(root: Path) -> int:
    if not (root / 'Makefile').is_file() or not (root / 'configs').is_dir():
        print('ERROR: not a recognizable U-Boot source tree')
        return 2
    config = root / CONFIG
    board = root / BOARD
    checks = {
        CONFIG: config.is_file() and config.stat().st_size > 0,
        BOARD: board.is_dir() and any(p.is_file() for p in board.rglob('*')),
    }
    for name, valid in checks.items():
        print(f'{"PRESENT" if valid else "MISSING/EMPTY"}: {name}')
    if not all(checks.values()):
        print('BLOCKED: source prerequisites missing or empty; build and tablet boot NOT verified')
        return 1
    print('SOURCE GATE ONLY: nonempty prerequisites present; build and tablet boot NOT verified')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('uboot_tree', type=Path)
    args = parser.parse_args()
    raise SystemExit(check(args.uboot_tree))
