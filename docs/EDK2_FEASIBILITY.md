# EDK2 / Windows ARM64 feasibility gate

**No RMP6768 UEFI firmware has been built or booted by this project.**

## Upstream facts
- Device family: RMP6768 (RMP2102 LTE / RMP2103 Wi-Fi).
- MediaTek Helio G80 ARM64 SoC.
- Upstream kernel build config references RMP6768_defconfig and multiple MediaTek DTBs, including mt6768.dtb, oppo8786.dtb and oppo8786_wlan.dtb.
- These are Linux device-tree artifacts, not Windows ACPI tables or working Windows drivers.

## Required implementation work
1. Identify boot ROM and vendor early boot constraints, without modifying a tablet.
2. Determine whether a signed / unlocked alternative boot path exists and whether recovery is independently verified.
3. Document CPU bring-up, exception levels, MMU and memory regions from sources and hardware observations.
4. Implement EDK2 platform DSC/FDF, SEC/PEI/DXE platform initialization and UEFI boot services **only after** a viable entry path is established.
5. Provide ACPI platform tables, interrupt/timer interfaces and boot-critical storage driver support.
6. Demonstrate minimal UEFI execution on hardware before attempting a Windows loader.

## Explicit non-goals for current CI
- No dummy EFI file presented as working firmware.
- No unsigned or generic firmware flashed to device.
- No copyrighted Windows distribution or proprietary vendor binaries.
- No automatic partition modifications.

## Go / no-go
Until a device-specific recoverable boot path is proven, this project is **NO-GO for flashing**.
