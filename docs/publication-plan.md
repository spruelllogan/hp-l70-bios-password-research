# Publication and expansion checklist

**This GitHub repository is already public.** Original HP L70 research was published earlier; every new platform must pass a fresh privacy/evidence review.

## Checks before publishing additions

- [ ] No original SPI/BIOS/EFI/NVRAM image or proprietary binary tracked.
- [ ] No actual credential, real digest, private verifier bytes, password, key sequence, Hashcat pot/restore file or raw candidate set.
- [ ] No serial, MAC, UUID, asset tag, credential token or private access path.
- [ ] No unreviewed terminal logs or screenshots.
- [ ] Claims scoped to the exact vendor/model/firmware revision and evidence level.
- [ ] Prior extraction mistakes and invalidated searches explicitly documented.
- [ ] Synthetic tests (if included) work without any private machine data.
- [ ] Final diff and relevant Git history reviewed.
- [ ] Existing HP documentation links preserved.

## Verified publication status

- **HP ZBook 17 / L70 01.08:** owner recovery **physically verified**; sanitized code research, tool and synthetic verifier published; later official BIOS update to 01.47 confirmed. No private password or digest.
- **Panasonic CF-54 Mk2 / AMI V2.20L20:** ongoing code-level research, corrected digest-record interpretation and dated aggregate search ledger only. **No successful plaintext recovery or physical F2 acceptance.**

GitHub is the canonical source for **sanitized research**, not raw machine state. Keep manufacturer-specific findings separate; upstream community sharing is optional and must accurately report limits.
