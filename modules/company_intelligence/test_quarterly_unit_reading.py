import unittest
from modules.company_intelligence.quarterly_unit_reading import assess_unit_reading


class UnitReadingTests(unittest.TestCase):
    def test_r_is_not_rupee_confirmation(self):
        for text in ('(R in Crores)', '(f in Crores)', 'in Crores)'):
            result = assess_unit_reading(text)
            self.assertEqual(result['status'], 'NEEDS_UNIT_REVIEW')
            self.assertIsNone(result['currency'])

    def test_explicit_rupee_markers_remain_candidates(self):
        for text in ('₹ in Crores', 'INR crore', 'Rs. in lakhs', 'rupees million'):
            result = assess_unit_reading(text)
            self.assertEqual(result['status'], 'UNIT_CANDIDATE_PENDING_REVIEW')
            self.assertFalse(result['creates_approved_facts'])

    def test_conflicting_currency_and_unit(self):
        for text in ('INR USD crore', '₹ rand crore', 'INR crore lakh', '₹'):
            self.assertEqual(assess_unit_reading(text)['status'], 'NEEDS_UNIT_REVIEW')

    def test_missing_reading_stays_held(self):
        self.assertEqual(assess_unit_reading(None)['status'], 'NEEDS_UNIT_REVIEW')
