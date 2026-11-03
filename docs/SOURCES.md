# Verified public sources (2026-11-03)

- Device tree (LineageOS 20): https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768
- Kernel: https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768
- Vendor tree (Android blobs; do not redistribute): https://github.com/Realme-Pad-Dev/android_vendor_realme_RMP6768
- Recovery tree: https://github.com/Realme-Pad-Dev/android_recovery_realme_RMP6768
- ArrowOS device tree: https://github.com/ArrowOS-Devices/android_device_realme_RMP6768
- ArrowOS OTA device listing: https://github.com/ArrowOS/arrow_ota/blob/master/arrow-13.1_vanilla_builds_unofficial.json

## Model mapping correction
RMP2102 = LTE; RMP2103 = Wi-Fi according to ArrowOS OTA records. Confirm physical device model before any board-specific work. Unified Android codename is RMP6768.

## Limits
Android Linux device-tree data cannot be used directly as Windows ACPI tables. Vendor binaries are not Windows drivers. No publicly verified Windows ARM or EDK2 boot for this exact board has been established here.
