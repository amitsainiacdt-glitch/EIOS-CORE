import unittest

from modules.company_intelligence.local_cash_flow_extractor import amount, extract_period, continuity_warnings, compare_cash_revisions


TEXT = """Standalone Cash flow statement 31 March 2025 / 31 March 2024 (in lakhs)
Net cash flows from operating activities (A) 1,000 2,000
Net cash used in investing activities (B) (300) (400)
Net cash used in financing activities (C) (200) (100)
Cash and cash equivalents at the beginning of the year 500 100
Cash and cash equivalents at the end of the year (as per Note 12) 1,000 1,600
Purchase of property, plant and equipment including
capital work-in-progress and capital advances
(250) (350)
"""


class LocalCashFlowExtractorTests(unittest.TestCase):
    def extract(self, text=TEXT, column=0, period="FY2024-25"):
        return extract_period({9: text}, column=column, period=period,
                              source={"column_periods": ["FY2024-25", "FY2023-24"], "document_hash": "test"})

    def test_units_signs_and_wrapped_capex(self):
        result = self.extract()
        self.assertEqual(result["facts"]["operating_cash_flow"]["value"], 10)
        self.assertEqual(result["facts"]["investing_cash_flow"]["value"], -3)
        self.assertEqual(result["derived"]["free_cash_flow"], 7.5)
        self.assertEqual(result["facts"]["cash_capex"]["pdf_page"], 9)
        self.assertFalse(result["creates_evidence"])

    def test_comparative_column(self):
        self.assertEqual(self.extract(column=1, period="FY2023-24")["derived"]["free_cash_flow"], 16.5)

    def test_rejects_wrong_period_column(self):
        with self.assertRaises(ValueError):
            self.extract(column=1)

    def test_rejects_bad_bridge(self):
        with self.assertRaisesRegex(ValueError, "does not reconcile"):
            self.extract(TEXT.replace("1,000 1,600", "1,010 1,600"))

    def test_rejects_missing_duplicate_or_wrong_unit(self):
        for text in ("", TEXT + TEXT, TEXT.replace("in lakhs", "in millions")):
            with self.subTest(text=text[:20]), self.assertRaises(ValueError):
                self.extract(text)

    def test_source_continuity_warning_is_separate_from_bridge(self):
        first = self.extract(column=1, period="FY2023-24")
        second = self.extract()
        self.assertEqual(continuity_warnings([first, second])[0]["difference_crore"], -11)

    def test_parentheses_and_indian_grouping(self):
        self.assertEqual(amount("(2,54,570)"), -254570)
        self.assertEqual(amount("—"), 0)

    def test_business_combination_cash_is_not_operating_cash(self):
        revised = self.extract(TEXT.replace("1,000 1,600", "1,100 1,700") +
            "Add: Cash and cash equivalents acquired on account of common control business combination\n(refer note 47) 100 100\n")
        self.assertEqual(revised["facts"]["business_combination_cash"]["value"], 1)
        self.assertEqual(revised["facts"]["operating_cash_flow"]["value"], 10)
        self.assertEqual(revised["derived"]["free_cash_flow"], 7.5)
        review = compare_cash_revisions(self.extract(), revised)
        self.assertEqual(review["deltas_crore"]["closing_cash"], 1)
        self.assertEqual(review["deltas_crore"]["business_combination_cash"], 1)
        self.assertFalse(review["creates_evidence"])

    def test_unreadable_adjustment_is_not_silently_zero(self):
        with self.assertRaisesRegex(ValueError, "unreadable"):
            self.extract(TEXT + "Add: Cash and cash equivalents acquired on account of common control business combination\nnot legible\n")

    def test_revision_comparison_rejects_different_years_and_bad_values(self):
        with self.assertRaisesRegex(ValueError, "same period"):
            compare_cash_revisions(self.extract(), self.extract(column=1, period="FY2023-24"))
        revised = self.extract()
        revised["facts"]["closing_cash"]["value"] += 1
        with self.assertRaisesRegex(ValueError, "unreconciled"):
            compare_cash_revisions(self.extract(), revised)

    def test_missing_capex_cannot_borrow_the_next_rows_numbers(self):
        text = TEXT.replace("(250) (350)", "Proceeds from sale of assets (250) (350)")
        with self.assertRaisesRegex(ValueError, "cash_capex"):
            self.extract(text)


if __name__ == "__main__":
    unittest.main()
