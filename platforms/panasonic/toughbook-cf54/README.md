# Panasonic Toughbook CF-54 Mk2 — BIOS supervisor research

**Status as of 2026-10-31: ongoing; no recovered password and no physical F2 BIOS acceptance.**

## Target and boundaries

- Target family: Panasonic Toughbook **CF-54 Mk2**.
- Firmware inspected: AMI Aptio **V2.20L20** from the owner's immutable, read-only original 8 MiB image.
- Purpose: investigate the actual supervisor/administrator password representation, distinguish the boot/resume and F2 Setup paths, and preserve a verifiable account of results.
- The original image, live digest, password candidates, local tooling, full logs and Hashcat checkpoints are **private on JORIE Main**, never stored in this public repository.

## Supported findings

- Administrator records in the active and mirrored NVAR structures match. The active user-password slot is blank.
- The 64-byte administrator verifier follows the `0x935B` word pattern. The **first 20 high bytes directly carry the digest**; an earlier XOR-all-bytes interpretation was wrong and corrected.
- Disassembled `S3PeiPassword`, `MiscFunc`, and Aptio Setup-engine routines support **SHA-1 of UTF-16LE/16-bit password input** in inspected paths—not the HP L70 physical-key hashing scheme.
- Setup-engine code links a 16-bit input path to the same encoder and a 64-byte comparison. The complete physical F2 keypress and credential-selection chain has **not** been independently verified.
- Searches against the **corrected** digest exhausted the configured printable 1–8-character stages; the nine-character letters/digits/spaces stage is **partial, 4.18%** as of October 31, 09:00 Arizona time. No valid match was recorded.

## Documentation

- [Firmware analysis and evidence levels](firmware-analysis.md)
- [Dated research and test ledger](research-log.md)
- [Offline runner state and requested duration-based design](runtime-design.md)
- [Unresolved verification and calibration questions](validation-gaps.md)

This is a **dated snapshot**, not live telemetry. No plaintext password, firmware patch, or unlocked BIOS image is published. The user-specific device image and checkpoint remain untouched by the repository reorganization.
