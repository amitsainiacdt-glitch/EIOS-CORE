from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence import test_quarterly_record_candidates as fixtures
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.governed_company_fact import GovernedCompanyFactRepository
from modules.company_intelligence.governed_quarterly_financial import GovernedQuarterlyFinancialRepository
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_review_bridge import quarterly_review_candidate
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials


class GovernedQuarterlyFinancialTests(unittest.TestCase):
    def inputs(self, root):
        evidence = build_record_candidates(*fixtures.RecordCandidateTests().fixture())['records'][0]
        candidate = quarterly_review_candidate(evidence, company='Example Company', source_url='https://example.org/report.pdf')
        now = datetime.now(timezone.utc)
        verification = {'status':'ACQUISITION_RECEIPT_PRESERVED_PENDING_REVIEW', 'provider_id':'EIOS_CORROBORATED_BROWSER_CAPTURE',
                        'document_hash':candidate.document_hash, 'source_url':candidate.source_url}
        meta = CompanyCandidateMetaReviewEngine().assess(candidate, reviewed_at=now, source_verification=verification)
        review = CompanyFactHumanReviewLedger(root/'human.jsonl').record(candidate, meta, review_id='H-1', decision='APPROVE',
            approved_confidence=85, rationale='Reviewed the exact quarterly result and all required notes.', reviewed_at=now, reviewer='Reviewer')
        fact = GovernedCompanyFactRepository(root/'facts.jsonl').materialize(candidate, meta, review, created_at=now)
        assessment = assess_quarterly_financials(evidence, source_verification=verification, reporting_notes={'review_complete':True})
        return candidate, fact, evidence, assessment, now

    def test_materializes_exact_figures_without_verdict_authority(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); candidate,fact,evidence,assessment,now=self.inputs(root)
            item=GovernedQuarterlyFinancialRepository(root/'quarterly.jsonl').materialize(candidate,fact,evidence,assessment,created_at=now)
            self.assertEqual(item.figures_inr_crore['revenue'],'100')
            self.assertEqual(item.figures_inr_crore['pat'],'10')
            self.assertFalse(item.changes_verdict); self.assertFalse(item.authorizes_trade)

    def test_incomplete_checks_and_tampering_are_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); candidate,fact,evidence,assessment,now=self.inputs(root); repo=GovernedQuarterlyFinancialRepository(root/'q.jsonl')
            held={**assessment,'decision':'HOLD_FOR_REPORTING_NOTE_REVIEW'}
            with self.assertRaisesRegex(ValueError,'not cleared'): repo.materialize(candidate,fact,evidence,held,created_at=now)
            evidence['values_inr_crore']['revenue']='999'
            with self.assertRaisesRegex(ValueError,'current evidence'): repo.materialize(candidate,fact,evidence,assessment,created_at=now)

    def test_duplicate_is_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); values=self.inputs(root); repo=GovernedQuarterlyFinancialRepository(root/'q.jsonl')
            repo.materialize(*values[:4],created_at=values[4])
            with self.assertRaisesRegex(ValueError,'already'): repo.materialize(*values[:4],created_at=values[4])


if __name__ == '__main__': unittest.main()
