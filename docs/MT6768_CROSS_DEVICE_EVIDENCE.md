# MT6768 cross-device bootchain evidence (2026-11-15)

This is a **source comparison, not Realme Pad boot evidence**. RMP2102 (LTE) and RMP2103 (Wi-Fi) remain independently unverified. Do not flash, unlock, erase or replace any partitions based on this note.

## Public references

- [Realme Pad Android device tree](https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768): identifies the RMP2102/RMP2103 family and shared Android device configuration. Android device-tree support does not establish a UEFI boot path.
- [Realme Pad downstream kernel](https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768) and [recovery sources](https://github.com/Realme-Pad-Dev/android_recovery_realme_RMP6768): references for later inventory; source availability does **not** independently verify a safe restore procedure.
- [MT6768 mainline U-Boot fork](https://github.com/mt6768-mainline/u-boot): platform-level research, not a verified RMP2102/RMP2103 port.
- [Redmi 9 / lancelot MT6768 research](https://github.com/hataketsu/mt6768-mainline-notes): reports a second-stage U-Boot handoff via LK and subsequent mainline Linux boot on **another device**. Its write-up describes gzip payload expectations, memory-map/relocation failures, and persistent recovery-loop risks. These findings are hypotheses to investigate, **not** reusable Realme Pad addresses, image formats, signing assumptions or proof of recovery.

## Next evidence gate (read-only)

For **each** variant separately: collect redacted Android properties and partition **names**; establish the actual bootloader stages, image/header expectations, verified-boot/signing constraints, and board-specific reserved-memory map from independently attributable sources. Verify an exact-variant recovery path before any boot experiment. Record provenance and distinguish observed on-device facts from cross-device hypotheses.

**Status:** no verified recoverable custom ARM64 handoff, hardware UEFI, or Windows ARM64 boot on either Realme Pad variant. Host builds and emulator EFI tests do not change this status.
