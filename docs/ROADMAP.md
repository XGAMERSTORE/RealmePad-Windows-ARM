# Roadmap

## Phase 0 — read-only discovery
- [ ] Confirm model RMP2103 using on-device properties.
- [ ] Identify SoC, kernel, Android version, boot mode and partition layout without reading raw partitions.
- [ ] Research bootloader unlock availability and official recovery path.
- [ ] Document known vendor firmware availability and licensing.

## Phase 1 — recovery prerequisites
- [ ] Back up personal files.
- [ ] Establish a **verified** recovery method for the exact hardware revision.
- [ ] Assess hard-brick risk and whether a safe boot-only test is supported.

## Phase 2 — boot feasibility
- [ ] Research MediaTek boot chain and any device-specific UEFI/EDK2 work.
- [ ] Build a minimal non-destructive boot proof of concept only if supported.
- [ ] Validate framebuffer, memory map, storage and USB.

## Phase 3 — operating system feasibility
- [ ] Evaluate Windows ARM64 boot prerequisites, ACPI, storage and display drivers.
- [ ] Assess touch, power, charging, audio, wireless and LTE.
- [ ] Keep Android intact until reliable recovery and boot are proven.

## Phase 4 — optional replacement
Only consider Android replacement after reproducible boot, usable drivers, documented recovery and informed acceptance of data-loss/bricking risks.

**No phase implies guaranteed Windows compatibility.**
