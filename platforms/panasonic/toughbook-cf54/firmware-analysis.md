# CF-54 Mk2 / AMI V2.20L20 — firmware analysis

**Scope:** read-only disassembly of one original 8 MiB BIOS image. These are **code-level observations**, not a physically verified successful password entry. No actual machine digest, ROM, or password is included here.

## NVAR verifier

The `AMITSESetup`-related administrator-password record appears in active NVAR data and in an older mirrored NVAR record. The 64-byte admin blocks are byte-for-byte identical; the active user-password block is blank.

Each of 32 little-endian 16-bit words has a low byte matching `(0x935B * (index + 1)) & 0xff`. The **high bytes of the first 20 words** hold the SHA-1 digest directly; the remainder follows the initialized record pattern.

**Important correction, October 27:** An early extraction mistakenly XORed both bytes of every word. In fact, the firmware initializes the word pattern and overwrites the first 20 high bytes with digest bytes. An independently checked corrected extraction matches both recorded administrator blocks. Searches against the old XOR-derived value are **invalid evidence** for this target's password.

NVAR byte positions in the owner's individual image are intentionally not published as if they were universal addresses.

## Evidence from firmware modules

### S3PeiPassword — boot/resume

The 32-bit TE module's input helper takes the printable Unicode field of a keyboard event (reported in the inspected path from `[ebx+8]`), checks `0x20 <= character <= 0x7e`, and stores 16-bit words without observed case folding. The hash routine counts those words and supplies **two bytes per character** to SHA-1, then produces the 0x935B-encoded record. This supports `SHA1(UTF-16LE(input))` on the inspected **boot/resume** path.

### MiscFunc / MiscFuncSmm

The inspected 64-bit `MiscFunc` image includes a helper that accepts printable input, widens each character into a 16-bit word buffer (at approximately `0x5BE9`), and calls the hash/record encoder (approximately `0x5C2A`). A related routine compares full 64-byte encoded records. A character-permission bitset is permissive across ASCII-printable characters; the actual F2 UI might apply stricter rules before this helper.

### Aptio Setup engine

Independent inspection of the Aptio Setup PE32+ image identified:

- SHA-1 and 0x935B record encoding in a routine near `0x4E210`;
- a thunk near `0x3084C` that jumps into the encoder and is associated with the engine's event-dispatch mechanism;
- 16-bit character-buffer copying in inspected code around `0x291F2` and `0x2E85B`, preceding dispatch of the encoder;
- a 64-byte comparison routine near `0x37B34` reached on an inspected verification path.

These form **strong evidence** that BIOS Setup uses the same family of encoding and comparison logic. We have **not** conclusively proven every step from a physical F2 keyboard event through role selection to the exact active supervisor record. Do not imply this static finding guarantees a recovered digest candidate would be accepted at F2.

## Manual versus firmware checks

The model-family Panasonic reference manual describes up to **32 alphanumeric characters including spaces** and case distinctions. Some lower-level input functions appear to accept punctuation. A broad low-level acceptance range does not prove the BIOS UI permits all symbols in every mode.

Manual: https://global-pc-support.connect.panasonic.com/dldocs/71673

## Evidence matrix

| Finding | Level |
| --- | --- |
| Active and mirrored administrator records equal | Verified from private original image |
| Correct 20-byte digest placement within 0x935B record | Verified against record layout and disassembly |
| SHA-1 on 16-bit input in boot/resume code | Code-level evidence |
| Setup-engine encoder and record-compare linkage | Strong code-level evidence |
| Every physical F2 keystroke and role-selection step | **Not fully traced** |
| Plaintext accepted in physical BIOS | **No successful candidate** |

HP L70's one-byte physical-key hashing is a *different* platform-specific algorithm, not an assumption to import here.
