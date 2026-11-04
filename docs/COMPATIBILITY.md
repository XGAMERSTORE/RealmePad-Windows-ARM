# Compatibility matrix

This project targets **RMP2102 (LTE)** and **RMP2103 (Wi-Fi)**. Evidence for one variant does **not** establish compatibility for the other. All statuses below are research statuses, not boot claims.

| Component | RMP2102 (LTE) | RMP2103 (Wi-Fi) | Evidence required |
| --- | --- | --- | --- |
| Exact device identity | Unverified on target | Unverified on target | Read-only ADB properties, with identifiers redacted |
| SoC / board revision | Unverified on target | Unverified on target | Device-specific board and boot metadata |
| Bootloader unlock | Unknown | Unknown | Verified exact-variant documentation |
| Verified recovery | Not demonstrated | Not demonstrated | Reproducible exact-variant restore path, independently checked |
| Boot-chain handoff to custom code | Not demonstrated | Not demonstrated | Device-specific proof of control transfer and boot logs |
| EDK2 / UEFI on hardware | Not demonstrated | Not demonstrated | Repeatable hardware boot, memory map and protocol checks |
| Windows ARM64 boot | Not demonstrated | Not demonstrated | Repeatable hardware boot logs |
| Display / touch | Unknown | Unknown | Working hardware drivers |
| eMMC / storage | Unknown | Unknown | Boot-critical storage driver validation |
| Wi-Fi / Bluetooth | Unknown | Unknown | Working hardware drivers |
| Audio | Unknown | Unknown | Working hardware drivers |
| LTE / modem | Unknown | Not applicable to Wi-Fi variant | Verified modem integration and drivers |
| Charging / sleep | Unknown | Unknown | Power management validation |

## Nearest technical blocker

The next **hardware** milestone is a verified, recoverable boot-chain handoff on each exact variant, not an EFI file that merely builds or passes static checks. A diagnostic EFI application running in an emulator does not demonstrate that the MT6768 boot chain can launch UEFI on either tablet.

Before considering any device-side experiment, collect read-only, redacted identity and partition-name inventory for each variant; verify exact-model recovery; establish what boot mode and signed-image constraints actually apply; and document an independently reproducible, non-destructive handoff. If these prerequisites remain unknown, **do not flash, unlock, erase or replace partitions**.

## Evidence levels

1. **Static / CI:** source checks, host unit tests and cross-compilation only.
2. **Emulated:** EFI execution under an emulator with recorded logs; not tablet boot evidence.
3. **On-device read-only:** ADB metadata inventory; not a custom-code boot.
4. **On-device boot proof:** repeatable handoff on the named model with recovery verified.
5. **Windows boot proof:** Windows ARM64 reaches a documented milestone on the named model, with logs.
6. **Usable system:** drivers, power management and recovery validated separately.

Do not promote a result to a higher level without corresponding evidence. Similar hardware or third-party boot-image metadata alone is insufficient.
