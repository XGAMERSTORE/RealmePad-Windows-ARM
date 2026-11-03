# RMP6768 evidence ledger

Verified from public upstream device sources:
- Realme Pad RMP2102 / RMP2103 share Android board codename RMP6768.
- SoC: MediaTek Helio G80; CPU ARM64, GPU Mali-G52 MC2.
- Kernel build configuration lists `RMP6768_defconfig` and `mt6768.dtb`, `oppo8786.dtb`, `oppo8786_wlan.dtb`, `oppo8786_21697.dtb`.

Sources:
- https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768
- https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/blob/arrow-13.1/build.config.RMP6768

## Critical unresolved items
The public Android source does not demonstrate a board-specific EDK2 port, secure boot unlock path, Windows ARM64 boot, ACPI tables or boot-critical Windows drivers. These remain unverified. Do not interpret the EFI application built in CI as firmware for the tablet.

## Next hardware-dependent milestone
Obtain evidence of a recoverable non-destructive alternate boot path for the exact device variant, then design a real platform initialization layer. No flashing is authorized by this repository.
