# Documentation index

This repository is organized by vendor, machine family and firmware revision.

## Platform records

- [HP ZBook 17 / L70](../platforms/hp/zbook-l70/README.md) — **validated on real firmware**.
  - Existing [reverse engineering](reverse-engineering.md), [keyboard mapping](keyboard-mapping.md), [owner workflow](recovery-workflow.md).
- [Panasonic Toughbook CF-54 Mk2 / AMI V2.20L20](../platforms/panasonic/toughbook-cf54/README.md) — **in progress**, no recovered password.
  - [Firmware record and code paths](../platforms/panasonic/toughbook-cf54/firmware-analysis.md)
  - [Research history and valid/invalid test ledger](../platforms/panasonic/toughbook-cf54/research-log.md)
  - [Checkpoints and duration-controller design](../platforms/panasonic/toughbook-cf54/runtime-design.md)
  - [Unresolved validation gaps](../platforms/panasonic/toughbook-cf54/validation-gaps.md)

## Cross-platform guidance

- [New platform template](PLATFORM_TEMPLATE.md)
- [Data handling](DATA_HANDLING.md)
- [Publication checklist](publication-plan.md)
- [Security](../SECURITY.md)

The original HP-specific files are deliberately **not moved** so previously published links remain valid.
