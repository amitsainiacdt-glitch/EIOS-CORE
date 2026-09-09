import unittest
from modules.company_intelligence.quarterly_exchange_corroboration import apply_exchange_unit_corroboration


class QuarterlyExchangeCorroborationTests(unittest.TestCase):
    def fixture(self):
        digest = "a" * 64
        base = {"document_hash": digest, "pdf_page": 1, "table_id": "t"}
        columns = [{"column_index": 0, "date_header_text": "30.06.2026"}]
        page = {"pdf_page": 1, "statement_context": {"basis_candidates": ["STANDALONE"],
                "current_quarter_end_text": "June 30, 2026"},
                "ruled_tables": [{"table_id": "t", "columns": columns}]}
        binding = {"tables": [{"table_id": "t", "unit_assessment": {
            "unit_candidates": ["lakh"], "issues": ["EXPLICIT_INR_MARKER_MISSING"]},
            "spans": [{**base, "kind": "basis", "text": "STANDALONE", "first_column": 0, "last_column": 0},
                      {**base, "kind": "duration", "text": "Quarter ended", "first_column": 0, "last_column": 0}],
            "columns": [{"column_index": 0, "resolution": {"status": "HOLD"},
                         "date_comparison": {"status": "DATE_READINGS_AGREE_PENDING_REVIEW",
                                             "native": {"date": "2026-06-30"}}}]}]}
        report = {"status": "EXCHANGE_CORROBORATION_CANDIDATE", "document_hash": "b" * 64,
                  "source_url": "https://nsearchives.nseindia.com/report.html",
                  "metadata": {"ticker": "TEST", "currency": "INR", "rounding": "Lakhs",
                               "basis": "Standalone", "period_end": "30-06-2026"}}
        return binding, page, report, digest

    def test_matching_exchange_metadata_supplies_held_unit_span(self):
        binding, page, report, digest = self.fixture()
        result = apply_exchange_unit_corroboration(binding, page, report, ticker="TEST", pdf_document_hash=digest)
        self.assertEqual(result["tables"][0]["columns"][0]["resolution"]["unit"], "INR_LAKH")
        self.assertFalse(result["tables"][0]["exchange_unit_corroboration"]["creates_approved_facts"])

    def test_identity_basis_or_period_mismatch_does_not_bind(self):
        for field, value in (("ticker", "OTHER"), ("basis", "Consolidated"), ("period_end", "30-09-2026")):
            binding, page, report, digest = self.fixture()
            report["metadata"][field] = value
            result = apply_exchange_unit_corroboration(binding, page, report, ticker="TEST", pdf_document_hash=digest)
            self.assertNotIn("exchange_unit_corroboration", result["tables"][0])

    def test_unreadable_title_date_can_use_unique_exchange_table_date(self):
        binding, page, report, digest = self.fixture()
        page["statement_context"]["current_quarter_end_text"] = "lune 30, 2026"
        binding["tables"][0]["spans"] = [span for span in binding["tables"][0]["spans"]
                                                if span["kind"] != "duration"]
        result = apply_exchange_unit_corroboration(binding, page, report, ticker="TEST", pdf_document_hash=digest)
        spans = result["tables"][0]["spans"]
        self.assertTrue(any(span["kind"] == "duration" and span["first_column"] == 0 for span in spans))
        self.assertTrue(any(span["kind"] == "unit" for span in spans))
