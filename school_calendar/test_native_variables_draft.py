"""Structural regression checks for review-only Variables AST generation.

These checks do not certify Hubitat runtime semantics.
"""
import unittest
from school_calendar.native_variables_draft import (
    draft_payload, function, local_date, school_expression,
)
from school_calendar.webcore_array import closure_array


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from walk(item)


class NativeDraftTests(unittest.TestCase):
    def test_all_four_outputs_exist(self):
        draft = draft_payload()
        for key in ("school_today", "school_tomorrow", "school_date", "school_tomorrow_date"):
            self.assertIn(key, draft)
            self.assertIsInstance(draft[key], dict)
        self.assertTrue(draft["review_only"])

    def test_closure_array_is_in_both_expressions(self):
        arr = closure_array()
        for tomorrow in (False, True):
            nodes = list(walk(school_expression(tomorrow)))
            self.assertTrue(any(n.get("t") == "string" and n.get("v") == arr for n in nodes))
            self.assertTrue(any(n.get("n") == "contains" for n in nodes))

    def test_tomorrow_has_adddays_today_does_not(self):
        self.assertFalse(any(n.get("n") == "adddays" for n in walk(local_date(False))))
        self.assertTrue(any(n.get("n") == "adddays" for n in walk(local_date(True))))

    def test_all_function_arguments_are_wrapped(self):
        for root in (school_expression(False), school_expression(True)):
            for node in walk(root):
                if node.get("t") == "function":
                    self.assertTrue(all(a.get("t") == "expression" and
                                        isinstance(a.get("i"), list) and len(a["i"]) == 1
                                        for a in node["i"]))


if __name__ == "__main__":
    unittest.main()
