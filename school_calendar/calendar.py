"""Pure, fail-closed Leander ISD academic calendar evaluator (no Hubitat writes)."""
import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chicago")

def load_calendar(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("status") != "verified":
        raise ValueError("Academic calendar is not verified; refuse to publish @School")
    start, end = date.fromisoformat(data["first_day"]), date.fromisoformat(data["last_day"])
    if start > end:
        raise ValueError("Invalid school-year boundaries")
    closures = set()
    for item in data["closures"]:
        a = date.fromisoformat(item["start"])
        b = date.fromisoformat(item.get("end", item["start"]))
        if a > b or a < start or b > end:
            raise ValueError("Invalid closure range")
        closures.update(date.fromordinal(i) for i in range(a.toordinal(), b.toordinal() + 1))
    return start, end, closures

def school_on_day(day, calendar):
    start, end, closures = calendar
    return start <= day <= end and day.weekday() < 5 and day not in closures

def today_status(path, now=None):
    now = now or datetime.now(TZ)
    if now.tzinfo is None:
        raise ValueError("Timezone-aware datetime required")
    day = now.astimezone(TZ).date()
    return {"date": day.isoformat(), "school": school_on_day(day, load_calendar(path))}

def tomorrow_status(path, now=None):
    """School attendance for the next local calendar day, for evening policy."""
    from datetime import timedelta
    now = now or datetime.now(TZ)
    if now.tzinfo is None:
        raise ValueError("Timezone-aware datetime required")
    day = now.astimezone(TZ).date() + timedelta(days=1)
    return {"date": day.isoformat(), "school": school_on_day(day, load_calendar(path))}


def status_pair(path, now=None):
    """Evaluate today and tomorrow from the same validated calendar snapshot."""
    from datetime import timedelta
    now = now or datetime.now(TZ)
    if now.tzinfo is None:
        raise ValueError("Timezone-aware datetime required")
    today = now.astimezone(TZ).date()
    tomorrow = today + timedelta(days=1)
    calendar = load_calendar(path)
    start, end, _ = calendar
    if not start <= today <= end or not start <= tomorrow <= end:
        raise ValueError("Calendar does not cover both dates; refuse publication")
    return {"date": today.isoformat(), "school_today": school_on_day(today, calendar), "tomorrow_date": tomorrow.isoformat(), "school_tomorrow": school_on_day(tomorrow, calendar)}

