# Public data-handling policy

This repository contains **sanitized research for specific HP and Panasonic firmware builds**, not machine-specific recovery state.

## Never commit

- Complete SPI/BIOS/NVRAM firmware dumps or extracted vendor modules, even temporarily.
- Actual credential hashes, verifier bytes, supervisor passwords, equivalent physical-key sequences, private candidates, Hashcat pot/restore files and checkpoints.
- Serial numbers, UUIDs, MAC addresses, service keys, host access tokens or private paths exposing those items.
- Unreviewed terminal transcripts, screenshots or runtime logs.
- Unique fingerprints of a private machine's full SPI image without explicit publication review.

## Acceptable after review

- Vendor/model family and firmware-version identifiers (not unique device IDs).
- General code-flow notes, documented offsets scoped to a particular firmware revision, limited excerpts needed for reproducibility.
- Tools operating on **user-provided** firmware and synthetic credentials, synthetic tests, coarse aggregate completion statistics.
- Reviewed claims and explicit unresolved issues.
- Checksums of **publicly distributed vendor firmware packages** where needed for reproducibility.

## Verification vocabulary

1. **Verified on hardware:** recovered entry was actually accepted by tested firmware.
2. **Code-level evidence:** an inspected firmware routine implements the described behavior.
3. **Synthetic verification:** an implementation reproduces a controlled fixture.
4. **Unverified or third-party:** not reproduced on matching firmware.

Don't conflate levels, and don't assume algorithms transfer from one manufacturer to another. Review the final diff and Git history before publishing: removing leaked content later does not reliably erase it. See [SECURITY.md](../SECURITY.md).
