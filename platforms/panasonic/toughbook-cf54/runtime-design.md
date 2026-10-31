# CF-54 offline runtime and checkpoint design

**Implementation status:** The current recovery runner remains private on JORIE Main. The requested **duration-based launcher is only a proposal**; it has **not** been installed, committed as executable recovery code, or used to resume the job.

## Existing observed behavior

- Private owner-operated runner validates the original ROM and extracted digest before executing research.
- Stage argument checksums and `.done` markers protect against skipping/repeating exhausted stages accidentally.
- Hashcat `.restore` checkpoint preserves the unfinished stage. A saved checkpoint is neither a match nor a successfully recovered password.
- The runner uses a persistent UNIX-epoch deadline; once expired, relaunching the service exits immediately.
- Hashcat's own runtime may be saved inside the checkpoint arguments. Updating only the outer deadline can leave the inner runtime expired.
- Thermal cutoff is **83°C**, with Hashcat's built-in protection and an independent fail-closed GPU telemetry watchdog; observed GPU power limits are **200 W / 220 W**.
- On October 31 the nine-character stage stopped at **4.18%**. No future session was started during documentation work.

## Proposed elapsed-duration interface

A future session should accept an explicitly approved **duration** (e.g., 8h or 12h) and calculate its cutoff **when the service actually starts**, not when the operator enters a calendar date or adds the job to a queue.

Acceptance requirements:

1. No implicit auto-resume; each continuation requires explicit authorization.
2. Validate and cap durations; refuse concurrent sessions.
3. Back up the exact checkpoint and metadata before any adjustment; never reset completed stages.
4. Keep the independent wall-clock cutoff and checkpointed inner runtime consistent.
5. Preserve immutable original firmware, per-stage identity checks, 83°C safeguards and GPU power limits.
6. Record actual start time, requested duration, stop reason and aggregate progress, without logging secrets.
7. Stop on timeout, exhaustion, verified digest match or telemetry/thermal fault. BIOS acceptance must still be tested physically.

This public project documents the design and known pitfalls. **It does not contain a machine-specific cracking script, raw hash, checkpoint, service launcher, or remote deployment pipeline.**
