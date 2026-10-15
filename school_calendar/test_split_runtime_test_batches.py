"""Offline coverage and preservation checks for the resized TEST matrix."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from school_calendar import split_runtime_test_batches as splitter


class TestSplitRuntimeBatches(unittest.TestCase):
    def test_exact_coverage_and_original_statements(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(splitter, "DEST", Path(tmp)):
                manifest = splitter.build()
                self.assertEqual((manifest["calendar_cases"], manifest["freshness_cases"]), (64, 16))
                self.assertEqual(len(manifest["entries"]), 80)
                self.assertEqual(len({x["file"] for x in manifest["entries"]}), 80)
                for batch in range(1, 8):
                    original = json.loads((splitter.SOURCE / f"TEST_{batch}.json").read_text())
                    restored = []
                    for entry in manifest["entries"]:
                        if entry["source"] != f"TEST_{batch}.json":
                            continue
                        body = json.loads((Path(tmp) / entry["file"]).read_text())
                        self.assertEqual(body["v"], original["v"])
                        self.assertEqual(body["r"], original["r"])
                        self.assertEqual(body["s"], list(splitter.partition(original["s"]))[entry["source_case"] - 1])
                        restored.extend(body["s"])
                    self.assertEqual(restored, original["s"])
                self.assertTrue(all(not x["prepared"] and not x["runtime_verified"]
                                    for x in manifest["entries"]))


if __name__ == "__main__":
    unittest.main()
