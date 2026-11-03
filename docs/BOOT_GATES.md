# Hardware boot gates for RMP6768

This is an evidence-based decision record, not a flashing guide.

| Gate | Required evidence | Status |
|---|---|---|
| Identify exact model | RMP2102 LTE or RMP2103 Wi-Fi | Public model mapping only |
| Bootloader alternative | Verified unlock / non-destructive boot procedure for exact model | Unknown |
| Recovery | Independently tested restore method for exact hardware | Unknown |
| Firmware entry | Device-specific early-boot chain and permitted entry point | Unknown |
| UEFI | Executing EDK2 on physical tablet | Not implemented |
| Windows | ACPI, interrupt controller, timer, boot storage drivers | Not implemented |

## Relevant upstream
- https://github.com/Realme-Pad-Dev/android_device_realme_RMP6768/tree/lineage-20.0
- https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768/blob/arrow-13.1/build.config.RMP6768
- https://github.com/tianocore/edk2

Do not assume that Linux DTBs can be passed directly to Windows, or that a generic ARM64 EDK2 build supports MT6768. The QEMU target is solely for host-side toolchain validation.
