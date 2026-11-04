# Windows ARM64 UEFI boot-chain component

This directory contains an **EDK II UEFI application**, not a complete UEFI
firmware implementation. It loads `\\EFI\\Microsoft\\Boot\\bootmgfw.efi` from the same
EFI device as the application, then transfers control using UEFI LoadImage
and StartImage. This is a genuine part of a UEFI boot flow, but it **cannot
run on RMP2102/RMP2103 until a compatible UEFI firmware exists**.

## Build (on an ARM64 EDK II build host or with ARM64 cross-toolchain)

Include `uefi/WindowsBoot/WindowsBoot.inf` in an ARM64 EDK II platform DSC,
build the platform for AARCH64, then copy the resulting WindowsBoot.efi to
an EFI system partition that already has a valid ARM64 Windows boot manager.
No Windows binaries are provided here.

## Limitations

- No MediaTek preloader / LK / AVB handoff or verified execution path
- No MT6768 DRAM initialization, interrupt controller, clocks, storage, display,
  USB or ACPI platform tables
- No claim that Windows can boot or be installed on Realme Pad
- Never flash this application into a bootloader or Android partition
