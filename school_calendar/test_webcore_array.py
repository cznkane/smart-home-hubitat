"""Regression checks for delimiter-safe WebCoRE closure array draft."""
import unittest
from datetime import date, timedelta
from school_calendar.calendar import load_calendar, school_on_day
from school_calendar.webcore_array import DATA, closure_array, is_closed
from school_calendar.generate_webcore_dates import generate


class ClosureArrayTests(unittest.TestCase):
    def test_all_days_match_canonical(self):
        cal = load_calendar(DATA)
        generated = generate(DATA)
        arr = closure_array()
        day = date.fromisoformat(generated["first_day"])
        end = date.fromisoformat(generated["last_day"])
        while day <= end:
            expected = school_on_day(day, cal)
            actual = (day.weekday() < 5
                      and not is_closed(day, arr))
            self.assertEqual(expected, actual, day.isoformat())
            day += timedelta(days=1)

    def test_membership_is_delimiter_safe(self):
        arr = closure_array()
        self.assertTrue(is_closed(date(2026, 10, 13), arr))
        self.assertFalse(is_closed(date(2026, 10, 14), arr))
        self.assertNotIn("|2026-10-1|", arr)

    def test_early_release_is_school_day(self):
        arr = closure_array()
        self.assertFalse(is_closed(date(2026, 12, 18), arr))
        self.assertFalse(is_closed(date(2027, 5, 27), arr))


if __name__ == "__main__":
    unittest.main()

