import unittest
from school_calendar.build_runtime_test import candidate, cases
from school_calendar.test_native_variables_draft import walk


class RuntimeTestSafety(unittest.TestCase):
    def test_only_local_assignments_and_logging(self):
        p = candidate({"s": [], "v": []}, cases()[:10])
        nodes = list(walk(p))
        for node in nodes:
            if node.get("t") == "action":
                self.assertEqual(node["d"], [])
            if "p" in node and "c" in node:
                self.assertIn(node["c"], ("log", "setVariable"))
            self.assertNotEqual(node.get("t"), "every")
            self.assertFalse(str(node.get("x", "")).startswith("@"))

    def test_matrix_includes_all_closures_and_early_releases(self):
        from school_calendar.generate_webcore_dates import generate
        from school_calendar.webcore_array import DATA
        matrix = cases()
        rows = {row["date"]: row for row in matrix}
        for day in generate(DATA)["closed_weekdays"]:
            self.assertFalse(rows[day]["school"])
        for day in generate(DATA)["early_release"]:
            self.assertTrue(rows[day]["school"])
