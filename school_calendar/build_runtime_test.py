"""Build device-free TEST bodies for explicit approval, never upload or execute.

Only local setVariable and console log commands. No globals, devices, schedules,
HTTP or other pistons. Each native assertion logs PASS or FAIL with actual values.
"""
import copy
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from school_calendar.calendar import load_calendar, school_on_day
from school_calendar.generate_webcore_dates import generate
from school_calendar.native_variables_draft import (
    constant_operand, draft_payload, expression_operand, function, literal,
)
from school_calendar.webcore_array import DATA, closure_array

TZ = ZoneInfo("America/Chicago")


def cases():
    data = generate(DATA)
    dates = set(data["closed_weekdays"])
    dates.update(("2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14",
                  "2026-08-15", "2026-08-16", "2026-08-17", "2026-12-18",
                  "2026-12-31", "2027-01-01", "2027-01-05", "2027-05-26",
                  "2027-05-27", "2027-05-28", "2027-08-12"))
    stamps = {day + "T12:00:00" for day in dates}
    stamps.update(("2026-10-08T23:59:59", "2026-10-14T00:00:00",
                   "2026-10-14T04:50:00", "2026-10-14T17:30:00",
                   "2026-10-14T23:59:59", "2026-10-15T00:00:00",
                   "2026-10-31T23:59:59", "2026-11-01T00:05:00",
                   "2026-11-01T01:30:00", "2026-11-01T23:59:59",
                   "2027-03-13T23:59:59", "2027-03-14T00:05:00",
                   "2027-03-14T01:30:00", "2027-03-14T03:30:00",
                   "2027-03-14T23:59:59"))
    calendar = load_calendar(DATA)
    result = []
    for stamp in sorted(stamps):
        now = datetime.fromisoformat(stamp).replace(tzinfo=TZ)
        day = now.date()
        tomorrow = day + timedelta(days=1)
        result.append({"label": now.isoformat(), "epoch": int(now.timestamp() * 1000),
                       "date": day.isoformat(), "school": school_on_day(day, calendar),
                       "tomorrow_date": tomorrow.isoformat(),
                       "tomorrow_school": school_on_day(tomorrow, calendar)})
    # Repeated autumn hour, second occurrence.
    now = datetime(2026, 11, 1, 1, 30, tzinfo=TZ, fold=1)
    result.append({"label": now.isoformat(), "epoch": int(now.timestamp() * 1000),
                   "date": "2026-11-01", "school": False,
                   "tomorrow_date": "2026-11-02", "tomorrow_school": False})
    return result


def variable_operand(name, vt):
    return {"t": "x", "x": name, "f": "l", "g": "avg", "vt": vt}


