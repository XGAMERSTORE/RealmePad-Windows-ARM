# RMP6768 board-specific kernel evidence (research only)

Checked 2026-11-12. This is a **source inventory**, not a boot procedure, validated firmware, UEFI port, Windows driver, or permission to flash.

## Public Realme Pad sources

- Device tree: https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768 (identifies RMP2102 VoLTE and RMP2103 Wi-Fi under the shared RMP6768 codename).
- Kernel tree: https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768
- Kernel build configuration: https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/blob/arrow-13.1/build.config.RMP6768
- Vendor tree: https://github.com/Realme-Pad-Dev/android_vendor_realme_RMP6768

The published kernel build configuration names `ARCH=arm64`, `DEFCONFIG=RMP6768_defconfig`, and these device-tree build outputs:

- `arch/arm64/boot/dts/mediatek/mt6768.dtb`
- `arch/arm64/boot/dts/mediatek/oppo8786.dtb`
- `arch/arm64/boot/dts/mediatek/oppo8786_wlan.dtb`
- `arch/arm64/boot/dts/mediatek/oppo8786_21697.dtb`

**Do not assume** that any one DTB is correct for a given physical unit merely from its filename. These are Android/Linux source-tree artifacts, not ACPI tables or Windows ARM drivers. The source configuration does not establish that a build boots, that a bootloader accepts it, or that the hardware can be recovered.

## Next non-destructive investigation

1. Compare the RMP6768 defconfig, DTS includes, board configuration and partition descriptions **offline** to map RMP2102 vs RMP2103 differences, documenting source revision and uncertainty.
2. Determine whether there is an independently verified **on-device stock restore path** for each variant; do not infer this from a generic MediaTek recovery guide.
3. Determine whether a **non-destructive ARM64 execution/chainload path** exists on each variant, with evidence from physical hardware and a known recovery plan.
4. Only after those gates: investigate a board-specific U-Boot/UEFI port and firmware-to-OS hardware descriptions. A diagnostic EFI binary alone does not demonstrate working UEFI or Windows.

No flashing, partition writes, bootloader unlocking, or executable payload delivery is specified or authorized by this note.

## Recovery source lead (not recovery validation)

- Public recovery source tree: https://github.com/Realme-Pad-Dev/android_recovery_realme_RMP6768 (branch `11.0`, with `BoardConfig.mk`, `twrp_RMP6768.mk`, and recovery-related sources).
- This establishes that recovery *source material* exists for the unified RMP6768 family. It does **not** demonstrate a tested stock-firmware restoration procedure for RMP2102 or RMP2103, a verified stock image, bootloader unlock support, or safe non-destructive chainloading.
- Next offline check: compare recovery `BoardConfig.mk` partition assumptions with device-tree `BoardConfig.mk`, separately record RMP2102/RMP2103 evidence, and retain `stock_restore_verified_on_device=false` until each physical variant has independently verified evidence. Do not run or publish flash commands as a substitute for validation.
