import unittest
from modules.company_intelligence.quarterly_date_comparison import parse_date_cell, compare_date_cells


class DateComparisonTests(unittest.TestCase):
    def test_named_date_spacing(self):
        for raw in ('30June2026', '30 June\n2026', '30 Jun 2026'):
            self.assertEqual(parse_date_cell(raw)['date'], '2026-06-30')

    def test_iso_and_day_first_agree(self):
        result = compare_date_cells('2026-03-31', '31.03.2026')
        self.assertEqual(result['status'], 'DATE_READINGS_AGREE_PENDING_REVIEW')
        self.assertFalse(result['creates_approved_facts'])

    def test_year_conflict(self):
        self.assertEqual(compare_date_cells('30 June 2026', '30 June 2025')['status'], 'DATE_CONFLICT_HOLD')

    def test_corrupt_month_not_repaired(self):
        result = compare_date_cells('31 March 2026', '31 Match 2026')
        self.assertEqual(result['status'], 'DATE_READING_INCOMPLETE_HOLD')
        self.assertEqual(result['ocr']['raw_text'], '31 Match 2026')

    def test_invalid_leap_day(self):
        self.assertEqual(parse_date_cell('29 February 2025')['issue'], 'INVALID_CALENDAR_DATE')
        self.assertEqual(parse_date_cell('29 February 2024')['date'], '2024-02-29')

    def test_multiple_dates_and_extra_digits_rejected(self):
        for raw in ('30 June 2026 30 June 2025', '30 June 20266', '30 June 2026 note 2'):
            self.assertNotIn('date', parse_date_cell(raw))

    def test_missing_date(self):
        for raw in ('', None, 2026):
            self.assertEqual(parse_date_cell(raw)['issue'], 'DATE_MISSING')

    def test_numeric_order_ambiguity(self):
        self.assertEqual(parse_date_cell('03/06/2026')['issue'], 'AMBIGUOUS_NUMERIC_DATE')

    def test_date_does_not_assign_quarter(self):
        result = compare_date_cells('31 March 2026', '31 March 2026')
        self.assertNotIn('quarter', result)
        self.assertNotIn('period_start', result)
