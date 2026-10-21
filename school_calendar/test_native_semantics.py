"""Off-hub regression model of the inspected WebCoRE function implementations.

This is independent calendar-oracle comparison, not certification of Hubitat's
installed Groovy runtime. The device-free TEST matrix remains a release gate.
"""
import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from school_calendar.calendar import load_calendar, school_on_day
from school_calendar.native_variables_draft import local_date, school_expression, expression_text
from school_calendar.webcore_array import DATA

TZ = ZoneInfo("America/Chicago")


def evaluate(node, now):
    kind = node["t"]
    if kind == "expression":
        return evaluate(node["i"][0], now)
    if kind == "variable":
        if node["x"] != "$now":
            raise ValueError(node["x"])
        return now
    if kind == "boolean":
        return node["v"] == "true"
    if kind in ("string", "integer"):
        return node["v"]
    name = node["n"]
    args = node["i"]
    if name == "if":
        return evaluate(args[1 if evaluate(args[0], now) else 2], now)
    values = [evaluate(a, now) for a in args]
    if name == "adddays":
        # Runtime addtimeHelper: epoch delta plus timezone offset correction.
        value, days = values
        result = value.astimezone(timezone.utc) + timedelta(days=days)
        result += value.astimezone(TZ).utcoffset() - result.astimezone(TZ).utcoffset()
        return result
    if name == "formatdatetime":
        value, pattern = values
        assert pattern == "yyyy-MM-dd"
        return value.astimezone(TZ).date().isoformat()
    if name == "weekdayname":
        return values[0].astimezone(TZ).strftime("%A")
    if name == "concat":
        return "".join(values)
    if name == "contains":
        return values[1] in values[0]
    if name == "isbetween":
        return values[1] <= values[0] <= values[2]
    raise ValueError(name)


class NativeSemanticsTests(unittest.TestCase):
    def test_every_date_and_rollover_against_independent_calendar(self):
        calendar = load_calendar(DATA)
        roots = [school_expression(False), school_expression(True)]
        dates = [local_date(False), local_date(True)]
        start = datetime(2026, 7, 1, tzinfo=TZ)
        for offset in range(426):
            for hour, minute in ((0, 5), (4, 50), (17, 30), (23, 59)):
                now = (start + timedelta(days=offset)).replace(hour=hour, minute=minute)
                for tomorrow in (False, True):
                    target = now.date() + timedelta(days=tomorrow)
                    with self.subTest(now=now, tomorrow=tomorrow):
                        actual = evaluate(roots[tomorrow], now)
                        self.assertIs(type(actual), bool)
                        self.assertEqual(actual, school_on_day(target, calendar))
                        self.assertEqual(evaluate(dates[tomorrow], now), target.isoformat())

    def test_utc_crosses_local_midnight(self):
        for stamp, expected in (("2026-10-15T04:59:59+00:00", "2026-10-14"),
                                ("2026-10-15T05:00:00+00:00", "2026-10-15"),
                                ("2027-01-06T05:59:59+00:00", "2027-01-05"),
                                ("2027-01-06T06:00:00+00:00", "2027-01-06")):
            self.assertEqual(evaluate(local_date(), datetime.fromisoformat(stamp)), expected)

    def test_renderer_has_real_text_and_no_placeholder(self):
        for tomorrow in (False, True):
            text = expression_text(school_expression(tomorrow))
            self.assertIn("isbetween(formatdatetime(", text)
            self.assertNotIn("REVIEW_ONLY_NATIVE_AST", text)

