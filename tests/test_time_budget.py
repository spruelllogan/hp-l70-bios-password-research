"""No private device data: deterministic tests for generic duration arithmetic."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from time_budget import parse_duration, plan_budget, remaining_seconds


class DurationTests(unittest.TestCase):
    def test_supported_durations(self):
        self.assertEqual(parse_duration("1m"), 60)
        self.assertEqual(parse_duration("90m"), 5400)
        self.assertEqual(parse_duration("8h"), 28800)
        self.assertEqual(parse_duration("12h"), 43200)
        self.assertEqual(parse_duration("24h"), 86400)
        self.assertEqual(parse_duration("1d"), 86400)

    def test_invalid_or_excessive_durations(self):
        for bad in ("", "0m", "30s", "25h", "2d", "08h", "1.5h", "8 hours", "-1h", " 8h", "8h "):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_duration(bad)

    def test_session_deadline_uses_actual_start(self):
        first = plan_budget("12h", started_epoch=1800000000)
        later = plan_budget("12h", started_epoch=1800003600)
        self.assertEqual(first["deadline_epoch"], 1800043200)
        self.assertEqual(later["deadline_epoch"], first["deadline_epoch"] + 3600)

    def test_elapsed_duration_is_independent_of_local_clock(self):
        # US daylight-saving transition: 24h elapsed need not equal one local clock day.
        first = plan_budget("1d", started_epoch=1793511000, tz_name="America/New_York")
        self.assertEqual(first["deadline_epoch"] - first["started_epoch"], 86400)

    def test_arizona_local_time_and_remaining(self):
        result = plan_budget("90m", started_epoch=1793511000, tz_name="America/Phoenix")
        self.assertTrue(result["started_local"].endswith("-07:00"))
        self.assertEqual(remaining_seconds(result["deadline_epoch"], now_epoch=result["started_epoch"]), 5400)
        self.assertEqual(remaining_seconds(result["deadline_epoch"], now_epoch=result["deadline_epoch"] + 1), 0)

    def test_invalid_timezone(self):
        with self.assertRaises(ValueError):
            plan_budget("1h", started_epoch=1800000000, tz_name="Nowhere/Unknown")


if __name__ == "__main__":
    unittest.main()
