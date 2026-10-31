# Security and sensitive-data policy

This is a **public** repository documenting owner-authorized, read-only firmware authentication research.

Do not include in Git commits, PRs, issues, discussions, or screenshots:

- any real administrator/supervisor password, equivalent physical-key sequence, real digest, or NVRAM credential record;
- complete SPI/BIOS/NVRAM dumps or extracted proprietary vendor binaries;
- real Hashcat pot/restore/checkpoint files, candidate lists, unreviewed logs or tool output containing private data;
- serial numbers, UUIDs, MAC addresses, inventory IDs, secrets, tokens or credentials.

Use synthetic fixtures and reviewed aggregate data. Public vendor **package** checksums may be appropriate for reproducibility; avoid checksums identifying a private machine's entire SPI dump.

Document vendor, exact firmware revision, method, uncertainty, and verification level. A static code trace is not proof a password was accepted on hardware. Do not generalize HP L70 results to Panasonic CF-54.

This repository does not maintain generic unlocked firmware, device-specific bypass images or firmware-write instructions. See [data handling](docs/DATA_HANDLING.md).
