#!/usr/bin/env python3
"""Synthetic demonstration of the verified HP L70 password preprocessing."""

from hashlib import sha1

# Physical-key bytes verified from the L70 01.08 US-English layout.
KEY = {
    "q": 0x10, "w": 0x11, "e": 0x12, "r": 0x13, "t": 0x14,
    "y": 0x15, "u": 0x16, "i": 0x17, "o": 0x18, "p": 0x19,
    "a": 0x1E, "s": 0x1F, "d": 0x20, "f": 0x21, "g": 0x22,
    "h": 0x23, "j": 0x24, "k": 0x25, "l": 0x26,
    "z": 0x2C, "x": 0x2D, "c": 0x2E, "v": 0x2F,
    "b": 0x30, "n": 0x31, "m": 0x32,
    "1": 0x02, "2": 0x03, "3": 0x04, "4": 0x05, "5": 0x06,
    "6": 0x07, "7": 0x08, "8": 0x09, "9": 0x0A, "0": 0x0B,
    "!": 0x02,
    "?": 0x35,
    "/": 0x35,
}


def encode_visible(text: str) -> bytes:
    out = bytearray()
    for ch in text:
        lookup = ch.lower() if ch.isalpha() else ch
        try:
            out.append(KEY[lookup])
        except KeyError as exc:
            raise ValueError(
                f"synthetic demo does not define key mapping for {ch!r}"
            ) from exc
    return bytes(out)


def main() -> None:
    visible = "root1234!?"
    converted = encode_visible(visible)
    digest = sha1(converted).hexdigest()

    expected_bytes = bytes.fromhex("13181814020304050235")
    expected_sha1 = "ad03a4db11fd1bda9b93f8a58474b735659872ab"

    assert converted == expected_bytes
    assert digest == expected_sha1

    assert encode_visible("root") == encode_visible("Root")
    assert encode_visible("root") == encode_visible("ROOT")
    assert encode_visible("1") == encode_visible("!")
    assert encode_visible("/") == encode_visible("?")

    print("Synthetic HP L70 verification")
    print("============================")
    print(f"visible password : {visible}")
    print(f"converted bytes  : {converted.hex()}")
    print(f"SHA1             : {digest}")
    print()
    print("Verified synthetic equivalences:")
    print("  root == Root == ROOT")
    print("  1 == !")
    print("  / == ?")
    print()
    print("All assertions passed.")


if __name__ == "__main__":
    main()
