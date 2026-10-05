# Read-only owner recovery workflow

This document describes the research workflow used on an owned HP ZBook 17. It intentionally stops short of firmware modification.

## 1. Preserve the original state

Before analysis:

- record the exact system model and BIOS revision;
- keep any firmware reads immutable;
- hash repeated reads and compare them;
- avoid writing to SPI/NVRAM while the format is still unknown.

On the research machine, repeated internal reads were compared before any password analysis was performed.

## 2. Work from a known firmware image

For reverse engineering, use:

- an official vendor BIOS package where possible; and
- a read of the owner's machine when machine-specific NVRAM must be inspected.

Never substitute a random "unlocked" image for the machine's own firmware.

## 3. Locate the password variable

On the tested L70 firmware, the administrator-password digest is associated with `HP_BIOSAdminScanCode`.

A 20-byte value is expected because the firmware path uses SHA-1.

Do not publish the real digest from a recovered machine. Treat it as credential material.

## 4. Reconstruct the preprocessing

The stored digest is not SHA-1 of the visible ASCII/UTF-16 password.

For this L70 build:

```text
UTF-16 characters
  -> forced US-English layout (0x0409)
  -> one physical-key byte per character
  -> SHA-1
```

Use `tools/extract_l70_mapping.py` to reconstruct the layout from the owner's own `SmmPlatform.efi`.

## 5. Validate with synthetic data first

Before testing a real digest, validate the implementation against a synthetic password.

`tools/verify_synthetic.py` demonstrates that:

- case variants collapse when they use the same physical key;
- shifted/unshifted variants such as `1`/`!` collapse;
- SHA-1 is computed over the converted key-byte sequence.

This guards against wasting time on an incorrectly encoded search space.

## 6. Search physical-key candidates offline

Once the mapping is verified, candidate generation should operate on the physical-key bytes rather than visible text.

Useful principles:

- deduplicate visible passwords that produce the same key-byte sequence;
- prioritize owner-specific remembered patterns first;
- record exhausted search partitions so they are not repeated;
- keep the search offline;
- do not upload the owner's real digest to public cracking services.

A recovered byte sequence identifies physical keys, not necessarily the exact visible characters. For example, a recovered `0x35` could correspond to `/` or `?` on the verified US layout.

## 7. Confirm on the actual system

Only after a candidate physical-key sequence is recovered should the owner test the corresponding visible-key variants in firmware setup.

Because Shift state is lost before hashing, multiple visible strings may be equivalent.

## What this workflow does not cover

This repository does not document:

- writing a modified NVRAM store;
- removing variables from an SPI dump;
- bypassing vendor authentication;
- flashing generic images;
- modifying Intel ME or descriptor regions.

Those are separate operations with materially higher risk.
