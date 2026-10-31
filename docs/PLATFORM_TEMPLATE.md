# Platform research template

Create one directory per tested vendor/model/firmware family.

## Identity

- Vendor, model family, relevant hardware revision:
- Exact firmware build and date:
- Evidence provenance (official package, original read-only device image, third-party sample):
- Toolchain and extraction method:
- Published data sanitization completed:

## Status and evidence levels

- Credential recovered? yes/no/not tested
- Candidate physically accepted by matching firmware? yes/no/not tested
- Static-code findings versus synthetic tests:
- Known uncertainties and what would resolve them:

## Technical research

- Storage variables, record layout, and mirroring (without private bytes):
- Character/physical-key input preprocessing:
- Hash and compare path:
- Differences between boot, resume and BIOS Setup:

## Test ledger

Record dates, the **digest-extraction revision** used, stage scope, aggregate outcome, verified match status and checkpoint state. Runs against an incorrect digest must be explicitly labeled invalid for the target.

## Private data

Never publish actual ROMs, machine-specific hashes, passwords, restore files, raw logs, candidate lists or unique device identifiers. The public repository is documentation, not live process storage.
