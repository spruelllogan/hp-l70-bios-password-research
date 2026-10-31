#!/usr/bin/env python3
"""Generic elapsed-time budget helper (no process launching or file writes).

Run this at the START of an approved work session, not when queuing it.
It deliberately does not control password searches or edit application checkpoints.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import sys
import time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MAX_BUDGET_SECONDS = 24 * 60 * 60
_UNITS = {"m": 60, "h": 3600, "d": 86400}
_DURATION_RE = re.compile(r"^([1-9][0-9]*)([mhd])$")


def parse_duration(spec: str) -> int:
    """Return duration in seconds, accepting 1m through 24h inclusive."""
    match = _DURATION_RE.fullmatch(spec)
    if match is None:
        raise ValueError("duration must look like 90m, 8h, or 1d")
    try:
        seconds = int(match.group(1)) * _UNITS[match.group(2)]
    except ValueError as exc:
        raise ValueError("invalid duration number") from exc
    if not 60 <= seconds <= MAX_BUDGET_SECONDS:
        raise ValueError("duration must be between 1 minute and 24 hours")
    return seconds


def plan_budget(spec: str, *, started_epoch: int | None = None, tz_name: str = "UTC") -> dict:
    """Compute a deadline relative to the session's actual start timestamp."""
    seconds = parse_duration(spec)
    try:
        tz = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown timezone: {tz_name}") from exc
    started = int(time.time()) if started_epoch is None else int(started_epoch)
    if started < 0:
        raise ValueError("start time cannot be negative")
    deadline = started + seconds
    return {
        "duration": spec,
        "duration_seconds": seconds,
        "started_epoch": started,
        "deadline_epoch": deadline,
        "started_local": datetime.fromtimestamp(started, tz).isoformat(),
        "deadline_local": datetime.fromtimestamp(deadline, tz).isoformat(),
        "timezone": tz_name,
    }


def remaining_seconds(deadline_epoch: int, *, now_epoch: int | None = None) -> int:
    """Nonnegative remaining seconds for an existing budget."""
    now = int(time.time()) if now_epoch is None else int(now_epoch)
    return max(0, int(deadline_epoch) - now)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="print a budget starting right now")
    plan.add_argument("duration", help="1m to 24h (e.g., 90m, 8h, 12h, 1d)")
    plan.add_argument("--timezone", default="UTC", help="IANA timezone, e.g., America/Phoenix")
    remaining = commands.add_parser("remaining", help="print seconds left until a saved epoch deadline")
    remaining.add_argument("deadline_epoch", type=int)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            output = plan_budget(args.duration, tz_name=args.timezone)
        else:
            output = {"remaining_seconds": remaining_seconds(args.deadline_epoch)}
    except (ValueError, OverflowError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
