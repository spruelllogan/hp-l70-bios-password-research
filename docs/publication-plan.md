# Publication plan

The repository should remain private until the final scrub checklist is complete.

## Before changing visibility

Confirm all of the following:

- [ ] no complete SPI/BIOS/EFI/SoftPaq binary is tracked;
- [ ] no serial number, UUID, MAC address, asset tag, or account token is present;
- [ ] the research machine's real administrator-password digest is absent;
- [ ] the recovered password and exact recovered physical-key sequence are absent;
- [ ] no Hashcat potfile, restore file, or raw candidate list is tracked;
- [ ] all terminal transcripts have been manually reviewed;
- [ ] all claims distinguish "verified on L70 01.08" from broader HP assumptions;
- [ ] the synthetic verifier runs successfully;
- [ ] the keyboard-map extractor is read-only;
- [ ] repository history is checked, not only the current working tree.

## Canonical publication

GitHub should be the canonical source so corrections, tooling, and additional verified platforms can be versioned in one place.

Suggested repository description:

> Reverse engineering and read-only recovery research for HP L70 BIOS administrator password handling.

## Upstream notification

After the repository is public, open an issue with:

https://github.com/libv/hp_bios_passwd_erase

Suggested title:

> HP ZBook 17 / L70 01.08: HP_BIOSAdminScanCode preprocessing and keyboard mapping

Suggested short body:

> I documented an independently verified HP ZBook 17 / L70 01.08 administrator-password path. The firmware converts UTF-16 input through the embedded US-English keyboard layout to one physical-key byte per character and then SHA-1 hashes that byte sequence into HP_BIOSAdminScanCode. Shift/case variants on the same physical key collapse before hashing. The repository includes a read-only parser, synthetic verification, offsets/call-chain notes, and sanitized checksums, but no firmware dumps or real credential material.
>
> Repository: <PUBLIC_REPOSITORY_URL>
>
> I am posting this in case the format/reproduction notes are useful for expanding the HP generation matrix.

## Firmware-community cross-post

A concise technical post can also be made to a BIOS/UEFI repair or firmware-research forum.

Suggested title:

> HP ZBook 17 L70 01.08 BIOS administrator-password hashing: physical-key mapping + SHA-1

Suggested opening:

> I reverse engineered the administrator-password path in HP L70 01.08 while recovering an owned ZBook 17. The notable behavior is that the visible UTF-16 password is first converted through HP's embedded US-English keyboard layout to one byte per physical key, then SHA-1 hashed. This makes Shift/case variants on the same key indistinguishable in the stored HP_BIOSAdminScanCode value. I published the call chain, layout reconstruction, synthetic verifier, and a read-only parser here: <PUBLIC_REPOSITORY_URL>.

Avoid attaching firmware dumps or machine-specific NVRAM data to forum posts.

## Reddit

Reddit is optional and is not part of the initial publication plan. A terminal/API client does not make a Reddit account anonymous; account and platform metadata still exist. The GitHub repository plus relevant firmware communities should be sufficient for discoverability.
