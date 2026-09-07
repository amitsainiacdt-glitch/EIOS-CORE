import unittest
from modules.company_intelligence.quarterly_column_reconciliation import reconcile_column, reconcile_extracted_column


class QuarterlyColumnReconciliationTests(unittest.TestCase):
    def test_header_to_arithmetic_integration(self):
        column = self.column()
        for key in ('period_start', 'period_end', 'quarter', 'basis', 'unit'):
            del column[key]
        column['header_text'] = 'Consolidated INR lakh Quarter ended 30 June 2026'
        result = reconcile_extracted_column(column)
        self.assertEqual(result['status'], 'CHECKED_PENDING_REVIEW')
        self.assertEqual(result['quarter'], 'Q1-FY2027')
        column['basis'] = 'STANDALONE'
        self.assertEqual(reconcile_extracted_column(column)['status'], 'HOLD')

    def column(self):
        binding = {'document_hash': 'b' * 64, 'pdf_page': 1, 'column_index': 0}
        return {**binding, 'ticker': 'SYNTHETIC', 'header_text': 'Quarter ended 30 June 2026',
                'period_start': '2026-04-01', 'period_end': '2026-06-30',
                'quarter': 'Q1-FY2027', 'basis': 'CONSOLIDATED', 'unit': 'INR_LAKH',
                'cells': {key: {**binding, 'value': value} for key, value in
                          {'revenue': '1000', 'other_income': '20', 'total_income': '1020', 'pat': '-10'}.items()}}

    def test_valid_normalization_is_still_unapproved(self):
        result = reconcile_column(self.column())
        self.assertEqual(result['status'], 'CHECKED_PENDING_REVIEW')
        self.assertEqual(result['values_inr_crore']['pat'], '-0.10')
        self.assertFalse(result['creates_approved_facts'])

    def test_annual_and_ytd_periods_rejected(self):
        for end in ('2027-03-31', '2026-09-30'):
            column = self.column()
            column['period_end'] = end
            self.assertEqual(reconcile_column(column)['status'], 'HOLD')

    def test_wrong_fiscal_year_rejected(self):
        column = self.column()
        column['quarter'] = 'Q1-FY2026'
        self.assertIn('QUARTER_LABEL_MISMATCH', reconcile_column(column)['issues'])

    def test_mixed_columns_rejected(self):
        column = self.column()
        column['cells']['pat']['column_index'] = 4
        self.assertEqual(reconcile_column(column)['values_inr_crore'], {})

    def test_arithmetic_failure_rejected(self):
        column = self.column()
        column['cells']['total_income']['value'] = '999'
        self.assertEqual(reconcile_column(column)['income_check'], 'FAIL')

    def test_unknown_units_or_basis_rejected(self):
        for key in ('unit', 'basis'):
            column = self.column()
            column[key] = 'UNKNOWN'
            self.assertEqual(reconcile_column(column)['status'], 'HOLD')

    def test_invalid_numbers_rejected(self):
        for value in (True, 'NaN', 'Infinity', '7,ll0l.32'):
            column = self.column()
            column['cells']['pat']['value'] = value
            self.assertEqual(reconcile_column(column)['status'], 'HOLD')

    def test_missing_is_not_zero(self):
        column = self.column()
        del column['cells']['other_income']
        self.assertEqual(reconcile_column(column)['income_check'], 'NOT_CHECKABLE')

    def test_march_quarter(self):
        column = self.column()
        column.update(period_start='2026-01-01', period_end='2026-03-31', quarter='Q4-FY2026')
        self.assertEqual(reconcile_column(column)['quarter'], 'Q4-FY2026')
