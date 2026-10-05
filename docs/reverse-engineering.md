# L70 reverse-engineering notes

## Tested target

These notes describe the behavior observed in `SmmPlatform.efi` from HP L70 Ver. 01.08 on an HP ZBook 17.

Relevant sanitized checksums are recorded in `evidence/firmware-checksums.txt`.

## NVRAM variables

The administrator-password digest is associated with:

- `HP_BIOSAdminScanCode`
- `HP_TempBIOSAdminScancode`

The stored administrator value is 20 bytes, consistent with SHA-1.

## Password-processing call chain

The relevant path in the tested `SmmPlatform.efi` is:

- around `0x18001458D`: password length is obtained;
- `0x180014592`: length is checked against `0x20` (32 characters);
- `0x1800145AD`: original password pointer is passed to a preparatory helper;
- `0x1800145F4` through `0x180014607`: UTF-16 password characters are converted into a one-byte-per-character buffer by `0x18001C714`;
- `0x18001460C` through `0x180014624`: that byte buffer is passed to `0x180020C18` with the original character count as input length and 20 bytes of output requested;
- the resulting digest is then used with the `HP_BIOSAdminScanCode` variable path.

The important property is that the hash input length is the password character count and the conversion output is one byte per character.

## SHA-1 wrapper

Function `0x180020C18` behaves as a SHA-1 wrapper:

1. requires at least `0x14` bytes of output space;
2. initializes a hash context;
3. updates it with the converted password byte buffer and supplied length;
4. finalizes the digest;
5. copies `0x14` bytes to the caller.

No salt was observed in this path.

## UTF-16 to physical-key conversion

Function `0x18001C714`:

- accepts the UTF-16 password pointer, character count, and destination byte buffer;
- establishes keyboard locale `0x0409`;
- converts each UTF-16 code point through `0x18001C65C`;
- writes one byte per input character;
- restores the previous locale afterward.

Space is handled specially as byte `0x39`.

The general character mapper `0x18001C65C` delegates to `0x18001C404`, which searches a runtime keyboard-layout table.

## Runtime keyboard table

Function `0x18001C240` builds the runtime table at `0x180034AB0`.

Observed behavior:

- it selects a keyboard-layout descriptor from a pointer table near `0x180031D20`;
- clears `0x708` bytes for the runtime table;
- parses a compact variable-length source blob;
- emits `0x12`-byte records;
- stores the record count at `0x1800351B8`.

For locale `0x0409`, the tested firmware points to an embedded layout blob at module file offset `0x2C6A0`, length `0x11A` bytes.

The parser reconstructed 47 records and consumed the blob exactly.

## Verified key equivalences

The reconstructed US layout proves that multiple Unicode characters associated with the same physical key are accepted by the same record and return the same one-byte key value.

Verified examples:

```text
'1' and '!' -> 0x02
'w' and 'W' -> 0x11
'r' and 'R' -> 0x13
'f' and 'F' -> 0x21
'/' and '?' -> 0x35
```

Therefore case and Shift state are not preserved in the digest input.

## Security/recovery implication

The stored value is best modeled as:

```text
visible password
    |
    v
US-English physical-key mapping
    |
    v
one byte per physical key
    |
    v
SHA-1
    |
    v
20-byte HP_BIOSAdminScanCode value
```

This means:

- the digest does not reveal password length or individual keys directly;
- conventional ASCII wordlists do not represent the actual hash input unless they are first converted;
- multiple visible passwords can be equivalent because they use the same physical keys;
- offline recovery can operate on physical-key sequences once the stored digest is obtained from an authorized device.

## Limits

The addresses and offsets above are for the tested binary. They should not be assumed stable across later L70 revisions or other HP firmware families.

The project deliberately avoids firmware-write procedures. Its focus is understanding and verifying the stored password representation.
