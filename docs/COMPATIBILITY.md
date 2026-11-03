# Compatibility matrix

| Component | Status | Evidence needed |
| --- | --- | --- |
| Exact RMP2103 identity | Unverified on target | ADB getprop |
| Bootloader unlock | Unknown | Device-specific verified documentation |
| Booting custom UEFI | Not demonstrated | Tested device-specific EDK2/UEFI |
| Windows ARM64 boot | Not demonstrated | Boot log and repeatable procedure |
| Display / touch | Unsupported / unknown | Working drivers |
| eMMC / storage | Unsupported / unknown | Boot-critical driver |
| Wi-Fi / Bluetooth | Unsupported / unknown | Working drivers |
| Audio | Unsupported / unknown | Working drivers |
| LTE / modem | Unsupported / unknown | Working drivers |
| Charging / sleep | Unsupported / unknown | Power management validation |
| Safe recovery | Unverified | Exact-model restore procedure |

Do not treat hardware similarity with another tablet as evidence of compatibility.
