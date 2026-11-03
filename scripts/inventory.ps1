$ErrorActionPreference = "Stop"
if (-not (Get-Command adb -ErrorAction SilentlyContinue)) { throw "Install Android platform-tools (adb)." }
adb get-state
$properties = @("ro.product.model","ro.product.device","ro.product.board","ro.hardware","ro.board.platform","ro.build.version.release","ro.build.version.sdk","ro.boot.slot_suffix","ro.boot.verifiedbootstate")
foreach ($p in $properties) { Write-Output ("{0}: {1}" -f $p, (adb shell getprop $p)) }
Write-Output "Kernel:"
adb shell uname -a
Write-Output "Partition names (metadata only):"
adb shell 'ls /dev/block/by-name 2>/dev/null || true'
Write-Output "Do NOT publish serial numbers, IMEI or raw partition contents."
