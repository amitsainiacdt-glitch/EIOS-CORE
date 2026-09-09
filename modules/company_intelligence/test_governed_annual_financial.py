from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.governed_annual_financial import (
    AnnualFinancialHumanReviewLedger, GovernedAnnualFinancialRepository,
)
from modules.intelligence_write import InformationClass, ValidationStatus, WriteReceiptStatus


class GovernedAnnualFinancialTests(unittest.TestCase):
    def inputs(self, root, statement_type="BALANCE_SHEET"):
        now = datetime.now(timezone.utc); digest = "a" * 64
        statement = {
            "statement_type": statement_type, "period": "FY2024-25", "basis": "STANDALONE",
            "facts": {"total_assets" if statement_type == "BALANCE_SHEET" else "operating_cash_flow": {
                "value": 125.5, "unit": "INR_CRORE", "document_hash": digest,
                "source_url": "https://issuer.example/annual.pdf", "pdf_page": 100}},
            "review_status": "PENDING_META_REVIEW", "creates_evidence": False,
        }
        repo = GovernedAnnualFinancialRepository(root / "annual.jsonl")
        review = AnnualFinancialHumanReviewLedger(root / "annual-reviews.jsonl").record(
            statement, review_id="H-1", reviewer="Human Reviewer", decision="APPROVE", confidence=90,
            rationale="Checked the exact source page, period, basis, units and figures.", reviewed_at=now)
        return repo, statement, review, now

    def test_human_approved_balance_sheet_becomes_verified_fact(self):
        with TemporaryDirectory() as directory:
            repo, statement, review, now = self.inputs(Path(directory))
            item = repo.materialize(statement, review, ticker="TEST", company="Example", created_at=now)
            receipt = repo.controlled_write_service.receipts()[-1]
            record = repo.controlled_write_service.get_record(receipt.record_id)
            self.assertEqual(receipt.status, WriteReceiptStatus.ACCEPTED)
            self.assertEqual(record.information_class, InformationClass.FACT)
            self.assertEqual(record.validation_status, ValidationStatus.VERIFIED)
            self.assertEqual(record.payload["value"]["total_assets"], "125.5")
            self.assertEqual(GovernedAnnualFinancialRepository(Path(directory) / "annual.jsonl").read_all(), (item,))

    def test_cash_flow_uses_separate_semantic_identity(self):
        with TemporaryDirectory() as directory:
            repo, statement, review, now = self.inputs(Path(directory), "CASH_FLOW")
            item = repo.materialize(statement, review, ticker="TEST", company="Example", created_at=now)
            receipt = repo.controlled_write_service.receipts()[-1]
            self.assertEqual(item.statement_type, "CASH_FLOW")
            self.assertIn("annual-cash-flow", repo.controlled_write_service.get_record(receipt.record_id).semantic_key)

    def test_pending_or_changed_statement_cannot_bypass_human_review(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); repo, statement, review, now = self.inputs(root)
            with self.assertRaisesRegex(ValueError, "bind"):
                repo.materialize({**statement, "period": "FY2023-24"}, review,
                                 ticker="TEST", company="Example", created_at=now)
            with self.assertRaisesRegex(ValueError, "fail-closed"):
                changed = {**statement, "review_status": "APPROVED"}
                changed_review = AnnualFinancialHumanReviewLedger(root / "changed-reviews.jsonl").record(
                    changed, review_id="H-2", reviewer="Human Reviewer", decision="APPROVE", confidence=90,
                    rationale="Checked changed candidate.", reviewed_at=now)
                repo.materialize(changed, changed_review,
                                 ticker="TEST", company="Example", created_at=now)
            self.assertFalse((root / "controlled-intelligence-write-journal.jsonl").exists())

    def test_source_mismatch_and_machine_shaped_review_are_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); repo, statement, review, now = self.inputs(root)
            bad = {**statement, "facts": {**statement["facts"], "cash": {
                "value": 1, "unit": "INR_CRORE", "document_hash": "b" * 64,
                "source_url": "https://other.example/a.pdf", "pdf_page": 2}}}
            with self.assertRaisesRegex(ValueError, "same source"):
                AnnualFinancialHumanReviewLedger(root / "bad-reviews.jsonl").record(
                    bad, review_id="H-BAD", reviewer="Human Reviewer", decision="APPROVE", confidence=90,
                    rationale="Attempted mixed-source review.", reviewed_at=now)
            with self.assertRaisesRegex(ValueError, "persisted human review"):
                repo.materialize(statement, {"decision": "APPROVE"},
                                 ticker="TEST", company="Example", created_at=now)

    def test_controlled_conflict_blocks_materialization(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); repo, statement, review, now = self.inputs(root)
            first = repo.materialize(statement, review, ticker="TEST", company="Example", created_at=now)
            changed = {**statement, "facts": {"total_assets": {**statement["facts"]["total_assets"], "value": 999}}}
            changed_review = AnnualFinancialHumanReviewLedger(root / "changed-reviews.jsonl").record(
                changed, review_id="H-2", reviewer="Human Reviewer", decision="APPROVE", confidence=90,
                rationale="Checked exact competing statement.", reviewed_at=now)
            with self.assertRaisesRegex(ValueError, "controlled annual Fact write blocked"):
                repo.materialize(changed, changed_review, ticker="TEST", company="Example", created_at=now)
            self.assertEqual(repo.read_all(), (first,))
            self.assertEqual(repo.controlled_write_service.trusted_records(), ())

    def test_review_ledger_is_append_only_and_tamper_evident(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); repo, statement, review, _ = self.inputs(root)
            ledger = AnnualFinancialHumanReviewLedger(root / "annual-reviews.jsonl")
            self.assertEqual(ledger.read_all(), (review,))
            with self.assertRaisesRegex(ValueError, "already has"):
                ledger.record(statement, review_id="H-2", reviewer="Other", decision="HOLD", confidence=None,
                              rationale="Needs another page.", reviewed_at=review.reviewed_at)
            changed = (root / "annual-reviews.jsonl").read_text().replace('"confidence":90', '"confidence":91')
            (root / "annual-reviews.jsonl").write_text(changed)
            with self.assertRaisesRegex(ValueError, "fingerprint"):
                ledger.read_all()


if __name__ == "__main__":
    unittest.main()
