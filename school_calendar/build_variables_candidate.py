"""Build a review-only Variables piston candidate from a freshly fetched native JSON baseline.

Usage:
    python -m school_calendar.build_variables_candidate live_variables.json > candidate.json

This program never connects to Hubitat, uploads a piston, or executes devices.
Expression functions are NOT yet native-runtime verified. The candidate is for
inspection and preparation validation only; do not deploy it.
"""
import copy
import json
import sys

from school_calendar.native_variables_draft import draft_payload


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
    data = draft_payload()
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
    for minute in (5, 290, None):
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
        action["k"] = []
        for variable, key, vt in (
            ("@SchoolDate", "school_date", "string"),
            ("@School", "school_today", "boolean"),
            ("@SchoolTomorrowDate", "school_tomorrow_date", "string"),
            ("@SchoolTomorrow", "school_tomorrow", "boolean"),
        ):
            task = copy.deepcopy(template)
            task["$"] = uid()
            task["p"][0]["x"] = variable
            task["p"][1] = {
                "t": "e", "e": "REVIEW_ONLY_NATIVE_AST",
                "exp": {"t": "expression", "ok": True, "str": "REVIEW_ONLY_NATIVE_AST", "i": [data[key]]},
                "f": "l", "g": "avg", "vt": vt,
            }
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
