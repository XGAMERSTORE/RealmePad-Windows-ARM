# MT6768 upstream U-Boot buildability gate (research only)

Checked 2026-11-17. This is a **source-level blocker**, separate from the tablet-specific secure boot / recovery gate.

## Public evidence

- [MT6768 mainline U-Boot](https://github.com/mt6768-mainline/u-boot) is a cross-device research tree, **not** a verified Realme Pad bootloader.
- [Redmi 9 investigation](https://github.com/hataketsu/mt6768-mainline-notes) reports that the public fork has `TARGET_MT6768` and a minimal `configs/merlin.config`, but lacks `board/mediatek/mt6768/` and `configs/mt6768_defconfig`. It reports `make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- mt6768_defconfig` failing. This is **third-party reported**, not a locally reproduced build result.
- The same notes identify a framebuffer base difference between Xiaomi merlin and lancelot. **Neither address is an RMP2102/RMP2103 address.** Do not transplant these hard-coded values.
- [Realme Pad kernel build configuration](https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/blob/arrow-13.1/build.config.RMP6768) declares `ARCH=arm64`, `DEFCONFIG=RMP6768_defconfig`, and lists multiple DTBs: `mt6768.dtb`, `oppo8786.dtb`, `oppo8786_wlan.dtb`, and `oppo8786_21697.dtb`. These are **Android kernel** build artifacts, not proof of U-Boot/UEFI payload support.

## Gates before attempting an RMP U-Boot port

1. Reproduce the public fork's defconfig/build issue in a clean host-only build, recording branch, commit, compiler version and error log; do not treat the reported failure as independently verified until reproduced.
2. Identify the correct RMP2102 versus RMP2103 DTB/board variant from tablet-specific sources and **redacted read-only** inventory. Do not infer RAM reservations from an Android build config or another phone.
3. Document exact-model image verification/signing, stage handoff, RAM reservations and an independently verified recovery path **before** any on-device custom code.
4. Only then consider a separate, host-testable board support patch. A compiled EFI, successful CI or a Redmi 9 boot does not establish Realme Pad bootability.

No flash, unlock, erase, BCB change, or arbitrary payload boot is authorized here. **Status: research only; no working UEFI or Windows ARM.**
