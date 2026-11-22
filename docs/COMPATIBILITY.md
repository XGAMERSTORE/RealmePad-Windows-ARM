# Compatibility matrix

This project targets **RMP2102 (LTE)** and **RMP2103 (Wi-Fi)**. Evidence for one variant does **not** establish compatibility for the other. All statuses below are research statuses, not boot claims.

| Component | RMP2102 (LTE) | RMP2103 (Wi-Fi) | Evidence required |
| --- | --- | --- | --- |
| Exact device identity | Unverified on target | Unverified on target | Read-only ADB properties, with identifiers redacted |
| SoC / board revision | Unverified on target | Unverified on target | Device-specific board and boot metadata |
| Bootloader unlock | Unknown | Unknown | Verified exact-variant documentation |
| Verified recovery | Not demonstrated | Not demonstrated | Reproducible exact-variant restore path, independently checked |
| Boot-chain handoff to custom code | Not demonstrated | Not demonstrated | Device-specific proof of control transfer and boot logs |
| EDK2 / UEFI on hardware | Not demonstrated | Not demonstrated | Repeatable hardware boot, memory map and protocol checks |
| Windows ARM64 boot | Not demonstrated | Not demonstrated | Repeatable hardware boot logs |
| Display / touch | Unknown | Unknown | Working hardware drivers |
| eMMC / storage | Unknown | Unknown | Boot-critical storage driver validation |
| Wi-Fi / Bluetooth | Unknown | Unknown | Working hardware drivers |
| Audio | Unknown | Unknown | Working hardware drivers |
| LTE / modem | Unknown | Not applicable to Wi-Fi variant | Verified modem integration and drivers |
| Charging / sleep | Unknown | Unknown | Power management validation |

## Nearest technical blocker

The next **hardware** milestone is a verified, recoverable boot-chain handoff on each exact variant, not an EFI file that merely builds or passes static checks. A diagnostic EFI application running in an emulator does not demonstrate that the MT6768 boot chain can launch UEFI on either tablet.

Before considering any device-side experiment, collect read-only, redacted identity and partition-name inventory for each variant; verify exact-model recovery; establish what boot mode and signed-image constraints actually apply; and document an independently reproducible, non-destructive handoff. If these prerequisites remain unknown, **do not flash, unlock, erase or replace partitions**.

## Evidence levels

1. **Static / CI:** source checks, host unit tests and cross-compilation only.
2. **Emulated:** EFI execution under an emulator with recorded logs; not tablet boot evidence.
3. **On-device read-only:** ADB metadata inventory; not a custom-code boot.
4. **On-device boot proof:** repeatable handoff on the named model with recovery verified.
5. **Windows boot proof:** Windows ARM64 reaches a documented milestone on the named model, with logs.
6. **Usable system:** drivers, power management and recovery validated separately.

Do not promote a result to a higher level without corresponding evidence. Similar hardware or third-party boot-image metadata alone is insufficient.

## Public Android board configuration (research evidence, not a memory map)

The public [RMP6768 LineageOS BoardConfig.mk](https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768/blob/lineage-20.0/BoardConfig.mk) covers both RMP2102 and RMP2103 through its OTA device assertions. It declares `TARGET_BOARD_PLATFORM := mt6768`, `TARGET_ARCH := arm64`, boot image header version **2**, page size **2048**, base **0x40078000**, kernel offset **0x00008000**, ramdisk offset **0x07c08000**, and DTB offset **0x0bc08000**. It also enables Android Verified Boot (`BOARD_AVB_ENABLE := true`).

These are **Android image-packaging parameters in a third-party device tree**, not measured DRAM reservations, firmware entry points, trusted boot signatures, or evidence of an LK-to-UEFI handoff. In particular, `TARGET_NO_BOOTLOADER := true` is an Android build setting, **not** proof that the physical device lacks a bootloader. The AVB test keys in this tree must not be confused with production signing keys. Do not use these offsets to load or flash EFI images.

**Next evidence gate:** obtain separate, redacted read-only inventories for RMP2102 and RMP2103 and independently document a model-specific, recoverable boot path before any custom-code execution attempt.

## MT6768 LK handoff lessons from another device (not Realme Pad proof)

The public [Redmi 9/lancelot MT6768 mainline notes](https://github.com/hataketsu/mt6768-mainline-notes) describe an LK-to-U-Boot second-stage experiment on **Xiaomi Redmi 9**, not RMP2102 or RMP2103. In that specific setup, LK expected a **gzip-compressed** kernel payload, and passing a raw ARM64 image caused an `lk_crash`. The same research reports that probing an assumed 8 GiB DRAM range with U-Boot `get_ram_size()` touched secure memory and led to an invalid relocation; the working memory layout had to be derived from that device's LK-provided FDT and reserved regions.

**Do not copy** the Redmi 9 compression requirement, framebuffer/ramoops addresses, memory reservations, U-Boot patches, boot-image repacking workflow or recovery procedure onto Realme Pad. They are useful hypotheses and hazards to investigate, **not validated Realme Pad facts**. A successful compile, Android boot-image header or similar SoC cannot establish a safe LK handoff.

**Read-only next gate, separately per variant:** document the exact model and board revision, obtain authorized non-destructive boot metadata and any publicly available *matching-device* FDT/reserved-memory evidence, and independently confirm a reversible recovery path. Until then, no flashing or device-side payload tests.

## Public MT6768 U-Boot fork buildability gate

The [mt6768-mainline/u-boot fork](https://github.com/mt6768-mainline/u-boot) is **not a drop-in bootloader for Realme Pad**. The independent [lancelot build investigation](https://github.com/hataketsu/mt6768-mainline-notes) reports missing `board/mediatek/mt6768/` support and `configs/mt6768_defconfig` in the base fork; its own device-specific patches fill those gaps for Xiaomi lancelot. A generic `mt6768-generic.dts` or a successful patched build for lancelot does not establish an RMP2102/RMP2103 board port, signed-image acceptance, memory layout, or a safe LK entry point.

**Host-only verification gate:** before proposing a Realme Pad U-Boot/EDK2 binary, require a reproducible source revision, exact board configuration and device tree, clean cross-build logs, and a separately documented read-only device-specific memory/boot-chain inventory. No device writes or boot claims follow from a cross-build.
