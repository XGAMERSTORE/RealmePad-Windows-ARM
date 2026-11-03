# RealmePad-Windows-ARM

Experimental research project for **realme Pad 10.4 LTE (RMP2103)** and possible Windows on ARM support.

**Current status: research only. No working Windows boot, UEFI port, drivers or installer.**

## Objective
Investigate whether Android could eventually be replaced by Windows ARM64. This is not known to be feasible on the MediaTek Helio G80 platform.

## First step: read-only inventory
Install Android platform-tools and enable USB debugging. Connect your tablet and approve the debugging prompt.

- Linux/macOS: `bash scripts/inventory.sh`
- Windows PowerShell: `powershell -ExecutionPolicy Bypass -File scripts/inventory.ps1`

The scripts read basic system properties and partition **names**, without flashing or changing the device. Check outputs for sensitive identifiers before sharing.

## Project documents
- [Roadmap](docs/ROADMAP.md)
- [Compatibility matrix](docs/COMPATIBILITY.md)

## Safety
Do not flash generic Windows images, unlock the bootloader, erase partitions or disable verified boot at this stage. Back up personal data before future experiments. Exact-model recovery must be verified first.

No Windows binaries, proprietary firmware or vendor drivers are distributed here.
