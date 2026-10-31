#!/usr/bin/env bash
# Install the reviewed, generic BIOS-research time-budget helper for this user.
# No password search, firmware access, service launch or checkpoint modification.
set -euo pipefail
umask 077

REPOSITORY='https://github.com/spruelllogan/hp-l70-bios-password-research.git'
EXPECTED_HELPER_BLOB='fa3fdabba2eaac0aff6456c687cc7b46586934c3'
EXPECTED_TESTS_BLOB='7896681149ce7d4f783e8e3567e41bc65548065d'
TARGET="$HOME/.local/bin/bios-time-budget"
SOURCE_NOTE="$HOME/.local/share/bios-time-budget/source-commit.txt"

if (( EUID == 0 )); then
  printf 'Run this as your normal user, without sudo.\n' >&2
  exit 2
fi
for program in git python3 mktemp install cmp; do
  command -v "$program" >/dev/null 2>&1 || {
    printf 'Missing required program: %s\n' "$program" >&2
    exit 2
  }
done

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/bios-time-budget.XXXXXXXX")"
trap 'rm -rf -- "$TEMP_DIR"' EXIT

printf 'Fetching public BIOS research timing utility...\n'
git clone --quiet --depth 1 --branch main "$REPOSITORY" "$TEMP_DIR/source"
HELPER="$TEMP_DIR/source/tools/time_budget.py"
TESTS="$TEMP_DIR/source/tests/test_time_budget.py"

# Pin the known-reviewed files. A changed upstream version requires review first.
if [[ "$(git -C "$TEMP_DIR/source" hash-object "$HELPER")" != "$EXPECTED_HELPER_BLOB" ]] ||
   [[ "$(git -C "$TEMP_DIR/source" hash-object "$TESTS")" != "$EXPECTED_TESTS_BLOB" ]]; then
  printf 'The timing helper or tests changed upstream. Installation aborted for review.\n' >&2
  exit 3
fi

printf 'Running offline, synthetic timing tests...\n'
(
  cd "$TEMP_DIR/source"
  python3 -m unittest discover -s tests -p test_time_budget.py -v
  python3 tools/time_budget.py plan 1m --timezone America/Phoenix >/dev/null
)

mkdir -p -- "$HOME/.local/bin" "$(dirname "$SOURCE_NOTE")"
if [[ -e "$TARGET" ]] && ! cmp -s "$HELPER" "$TARGET"; then
  BACKUP="$TARGET.backup.$(date +%Y%m%d-%H%M%S)"
  cp -p -- "$TARGET" "$BACKUP"
  printf 'Existing local timer backed up: %s\n' "$BACKUP"
fi
install -m 0755 -- "$HELPER" "$TARGET"
git -C "$TEMP_DIR/source" rev-parse HEAD > "$SOURCE_NOTE"
chmod 600 "$SOURCE_NOTE"

printf '\nInstalled generic timer: %s\n' "$TARGET"
printf 'Check: python3 "%s" plan 8h --timezone America/Phoenix\n' "$TARGET"
printf 'No CF-54 recovery runner, Hashcat checkpoint, firmware file, or service was changed.\n'
