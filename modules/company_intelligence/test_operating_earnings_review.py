import unittest
from modules.company_intelligence.operating_earnings_review import extract_operating_earnings, validate_earnings_review
TEXT = '''in lakhs
Revenue from operations 1000 900
Other income 10 20
Finance costs 30 40
Depreciation and amortisation expense 50 60
III Profit before exceptional items and tax 100 200
IV Exceptional items 20 -
V Profit before tax 120 200
'''
class EarningsTests(unittest.TestCase):
    def run_extract(self, text=TEXT, column=0, period='FY2024-25'):
        return extract_operating_earnings(text, period, column, {'column_periods': ['FY2024-25','FY2023-24']})
    def test_excludes_exceptional_gain_and_other_income(self):
        r = self.run_extract()
        self.assertEqual(r['calculated_operating_ebitda'], 1.7)
        self.assertFalse(r['creates_evidence'])
    def test_comparative_column(self):
        self.assertEqual(self.run_extract(column=1, period='FY2023-24')['calculated_operating_ebitda'], 2.8)
    def test_bad_mapping_and_missing_row_rejected(self):
        with self.assertRaises(ValueError): self.run_extract(column=1)
        with self.assertRaises(ValueError): self.run_extract(TEXT.replace('Finance costs 30 40',''))
    def test_missing_pre_exceptional_profit_is_not_guessed(self):
        with self.assertRaises(ValueError): self.run_extract(TEXT.replace('III Profit before exceptional items and tax 100 200',''))

    def valid_pack(self):
        row = extract_operating_earnings(TEXT, 'FY2024-25', 0, {
            'column_periods': ['FY2024-25','FY2023-24'], 'document_hash': 'a'*64, 'pdf_page': 140})
        return {'periods': [row]}

    def test_validation_checks_arithmetic_without_approval_or_mutation(self):
        pack = self.valid_pack()
        validated = validate_earnings_review(pack)
        self.assertEqual(validated['periods'][0]['arithmetic_status'], 'INPUTS_AND_CALCULATION_CHECKED')
        self.assertNotIn('arithmetic_status', pack['periods'][0])
        self.assertEqual(validated['periods'][0]['review_status'], 'PENDING_META_REVIEW')
        self.assertFalse(validated['periods'][0]['creates_evidence'])

    def test_tampered_calculation_or_units_rejected(self):
        pack = self.valid_pack()
        pack['periods'][0]['calculated_operating_ebitda'] += .01
        with self.assertRaises(ValueError): validate_earnings_review(pack)
        pack = self.valid_pack()
        pack['periods'][0]['facts']['finance_costs']['unit'] = 'INR_LAKH'
        with self.assertRaises(ValueError): validate_earnings_review(pack)

    def test_changed_raw_value_and_mixed_sources_rejected(self):
        pack = self.valid_pack()
        pack['periods'][0]['facts']['finance_costs']['raw_value'] = '31'
        with self.assertRaises(ValueError): validate_earnings_review(pack)
        pack = self.valid_pack()
        pack['periods'][0]['facts']['finance_costs']['document_hash'] = 'b'*64
        with self.assertRaises(ValueError): validate_earnings_review(pack)

    def test_duplicate_and_nonfinite_rows_rejected(self):
        pack = self.valid_pack()
        pack['periods'].append(pack['periods'][0])
        with self.assertRaises(ValueError): validate_earnings_review(pack)
        pack = self.valid_pack()
        pack['periods'][0]['calculated_operating_ebitda'] = float('nan')
        with self.assertRaises(ValueError): validate_earnings_review(pack)
