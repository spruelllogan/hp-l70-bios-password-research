# References

## HP vendor material

### L70 01.08 / SoftPaq sp66154

HP's archived release notes identify `sp66154.exe` as BIOS version 01.08 for the L70 ROM family and list the HP ZBook 15 and HP ZBook 17 Mobile Workstations as supported models.

- HP release notes:
  https://support.hp.com/soar-attachment/1021/col53066-ob-132634-1-ob-132634-1_sp66154.html
- Version: 01.08
- Effective date: 2014-04-10
- HP-published SoftPaq MD5: `ab5c9152e7a5ad2b7345dc75123f62e4`

The research repository does not redistribute this package or its extracted binaries.

### L70 01.47 Rev. A / SoftPaq sp103514

HP's archived release notes identify `sp103514.exe` as BIOS version 01.47 Rev. A for the L70 ROM family and list the HP ZBook 15 and HP ZBook 17 Mobile Workstations as supported models.

- HP release notes:
  https://support.hp.com/soar-attachment/759/col53066-ob-250848-1-ob-250848-1_sp103514_releasedoc.html
- Version: 01.47 Rev. A
- Effective date: 2020-05-08
- HP-published SoftPaq MD5: `4b38efa2c5f3c85d9a8c89991ec4c752`

## Prior public reverse engineering

### chris-pcguy/reveng-misc

Repository:
https://github.com/chris-pcguy/reveng-misc

Its public notes describe an HP UEFI administrator password being converted to scan codes, SHA-1 hashed, and stored in the NVRAM variable `HP_BIOSAdminScanCode`. The included `hp_bas.py` demonstrates lowercase letter conversion for the platform examined there.

The L70 work in this repository independently traced the password-processing implementation and reconstructed the firmware's own US-English keyboard-layout data to establish case/Shift equivalence.

### libv/hp_bios_passwd_erase

Repository:
https://github.com/libv/hp_bios_passwd_erase

This project catalogs several HP firmware generations and password-storage formats and provides an open-source password-clearing utility for supported systems.

Its README is useful historical context for HP VSS/BiosUser-era systems, but support for any particular machine should not be inferred without verification.

## Tools used during analysis

The reverse-engineering workflow used standard open-source tooling including:

- flashrom, for read-only SPI probing/reads;
- UEFITool / UEFIExtract, for firmware-volume/module extraction;
- GNU objdump, for x86-64 disassembly;
- IFRExtractor-RS, for setup-form inspection;
- Python, for binary parsing and verification;
- Hashcat, for offline SHA-1 candidate testing after the preprocessing format was verified.

No third-party firmware image is required by the tools in this repository.
