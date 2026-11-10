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

## Additional cross-checks (2026-11-04)

- [mtk-mainline MT6768/MT6769 project](https://gitlab.com/mtk-mainline/mt6768)
  researches Linux support for this SoC family; it is **not** a tested Realme Pad
  EDK II implementation or a Windows driver set.
- [Realme Pad recovery tree](https://github.com/Realme-Pad-Dev/android_recovery_realme_RMP6768)
  is evidence of Android recovery support, not a UEFI execution handoff.
- [RMP2103 third-party service log](https://forum.gsmhosting.com/vbb/f296/realme-rmp2103-firmware-read-ok-3313174/)
  reports secure boot and download-agent authentication. This is an unverified
  external log, **not** proof of a safe unsigned payload path.

**SoC nomenclature caution:** Helio G80 is publicly described as
MT6769V/CU; MT6768/MT6769 also names the related bootchain family. Do not
assume that a payload for a different MT6768 board can run on this tablet.

**Nearest firmware blocker:** no demonstrated, recoverable handoff from
Realme's authenticated bootchain to an arbitrary AArch64 UEFI payload on
either model. Before an on-device test, require evidence of the accepted
image format, signing policy, exception level, entry address, DRAM/reserved
memory map, and an independently validated model-specific recovery path.
None of those values should be guessed from another MediaTek board.

**Artifact boundary:** `uefi/WindowsBoot` is only an EDK II UEFI application
that requires existing working UEFI. Even a successful host build cannot
be described as a complete firmware port or proof of Windows boot.

## Source-quality update (2026-11-10)

A newly indexed third-party Realme Pad guide dated 2026-10-04
(https://techfanciers.com/realme-pad-complete-development-guide) contains
**internally conflicting variant labels**: its feature table labels RMP2102
as Wi-Fi and RMP2103 as LTE, while its introduction and the independently
maintained Realme Pad device trees identify RMP2102 as VoLTE/LTE and RMP2103
as Wi-Fi. Do **not** use the guide's variant table as a firmware selection
or recovery authority. Its generic fastboot/AVB flashing instructions are
not evidence of a tested, recoverable custom AArch64 handoff on either model.

An RMP2102 bootloop report dated 2026-06-07
(https://www.reddit.com/r/FirmwareDevelopment/comments/1tzfn2e/plz_help_plzzzz/)
describes unsuccessful custom ROM installation and missing stock backup.
It is anecdotal, but reinforces the recovery gate; it does not establish
bootchain behavior or a safe restore method.

**Decision remains BLOCKED:** no verified per-device non-destructive
LK-to-custom-payload handoff and no independently validated exact-device
recovery. Do not infer UEFI or Windows support from Android device trees,
third-party unlock recipes, or emulator diagnostics.
