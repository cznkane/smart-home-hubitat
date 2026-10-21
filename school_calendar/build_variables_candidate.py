"""Build a complete native Variables candidate from a fresh baseline.

No network or live writes. Production requires approved TEST runtime evidence,
reviewed preparation hashes, global type checks, and stale-baseline protection.
"""
import copy
import json
import sys

from school_calendar.native_variables_draft import draft_payload, expression_operand, constant_operand
from school_calendar.webcore_array import closure_array


def candidate(baseline):
    p = copy.deepcopy(baseline)
    if not isinstance(p.get("s"), list):
        raise ValueError("Expected native WebCoRE statements array")
    by_id = {x.get("$"): x for x in p["s"]}
    for required in (7, 10, 13):
        if required not in by_id:
            raise ValueError(f"Unexpected Variables baseline: missing section {required}")
    def target(section):
        actions = section.get("s", [])
        if len(actions) != 1 or len(actions[0].get("k", [])) != 1:
            raise ValueError("Unexpected Variables section action shape")
        return actions[0]["k"][0]
    if target(by_id[7])["p"][0].get("x") != "@School" or target(by_id[10])["p"][0].get("x") != "@School":
        raise ValueError("Seasonal sections no longer target @School; manual review required")
    sample = by_id[13]
    if sample.get("t") != "every" or sample.get("lo2", {}).get("c") != 290:
        raise ValueError("04:50 baseline section changed; manual review required")
    template = target(sample)
    if template.get("c") != "setVariable":
        raise ValueError("Expected setVariable command template")
    variables = p.setdefault("v", [])
    if any(v.get("n") in ("schoolCalendarNow", "schoolCalendarClosures") for v in variables):
        raise ValueError("Calendar local variable name collision")
    variables.extend([
        {"a": "d", "n": "schoolCalendarNow", "t": "datetime"},
        {"a": "s", "n": "schoolCalendarClosures", "t": "string", "v":
         constant_operand(closure_array(), "string")},
    ])
    data = draft_payload("schoolCalendarNow", "schoolCalendarClosures")
    existing_ids = []
    def collect(x):
        if isinstance(x, dict):
            if isinstance(x.get("$"), int):
                existing_ids.append(x["$"])
            for v in x.values():
                collect(v)
        elif isinstance(x, list):
            for v in x:
                collect(v)
    collect(p)
    next_id = max(existing_ids, default=0) + 1
    def uid():
        nonlocal next_id
        n = next_id
        next_id += 1
        return n
    p["s"] = [s for s in p["s"] if s.get("$") not in (7, 10)]
    # Modes starts collecting dusk at 17:30, potentially before solar sunset.
    # A 17:00 recovery refresh prevents relying on sunset to initialize its inputs.
    for minute in (5, 290, 1020, None):
        section = copy.deepcopy(sample)
        section["$"] = uid()
        if minute is None:
            section["lo2"] = {"f": "l", "g": "avg", "s": "sunset", "t": "s", "vt": "time"}
        else:
            section["lo2"]["c"] = minute
            section["lo2"]["exp"] = {
                "t": "expression", "str": str(minute), "ok": True,
                "i": [{"t": "integer", "v": minute, "ok": True}],
            }
        action = copy.deepcopy(sample["s"][0])
        action["$"] = uid()
        anchor = copy.deepcopy(template)
        anchor["$"] = uid()
        anchor["p"][0]["x"] = "schoolCalendarNow"
        anchor["p"][1] = {"t": "x", "x": "$now", "f": "l", "g": "avg", "vt": "datetime"}
        action["k"] = [anchor]
        for variable, key, vt in (
            ("@School", "school_today", "boolean"),
            ("@SchoolDate", "school_date", "string"),
            ("@SchoolTomorrow", "school_tomorrow", "boolean"),
            ("@SchoolTomorrowDate", "school_tomorrow_date", "string"),
        ):
            task = copy.deepcopy(template)
            task["$"] = uid()
            task["p"][0]["x"] = variable
            task["p"][1] = expression_operand(data[key], vt)
            action["k"].append(task)
        section["s"] = [action]
        p["s"].append(section)
    return p


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m school_calendar.build_variables_candidate baseline.json")
    with open(sys.argv[1], encoding="utf-8") as f:
        baseline = json.load(f)
    print(json.dumps(candidate(baseline), indent=2))


if __name__ == "__main__":
    main()