def candidate(baseline, selected, include_freshness=False):
    p = copy.deepcopy(baseline)
    p.update(r=[], rn=False, rop="and", s=[], v=[])
    p["v"] = [{"a": "s", "n": "schoolCalendarClosures", "t": "string",
               "v": constant_operand(closure_array(), "string")}] + [
        {"a": "d", "n": name, "t": vt} for name, vt in (
            ("schoolCalendarNow", "datetime"), ("actualToday", "boolean"),
            ("actualTomorrow", "boolean"), ("actualDate", "string"),
            ("actualTomorrowDate", "string"), ("testSchool", "boolean"),
            ("testKids", "boolean"), ("testStamp", "string"), ("freshnessPassed", "boolean"))]
    next_id = 1
    def uid():
        nonlocal next_id
        value = next_id
        next_id += 1
        return value
    def action(tasks):
        return {"$": uid(), "t": "action", "a": "0", "d": [], "k": tasks,
                "r": [], "rop": "and", "tcp": "c"}
    def set_value(name, value):
        return {"$": uid(), "c": "setVariable",
                "p": [variable_operand(name, "variable"), value]}
    def log(node):
        return action([{"$": uid(), "c": "log", "p": [constant_operand("info", "enum"),
                       expression_operand(node, "string"), constant_operand(False, "boolean")]}])
    expressions = draft_payload("schoolCalendarNow", "schoolCalendarClosures")
    for case in selected:
        tasks = [set_value("schoolCalendarNow", constant_operand(case["epoch"], "datetime"))]
        comparisons = []
        for name, key, expected, vt in (
            ("actualToday", "school_today", case["school"], "boolean"),
            ("actualDate", "school_date", case["date"], "string"),
            ("actualTomorrow", "school_tomorrow", case["tomorrow_school"], "boolean"),
            ("actualTomorrowDate", "school_tomorrow_date", case["tomorrow_date"], "string")):
            tasks.append(set_value(name, expression_operand(expressions[key], vt)))
            comparisons.append({"$": uid(), "t": "condition", "ct": "c", "co": "is",
                "lo": variable_operand(name, vt), "ro": constant_operand(expected, vt),
                "ro2": {"t": "c", "g": "any"}, "to": {"t": "c", "g": "any"},
                "to2": {"t": "c", "g": "any"}, "s": False, "sm": "never", "fs": [], "ts": []})
        p["s"].append(action(tasks))
        actuals = [{"t": "variable", "x": name, "ok": True} for name in
                   ("actualToday", "actualDate", "actualTomorrow", "actualTomorrowDate")]
        fail = function("concat", literal("FAIL|" + case["label"] + "|"),
                        actuals[0], literal("|"), actuals[1], literal("|"),
                        actuals[2], literal("|"), actuals[3])
        p["s"].append({"$": uid(), "t": "if", "a": "0", "c": comparisons, "o": "and",
                       "s": [log(literal("PASS|" + case["label"]))], "e": [log(fail)],
                       "ei": [], "r": [], "rop": "and", "tcp": "c"})
    if include_freshness:
        now = datetime(2026, 10, 14, 5, tzinfo=TZ)
        for school in (False, True):
            for kids in (False, True):
                for stamp in ("2026-10-14", "2026-10-13", "2026-10-15", ""):
                    label = f"freshness|school={school}|kids={kids}|stamp={stamp}"
                    p["s"].append(action([set_value(name, constant_operand(value, vt)) for name, value, vt in (
                        ("schoolCalendarNow", int(now.timestamp()*1000), "datetime"),
                        ("testSchool", school, "boolean"), ("testKids", kids, "boolean"),
                        ("testStamp", stamp, "string"), ("freshnessPassed", False, "boolean"))]))
                    gate = action([set_value("freshnessPassed", constant_operand(True, "boolean"))])
                    # Same native top-level AND restrictions as School Mornings,
                    # applied to a device-free action; third restriction uses date expression.
                    for name, expected in (("testSchool", True), ("testKids", True)):
                        gate["r"].append({"$": uid(), "t": "restriction", "co": "is",
                            "lo": variable_operand(name, "boolean"), "ro": constant_operand(expected, "boolean"),
                            "ro2": {"t": "c", "g": "any"}, "to": {"t": "c", "g": "any"},
                            "to2": {"t": "c", "g": "any"}})
                    gate["r"].append({"$": uid(), "t": "restriction", "co": "is",
                        "lo": expression_operand(expressions["school_date"], "string", "any"),
                        "ro": variable_operand("testStamp", "string"), "ro2": {"t": "c", "g": "any"},
                        "to": {"t": "c", "g": "any"}, "to2": {"t": "c", "g": "any"}})
                    p["s"].append(gate)
                    expected = school and kids and stamp == "2026-10-14"
                    check = {"$": uid(), "t": "condition", "ct": "c", "co": "is",
                        "lo": variable_operand("freshnessPassed", "boolean"),
                        "ro": constant_operand(expected, "boolean"), "ro2": {"t": "c", "g": "any"},
                        "to": {"t": "c", "g": "any"}, "to2": {"t": "c", "g": "any"},
                        "s": False, "sm": "never", "fs": [], "ts": []}
                    p["s"].append({"$": uid(), "t": "if", "a": "0", "c": [check], "o": "and",
                        "s": [log(literal("PASS|" + label))], "e": [log(literal("FAIL|" + label))],
                        "ei": [], "r": [], "rop": "and", "tcp": "c"})
    return p
