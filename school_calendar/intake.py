"""Validate a ChatGPT-interpreted academic calendar before publishing to Git."""
import json
from datetime import date
from pathlib import Path

REQUIRED = {"schema_version", "status", "district", "timezone", "source", "first_day", "last_day", "closures", "early_release"}

def validate_submission(payload):
    if not isinstance(payload, dict) or REQUIRED - payload.keys():
        raise ValueError("Missing required calendar fields")
    if payload["schema_version"] != 1 or payload["district"] != "Leander ISD":
        raise ValueError("Unexpected calendar identity")
    if payload["timezone"] != "America/Chicago":
        raise ValueError("Unexpected timezone")
    if payload["status"] != "verified":
        raise ValueError("Only verified calendar submissions can be accepted")
    if payload["source"] != "https://www.leanderisd.org/calendar/":
        raise ValueError("Unexpected source")
    start = date.fromisoformat(payload["first_day"])
    end = date.fromisoformat(payload["last_day"])
    if not 150 <= (end - start).days <= 340:
        raise ValueError("Implausible academic year")
    if not isinstance(payload["closures"], list) or len(payload["closures"]) < 5:
        raise ValueError("Suspiciously few closure ranges")
    if not isinstance(payload["early_release"], list):
        raise ValueError("Invalid early release dates")
    seen = set()
    for item in payload["closures"]:
        if not isinstance(item, dict) or not item.get("reason"):
            raise ValueError("Closure requires a reason")
        a = date.fromisoformat(item["start"])
        b = date.fromisoformat(item.get("end", item["start"]))
        if a > b or a < start or b > end:
            raise ValueError("Invalid closure range")
        for n in range(a.toordinal(), b.toordinal() + 1):
            if n in seen:
                raise ValueError("Overlapping closure ranges")
            seen.add(n)
    for value in payload["early_release"]:
        day = date.fromisoformat(value)
        if day < start or day > end or day.toordinal() in seen or day.weekday() >= 5:
            raise ValueError("Invalid early release date")
    provenance = payload.get("provenance")
    if not isinstance(provenance, dict) or not provenance.get("retrieved_at") or not provenance.get("academic_calendar_url"):
        raise ValueError("Missing source provenance")
    return payload

def validate_file(path):
    return validate_submission(json.loads(Path(path).read_text(encoding="utf-8")))
