# Windows ARM64 driver gap: MT6768

As of 2026-11-03, the public Android RMP6768 source tree is not evidence of a Windows ARM64 port.

## Boot-critical blockers
- MediaTek boot-chain entry path and a recoverable EDK2 firmware port: not established.
- UEFI firmware for this specific board: not implemented.
- Windows ACPI tables for this specific board: not implemented.
- Windows boot storage driver and validated storage initialization: not implemented.
- Windows display and input: not implemented.

## Why existing ports cannot be reused unchanged
Qualcomm edk2-msm and Rockchip EDK2 projects target different SoCs. Their firmware and device-specific Windows drivers cannot be flashed onto Helio G80. They can inform architecture and testing methodology only.

## Evidence required to advance
1. Verified non-destructive boot mechanism or tested recovery.
2. Measured RAM map and boot-stage handoff.
3. Board-specific serial or framebuffer console.
4. UEFI boot services on real hardware.
5. ACPI and Windows boot-critical drivers.

Never publish or redistribute extracted proprietary firmware without permission. No installer should be offered until these requirements are met.
