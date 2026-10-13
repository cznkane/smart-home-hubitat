"""Check generated closure lookup against canonical evaluator."""
import unittest
from datetime import date, timedelta
from pathlib import Path
from school_calendar.calendar import load_calendar, school_on_day
from school_calendar.generate_webcore_dates import generate, is_school_day

DATA = Path(__file__).with_name("academic_2026_2027.json")


class WebcoreDatesTests(unittest.TestCase):
    def test_all_days_match(self):
        generated = generate(DATA)
        calendar = load_calendar(DATA)
        day = date.fromisoformat(generated["first_day"])
        end = date.fromisoformat(generated["last_day"])
        while day <= end:
            self.assertEqual(is_school_day(day, generated),
                             school_on_day(day, calendar), day.isoformat())
            day += timedelta(days=1)

    def test_early_release_remains_school(self):
        generated = generate(DATA)
        for value in generated["early_release"]:
            self.assertTrue(is_school_day(date.fromisoformat(value), generated))

    def test_outside_year_is_false(self):
        generated = generate(DATA)
        self.assertFalse(is_school_day(date(2027, 5, 28), generated))
        self.assertFalse(is_school_day(date(2026, 8, 11), generated))
