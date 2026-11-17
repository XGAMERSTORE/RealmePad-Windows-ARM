#!/usr/bin/env python3
"""Record a host-only MT6768 U-Boot defconfig dry-run (not a build or boot test)."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def probe(root: Path, output: Path, timeout: int = 120) -> int:
    if not (root / 'Makefile').is_file() or not (root / 'configs').is_dir():
        print('ERROR: expected a U-Boot source checkout', file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)

    def run(argv):
        try:
            result = subprocess.run(
                argv, cwd=root, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=timeout, check=False)
            return {'command': argv, 'exit_code': result.returncode,
                    'output': result.stdout[-20000:]}
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {'command': argv, 'exit_code': None, 'error': str(exc)}

    git = run(['git', 'rev-parse', 'HEAD'])
    make = run(['make', '-n', 'O=' + str(output.resolve() / 'build'),
                'ARCH=arm', 'CROSS_COMPILE=aarch64-linux-gnu-',
                'mt6768_defconfig'])
    report = {'kind': 'host-only make dry-run; NOT a build or boot test',
              'git': git, 'make_dry_run': make}
    (output / 'mt6768_defconfig_probe.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print('Saved host-only dry-run report; no tablet accessed')
    return 0 if make.get('exit_code') == 0 else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('uboot_tree', type=Path)
    parser.add_argument('report_dir', type=Path)
    args = parser.parse_args()
    raise SystemExit(probe(args.uboot_tree.resolve(), args.report_dir.resolve()))
