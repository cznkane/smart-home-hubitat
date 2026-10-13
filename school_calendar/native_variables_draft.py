"""Construct a review-only native WebCoRE calendar expression AST.

This generates an expression payload, NOT a complete or deployable piston.
Native parser shapes for contains/concat/formatdatetime/$now were captured from
the isolated TEST piston. adddays/weekdayname/isbetween/if shapes are inferred
from the language DB and MUST be checked in the editor before production use.
"""
from datetime import date
from school_calendar.webcore_array import closure_array


def literal(value):
    return {"t": "string", "v": value, "ok": True}


def integer(value):
    return {"t": "integer", "v": value, "ok": True}


def function(name, *args):
    return {"t": "function", "n": name.lower(), "ok": True,
            "i": [{"t": "expression", "ok": True, "i": [arg]} for arg in args]}


def local_date(tomorrow=False):
    now = {"t": "variable", "x": "$now", "ok": True}
    when = function("adddays", now, integer(1)) if tomorrow else now
    return function("formatdatetime", when, literal("yyyy-MM-dd"))


def school_expression(tomorrow=False):
    day = local_date(tomorrow)
    when = (function("adddays", {"t": "variable", "x": "$now", "ok": True},
                     integer(1)) if tomorrow
            else {"t": "variable", "x": "$now", "ok": True})
    closed = function("contains", literal(closure_array()),
                      function("concat", literal("|"), day, literal("|")))
    weekday = function("contains", literal("|Monday|Tuesday|Wednesday|Thursday|Friday|"),
                       function("concat", literal("|"),
                                function("weekdayname", when), literal("|")))
    # The next three function signatures require native editor verification.
    return function("if",
                    function("isbetween", day, literal("2026-08-12"), literal("2027-05-27")),
                    function("if", weekday,
                             function("if", closed, literal("false"), literal("true")),
                             literal("false")),
                    literal("false"))


def draft_payload():
    return {
        "review_only": True,
        "requires_native_editor_confirmation": ["adddays", "weekdayname", "isbetween", "if"],
        "school_today": school_expression(False),
        "school_tomorrow": school_expression(True),
        "school_date": local_date(False),
        "school_tomorrow_date": local_date(True),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(draft_payload(), indent=2))
