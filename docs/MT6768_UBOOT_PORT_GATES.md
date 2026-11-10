# MT6768 U-Boot -> UEFI port: Realme Pad gates

**Status: no proven Realme Pad U-Boot boot or UEFI firmware. DO NOT FLASH.**

## Public upstream evidence

- https://github.com/mt6768-mainline/u-boot is a work-in-progress fork, not an RMP2102/RMP2103 port.
- https://github.com/hataketsu/mt6768-mainline-notes describes LK -> U-Boot experiments on *Xiaomi* MT6768/MT6769 hardware. The original public fork lacked board files/defconfig, but the researcher subsequently supplied patches and reports a booting U-Boot -> mainline Linux chain on Redmi 9 (lancelot). This **supersedes** the earlier claim that the Xiaomi port cannot build. The researcher's LK experiments also identify gzip-compressed kernel-slot payload and nonempty ramdisk as necessary for that Xiaomi boot path. These are **device-specific observations**, not established Realme Pad image requirements, signed-boot acceptance, or a safe flashing recipe. Xiaomi framebuffer and memory addresses must not be reused on Realme Pad.
- https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/blob/arrow-13.1/build.config.RMP6768 lists mt6768.dtb, oppo8786.dtb, oppo8786_wlan.dtb, oppo8786_21697.dtb.
- https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768 documents both RMP2102 (LTE) and RMP2103 (Wi-Fi).

## Upstream snapshot verified 2026-11-10 (not a Realme Pad port)

The public `mt6768-mainline/u-boot` main branch currently points to
[`4227900a21da`](https://github.com/mt6768-mainline/u-boot/commit/4227900a21da).
Recent upstream commits include MMC CMD23 support
([`4227900a21da`](https://github.com/mt6768-mainline/u-boot/commit/4227900a21da)),
MMC I/O-voltage switching
([`568b7ba99baf`](https://github.com/mt6768-mainline/u-boot/commit/568b7ba99baf)),
and an MT6768 T-PHY addition
([`4cb79cf00cb4`](https://github.com/mt6768-mainline/u-boot/commit/4cb79cf00cb4)).
These are useful *upstream implementation candidates* for storage and PHY
bring-up, **not** proof of RMP2102/RMP2103 hardware compatibility or of
an authenticated LK handoff. Do not import board-specific memory addresses,
device trees or boot artifacts from other vendors.

Before using any of these changes for the Realme Pad, require an exact-model
DT/clock/regulator comparison and a reproducible host-side build at a pinned
revision. No physical boot, stock restore, or secure-boot acceptance was
verified by this snapshot.

## Gates before writing or booting firmware

1. **Reproducible upstream build:** obtain a specific pinned U-Boot revision and verify a clean AARCH64 build with its actual board config. Record compiler version, config and SHA-256 of build outputs. Upstream Xiaomi configs are not Realme Pad support.
2. **Per-model DT validation:** inspect the relevant Realme Pad DTBs, including RAM banks, reserved-memory, UART, display/framebuffer, eMMC, interrupts and clocks. Do not substitute Xiaomi addresses. Record which values are *observed* versus *assumed*.
3. **Boot handoff:** establish exact LK-to-image format, load address, entry exception level, FDT address, verified-boot policy and whether custom code can be loaded without modifying partitions. An ARM64 image header alone does not establish this.
4. **Recovery:** verify an independently documented, exact-model recovery path for both RMP2102 and RMP2103 before any write or unlock operation.
5. **UEFI services:** only after an executable handoff, integrate firmware providing EFI memory map, boot/runtime services, storage/block I/O, console/GOP, ACPI and EFI system partition access. The existing WindowsBoot EFI application is *not* firmware.
6. **Windows:** Windows ARM64 additionally needs correct ACPI/platform drivers; a working U-Boot or EFI shell does not imply Windows bootability.

## Immediate engineering blocker

**No demonstrated, safely recoverable LK -> custom ARM64 image handoff on either Realme Pad variant.** The Xiaomi work is useful upstream evidence but is not a drop-in firmware or proof of boot on Realme Pad.

No firmware binary should be labeled flashable, tested or compatible until the model-specific gates above have evidence.
