# MT6768 LK handoff: external evidence and tablet verification gates

**Research note only; not a boot recipe.** Neither RMP2102 nor RMP2103 has a demonstrated custom-code handoff, working UEFI, or Windows ARM boot. Do not flash, unlock, or overwrite partitions based on this note.

## External evidence (different device)

The [Redmi 9 / lancelot MT6769T research](https://github.com/hataketsu/mt6768-mainline-notes) reports LK → U-Boot → Linux 6.18. Its failure analysis documents two conditions for **that phone's** LK implementation:

- LK decompresses a gzip kernel payload before transfer; a raw ARM64 payload caused `lk_crash` in the reported tests.
- A zero-length ramdisk also caused `lk_crash`; the reported working second-stage image included a non-empty ramdisk.

The report also documents failures caused by probing/relocating across reserved or secure DRAM. **Do not transfer lancelot addresses, carveouts, boot-image layout, signing assumptions, or recovery instructions to Realme Pad.**

## Missing device-specific proof

| Gate | RMP2102 | RMP2103 | Safe evidence |
| --- | --- | --- | --- |
| Exact board/SoC and stock image header | Unverified | Unverified | Redacted read-only properties and sourced stock firmware metadata |
| LK compression and ramdisk constraints | Unverified | Unverified | Exact-version LK and stock-image analysis; no assumptions from lancelot |
| Verified boot and signing policy | Unverified | Unverified | Exact-variant documentation; no unlocking |
| DRAM and firmware reservations | Unverified | Unverified | Exact-board DT/stock kernel metadata; no borrowed addresses |
| Independently reproducible recovery | Unverified | Unverified | Exact-model and revision restore evidence |
| LK → custom-code handoff | Not demonstrated | Not demonstrated | Repeatable hardware logs only after safety prerequisites |

**Next safe milestone:** collect provenance-tagged, redacted, read-only inventories for both variants and compare stock boot-image metadata against these *hypotheses*. Host-only checks and diagnostic EFI remain research artifacts, never working tablet UEFI or Windows evidence.

Source: https://github.com/hataketsu/mt6768-mainline-notes (consulted 2026-11-19). Third-party lancelot claims have not been reproduced on either Realme Pad variant.
