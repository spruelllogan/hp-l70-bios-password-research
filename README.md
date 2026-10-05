# HP L70 BIOS password research

Reverse engineering and read-only recovery research for HP L70 BIOS administrator-password handling.

## Status

Verified on:

- HP ZBook 17
- Hewlett-Packard L70 Ver. 01.08
- BIOS release date 2014-04-10
- baseboard product 190A

The repository is intentionally narrow. Findings are stated as verified for this platform/firmware unless another system is independently reproduced.

### End-to-end validation

The documented preprocessing model was validated against the original research machine:

- an offline physical-key candidate matching the stored digest was recovered;
- the candidate was accepted by the real firmware setup;
- the BIOS administrator password was removed successfully;
- the official HP BIOS update was then installed from USB;
- after reboot, the operating system reported `L70 Ver. 01.47`, BIOS release date `03/03/2020`.

The real password hash, recovered password, and recovered physical-key sequence are intentionally not published.

## Main finding

On the tested L70 firmware, the BIOS administrator password is not hashed directly as the visible text.

The firmware:

1. receives the password as UTF-16 characters;
2. temporarily selects keyboard locale `0x0409` (US English);
3. maps each character to a one-byte physical-key code;
4. computes SHA-1 over exactly one output byte per password character; and
5. stores the 20-byte digest in the NVRAM variable `HP_BIOSAdminScanCode`.

For the tested US layout, the one-byte values match the familiar PC Set-1 key numbers for the keys examined.

### Important consequence: Shift/case information is lost

Characters produced by the same physical key map to the same byte. Verified examples include:

| Visible characters | Stored key byte |
| --- | ---: |
| `r` / `R` | `0x13` |
| `w` / `W` | `0x11` |
| `f` / `F` | `0x21` |
| `1` / `!` | `0x02` |
| `/` / `?` | `0x35` |

Therefore the stored digest cannot distinguish, for example, `root`, `Root`, and `ROOT`.

This also means an offline recovery tool should search **physical-key sequences**, not ordinary ASCII strings.

## Why this repository exists

The goal is to preserve a reproducible path for owners and firmware researchers without redistributing proprietary firmware or encouraging blind firmware modification.

The work was performed read-only until the password representation and verifier were understood. No generic "unlocked BIOS" image is provided.

## Repository layout

- `docs/reverse-engineering.md` — verified call chain and firmware behavior
- `docs/keyboard-mapping.md` — runtime keyboard-layout reconstruction
- `docs/recovery-workflow.md` — read-only owner-recovery workflow
- `tools/extract_l70_mapping.py` — reconstruct the L70 US-English key map from a user-supplied `SmmPlatform.efi`
- `tools/verify_synthetic.py` — synthetic demonstration of HP's preprocessing + SHA-1
- `examples/synthetic-example.txt` — example output using no real device secret
- `evidence/` — sanitized platform/checksum/outcome evidence only
- `docs/DATA_HANDLING.md` — what must never be committed

## Privacy and safety

This repository intentionally excludes:

- complete SPI/BIOS dumps;
- extracted proprietary firmware binaries;
- system serial numbers and UUIDs;
- the real administrator-password hash from the research machine;
- the recovered administrator password or its exact physical-key sequence;
- Hashcat potfiles, restore files, and raw cracking state.

See [docs/DATA_HANDLING.md](docs/DATA_HANDLING.md).

## Reproduce the keyboard map

Obtain `SmmPlatform.efi` from your own legally obtained L70 01.08 firmware image, then run:

```bash
python3 tools/extract_l70_mapping.py /path/to/SmmPlatform.efi
```

The tool performs no writes. It validates the expected L70 01.08 structure, locates the embedded US-English layout, reconstructs the runtime records, and prints the character-to-key equivalence classes.

For the synthetic hash demonstration:

```bash
python3 tools/verify_synthetic.py
```

## Prior public work

This research builds on and independently verifies parts of earlier public HP BIOS-password work:

- `chris-pcguy/reveng-misc`: documents `HP_BIOSAdminScanCode`, scan-code conversion, and SHA-1 for an HP ProBook generation:
  https://github.com/chris-pcguy/reveng-misc
- `libv/hp_bios_passwd_erase`: open-source work cataloging HP firmware password-storage formats across several generations:
  https://github.com/libv/hp_bios_passwd_erase

Those projects should not be treated as proof that every HP generation behaves identically. This repository documents the exact L70 path observed here.

## Non-goals

This project does not provide:

- a vendor firmware image;
- a machine-specific dump;
- a universal HP password bypass;
- instructions to flash someone else's firmware;
- claims that this implementation applies to all HP systems.

## Responsible use

Use this material only on systems you own or are explicitly authorized to service. Prefer read-only extraction and verification before considering any firmware modification.
