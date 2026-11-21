#!/usr/bin/env bash
# Host-only regression tests: fake adb, never communicate with a tablet.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/adb" <<'MOCK'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >> "$ADB_CALL_LOG"
case "$*" in
  get-state) [[ "${ADB_SCENARIO:-ok}" != "offline" ]] && echo device ;;
  'shell getprop '*) [[ "${ADB_SCENARIO:-ok}" != "property_error" ]] && echo test-value ;;
  'shell uname -r') [[ "${ADB_SCENARIO:-ok}" != "kernel_error" ]] && echo 4.14-test ;;
  'shell uname -m') echo aarch64 ;;
  'shell ls /dev/block/by-name') [[ "${ADB_SCENARIO:-ok}" != "partition_error" ]] && echo boot ;;
  *) echo 'Unexpected adb command' >&2; exit 98 ;;
esac
MOCK
chmod +x "$tmp/adb"
export PATH="$tmp:$PATH" ADB_CALL_LOG="$tmp/calls"
for scenario in ok offline property_error kernel_error partition_error; do
  export ADB_SCENARIO="$scenario"
  : > "$ADB_CALL_LOG"
  if bash "$root/scripts/inventory.sh" > "$tmp/output" 2>&1; then status=0; else status=$?; fi
  case "$scenario" in
    ok) [[ "$status" == 0 ]] && grep -q 'Kernel:' "$tmp/output" && grep -q 'aarch64' "$tmp/output" ;;
    offline) [[ "$status" != 0 ]] && ! grep -q 'shell getprop' "$ADB_CALL_LOG" ;;
    property_error) [[ "$status" != 0 ]] && grep -q 'ADB property read failed' "$tmp/output" ;;
    kernel_error) [[ "$status" != 0 ]] && grep -q 'ADB kernel metadata read failed' "$tmp/output" && ! grep -q 'shell ls /dev/block/by-name' "$ADB_CALL_LOG" ;;
    partition_error) [[ "$status" == 0 ]] && grep -q 'Partition-name metadata unavailable' "$tmp/output" ;;
  esac || { echo "FAIL: $scenario" >&2; exit 1; }
  if grep -Eiq '(^|[[:space:]])(flash|erase|reboot|push|pull|root|remount|sideload|install|shell dd)([[:space:]]|$)' "$ADB_CALL_LOG"; then
    echo "FAIL: mutating adb command in $scenario" >&2; exit 1
  fi
  echo "PASS: $scenario"
done
