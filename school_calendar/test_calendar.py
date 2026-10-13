import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from school_calendar.calendar import load_calendar, school_on_day, tomorrow_status, status_pair

DATA = Path(__file__).with_name("academic_2026_2027.json")

class SchoolCalendarTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DATA.read_text())

    def verified(self):
        data = {**self.data, "status": "verified"}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "calendar.json"
            path.write_text(json.dumps(data))
            return load_calendar(path)

    def test_unverified_submission_is_blocked(self):
        data = {**self.data, "status": "provisional"}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "unverified.json"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "not verified"):
                load_calendar(path)

    def test_current_verified_calendar_loads(self):
        self.assertIsNotNone(load_calendar(DATA))

    def test_school_day(self):
        self.assertTrue(school_on_day(date(2026, 10, 14), self.verified()))

    def test_october_break(self):
        self.assertFalse(school_on_day(date(2026, 10, 13), self.verified()))

    def test_weekend(self):
        self.assertFalse(school_on_day(date(2026, 10, 17), self.verified()))

    def test_early_release_still_school(self):
        self.assertTrue(school_on_day(date(2026, 12, 18), self.verified()))
        self.assertTrue(school_on_day(date(2027, 5, 27), self.verified()))

    def test_evening_looks_at_following_day(self):
        data = {**self.data, "status": "verified"}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "calendar.json"
            path.write_text(json.dumps(data))
            result = tomorrow_status(path, datetime(2026, 10, 8, 23, 0, tzinfo=timezone.utc))
            self.assertEqual(result, {"date": "2026-10-09", "school": False})

    def test_status_pair(self):
        data = {**self.data, "status": "verified"}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "calendar.json"
            path.write_text(json.dumps(data))
            result = status_pair(path, datetime(2026, 10, 8, 23, tzinfo=timezone.utc))
            self.assertEqual(result["date"], "2026-10-08")
            self.assertTrue(result["school_today"])
            self.assertFalse(result["school_tomorrow"])

    def test_pair_refuses_uncovered_next_day(self):
        data = {**self.data, "status": "verified"}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "calendar.json"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "does not cover"):
                status_pair(path, datetime(2027, 5, 27, 16, tzinfo=timezone.utc))

    def test_outside_year(self):
        self.assertFalse(school_on_day(date(2027, 6, 1), self.verified()))

if __name__ == "__main__":
    unittest.main()
