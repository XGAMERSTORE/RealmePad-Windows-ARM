# First executable UEFI milestone (emulator only)

The source under `uefi/RmpResearchApp` is a real UEFI ARM64 application using EDK2 APIs. It prints a research banner and exits. It has **no MediaTek-specific initialization**, no ACPI tables, and no flashable payload.

## Why emulator first?
The upstream Android device tree confirms the RMP6768 family and Helio G80. That does not establish a bootable UEFI entry point. QEMU with ArmVirtPkg is an independent test environment; a successful emulated build **does not imply** that the binary will boot on the realme Pad.

## Build intent
Use the `uefi-emulator.yml` workflow to compile the application against upstream EDK2 for AARCH64. Output is an EFI application for inspection/testing only, not a Windows image or board firmware.

## Required before hardware work
1. Proven device-specific boot chain and safe recovery.
2. Working platform firmware initialization, memory map, timers, interrupt controller, console and boot storage.
3. Windows ARM64 UEFI and ACPI requirements: https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/uefi-requirements-that-apply-to-all-windows-platforms
4. Hardware-compatible Windows drivers.

Do not flash or attempt to boot the EFI application as an Android boot image.
