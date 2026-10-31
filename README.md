# BIOS authentication and recovery research

Read-only firmware authentication research and owner-authorized recovery notes, **scoped to exact platform and firmware revision**. This repository began as HP L70 research; the existing repository name is retained for link compatibility while the documentation expands.

## Platforms

| Platform | Firmware | Verification | Details |
| --- | --- | --- | --- |
| HP ZBook 17 | HP L70 01.08 (later updated to 01.47) | **End-to-end verified**: digest match and physical Setup acceptance | [HP L70](platforms/hp/zbook-l70/README.md) |
| Panasonic Toughbook CF-54 Mk2 | AMI V2.20L20 | **Ongoing**: corrected NVAR verifier, several code paths traced; no recovered password or physical acceptance | [CF-54](platforms/panasonic/toughbook-cf54/README.md) |

**Do not transfer assumptions between platforms.** The tested HP L70 firmware hashes a physical-key sequence (case/Shift variants collapse); investigated CF-54 paths process 16-bit characters with SHA-1. The exact F2 UI chain is not fully validated.

## Documentation

- [Documentation index](docs/README.md) and [platform research template](docs/PLATFORM_TEMPLATE.md)
- [HP L70 research](platforms/hp/zbook-l70/README.md)
- [Panasonic CF-54 research](platforms/panasonic/toughbook-cf54/README.md)
- [Privacy and data handling](docs/DATA_HANDLING.md), [security policy](SECURITY.md), [publication review](docs/publication-plan.md)

Original HP files, tools, examples and evidence **remain at their existing paths** under `docs/`, `tools/`, `examples/`, and `evidence/`; existing external links continue to work.

## Scope

This public repository does **not** contain original device firmware, extracted proprietary modules, private password digests, actual recovered passwords, serial numbers, raw logs, private dictionaries or Hashcat restore/pot files. Research findings are version-specific. Prefer vendor-supported service and use this material only for devices you own or are explicitly authorized to repair.
