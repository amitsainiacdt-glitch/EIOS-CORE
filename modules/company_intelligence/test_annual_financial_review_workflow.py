from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.annual_financial_review_workflow import AnnualFinancialReviewWorkflow
from modules.company_intelligence.governed_annual_financial import (
    AnnualFinancialHumanReviewLedger, GovernedAnnualFinancialRepository,
)


class AnnualFinancialReviewWorkflowTests(unittest.TestCase):
    def setup_workflow(self, root):
        workflow = AnnualFinancialReviewWorkflow(
            AnnualFinancialHumanReviewLedger(root / "reviews.jsonl"),
            GovernedAnnualFinancialRepository(root / "annual.jsonl"))
        fact = {"value": 10, "unit": "INR_CRORE", "document_hash": "a" * 64,
                "source_url": "https://issuer.example/ar.pdf", "pdf_page": 9}
        pack = {"schema_version": 1, "ticker": "TEST", "company": "Example",
                "periods": [{"period": "FY2024-25", "basis": "STANDALONE",
                             "facts": {"total_assets": fact},
                             "review_status": "PENDING_META_REVIEW", "creates_evidence": False}]}
        return workflow, pack

    def test_prepare_exposes_source_bound_human_queue(self):
        with TemporaryDirectory() as directory:
            workflow, pack = self.setup_workflow(Path(directory))
            item, statement = workflow.prepare(pack, "BALANCE_SHEET")[0]
            self.assertEqual(item.status, "AWAITING_HUMAN_DECISION")
            self.assertEqual(item.figure_count, 1); self.assertEqual(item.source_pages, (9,))
            self.assertEqual(statement["statement_type"], "BALANCE_SHEET")

    def test_approve_records_decision_and_materializes(self):
        with TemporaryDirectory() as directory:
            workflow, pack = self.setup_workflow(Path(directory)); now = datetime.now(timezone.utc)
            review, governed = workflow.decide(
                pack, "BALANCE_SHEET", period="FY2024-25", basis="STANDALONE",
                review_id="H-1", reviewer="Reviewer", decision="APPROVE", confidence=88,
                rationale="Compared exact source statement and units.", reviewed_at=now)
            self.assertEqual(review.decision, "APPROVE"); self.assertIsNotNone(governed)
            self.assertEqual(workflow.prepare(pack, "BALANCE_SHEET")[0][0].status, "DECISION_RECORDED")

    def test_hold_is_permanent_but_never_materializes(self):
        with TemporaryDirectory() as directory:
            workflow, pack = self.setup_workflow(Path(directory)); now = datetime.now(timezone.utc)
            review, governed = workflow.decide(
                pack, "BALANCE_SHEET", period="FY2024-25", basis="STANDALONE",
                review_id="H-1", reviewer="Reviewer", decision="HOLD", confidence=None,
                rationale="Source note needs clarification.", reviewed_at=now)
            self.assertEqual(review.decision, "HOLD"); self.assertIsNone(governed)
            self.assertFalse((Path(directory) / "annual.jsonl").exists())
            with self.assertRaisesRegex(ValueError, "already"):
                workflow.decide(pack, "BALANCE_SHEET", period="FY2024-25", basis="STANDALONE",
                                review_id="H-2", reviewer="Reviewer", decision="APPROVE", confidence=80,
                                rationale="Second decision not allowed.", reviewed_at=now)

    def test_selection_and_duplicate_periods_fail_closed(self):
        with TemporaryDirectory() as directory:
            workflow, pack = self.setup_workflow(Path(directory)); now = datetime.now(timezone.utc)
            with self.assertRaisesRegex(ValueError, "exactly one"):
                workflow.decide(pack, "BALANCE_SHEET", period="FY2023-24", basis="STANDALONE",
                                review_id="H", reviewer="R", decision="HOLD", confidence=None,
                                rationale="Not found.", reviewed_at=now)
            pack["periods"].append(dict(pack["periods"][0]))
            with self.assertRaisesRegex(ValueError, "duplicate"):
                workflow.prepare(pack, "BALANCE_SHEET")


if __name__ == "__main__":
    unittest.main()
