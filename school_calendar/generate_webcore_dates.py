"""Generate a compact annual closure lookup for a WebCoRE piston draft.

This module emits data, not an unverified native WebCoRE condition body.
"""
import argparse
import json
from datetime import date, timedelta
from pathlib import Path
from school_calendar.intake import validate_file


def generate(path):
    data = validate_file(path)
    first, last = date.fromisoformat(data["first_day"]), date.fromisoformat(data["last_day"])
    closed = set()
    for item in data["closures"]:
        day = date.fromisoformat(item["start"])
        end = date.fromisoformat(item.get("end", item["start"]))
        while day <= end:
            closed.add(day)
            day += timedelta(days=1)
    # Only weekday closure dates matter; weekends are excluded by the evaluator.
    days = sorted(d.isoformat() for d in closed if d.weekday() < 5)
    return {"year": first.year, "first_day": first.isoformat(),
            "last_day": last.isoformat(), "closed_weekdays": days,
            "early_release": data["early_release"]}


def is_school_day(day, generated):
    if not isinstance(day, date):
        raise TypeError("day must be a date")
    return (generated["first_day"] <= day.isoformat() <= generated["last_day"]
            and day.weekday() < 5
            and day.isoformat() not in generated["closed_weekdays"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("calendar", type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.calendar), indent=2))


if __name__ == "__main__":
    main()
