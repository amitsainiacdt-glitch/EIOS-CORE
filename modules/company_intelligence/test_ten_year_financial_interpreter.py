import unittest

from modules.company_intelligence.ten_year_financial_interpreter import TenYearFinancialInterpreter


class TenYearFinancialInterpreterTests(unittest.TestCase):
    def test_missing_years_remain_null_and_are_not_zero(self):
        extraction = {"facts": [{"fact_id": "CORO-FY25-REVENUE", "period": "FY2024-25", "value": 24064}]}
        result = TenYearFinancialInterpreter().build(extraction)
        self.assertEqual(len(result["periods"]), 8)
        self.assertIsNone(result["periods"][0]["values"]["revenue"])
        self.assertEqual(result["periods"][-1]["values"]["revenue"], 24064)
        self.assertEqual(result["chartStatus"], "INSUFFICIENT_COMPARABLE_YEARS")

    def test_empty_extraction_has_zero_coverage(self):
        result = TenYearFinancialInterpreter().build(None)
        self.assertEqual(result["coveragePercent"], 0)
        self.assertEqual(result["verifiedYears"], 0)

    def test_governed_history_creates_multi_year_highlight(self):
        history = {"periods": [
            {"period": "FY2018-19", "values": {"revenue": 100, "pat": 10}, "evidence_ids": ["FY19"]},
            {"period": "FY2024-25", "values": {"revenue": 200, "pat": 30}, "evidence_ids": ["FY25"]},
        ]}
        result = TenYearFinancialInterpreter().build(None, history)
        self.assertEqual(result["verifiedYears"], 2)
        self.assertEqual(result["chartStatus"], "READY")
        self.assertIn("Profit compounded faster", result["metaHighlights"][0]["title"])

    def test_balance_sheet_warns_on_material_cash_decline(self):
        history = {"periods": [
            {"period": "FY2023-24", "values": {"cash_and_equivalents": 1000, "trade_receivables": 100, "inventory": 100, "net_worth": 500}},
            {"period": "FY2024-25", "values": {"cash_and_equivalents": 500, "trade_receivables": 90, "inventory": 105, "net_worth": 550}},
        ]}
        result = TenYearFinancialInterpreter().build(None, history)
        self.assertTrue(result["balanceSheetReview"]["comparison"]["warnings"])


if __name__ == "__main__":
    unittest.main()
