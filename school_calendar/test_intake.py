import copy
import unittest
from school_calendar.intake import validate_submission

BASE = {'schema_version': 1, 'status': 'verified', 'district': 'Leander ISD', 'timezone': 'America/Chicago', 'source': 'https://www.leanderisd.org/calendar/', 'first_day': '2026-08-12', 'last_day': '2027-05-27', 'closures': [{'start': '2026-09-07', 'reason': 'Holiday'}, {'start': '2026-09-21', 'reason': 'Staff'}, {'start': '2026-10-09', 'reason': 'Break'}, {'start': '2026-11-02', 'reason': 'Staff'}, {'start': '2026-11-23', 'reason': 'Break'}], 'early_release': ['2026-12-18'], 'provenance': {'retrieved_at': '2026-10-13T12:00:00Z', 'academic_calendar_url': 'https://www.leanderisd.org/calendar/'}}

class IntakeTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_submission(copy.deepcopy(BASE))['status'], 'verified')

    def test_missing_provenance(self):
        data = copy.deepcopy(BASE)
        del data['provenance']
        with self.assertRaises(ValueError):
            validate_submission(data)

    def test_sparse_closures(self):
        data = copy.deepcopy(BASE)
        data['closures'] = []
        with self.assertRaises(ValueError):
            validate_submission(data)

    def test_early_release_on_holiday(self):
        data = copy.deepcopy(BASE)
        data['early_release'] = ['2026-09-07']
        with self.assertRaises(ValueError):
            validate_submission(data)

if __name__ == '__main__':
    unittest.main()
