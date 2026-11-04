#!/usr/bin/env bash
set -euo pipefail
command -v adb >/dev/null || { echo "Install Android platform-tools (adb)."; exit 1; }
echo "Checking authorized device..."
state="$(adb get-state)" || { echo "ADB device state unavailable." >&2; exit 1; }
if [[ "$state" != "device" ]]; then
  printf 'Expected one authorized Android device, got: %s\n' "$state" >&2
  exit 1
fi
echo "Read-only system properties (no serial/IMEI):"
for p in ro.product.model ro.product.device ro.product.board ro.hardware ro.board.platform ro.build.version.release ro.build.version.sdk ro.boot.slot_suffix ro.boot.verifiedbootstate; do
  printf '%s: ' "$p"
  adb shell getprop "$p" | tr -d '\r'
done
echo "Kernel:"
adb shell uname -a
echo "Partition names (metadata only):"
adb shell 'ls /dev/block/by-name 2>/dev/null || true'
echo "Do NOT publish serial numbers, IMEI or raw partition contents."
