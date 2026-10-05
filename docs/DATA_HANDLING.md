# Data handling and publication scope

This repository documents reverse engineering of HP L70 BIOS administrator-password handling using reproducible, read-only analysis.

## Do not commit

The public research record must not contain:

- complete SPI, BIOS, or firmware dumps;
- extracted proprietary firmware binaries;
- machine serial numbers, UUIDs, MAC addresses, or other unique identifiers;
- the real recovered administrator-password hash;
- the recovered administrator password or equivalent physical-key sequence from the research machine;
- Hashcat potfiles, restore files, raw candidate lists, or other cracking-session state;
- raw terminal logs that have not been reviewed and sanitized.

## Safe to commit

The repository may contain:

- model-family and firmware-version information needed to identify the tested platform;
- cryptographic hashes of publicly distributed HP firmware packages for reproducibility;
- function addresses, offsets, control-flow notes, and short disassembly excerpts needed to explain the reverse engineering;
- original scripts that parse a user-supplied firmware image or verify synthetic examples;
- synthetic hashes, synthetic passwords, and synthetic scan-code examples;
- aggregate benchmark figures that do not expose private machine identifiers;
- sanitized terminal transcripts when they materially support a finding.

## Scope of claims

Findings should be described as verified for the exact firmware/platform tested unless independently reproduced elsewhere. Similar behavior on other HP business systems should be labeled as unverified until confirmed.
