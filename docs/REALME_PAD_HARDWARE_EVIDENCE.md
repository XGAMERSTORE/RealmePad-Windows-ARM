# Realme Pad RMP2102/RMP2103 hardware evidence (source-level only)

This is a **research inventory**, not a bootable board description. **DO NOT FLASH** the Redmi 9 reference U-Boot artifact.

## Reproducible source locations

Public kernel tree: [Realme-Pad-Dev/android_kernel_realme_RMP6768](https://github.com/Realme-Pad-Dev/android_kernel_realme_RMP6768), branch `arrow-13.1`.

- `build.config.RMP6768` names `RMP6768_defconfig` and lists `mt6768.dtb`, `oppo8786.dtb`, `oppo8786_wlan.dtb`, `oppo8786_21697.dtb` as outputs.
- `arch/arm64/boot/dts/mediatek/oppo8786.dts` and `oppo8786_wlan.dts` are **DTS plugin overlays**, not independently complete base device trees.
- Both overlays declare `&chosen` properties `atag,videolfb-fb_base_l = <0x7e605000>`, `atag,videolfb-fb_base_h = <0x0>`, and `atag,videolfb-vramSize = <0x017e8000>`.
- Both declare a `reserve-memory-scp_share` child of `&reserved_memory` with `size = <0 0x00d00000>`, `alignment = <0 0x1000000>`, and `alloc-ranges = <0 0x40000000 0 0x50000000>`.

**Important:** These values are *source-level observations*, not proof of the runtime memory map, a safe U-Boot relocation address, a stable framebuffer, or an LK handoff contract. In particular, a reserved-memory `size` with `alloc-ranges` does **not** provide the actual physical base allocated at runtime. Never derive an image load address from the displayed framebuffer base.

## Required evidence before board code

1. Establish the exact source revision and which overlay applies to each RMP2102/RMP2103 hardware revision; do not assume the `_wlan` suffix is sufficient identification.
2. Obtain a **read-only**, device-specific runtime DT dump and LK boot arguments for each variant. Compare RAM banks, reserved-memory and bootloader-supplied framebuffer values against the source overlays.
3. Establish the LK image header format, entry state, verified-boot policy and a **non-destructive** test route. An ARM64 image header alone is insufficient.
4. Prove a documented exact-model recovery path *before* modifying any partition.
5. Only then implement a separate Realme Pad defconfig/board DTS, validate non-overlapping allocations, and test U-Boot -> EDK II -> EFI shell. Windows ARM64 additionally requires platform ACPI and drivers.

## Reference-port separation

The existing `mt6768-uboot-build.yml` builds a **Xiaomi Redmi 9 (lancelot)** reference from the published three-patch series. Its addresses, memory reservations, pstore region and cache workarounds are not established for Realme Pad. Do not rename or distribute that binary as RMP2102/RMP2103 firmware.
