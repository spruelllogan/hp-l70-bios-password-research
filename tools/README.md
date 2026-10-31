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

## Install the generic timing utility on your own machine

The optional [installer](install_time_budget.sh) fetches the public repository, verifies the previously reviewed helper and tests by Git object ID, runs six offline synthetic unit tests, and places a user-local `bios-time-budget` command under `~/.local/bin/`. It requires Git, Python 3, and no administrator access.

```bash
curl -fL --proto '=https' --tlsv1.2 -o /tmp/install-time-budget.sh \
  https://raw.githubusercontent.com/spruelllogan/hp-l70-bios-password-research/main/tools/install_time_budget.sh
bash -n /tmp/install-time-budget.sh
bash /tmp/install-time-budget.sh
python3 ~/.local/bin/bios-time-budget plan 8h --timezone America/Phoenix
```

This **only installs a general timing calculator**; it does not install or update the private CF-54 recovery runner or its checkpoint integration, and it will not start a GPU job.
