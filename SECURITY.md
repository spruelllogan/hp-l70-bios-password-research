# Security and sensitive-data policy

This repository is intended for authorized repair and firmware research.

## Please do not submit

Do not open an issue, discussion, pull request, or attachment containing:

- a real BIOS administrator password;
- a real BIOS password hash/digest;
- a complete SPI or BIOS dump;
- extracted proprietary HP firmware binaries;
- system serial numbers, UUIDs, MAC addresses, or asset tags;
- private keys, tokens, or account credentials.

If reproduction requires machine-specific data, describe the behavior and provide sanitized metadata or synthetic fixtures instead.

## Responsible scope

Reports that add support for another firmware revision or platform should include enough information to reproduce the finding without assuming that offsets or storage formats are identical to L70 01.08.

Prefer read-only analysis and verification. This project does not maintain generic unlocked firmware images.
