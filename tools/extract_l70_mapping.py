#!/usr/bin/env python3
"""Reconstruct the HP L70 01.08 runtime keyboard map from SmmPlatform.efi.

Read-only: this script never writes to the supplied firmware module.

Verified target:
  HP ZBook 17
  L70 Ver. 01.08
  SmmPlatform.efi SHA256:
  1f770c776c85d3c3a6df65fae2f176c48a3f7dfa33a2e366cb4f21185d0ad582

The offsets in this script are specific to the verified binary. An unknown
module is not silently treated as equivalent; the script warns and still
requires all expected structures to validate before producing a map.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

IMAGE_BASE = 0x180000000
LAYOUT_POINTER_TABLE_OFF = 0x31D20
LAYOUT_DESCRIPTOR_COUNT = 0x3E
US_ENGLISH_LOCALE = 0x0409

KNOWN_SHA256 = (
    "1f770c776c85d3c3a6df65fae2f176c48a3f7dfa33a2e366cb4f21185d0ad582"
)
KNOWN_US_BLOB_OFF = 0x2C6A0
KNOWN_US_BLOB_SIZE = 0x11A
KNOWN_RECORD_COUNT = 47


class ParseError(RuntimeError):
    pass


def u16(data: bytes, off: int) -> int:
    if off < 0 or off + 2 > len(data):
        raise ParseError(f"u16 out of bounds at 0x{off:X}")
    return struct.unpack_from("<H", data, off)[0]


def u32(data: bytes, off: int) -> int:
    if off < 0 or off + 4 > len(data):
        raise ParseError(f"u32 out of bounds at 0x{off:X}")
    return struct.unpack_from("<I", data, off)[0]


def u64(data: bytes, off: int) -> int:
    if off < 0 or off + 8 > len(data):
        raise ParseError(f"u64 out of bounds at 0x{off:X}")
    return struct.unpack_from("<Q", data, off)[0]


def va_to_off(va: int) -> int:
    return va - IMAGE_BASE


def locate_layout(data: bytes, locale: int = US_ENGLISH_LOCALE) -> tuple[int, int, int, int]:
    """Return (descriptor_index, descriptor_off, blob_off, blob_size)."""
    for idx in range(LAYOUT_DESCRIPTOR_COUNT):
        ptr_off = LAYOUT_POINTER_TABLE_OFF + idx * 8
        descriptor_va = u64(data, ptr_off)
        if descriptor_va == 0:
            continue

        descriptor_off = va_to_off(descriptor_va)
        if descriptor_off < 0 or descriptor_off + 0x1C > len(data):
            continue

        if u32(data, descriptor_off + 0x18) != locale:
            continue

        blob_va = u64(data, descriptor_off)
        blob_off = va_to_off(blob_va)
        blob_size = u32(data, descriptor_off + 8)

        if blob_off < 0 or blob_size <= 0 or blob_off + blob_size > len(data):
            raise ParseError("layout descriptor points outside the supplied module")

        return idx, descriptor_off, blob_off, blob_size

    raise ParseError(f"locale 0x{locale:04X} was not found")


def parse_records(data: bytes, blob_off: int, blob_size: int) -> list[dict]:
    """Mirror the stream consumption and runtime writes in 0x18001C240."""
    pos = 0
    records: list[dict] = []

    def read_byte() -> int:
        nonlocal pos
        if pos >= blob_size:
            raise ParseError("unexpected end of keyboard-layout blob")
        value = data[blob_off + pos]
        pos += 1
        return value

    def read_word() -> int:
        nonlocal pos
        if pos + 2 > blob_size:
            raise ParseError("unexpected end of keyboard-layout blob")
        value = u16(data, blob_off + pos)
        pos += 2
        return value

    while pos < blob_size:
        src_start = pos
        scan = read_byte()
        flags = read_byte()

        # Runtime record: key word at +0x00, then Unicode words at +0x02..+0x10.
        slots = [0] * 8

        a = read_word()
        b = read_word()
        slots[0] = a
        slots[1] = b

        if flags & 0x80:
            c = 0
        else:
            c = read_word()
        slots[2] = c

        if flags & 0x01:
            slots[3] = a
        elif flags & 0x02:
            slots[3] = b
        else:
            slots[3] = read_word()

        if flags & 0x04:
            slots[4] = a
        elif flags & 0x08:
            slots[4] = b
        else:
            slots[4] = read_word()

        if (flags & 0x10) or (flags & 0x80):
            slots[5] = 0
        else:
            slots[5] = read_word()

        # This intentionally mirrors the observed firmware writes. In the
        # no-0x20/non-0x80 branch, the consumed word is written to runtime
        # slot +0x0C again rather than +0x0E.
        if flags & 0x20:
            slots[6] = c
        elif flags & 0x80:
            slots[6] = 0
        else:
            slots[5] = read_word()

        if flags & 0x40:
            slots[7] = slots[5]
        elif flags & 0x80:
            slots[7] = 0
        else:
            slots[7] = read_word()

        records.append(
            {
                "scan": scan,
                "flags": flags,
                "chars": slots,
                "source_offset": src_start,
            }
        )

    if pos != blob_size:
        raise ParseError(
            f"parser consumed 0x{pos:X} bytes, expected 0x{blob_size:X}"
        )

    return records


def display_char(cp: int) -> str:
    if cp == 0:
        return "0"
    if 0x20 <= cp <= 0x7E:
        ch = chr(cp)
        return repr(ch)
    try:
        ch = chr(cp)
        if ch.isprintable():
            return f"{ch!r}(U+{cp:04X})"
    except ValueError:
        pass
    return f"U+{cp:04X}"


def build_character_map(records: list[dict]) -> dict[int, int]:
    result: dict[int, int] = {}
    for record in records:
        scan = int(record["scan"])
        for cp in record["chars"]:
            cp = int(cp)
            if cp and cp not in result:
                result[cp] = scan

    # 0x18001C65C handles space directly.
    result[ord(" ")] = 0x39
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct HP L70 01.08 US-English password key mapping"
    )
    parser.add_argument("module", type=Path, help="path to SmmPlatform.efi")
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of the text table",
    )
    args = parser.parse_args()

    try:
        data = args.module.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {args.module}: {exc}", file=sys.stderr)
        return 2

    sha256 = hashlib.sha256(data).hexdigest()
    known = sha256 == KNOWN_SHA256

    try:
        idx, descriptor_off, blob_off, blob_size = locate_layout(data)
        records = parse_records(data, blob_off, blob_size)
    except ParseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    if known:
        if blob_off != KNOWN_US_BLOB_OFF or blob_size != KNOWN_US_BLOB_SIZE:
            print(
                "error: known module hash has unexpected US-layout offsets",
                file=sys.stderr,
            )
            return 4
        if len(records) != KNOWN_RECORD_COUNT:
            print(
                "error: known module hash has unexpected record count",
                file=sys.stderr,
            )
            return 4

    cmap = build_character_map(records)

    if args.json:
        payload = {
            "module": str(args.module),
            "sha256": sha256,
            "known_verified_module": known,
            "locale": "0x0409",
            "descriptor_index": idx,
            "descriptor_offset": f"0x{descriptor_off:X}",
            "blob_offset": f"0x{blob_off:X}",
            "blob_size": blob_size,
            "record_count": len(records),
            "records": [
                {
                    "scan": f"0x{int(r['scan']):02X}",
                    "flags": f"0x{int(r['flags']):02X}",
                    "source_offset": f"0x{int(r['source_offset']):X}",
                    "codepoints": [
                        None if int(cp) == 0 else f"U+{int(cp):04X}"
                        for cp in r["chars"]
                    ],
                }
                for r in records
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    print("HP L70 keyboard-layout reconstruction")
    print("====================================")
    print(f"module SHA256      : {sha256}")
    print(f"verified module    : {'yes' if known else 'NO - structure only'}")
    print(f"locale             : 0x0409 (US English)")
    print(f"descriptor index   : {idx}")
    print(f"descriptor offset  : 0x{descriptor_off:X}")
    print(f"layout blob offset : 0x{blob_off:X}")
    print(f"layout blob size   : 0x{blob_size:X} ({blob_size})")
    print(f"decoded records    : {len(records)}")
    print()

    if not known:
        print(
            "WARNING: module SHA256 is not the independently verified L70 01.08 "
            "SmmPlatform.efi."
        )
        print(
            "The structure parsed successfully, but do not treat identical behavior "
            "as proven without review."
        )
        print()

    print("Physical-key equivalence classes")
    print("--------------------------------")

    for record in records:
        chars = [display_char(int(cp)) for cp in record["chars"] if int(cp)]
        if not chars:
            continue
        print(
            f"0x{int(record['scan']):02X}  "
            + " ".join(chars)
            + f"    flags=0x{int(record['flags']):02X}"
        )

    print()
    print("Special case:")
    print("0x39  ' '")
    print()
    print("Character lookup entries:", len(cmap))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
