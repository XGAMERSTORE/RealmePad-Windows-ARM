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

## Next hardware milestone: non-destructive UEFI entry proof

The next meaningful progress is **not** another Android boot header parser.
A Windows-compatible UEFI port needs a demonstrable handoff from the actual
MT6768 boot chain, plus an independently verified recovery path.

Required evidence, in order:

1. **Variant identification:** record the exact retail model (RMP2102 LTE or
   RMP2103 Wi-Fi), Android build, board identity, and boot state using the
   read-only metadata collector. Remove serial numbers and unique IDs before
   publishing.
2. **Recovery proof:** document an independently tested method of returning
   this *specific* device to stock firmware. An online flashing tutorial is
   not proof of recovery on the test device.
3. **Entry-point proof:** establish, from primary sources and physical tests,
   whether a temporary, non-destructive ARM64 payload can be loaded. Do not
   infer support from other MediaTek devices.
4. **UEFI execution proof:** capture reproducible output of a genuine
   device-specific EDK2 firmware entry, memory map and exception handling.
   Running an EFI application under QEMU does **not** satisfy this gate.
5. **Windows boot requirements:** establish ACPI tables, GIC/timer, memory,
   storage, display and input support. Android kernel device trees and Linux
   drivers do not satisfy Windows driver requirements.
6. **End-to-end validation:** only after the above, test Windows boot and
   device functionality, with a verified rollback procedure.

**Current gate decision:** BLOCKED. No device-tested UEFI handoff, no
validated stock recovery on the target unit, and no Windows boot-critical
driver stack. Do not publish a flashable image or claim Windows boot support.

## What host-side CI proves

The Python tests validate parsers and metadata checks against synthetic
inputs. A successful CI run proves only those code paths, not device
compatibility. Keep `windows_boot_ready` and `safe_to_flash` false until
physical evidence has been independently reviewed.
