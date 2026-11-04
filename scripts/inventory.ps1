$ErrorActionPreference = "Stop"
if (-not (Get-Command adb -ErrorAction SilentlyContinue)) { throw "Install Android platform-tools (adb)." }

# Do not enumerate device IDs: adb devices would expose serial numbers in logs.
# adb get-state fails when no device or multiple devices are connected.
$stateOutput = & adb get-state 2>&1
if ($LASTEXITCODE -ne 0) { throw "ADB device state unavailable; connect exactly one authorized device." }
$state = ($stateOutput | Out-String).Trim()
if ($state -ne "device") { throw "Expected exactly one authorized Android device; check USB debugging authorization." }

$properties = @("ro.product.model","ro.product.device","ro.product.board","ro.hardware","ro.board.platform","ro.build.version.release","ro.build.version.sdk","ro.boot.slot_suffix","ro.boot.verifiedbootstate")
foreach ($p in $properties) {
    $value = & adb shell getprop $p
    if ($LASTEXITCODE -ne 0) { throw "ADB property read failed: $p" }
    Write-Output ("{0}: {1}" -f $p, (($value | Out-String).Trim()))
}
Write-Output "Kernel:"
& adb shell uname -a
if ($LASTEXITCODE -ne 0) { throw "ADB kernel metadata read failed." }
Write-Output "Partition names (metadata only):"
& adb shell 'ls /dev/block/by-name 2>/dev/null || true'
if ($LASTEXITCODE -ne 0) { throw "ADB partition-name metadata read failed." }
Write-Output "Do NOT publish serial numbers, IMEI or raw partition contents."
