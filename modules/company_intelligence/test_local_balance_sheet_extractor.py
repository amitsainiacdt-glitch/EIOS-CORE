import unittest
from modules.company_intelligence.local_balance_sheet_extractor import extract_balance_sheet

TEXT = """Balance Sheet 31 March 2025 / 31 March 2024 (in lakhs)
1 Non-current assets
(a) Property, plant and equipment 3 100 90
(b) Capital work-in-progress 3 10 10
110 100
2 Current assets
(a) Inventories 9 20 20
ii) Trade receivables 11 10 10
iii) Government subsidies receivable 10 10
iv) Cash and cash equivalents 12 20 20
v) Bank balances other than cash and cash
equivalents
13 30 40
90 100
Total assets 200 200
1 Equity
Total equity 100 100
2 Non-current liabilities
i) Lease liabilities 5 20 20
20 20
3 Current liabilities
i) Borrowings 18 80 80
80 80
Total liabilities 100 100
Total equity and liabilities 200 200
"""

class BalanceSheetTests(unittest.TestCase):
    def extract(self, text=TEXT, column=0, period="FY2024-25"):
        return extract_balance_sheet(text, column=column, period=period,
            source={"column_periods": ["FY2024-25", "FY2023-24"], "pdf_page": 1})

    def test_values_units_wrapping_and_totals(self):
        p = self.extract()
        self.assertEqual(p["facts"]["other_bank_balances"]["value"], 0.3)
        self.assertEqual(p["facts"]["total_assets"]["value"], 2)
        self.assertTrue(all(v == 0 for v in p["checks_residual_crore"].values()))
        self.assertFalse(p["creates_evidence"])

    def test_absent_borrowings_are_not_zero(self):
        self.assertIsNone(self.extract()["facts"]["non_current_liabilities_borrowings"])

    def test_comparative_column(self):
        self.assertEqual(self.extract(column=1, period="FY2023-24")["facts"]["other_bank_balances"]["value"], 0.4)

    def test_rejects_bad_totals_and_mapping(self):
        with self.assertRaises(ValueError):
            self.extract(TEXT.replace("Total assets 200", "Total assets 210"))
        with self.assertRaises(ValueError):
            self.extract(column=1)

    def test_rejects_missing_duplicate_and_wrong_units(self):
        for text in (TEXT.replace("in lakhs", "in millions"), TEXT.replace("Total equity 100 100", ""),
                     TEXT.replace("Total equity 100 100", "Total equity 100 100\nTotal equity 100 100")):
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                self.extract(text)

    def test_equity_does_not_match_equity_and_liabilities(self):
        self.assertEqual(self.extract()["facts"]["total_equity"]["value"], 1)

    def test_split_trade_payables_are_calculated_not_quoted(self):
        text = TEXT.replace("i) Borrowings 18 80 80", "i) Borrowings 18 40 40\nTotal outstanding dues of micro enterprises and small enterprises 10 10\nTotal outstanding dues of creditors other than micro enterprises and\nsmall enterprises\n30 30")
        result = self.extract(text)["facts"]
        self.assertEqual(result["trade_payables_total"]["value"], 0.4)
        self.assertIsNone(result["trade_payables_total"]["raw_value"])
        self.assertIn("calculation", result["trade_payables_total"])

    def test_legacy_single_payables_row_keeps_original_source(self):
        text = TEXT.replace("i) Borrowings 18 80 80", "ii) Trade payables 23 80 80")
        result = self.extract(text)["facts"]["trade_payables_total"]
        self.assertEqual(result["value"], 0.8)
        self.assertEqual(result["raw_value"], "80")

if __name__ == "__main__":
    unittest.main()
