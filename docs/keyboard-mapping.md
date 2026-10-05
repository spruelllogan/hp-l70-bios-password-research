# Keyboard-layout reconstruction

## Why the table initially looks empty

The character mapper searches records at runtime address `0x180034AB0`, but the corresponding area of the PE image is zero-filled. It is runtime storage, not a static table.

The table is populated by `0x18001C240`.

## Layout selection

A layout-descriptor pointer table is located near module offset `0x31D20`.

The firmware searches up to `0x3E` descriptors and compares the locale field at descriptor offset `0x18`.

For the tested image, locale `0x0409` resolves to:

```text
descriptor index: 6
descriptor VA:    0x180031458
descriptor off:   0x31458
blob VA:          0x18002C6A0
blob off:         0x2C6A0
blob size:        0x11A (282 bytes)
```

The blob checksum is listed in `evidence/firmware-checksums.txt`.

## Record construction

The builder parses a variable-length sequence.

Each source entry begins with:

1. one output key byte;
2. one flags byte;
3. Unicode values whose presence or reuse is controlled by the flags.

The resulting runtime record is 18 bytes:

```text
offset  size  meaning
0x00    1     output physical-key byte
0x01    1     reserved/alignment in runtime representation
0x02    2     Unicode alternative 1
0x04    2     Unicode alternative 2
0x06    2     Unicode alternative 3
0x08    2     Unicode alternative 4
0x0A    2     Unicode alternative 5
0x0C    2     Unicode alternative 6
0x0E    2     Unicode alternative 7
0x10    2     Unicode alternative 8
```

The lookup routine compares the requested Unicode character against all eight Unicode slots. Any match returns the single key byte at offset `0x00`.

That structure explains why shifted and unshifted characters on the same physical key collapse to one hash input byte.

## Verified US-English examples

Reconstructing the tested `0x0409` layout produced:

```text
scan=0x02 chars='1' '!' ...
scan=0x11 chars='w' 'W' ...
scan=0x13 chars='r' 'R' ...
scan=0x21 chars='f' 'F' ...
scan=0x35 chars='/' '?' ...
```

The complete mapping can be reproduced from an authorized copy of the module with:

```bash
python3 tools/extract_l70_mapping.py /path/to/SmmPlatform.efi
```

## Physical-key equivalence

For password recovery, the correct equivalence relation is not "same character". It is "same physical-key record".

For example, the visible strings:

```text
root
Root
ROOT
rOoT
```

all convert to the same byte sequence in the tested firmware.

Similarly, `1` and `!` are indistinguishable after preprocessing, as are `/` and `?`.

The original Shift state cannot be recovered from the stored digest because that information was discarded before hashing.
