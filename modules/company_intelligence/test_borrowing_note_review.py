import unittest
from modules.company_intelligence.borrowing_note_review import apply_borrowing_note

class BorrowingNoteTests(unittest.TestCase):
    def record(self):
        return {"period": "FY2024-25", "facts": {"current_liabilities_borrowings": {"value": 0.18}}}
    def source(self):
        return {"column_periods": ["FY2024-25", "FY2023-24"], "pdf_page": 156}
    def test_explicit_zero_and_note_total(self):
        text = 'in lakhs\n18. Borrowings\nShort term borrowings 18 29\nLong term borrowings - -\n'
        p = apply_borrowing_note(self.record(), text, self.source())
        self.assertEqual(p['facts']['non_current_liabilities_borrowings']['value'], 0)
        self.assertEqual(p['facts']['total_borrowings_ex_leases']['value'], .18)
        self.assertIn('excludes lease', p['facts']['total_borrowings_ex_leases']['calculation'])
    def test_absence_is_not_zero(self):
        with self.assertRaises(ValueError):
            apply_borrowing_note(self.record(), 'in lakhs\n18. Borrowings\nShort term borrowings 18 29\n', self.source())
    def test_narrative_zero_is_year_bound(self):
        text = 'in lakhs\n18. Borrowings\nShort term borrowings 18 29\nThere are no outstanding long-term borrowings as at 31 March 2025 and 31 March 2024.'
        self.assertEqual(apply_borrowing_note(self.record(), text, self.source())['facts']['total_borrowings_ex_leases']['value'], .18)
        with self.assertRaises(ValueError):
            apply_borrowing_note(self.record(), text.replace('2025', '2023'), self.source())
    def test_disagreement_blocks_total(self):
        with self.assertRaises(ValueError):
            apply_borrowing_note(self.record(), 'in lakhs\n18. Borrowings\nShort term borrowings 19 29\nLong term borrowings - -\n', self.source())
