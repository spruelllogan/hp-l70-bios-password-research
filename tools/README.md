# Existing research tools

These scripts are **HP L70-specific**; they must not be interpreted as Panasonic AMI implementations.

- [extract_l70_mapping.py](extract_l70_mapping.py) — read-only reconstruction of the HP L70 layout table from a user-provided firmware module.
- [verify_synthetic.py](verify_synthetic.py) — synthetic verification of HP L70 physical-key mapping and SHA-1 processing.

The Panasonic [CF-54 research](../platforms/panasonic/toughbook-cf54/README.md) currently publishes **documentation only**, not private firmware or executable password-search tooling.

## Generic duration-budget utility

[time_budget.py](time_budget.py) is a **read-only and non-launching** elapsed-time helper shared across projects. It validates durations such as `90m`, `8h`, `12h`, and `1d` (maximum 24 hours) and calculates an epoch deadline based on **invocation time**.

```bash
python3 tools/time_budget.py plan 8h --timezone America/Phoenix
python3 tools/time_budget.py remaining 1800043200
python3 -m unittest discover -s tests -v
```

The helper does not run Hashcat, alter checkpoints, access private credentials, or restart the recovery service. It is **not** a deployed CF-54 duration-based recovery launcher. See [CF-54 runtime design](../platforms/panasonic/toughbook-cf54/runtime-design.md) for the incomplete integration requirements.
