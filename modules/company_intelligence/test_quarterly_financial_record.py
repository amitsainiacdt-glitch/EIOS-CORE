import unittest

from modules.company_intelligence.quarterly_financial_record import QuarterlyFinancialRecord


class QuarterlyFinancialRecordTests(unittest.TestCase):
    def test_core_metrics_are_detected(self):
        record = QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", revenue=100, pat=8)
        self.assertTrue(record.has_core_metrics)

    def test_governed_record_requires_source(self):
        with self.assertRaises(ValueError):
            QuarterlyFinancialRecord("COROMANDEL", "Q1-FY2025", revenue=100, pat=8, status="GOVERNED")


if __name__ == "__main__":
    unittest.main()
