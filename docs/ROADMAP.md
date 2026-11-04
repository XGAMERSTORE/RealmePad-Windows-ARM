# Roadmap

All hardware evidence is tracked **separately** for RMP2102 (LTE) and RMP2103 (Wi-Fi). See [compatibility matrix](COMPATIBILITY.md). A host build or emulator run is not evidence of a working tablet boot.

## Phase 0 — read-only discovery (each variant)
- [ ] Confirm exact model and board revision using redacted on-device properties.
- [ ] Record SoC, kernel, Android version, boot mode and partition **names**, without dumping partitions or secrets.
- [ ] Research bootloader unlock policy and exact-variant recovery documentation; do not unlock.
- [ ] Document firmware provenance, availability and licensing separately for RMP2102 and RMP2103.

## Phase 1 — recovery prerequisites (each variant)
- [ ] Back up personal data before any future device-side work.
- [ ] Independently verify an exact-model, exact-revision recovery method.
- [ ] Assess hard-brick risk and whether a genuinely non-destructive boot-only test exists.
- [ ] Do not attempt flashing, unlocking or partition replacement while recovery is unverified.

## Phase 2 — boot-chain feasibility (each variant)
- [ ] Identify the actual MT6768 boot-chain stages, signing and verified-boot constraints from device-specific evidence.
- [ ] Establish a documented, recoverable handoff to custom code **before** claiming a UEFI port.
- [ ] Only after those gates, consider a minimal non-destructive hardware boot proof with reproducible logs.
- [ ] Separately validate framebuffer, memory map, storage and USB on real hardware.

## Phase 3 — Windows ARM64 feasibility (each variant)
- [ ] Evaluate ARM64 boot prerequisites, ACPI tables and boot-critical storage/display support.
- [ ] Assess touch, power, charging, audio and wireless; LTE/modem applies to RMP2102 only.
- [ ] Require repeatable Windows hardware boot evidence before calling the system functional.
- [ ] Keep Android intact until reliable recovery and boot are demonstrated.

## Phase 4 — optional replacement
Only consider replacement after reproducible hardware boot, usable drivers, independently documented recovery and informed acceptance of data-loss/bricking risks.

**No phase implies guaranteed Windows compatibility. Diagnostic EFI binaries, static checks and emulator execution do not establish device UEFI or Windows support.**
