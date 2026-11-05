#!/usr/bin/env bash
set -euo pipefail
command -v adb >/dev/null || { echo "Install Android platform-tools (adb)."; exit 1; }
echo "Checking authorized device..."
state="$(adb get-state)" || { echo "ADB device state unavailable." >&2; exit 1; }
if [[ "$state" != "device" ]]; then
  echo "Expected exactly one authorized Android device." >&2
  exit 1
fi
echo "Read-only system properties (no serial/IMEI):"
for p in ro.product.model ro.product.device ro.product.board ro.hardware ro.board.platform ro.build.version.release ro.build.version.sdk ro.boot.slot_suffix ro.boot.verifiedbootstate; do
  value="$(adb shell getprop "$p")" || { printf 'ADB property read failed: %s\n' "$p" >&2; exit 1; }
  printf '%s: %s\n' "$p" "${value//$'\r'/}"
done
echo "Kernel:"
adb shell uname -a || { echo "ADB kernel metadata read failed." >&2; exit 1; }
echo "Partition names (metadata only):"
if ! adb shell 'ls /dev/block/by-name'; then
  echo "Partition-name metadata unavailable (no partitions read or modified)." >&2
fi
echo "Do NOT publish serial numbers, IMEI or raw partition contents."
