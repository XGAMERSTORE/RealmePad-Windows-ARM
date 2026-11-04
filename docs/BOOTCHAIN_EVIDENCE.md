# Public boot-chain evidence ledger (research only)

Checked 2026-11-04. This ledger records what publicly visible sources actually establish, not a boot procedure or a compatibility claim. No firmware images are redistributed.

| Source | Verified scope | Does **not** establish |
| --- | --- | --- |
| [Realme-Pad-Dev device tree](https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768) | Android device configuration for both RMP2102 and RMP2103, unified as RMP6768; Helio G80 family | Working UEFI, a Windows boot path, unlock policy or tested recovery |
| [Realme-Pad-Dev project index](https://github.com/Realme-Pad-Dev) | Public Android device/kernel/vendor/recovery research repositories exist | Firmware authenticity, executable handoff into arbitrary unsigned ARM64 code |
| [ArrowOS device tree](https://github.com/ArrowOS-Devices/android_device_realme_RMP6768) | Independent public Android build configuration names both variants | Model-specific boot-chain trust boundary or a proven EDK2 port |

## Critical missing evidence

1. **Per-variant, on-device identity:** redacted read-only build properties and board identifiers from an actual RMP2102 and RMP2103. A shared Android device tree is not proof that their low-level partitions or signing policy are identical.
2. **Boot-chain provenance:** exact firmware build/revision, authenticated preloader / LK / verified-boot behavior and whether any non-destructive custom-code handoff is supported. Android kernel and recovery sources alone cannot answer this.
3. **Recovery gate:** independently verified, exact-model restoration procedure before any hardware experiment. Public claims about generic MediaTek tools or another device are insufficient.
4. **Hardware boot evidence:** repeatable serial/other trustworthy logs of control reaching a minimal payload, with a documented recovery route. Until then, EFI binaries are host/emulator diagnostics only.

## Research hygiene

- Treat the board/platform identifier `RMP6768` as an Android project identifier, **not** a demonstrated universal bootloader or binary compatibility target.
- Do not infer the presence of UEFI from a PE/COFF EFI artifact or from Android boot image headers.
- Do not rely on unofficial tutorials to decide which variant has LTE: use exact-device read-only properties and manufacturer evidence. Track the two models separately.
- Do not unlock, flash, bypass verified boot, erase, or distribute proprietary firmware to fill these evidence gaps.
