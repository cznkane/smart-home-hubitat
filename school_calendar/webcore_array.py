"""Generate delimiter-safe closure lookup expressions for the WebCoRE draft.

Produces expression text for native WebCoRE review, NOT a deployable piston AST.
"""
from datetime import date
from pathlib import Path
from school_calendar.generate_webcore_dates import generate

DATA = Path(__file__).with_name("academic_2026_2027.json")


def closure_array(path=DATA):
    dates = generate(path)["closed_weekdays"]
    if any("|" in value for value in dates):
        raise ValueError("Unexpected delimiter in closure date")
    return "|" + "|".join(dates) + "|"


def is_closed(day, array):
    if not isinstance(day, date):
        raise TypeError("day must be a date")
    return "|" + day.isoformat() + "|" in array


def draft():
    data = generate(DATA)
    return {
        "first_day": data["first_day"],
        "last_day": data["last_day"],
        "closure_array": closure_array(),
        "membership_pattern": "|YYYY-MM-DD|",
        "note": "Use exact delimited membership; native WebCoRE expression AST must be verified separately.",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(draft(), indent=2))
