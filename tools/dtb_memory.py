#!/usr/bin/env python3
"""Read-only binary DTB memory-map inspection for MT6768 port research.

DTB properties do not establish a safe LK load address. NEVER FLASH.
"""
import argparse
import struct
from pathlib import Path

def inspect(blob):
    if len(blob) < 40:
        raise ValueError("truncated FDT header")
    magic, total, os, ot, _, _, _, _, ns, nb = struct.unpack_from(">10I", blob)
    if magic != 0xd00dfeed or total > len(blob) or total < 40:
        raise ValueError("invalid FDT header")
    if os < 40 or ot < 40 or os + nb > total or ot + ns > total:
        raise ValueError("FDT block outside file")
    # Both blocks must be disjoint. Overlap would allow malformed input to
    # masquerade as valid node/property data and produce misleading RAM maps.
    if max(os, ot) < min(os + nb, ot + ns):
        raise ValueError("FDT structure and strings blocks overlap")
    # The memreserve table is distinct from /reserved-memory and may describe
    # firmware-owned RAM. Do not report a map without acknowledging it.
    reserve_offset = struct.unpack_from(">I", blob, 16)[0]
    if reserve_offset < 40 or reserve_offset + 16 > total or reserve_offset % 8:
        raise ValueError("invalid FDT memreserve offset")
    cursor = reserve_offset
    reservations = []
    reserved_ranges = []
    while cursor + 16 <= total:
        address, size = struct.unpack_from(">QQ", blob, cursor)
        cursor += 16
        if address == 0 and size == 0:
            break
        if size == 0 or address + size > (1 << 64):
            raise ValueError("invalid FDT memreserve range")
        end = address + size
        if any(address < prior_end and prior_start < end
               for prior_start, prior_end in reserved_ranges):
            raise ValueError("overlapping FDT memreserve ranges")
        reserved_ranges.append((address, end))
        reservations.append(("RESERVED", f"base=0x{address:x} size=0x{size:x}"))
    else:
        raise ValueError("unterminated FDT memreserve table")
    # Include the mandatory zero terminator when checking reservation-table overlap.
    # A zero-only table can otherwise hide inside the structure or strings block.
    if max(reserve_offset, os) < min(cursor, os + nb) or max(reserve_offset, ot) < min(cursor, ot + ns):
        raise ValueError("FDT memreserve overlaps data blocks")
    block, names = blob[os:os+nb], blob[ot:ot+ns]
    pos, stack, ac, sc, found, ram_ranges = 0, [], [2], [1], list(reservations), []
    while pos + 4 <= len(block):
        token, = struct.unpack_from(">I", block, pos)
        pos += 4
        if token == 1:
            end = block.find(b"\0", pos)
            if end < 0: raise ValueError("unterminated node")
            stack.append(block[pos:end].decode("ascii", "replace"))
            pos = (end + 4) & ~3
            if pos > len(block):
                raise ValueError("node name padding exceeds FDT structure block")
            ac.append(ac[-1]); sc.append(sc[-1])
        elif token == 2:
            if not stack: raise ValueError("unbalanced node")
            stack.pop(); ac.pop(); sc.pop()
        elif token == 3:
            if pos + 8 > len(block): raise ValueError("truncated property")
            size, noff = struct.unpack_from(">II", block, pos); pos += 8
            if not stack or noff >= len(names) or pos + size > len(block):
                raise ValueError("invalid property")
            end = names.find(b"\0", noff)
            if end < 0: raise ValueError("unterminated property name")
            key = names[noff:end].decode("ascii", "replace")
            value = block[pos:pos+size]
            pos = (pos + size + 3) & ~3
            if pos > len(block):
                raise ValueError("property padding exceeds FDT structure block")
            if key == "#address-cells" and size == 4: ac[-1] = int.from_bytes(value, "big")
            if key == "#size-cells" and size == 4: sc[-1] = int.from_bytes(value, "big")
            if key == "compatible":
                found.append(("compatible", value.rstrip(b"\0").replace(b"\0", b", ").decode("ascii", "replace")))
            if key == "reg" and stack and (stack[-1] == "memory" or stack[-1].startswith("memory@")):
                a, s = ac[-2], sc[-2]
                if a not in (1, 2) or s not in (1, 2) or not value or len(value) % (4*(a+s)):
                    raise ValueError("unsupported or empty RAM reg encoding")
                for i in range(0, len(value), 4*(a+s)):
                    cells = struct.unpack_from(">"+"I"*(a+s), value, i)
                    base = length = 0
                    for c in cells[:a]: base = (base << 32) | c
                    for c in cells[a:]: length = (length << 32) | c
                    if length == 0 or base + length > (1 << 64):
                        raise ValueError("invalid RAM range: empty or exceeds 64-bit physical address space")
                    for old_base, old_end in ram_ranges:
                        if base < old_end and old_base < base + length:
                            raise ValueError("overlapping RAM ranges")
                    ram_ranges.append((base, base + length))
                    found.append(("RAM", f"base=0x{base:x} size=0x{length:x}"))
        elif token == 4:
            continue
        elif token == 9:
            if stack:
                raise ValueError("FDT_END encountered before closing all nodes")
            if pos != len(block):
                raise ValueError("trailing data after FDT_END")
            return found
        else:
            raise ValueError(f"invalid FDT token {token}")
    raise ValueError("missing FDT_END")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dtb", type=Path)
    args = parser.parse_args()
    try:
        rows = inspect(args.dtb.read_bytes())
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for key, value in rows:
        print(f"{key}: {value}")
    print("NOT VERIFIED: LK handoff, RAM ownership, firmware load address, Realme Pad boot")

if __name__ == "__main__":
    main()
