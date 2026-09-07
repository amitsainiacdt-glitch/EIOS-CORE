import unittest
from modules.company_intelligence.quarterly_table_candidates import extract_table_candidates


class QuarterlyTableCandidateTests(unittest.TestCase):
    def extract(self, text):
        return extract_table_candidates([text], document_hash='a' * 64,
                                        source_url='https://issuer.example/report.pdf', ticker='TEST')

    def test_numbers_do_not_approve_or_assign_columns(self):
        result = self.extract('Revenue from operations  1,234.50  0  (4.25)')
        row = result['candidates'][0]
        self.assertEqual([cell['value'] for cell in row['cells']], [1234.5, 0, -4.25])
        self.assertIsNone(row['column_mapping'])
        self.assertIsNone(row['accounting_basis'])
        self.assertFalse(result['creates_approved_facts'])

    def test_ocr_and_dashes_are_not_repaired(self):
        row = self.extract('Revenue from operations  7,ll0l.32  -')['candidates'][0]
        self.assertTrue(row['requires_ocr_review'])
        self.assertEqual([cell['value'] for cell in row['cells']], [None, None])

    def test_income_is_not_revenue(self):
        self.assertEqual(self.extract('Total income  900.00')['candidates'][0]['metric_candidate'], 'total_income')

    def test_unknown_layout_does_not_invent_rows(self):
        self.assertEqual(self.extract('A scanned page with no text')['status'], 'NO_TABLE_ROWS_IDENTIFIED')

    def test_hash_required(self):
        with self.assertRaises(ValueError):
            extract_table_candidates([], document_hash='report-name', source_url='', ticker='TEST')

    def test_numeric_overflow_is_held(self):
        row = self.extract('Revenue from operations  ' + '9' * 400)['candidates'][0]
        self.assertIsNone(row['cells'][0]['value'])
        self.assertTrue(row['requires_ocr_review'])

    def test_pre_tax_profit_is_not_pat(self):
        self.assertEqual(self.extract('Profit before tax for the period  100')['candidate_count'], 0)

    def test_layout_spacing_preserved_for_column_matching(self):
        line = '     Revenue from operations       10.00        20.00'
        self.assertEqual(self.extract(line)['candidates'][0]['source_layout_row'], line)
