import unittest

from modules.company_intelligence.plain_english_company_interpreter import PlainEnglishCompanyInterpreter


class PlainEnglishCompanyInterpreterTests(unittest.TestCase):
    def test_missing_balance_sheet_is_not_called_a_red_flag(self):
        result = PlainEnglishCompanyInterpreter().build(extraction={"facts": []}, intelligence_snapshot={"layers": {"financials": {"warnings": ["CASH_FLOW_SERIES_MISSING"]}}}, discoveries=[])
        self.assertEqual(result["balanceSheet"]["status"], "INSUFFICIENT_EVIDENCE")
        self.assertIn("not proof", result["balanceSheet"]["explanation"])
        self.assertFalse(result["createsVerdict"])

    def test_unreviewed_news_cannot_claim_fundamental_change(self):
        result = PlainEnglishCompanyInterpreter().build(extraction=None, intelligence_snapshot=None, discoveries=[{"title": "New order", "reviewStatus": "PENDING"}])
        self.assertEqual(result["newsFundamentalMonitor"][0]["fundamental_status"], "FUNDAMENTAL_CHANGE_NOT_PROVEN")
        self.assertIn("order book", result["newsFundamentalMonitor"][0]["possible_pathway"])
        self.assertEqual(result["decisionJourney"][6]["status"], "PARTIAL")
        self.assertFalse(result["createsVerdict"])

    def test_financial_facts_are_compared_and_not_merely_repeated(self):
        facts = [
            {"fact_id": "CORO-FY25-REVENUE", "statement": "Revenue grew 9%"},
            {"fact_id": "CORO-FY25-EBITDA", "statement": "EBITDA grew 11%"},
            {"fact_id": "CORO-FY25-PAT", "statement": "PAT grew 13%"},
            {"fact_id": "CORO-FY25-CAPEX", "statement": "Capital expenditure grew 61%"},
            {"fact_id": "CORO-FY25-CROP-PROTECTION-REVENUE", "statement": "Crop Protection revenue grew 7%"},
        ]
        result = PlainEnglishCompanyInterpreter().build(extraction={"facts": facts}, intelligence_snapshot=None, discoveries=[])
        comparisons = result["numberComparisons"]
        self.assertEqual(len(comparisons), 3)
        self.assertEqual(comparisons[0]["title"], "Profit grew faster than sales")
        self.assertIn("one year is not enough", comparisons[0]["impact"])
        self.assertEqual(comparisons[1]["status"], "REQUIRES_MONITORING")


if __name__ == "__main__":
    unittest.main()
