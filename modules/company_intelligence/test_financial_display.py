import unittest
from datetime import datetime, timezone
from modules.company_intelligence.financial_display import add_display_cells
from modules.company_intelligence.governed_annual_financial import GovernedAnnualFinancial

class FinancialDisplayTests(unittest.TestCase):
    def setUp(self):
        self.history = {"periods": [{"period": "FY2024-25", "values": {"operating_cash_flow": None, "capex": None, "total_debt": None}}]}
        self.pack = {"periods": [{"period": "FY2024-25", "basis": "STANDALONE", "review_status": "PENDING_META_REVIEW", "facts": {
            "operating_cash_flow": {"value": 0, "unit": "INR_CRORE", "document_hash": "abc", "pdf_page": 1},
            "cash_capex": {"value": 3}, "current_liabilities_borrowings": {"value": 4}}}]}

    def test_staging_display_does_not_mutate_analysis(self):
        p = add_display_cells(self.history, self.pack)["periods"][0]
        self.assertIsNone(p["values"]["operating_cash_flow"])
        self.assertEqual(p["displayCells"]["operating_cash_flow"]["value"], 0)
        self.assertNotIn("displayCells", self.history["periods"][0])

    def test_different_metrics_are_not_substituted(self):
        p = add_display_cells(self.history, self.pack, self.pack)["periods"][0]
        for key in ("capex", "total_debt"):
            self.assertIsNone(p["displayCells"][key]["value"])
            self.assertTrue(p["displayCells"][key]["reason"])

    def test_unbound_wrong_basis_and_wrong_year_are_rejected(self):
        for key, value in (("basis", "CONSOLIDATED"), ("period", "FY2023-24")):
            pack = {"periods": [{**self.pack["periods"][0], key: value}]}
            self.assertIsNone(add_display_cells(self.history, pack)["periods"][0]["displayCells"]["operating_cash_flow"]["value"])
        self.pack["periods"][0]["facts"]["operating_cash_flow"].pop("document_hash")
        self.assertIsNone(add_display_cells(self.history, self.pack)["periods"][0]["displayCells"]["operating_cash_flow"]["value"])

    def test_existing_values_not_overwritten(self):
        self.history["periods"][0]["values"]["operating_cash_flow"] = 9
        self.assertEqual(add_display_cells(self.history, self.pack)["periods"][0]["displayCells"]["operating_cash_flow"]["value"], 9)

    def test_verified_annual_record_precedes_pending_display_candidate(self):
        record = GovernedAnnualFinancial(
            1, "record", "TEST", "Example", "CASH_FLOW", "FY2024-25", "STANDALONE",
            {"operating_cash_flow": "44.25"}, "a" * 64, "https://issuer.example/ar.pdf", (9,),
            "b" * 64, "H-1", datetime.now(timezone.utc), "receipt")
        period = add_display_cells(self.history, self.pack, governed_annual=(record,))["periods"][0]
        cell = period["displayCells"]["operating_cash_flow"]
        self.assertEqual(cell["value"], 44.25)
        self.assertEqual(cell["status"], "VERIFIED_HUMAN_REVIEWED")
        self.assertEqual(cell["source"]["receipt_id"], "receipt")

    def test_untrusted_object_cannot_claim_verified_display(self):
        class Fake:
            status = "GOVERNED_ANNUAL_FINANCIAL"; controlled_write_receipt_id = None
            changes_verdict = False; authorizes_trade = False
        with self.assertRaisesRegex(ValueError, "invalid governed"):
            add_display_cells(self.history, self.pack, governed_annual=(Fake(),))
