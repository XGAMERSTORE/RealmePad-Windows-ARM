# MT6768 evidence provenance (research only)

This index distinguishes **tablet-specific source trees** from boot results on other MT6768-family devices. Links are research leads, not proof of a working bootloader, UEFI or Windows.

| Source | Scope | What it can support | What it cannot establish |
| --- | --- | --- | --- |
| [Realme-Pad-Dev device tree](https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768) | RMP2102 and RMP2103 Android device configuration | Leads for board identifiers, partition naming and Android integration | Signed boot-chain policy, a recoverable custom-code handoff or Windows boot |
| [Realme-Pad-Dev kernel tree](https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768) | RMP6768 Android kernel sources | Leads for kernel config, hardware peripherals and device-tree study | Actual on-device memory reservations, UEFI drivers or verified boot behavior |
| [RMP6768 kernel build configuration](https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/blob/arrow-13.1/build.config.RMP6768) | Android ARM64 kernel build configuration | Source-level confirmation of ARM64 toolchain/defconfig conventions | Bootability of an arbitrary ARM64 payload |
| [MT6768 mainline U-Boot fork](https://github.com/mt6768-mainline/u-boot) | Generic/other-device MT6768 research | Reusable ideas and possible code review targets | A ready-to-flash RMP2102/RMP2103 bootloader |
| [Redmi 9 mainline notes](https://github.com/hataketsu/mt6768-mainline-notes) | Xiaomi lancelot, **not** Realme Pad | Concrete warnings about LK decompression, MMU, RAM reservations and recovery traps | Identical boot image format, framebuffer addresses, recovery path or memory map on Realme Pad |

## Next evidence gate, separately for each model

1. Capture **redacted, read-only** properties and partition *names* using the existing inventory tool; record model and board revision without serial/IMEI.
2. Compare observed identity with the RMP6768 device/kernel sources; mark any inference from another device as unverified.
3. Identify exact-model signed-image constraints, boot stages and a **separately verified recovery path** from trustworthy documentation.
4. Only after those gates, evaluate whether a non-destructive custom-code handoff can be demonstrated. No flash, unlock, erase, boot image replacement or BCB modification is authorized by this document.

A passing host test, built EFI binary or successful U-Boot boot on Xiaomi is **not** evidence of RMP2102/RMP2103 UEFI or Windows ARM functionality.
