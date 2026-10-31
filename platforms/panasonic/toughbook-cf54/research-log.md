# CF-54 research history and corrected-digest test ledger

Dates are **America/Phoenix, 2026**. Aggregate outcomes only. The user's original firmware, real digest, candidates, logs and restore files are kept outside this public repository.

## October 27 — extraction, calibration, and correction

- Preserved an unchanged original **8 MiB ROM** and inspected extracted firmware modules locally with UEFIExtract and disassembly libraries.
- Identified NVAR active and mirrored administrator slots, with blank active user-password slot.
- **Correction:** initial extraction incorrectly XORed the digest-bearing high bytes. Every candidate search performed against that incorrect derived digest is **invalid for the real target** regardless of its size or duration.
- Re-extracted the digest directly from the first 20 high-byte positions, checked the low-byte record template and mirrored slot, and used that corrected value in later work.
- Inspected `S3PeiPassword` to establish its Unicode/16-bit SHA-1 path. A public calibration example called `tsipub` remained unresolved because exact firmware provenance, verifier representation and entry context were not established.
- Corrected-digest dictionary/rule trials and short-pattern trials did not produce a verified candidate.

## October 28 — corrected-digest staged testing

- The on-device, owner-run research script checked original ROM integrity, the corrected verifier, stage argument identities, a single-run lock, restart state, and GPU temperature sensors.
- Investigated and corrected an option-detection pipeline issue and timeout foreground handling.
- `word4digits`, `alnumspace1to8` and `printable1to7` were marked **exhausted** against the **corrected** digest; no recovered candidate.
- Exactly eight ASCII-printable characters (`printable8`) remained partial at the scheduled stop.
- GPU power limits were held at **200 W / 220 W** after thermal concerns; independent telemetry and Hashcat's 83°C cutoff remained in place.

## October 29–31 — saved checkpoint continuations

- The eight-character stage advanced from roughly 12% to 35%, then around 82%, using preserved checkpoints across separate approved sessions.
- **October 31, 04:05:** `printable8` **exhausted** with zero matches. Together with the previous completed stages, the configured 1–8-character ASCII-printable spaces were exhausted for the chosen corrected digest/transform.
- **October 31, 04:05:** began `alnumspace9` (exactly nine characters drawn from letters, digits and space).
- **October 31, 09:00:** `alnumspace9` stopped at a runtime limit, last recorded progress **4.18%**, zero matches, resumable private checkpoint saved.
- Later read-only checks confirmed the job was stopped. Attempts to install a duration-based launcher were blocked; **no such launcher is deployed**.
- A follow-up Setup-engine code trace strengthened the linkage between 16-bit password buffers, SHA-1/0x935B encoding and 64-byte verifier comparison, but did not prove physical F2 acceptance.

## Last verified stage snapshot (2026-10-31, 09:00)

| Stage | Digest version | Result |
| --- | --- | --- |
| Dictionary with four-digit suffix | Corrected | Exhausted; no match |
| 1–8 letters/digits/spaces | Corrected | Exhausted; no match |
| 1–7 ASCII-printable | Corrected | Exhausted; no match |
| Exactly 8 ASCII-printable | Corrected | **Exhausted**; no match |
| Exactly 9 letters/digits/spaces | Corrected | **Partial: 4.18%;** checkpoint saved |

Stages can overlap, so do **not** add their raw candidate counts as though all were unique. Exhaustion is conditional on the hash representation and entry assumptions being correct. The ongoing nine-character search is not proof the actual F2 password has nine characters.

**Outcome: no verified plaintext recovered, no physical BIOS acceptance.** This file is not a real-time process monitor.
