# TWRP integration — read-only check, not a Windows installer

The research repository currently has no functional UEFI for MediaTek Helio G80, no Windows ARM64 board-specific ACPI, and no Windows boot-critical storage drivers. A Windows installer ZIP is therefore not available.

The optional `RMP6768-TWRP-READONLY-CHECK.zip` runs a shell script inside an existing compatible TWRP environment and prints Android device properties. It intentionally does not modify partitions, install an operating system, or alter the boot chain.

Build: `python3 tools/package_twrp_check.py`.

Do not install TWRP solely to run this check. TWRP availability and compatibility must be verified for the precise RMP2102/RMP2103 model and firmware before any recovery changes. Recovery modifications may cause data loss or a non-booting tablet. Prefer collecting properties from a running Android device through `adb shell getprop` when possible.

This ZIP is not a bootloader unlock tool, a Windows image, or a firmware update. Do not distribute it as a Windows installer.
