"""Check real captured production baselines, not synthetic statement templates."""
import copy
import json
import unittest
from pathlib import Path
from school_calendar.build_consumers_candidate import modes_candidate, school_mornings_candidate
from school_calendar.build_variables_candidate import candidate

ROOT = Path(__file__).parent / "cutover" / "2026-10-14"


def baseline(name):
    return json.loads((ROOT / "baselines" / (name + ".json")).read_text())


class PreservationTests(unittest.TestCase):
    def test_variables_only_retires_two_seasonal_sections(self):
        original = baseline("Variables")
        result = candidate(original)
        retained = [s for s in original["s"] if s["$"] not in (7, 10)]
        self.assertEqual(result["s"][:len(retained)], retained)
        for key in set(original) - {"s", "v"}:
            self.assertEqual(result[key], original[key])
        self.assertEqual(len(result["s"]) - len(retained), 4)

    def test_mornings_changes_only_one_restriction(self):
        original = baseline("School_Mornings")
        result = school_mornings_candidate(original)
        self.assertEqual(result["r"][:2], original["r"])
        self.assertEqual(len(result["r"]), 3)
        for key in set(original) - {"r"}:
            self.assertEqual(result[key], original[key])

    def test_modes_has_exactly_two_operand_substitutions(self):
        original = baseline("Modes")
        result = modes_candidate(original)
        restored = copy.deepcopy(result)
        count = 0
        def restore(obj):
            nonlocal count
            if isinstance(obj, dict):
                if obj.get("t") == "x" and obj.get("x") == "@SchoolTomorrow":
                    count += 1
                    obj["x"] = "@School"
                for value in obj.values():
                    restore(value)
            elif isinstance(obj, list):
                for value in obj:
                    restore(value)
        restore(restored)
        self.assertEqual(count, 2)
        self.assertEqual(restored, original)
