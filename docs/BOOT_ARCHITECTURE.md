# Boot architecture research: RMP6768

## Existing chain
MediaTek SoC boot ROM -> vendor-specific early boot stages -> Android boot image/kernel -> Android userspace.

The exact secure boot configuration, early boot stage formats, partition layout and supported alternative boot methods have NOT been verified for the target hardware.

## Windows ARM64 requirements
1. A verified route to launch a custom UEFI implementation (such as EDK2), without destroying the vendor recovery path.
2. Correct memory map, exception levels, timers, interrupts and storage initialization.
3. ACPI tables and Windows-compatible platform support.
4. Boot-critical storage and display support, followed by touch, USB, power, audio, Wi-Fi and modem drivers.
5. Legal Windows ARM64 image supplied separately by the device owner.

## Decision gates
- Gate A: identify exact model and vendor boot-chain constraints.
- Gate B: independently verify recovery and a reversible test path.
- Gate C: build a minimal boot payload in CI (not device-flashable).
- Gate D: demonstrate serial/framebuffer output on physical hardware.
- Gate E: demonstrate UEFI services and OS loader boot.
- Gate F: validate Windows hardware drivers before considering Android replacement.

No untested boot image is labeled as flashable or release-ready.
