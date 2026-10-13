import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from calendar import monthrange

from school_calendar.calendar import load_calendar, school_on_day

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

    def test_provisional_is_blocked(self):
        with self.assertRaisesRegex(ValueError, "not verified"):
            load_calendar(DATA)

    def test_school_day(self):
        self.assertTrue(school_on_day(date(2026, 10, 14), self.verified()))

    def test_october_break(self):
        self.assertFalse(school_on_day(date(2026, 10, 13), self.verified()))

    def test_weekend(self):
        self.assertFalse(school_on_day(date(2026, 10, 17), self.verified()))

    def test_early_release_still_school(self):
        self.assertTrue(school_on_day(date(2026, 12, 18), self.verified()))
        self.assertTrue(school_on_day(date(2027, 5, 27), self.verified()))

    def test_outside_year(self):
        self.assertFalse(school_on_day(date(2027, 6, 1), self.verified()))

if __name__ == "__main__":
    unittest.main()
