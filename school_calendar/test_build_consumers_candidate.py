"""Safety tests for native consumer candidates."""
import unittest

from school_calendar.build_consumers_candidate import (
    modes_candidate, school_mornings_candidate,
)


class ConsumerTests(unittest.TestCase):
    def test_school_mornings_appends_only_guard(self):
        base = {"r": [
            {"$": 1, "co": "is", "lo": {"t": "x", "x": "@School"},
             "ro": {"t": "c", "c": "true"}, "ro2": {"t": "c", "g": "any"},
             "to": {"t": "c", "g": "any"}, "to2": {"t": "c", "g": "any"}},
            {"$": 2, "co": "is", "lo": {"t": "x", "x": "@KidsPresent"}},
        ], "s": [{"$": 3, "t": "every", "s": []}]}
        base["r"][1]["ro"] = {"t": "c", "c": "true"}
        result = school_mornings_candidate(base)
        self.assertEqual(len(base["r"]), 2)
        self.assertEqual(result["r"][:2], base["r"])
        self.assertEqual(result["s"], base["s"])
        self.assertEqual(result["r"][2]["ro"]["x"], "@SchoolDate")
        self.assertEqual(result["r"][2]["lo"]["exp"]["i"][0]["n"], "formatdatetime")
        self.assertEqual(result["r"][2]["$"], 4)

    def test_school_mornings_preserves_distributed_restrictions(self):
        def restrict(target, ident):
            return {"$": ident, "t": "restriction", "co": "is",
                    "lo": {"t": "x", "x": target},
                    "ro": {"t": "c", "c": "true"}}

        base = {"r": [], "s": [
            {"$": ident, "t": "every", "r": [
                restrict("@School", ident + 1),
                restrict("@KidsPresent", ident + 2),
            ], "s": []}
            for ident in (1, 4, 7)
        ]}
        result = school_mornings_candidate(base)
        self.assertEqual(len(result["r"]), 1)
        self.assertEqual(result["r"][0]["ro"]["x"], "@SchoolDate")
        self.assertEqual(result["s"], base["s"])
        self.assertEqual(base["r"], [])

    def test_school_mornings_rejects_missing_distributed_restriction(self):
        base = {"r": [], "s": [{"$": 1, "t": "every", "r": [
            {"co": "is", "lo": {"t": "x", "x": "@School"},
             "ro": {"t": "c", "c": "true"}},
        ], "s": []}]}
        with self.assertRaises(ValueError):
            school_mornings_candidate(base)

    def test_morning_baseline_change_is_rejected(self):
        with self.assertRaises(ValueError):
            school_mornings_candidate({"r": [], "s": []})

    def test_modes_only_replaces_two_references(self):
        base = {"s": [{"t": "if", "c": [
            {"lo": {"t": "x", "x": "@School"}},
            {"lo": {"t": "x", "x": "@School"}},
            {"lo": {"t": "x", "x": "@Other"}},
        ]}]}
        result = modes_candidate(base)
        self.assertEqual([c["lo"]["x"] for c in result["s"][0]["c"]],
                         ["@SchoolTomorrow", "@SchoolTomorrow", "@Other"])
        self.assertEqual(base["s"][0]["c"][0]["lo"]["x"], "@School")

    def test_modes_unexpected_reference_count_is_rejected(self):
        with self.assertRaises(ValueError):
            modes_candidate({"s": [{"lo": {"t": "x", "x": "@School"}}]})


if __name__ == "__main__":
    unittest.main()

