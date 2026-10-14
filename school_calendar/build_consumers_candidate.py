"""Review-only School Mornings and Modes candidate builders.

Accept freshly fetched native piston JSON. No network or production writes.
"""
import copy
import json
import sys

from school_calendar.native_variables_draft import function, literal


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _walk(value)


def school_mornings_candidate(baseline):
    p = copy.deepcopy(baseline)
    restrictions = p.get("r")
    if not isinstance(restrictions, list) or len(restrictions) != 2:
        raise ValueError("Unexpected School Mornings restrictions; manual review required")
    if [r.get("lo", {}).get("x") for r in restrictions] != ["@School", "@KidsPresent"]:
        raise ValueError("School Mornings restriction targets changed")
    if any(r.get("co") != "is" for r in restrictions):
        raise ValueError("School Mornings restriction operators changed")
    guard = copy.deepcopy(restrictions[0])
    ids = [n["$"] for n in _walk(p) if isinstance(n.get("$"), int)]
    guard["$"] = max(ids, default=0) + 1
    expression = 'formatDateTime($now, "yyyy-MM-dd")'
    guard["lo"] = {
        "t": "e", "e": expression, "f": "l", "g": "any", "vt": "string",
        "exp": {
            "t": "expression", "str": expression, "ok": True,
            "i": [function("formatdatetime", {"t": "variable", "x": "$now", "ok": True},
                           literal("yyyy-MM-dd"))],
        },
    }
    guard["ro"] = {"t": "x", "x": "@SchoolDate", "f": "l", "g": "any", "vt": "string"}
    p["r"].append(guard)
    return p


def modes_candidate(baseline):
    p = copy.deepcopy(baseline)
    found = []
    for node in _walk(p.get("s", [])):
        if node.get("t") == "x" and node.get("x") == "@School":
            found.append(node)
    if len(found) != 2:
        raise ValueError(f"Expected exactly two Modes @School references; found {len(found)}")
    for node in found:
        node["x"] = "@SchoolTomorrow"
    return p


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("school-mornings", "modes"):
        raise SystemExit("Usage: python -m school_calendar.build_consumers_candidate school-mornings|modes baseline.json")
    with open(sys.argv[2], encoding="utf-8") as f:
        baseline = json.load(f)
    builder = school_mornings_candidate if sys.argv[1] == "school-mornings" else modes_candidate
    print(json.dumps(builder(baseline), indent=2))


if __name__ == "__main__":
    main()

