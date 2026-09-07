import unittest

from modules.company_intelligence.quarterly_financial_record import QuarterlyFinancialRecord


class QuarterlyFinancialRecordTests(unittest.TestCase):
    def test_core_metrics_are_detected(self):
        record = QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", revenue=100, pat=8)
        self.assertTrue(record.has_core_metrics)

    def test_governed_record_requires_source(self):
        with self.assertRaises(ValueError):
            QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", revenue=100, pat=8, status="GOVERNED")

    def test_source_identifier_cannot_approve_a_staging_record(self):
        for status in ("GOVERNED", "APPROVED", "", None):
            with self.subTest(status=status), self.assertRaises(ValueError):
                QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", source_id="report-1", status=status)

    def test_nonfinancial_numbers_are_rejected_for_every_metric(self):
        for metric in ("revenue", "ebitda", "pat", "operating_cash_flow"):
            for value in (True, False, float("nan"), float("inf"), -float("inf"), "100", 10**400):
                with self.subTest(metric=metric, value=repr(value)), self.assertRaises(ValueError):
                    QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", **{metric: value})

    def test_missing_zero_and_losses_remain_distinct(self):
        missing = QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025")
        self.assertFalse(missing.has_core_metrics)
        record = QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", revenue=0, pat=-8, operating_cash_flow=-12)
        self.assertTrue(record.has_core_metrics)
        self.assertEqual(record.revenue, 0)
        self.assertEqual(record.pat, -8)
        self.assertIsNone(record.ebitda)

    def test_quarter_cannot_be_an_annual_or_year_to_date_period(self):
        for quarter in ("FY2025", "9M-FY2025", "Q5-FY2025", "Q0-FY2025", "Q1-FY25", " Q1-FY2025", None, 2025):
            with self.subTest(quarter=quarter), self.assertRaises(ValueError):
                QuarterlyFinancialRecord("COROMANDEL", quarter)
        for number in range(1, 5):
            self.assertEqual(QuarterlyFinancialRecord("COROMANDEL", f"Q{number}-FY2025").status, "STAGED")

    def test_identifiers_are_validated(self):
        for ticker in (None, 123, "", " "):
            with self.subTest(ticker=ticker), self.assertRaises(ValueError):
                QuarterlyFinancialRecord(ticker, "Q1-FY2025")
        for source in ("", " ", 123):
            with self.subTest(source=source), self.assertRaises(ValueError):
                QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", source_id=source)


if __name__ == "__main__":
    unittest.main()
