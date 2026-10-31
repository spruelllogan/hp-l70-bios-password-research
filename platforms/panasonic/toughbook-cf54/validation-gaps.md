# CF-54 remaining validation questions

A candidate has **not** been recovered or accepted in the physical F2 BIOS Setup prompt.

## Physical F2 keystroke-to-verifier chain

**Observed:** S3PeiPassword hashes 16-bit input; MiscFunc widens ASCII input to 16-bit words; Aptio Setup calls an encoder and compares a 64-byte verifier.

**Not fully proven:** earlier physical-key-to-Unicode conversion, possible normalization, administrator versus user role selection, and correspondence to the active `AMITSESetup` slot. A static code link is stronger than a guess but not proof of end-to-end F2 acceptance.

## Public example discrepancy

An earlier public CF-54 example labeled `tsipub` did not reproduce the reported stored value under the simple UTF-16LE transform. The example's matching firmware revision, actual stored-record extraction and password-entry context are unverified. Keep this discrepancy open; don't use that external sample to declare success or invalidate the exact owner's ROM.

## Character constraints and search coverage

The reference manual describes alphanumeric characters and spaces, with length up to 32 and case sensitivity. Some lower-level firmware helpers allow broader ASCII-printable input. These may be distinct interfaces or validation layers.

Correctly exhausting ASCII-printable lengths 1–8 **only** establishes no matching candidate was found for the chosen digest and transform within that tested space. It does not prove the actual F2 password is longer than eight characters.

## Corrected verifier provenance

A historical XOR-based extraction was wrong. **Only corrected-digest test runs count** toward evaluating this supervisor record. Archive summaries must distinguish them explicitly.

## Future priorities

Obtain an owner-authorized **matching-firmware known-password calibration** or complete a static end-to-end F2 event-to-credential comparison trace without writing firmware. Recheck assumptions before treating more GPU time as definitive proof.

The private nine-character restore checkpoint (4.18% at the 2026-10-31 cutoff) must never be uploaded to this repository.
