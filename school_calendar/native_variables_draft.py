"""Native expression builder with matching text and AST.

Parser grammar is checked against upstream dashboard source. Runtime certification
is separate: execute the approved device-free TEST matrix before production.
"""
import json
from school_calendar.webcore_array import closure_array, DATA
from school_calendar.generate_webcore_dates import generate


def literal(value):
    return {"t": "string", "v": value, "ok": True}


def boolean(value):
    return {"t": "boolean", "v": "true" if value else "false", "ok": True}


def integer(value):
    return {"t": "integer", "v": value, "ok": True}


def function(name, *args):
    return {"t": "function", "n": name.lower(), "ok": True,
            "i": [{"t": "expression", "ok": True, "i": [arg]} for arg in args]}


def local_date(tomorrow=False, now_name="$now"):
    now = {"t": "variable", "x": now_name, "ok": True}
    when = function("adddays", now, integer(1)) if tomorrow else now
    return function("formatdatetime", when, literal("yyyy-MM-dd"))


def school_expression(tomorrow=False, now_name="$now", closure_name=None):
    data = generate(DATA)
    day = local_date(tomorrow, now_name)
    when = (function("adddays", {"t": "variable", "x": now_name, "ok": True},
                     integer(1)) if tomorrow
            else {"t": "variable", "x": now_name, "ok": True})
    closures = ({"t": "variable", "x": closure_name, "ok": True}
                if closure_name else literal(closure_array()))
    closed = function("contains", closures,
                      function("concat", literal("|"), day, literal("|")))
    weekday = function("contains", literal("|Monday|Tuesday|Wednesday|Thursday|Friday|"),
                       function("concat", literal("|"),
                                function("weekdayname", when), literal("|")))
    # Signatures and string comparison semantics were inspected in upstream Groovy.
    # On-hub evaluation remains a mandatory release gate.
    return function("if",
                    function("isbetween", day, literal(data["first_day"]), literal(data["last_day"])),
                    function("if", weekday,
                             function("if", closed, boolean(False), boolean(True)),
                             boolean(False)),
                    boolean(False))


def expression_text(node):
    """Render exactly the small native expression grammar emitted by this builder."""
    kind = node["t"]
    if kind == "expression":
        if len(node["i"]) != 1:
            raise ValueError("Only single-node argument expressions are supported")
        return expression_text(node["i"][0])
    if kind == "function":
        return node["n"] + "(" + ", ".join(expression_text(a) for a in node["i"]) + ")"
    if kind == "variable":
        return node["x"]
    if kind == "string":
        return json.dumps(node["v"])
    if kind == "boolean":
        return node["v"]
    if kind == "integer":
        return str(node["v"])
    raise ValueError(f"Unsupported native node: {kind}")


def expression_operand(node, vt, grouping="avg"):
    text = expression_text(node)
    return {"t": "e", "e": text, "exp": {"t": "expression", "ok": True,
            "str": text, "i": [node]}, "f": "l", "g": grouping, "vt": vt}


def constant_operand(value, vt):
    node = boolean(value) if isinstance(value, bool) else (integer(value) if isinstance(value, int) else literal(value))
    text = expression_text(node)
    return {"t": "c", "c": node["v"], "exp": {"t": "expression", "ok": True,
            "str": text, "i": [node]}, "f": "l", "g": "avg", "vt": vt}


def draft_payload(now_name="$now", closure_name=None):
    return {
        "review_only": True,
        "requires_runtime_confirmation": ["adddays", "weekdayname", "isbetween", "if"],
        "school_today": school_expression(False, now_name, closure_name),
        "school_tomorrow": school_expression(True, now_name, closure_name),
        "school_date": local_date(False, now_name),
        "school_tomorrow_date": local_date(True, now_name),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(draft_payload(), indent=2))

