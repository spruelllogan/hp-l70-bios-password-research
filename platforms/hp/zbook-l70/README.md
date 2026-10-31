# HP ZBook 17 — L70 BIOS administrator-password research

**Status: end-to-end verified on the original research machine.**

- Platform: HP ZBook 17, L70 BIOS 01.08, baseboard product 190A.
- An offline-recovered physical-key sequence matched the stored administrator digest, was accepted in firmware Setup, and the owner removed the BIOS administrator password.
- The official BIOS update subsequently installed successfully; the system reported L70 01.47.
- In **this firmware**, the hash input is one physical-key byte per character after selecting the US English keyboard map (0x0409), then SHA-1. Shift and case variants on one key collapse before hashing.
- This finding **does not apply automatically to Panasonic AMI**.

## Existing, stable documentation

- [Firmware reverse engineering](../../../docs/reverse-engineering.md)
- [Keyboard layout reconstruction](../../../docs/keyboard-mapping.md)
- [Owner-recovery workflow](../../../docs/recovery-workflow.md)
- [Read-only HP extractor](../../../tools/extract_l70_mapping.py)
- [HP synthetic verifier](../../../tools/verify_synthetic.py)
- [Reviewed evidence](../../../evidence/README.md)

Original paths were preserved to avoid breaking links. The actual password, physical-key sequence and real digest are not published.
