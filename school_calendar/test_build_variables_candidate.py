"""Safety and determinism checks for the review-only native candidate builder."""
import unittest

from school_calendar.build_variables_candidate import candidate


def section(number, variable, minute=None):
    s = {"$": number, "t": "every", "lo": {"t": "c", "c": 1},
         "lo2": {"t": "c", "c": minute} if minute is not None else {"t": "s", "s": "sunset"},
         "s": [{"$": number + 1, "t": "action", "k": [
             {"$": number + 2, "c": "setVariable", "p": [
                 {"t": "x", "x": variable}, {"t": "c", "c": "false"}]}]}]}
    return s


class BuilderTests(unittest.TestCase):
    def baseline(self):
        return {"s": [section(7, "@School"), section(10, "@School"),
                      section(13, "@LateArrivalActive", 290),
                      section(20, "@GuestsPresent")], "r": [], "n": "Variables"}

    def test_preserves_unrelated_and_builds_refreshes(self):
        original = self.baseline()
        result = candidate(original)
        self.assertEqual(original["s"][0]["$"], 7)
        self.assertEqual([s["$"] for s in result["s"][:2]], [13, 20])
        self.assertEqual(len(result["s"]), 5)
        self.assertEqual([s["lo2"].get("c", s["lo2"].get("s")) for s in result["s"][-3:]],
                         [5, 290, "sunset"])
        for s in result["s"][-3:]:
            self.assertEqual([k["p"][0]["x"] for k in s["s"][0]["k"]],
                             ["@SchoolDate", "@School", "@SchoolTomorrowDate", "@SchoolTomorrow"])

    def test_rejects_changed_seasonal_writer(self):
        baseline = self.baseline()
        baseline["s"][0]["s"][0]["k"][0]["p"][0]["x"] = "@Other"
        with self.assertRaises(ValueError):
            candidate(baseline)


if __name__ == "__main__":
    unittest.main()
