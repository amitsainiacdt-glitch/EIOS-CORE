from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate
from modules.company_intelligence.governed_company_fact import GovernedCompanyFactRepository


def candidate():
    return CompanyFactReviewCandidate(
        1, "CANDIDATE-1", "Coromandel International", "CAPACITY_CHANGE", "ASSERTED",
        "Coromandel International commissioned capacity worth INR 125 crore on 28 August 2026.",
        ("INR 125 crore",), ("28 August 2026",), 7,
        "https://www.coromandel.biz/report.pdf", "a" * 64, "EXT-1", "pypdf_text_layer_v1",
    )


class CompanyFactHumanReviewTests(unittest.TestCase):
    def test_approved_review_materializes_governed_fact_only(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); now = datetime.now(timezone.utc)
            item = candidate(); meta = CompanyCandidateMetaReviewEngine().assess(item, reviewed_at=now)
            review = CompanyFactHumanReviewLedger(root / "reviews.jsonl").record(
                item, meta, review_id="REV-1", decision="APPROVE", approved_confidence=82,
                rationale="Official passage and page citation reviewed against the archived document.",
                reviewed_at=now, reviewer="Human Reviewer",
            )
            fact = GovernedCompanyFactRepository(root / "facts.jsonl").materialize(item, meta, review, created_at=now)
            self.assertEqual(fact.status, "GOVERNED_FACT")
            self.assertFalse(fact.creates_evidence)
            self.assertFalse(fact.creates_catalyst)
            self.assertFalse(fact.changes_verdict)

    def test_hold_cannot_materialize_and_second_review_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); now = datetime.now(timezone.utc)
            item = candidate(); meta = CompanyCandidateMetaReviewEngine().assess(item, reviewed_at=now)
            ledger = CompanyFactHumanReviewLedger(root / "reviews.jsonl")
            review = ledger.record(item, meta, review_id="REV-1", decision="HOLD", rationale="Independent confirmation remains incomplete.", reviewed_at=now, reviewer="Reviewer")
            with self.assertRaisesRegex(ValueError, "approved"):
                GovernedCompanyFactRepository(root / "facts.jsonl").materialize(item, meta, review, created_at=now)
            with self.assertRaisesRegex(ValueError, "already"):
                ledger.record(item, meta, review_id="REV-2", decision="REJECT", rationale="Duplicate decision attempt.", reviewed_at=now, reviewer="Reviewer")

    def test_tampered_candidate_breaks_review_binding(self):
        with TemporaryDirectory() as directory:
            root = Path(directory); now = datetime.now(timezone.utc)
            item = candidate(); meta = CompanyCandidateMetaReviewEngine().assess(item, reviewed_at=now)
            review = CompanyFactHumanReviewLedger(root / "reviews.jsonl").record(
                item, meta, review_id="REV-1", decision="APPROVE", approved_confidence=80,
                rationale="Reviewed exact official passage and citation.", reviewed_at=now, reviewer="Reviewer",
            )
            tampered = replace(item, source_passage="Altered statement")
            with self.assertRaisesRegex(ValueError, "current candidate"):
                GovernedCompanyFactRepository(root / "facts.jsonl").materialize(tampered, meta, review, created_at=now)


if __name__ == "__main__":
    unittest.main()
