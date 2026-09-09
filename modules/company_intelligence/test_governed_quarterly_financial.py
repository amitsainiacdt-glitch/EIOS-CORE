from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from dataclasses import replace
from hashlib import sha256

from modules.company_intelligence import test_quarterly_record_candidates as fixtures
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.governed_company_fact import GovernedCompanyFactRepository
from modules.company_intelligence.governed_quarterly_financial import GovernedQuarterlyFinancialRepository
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_review_bridge import quarterly_review_candidate
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials
from modules.intelligence_write import InformationClass, ValidationStatus, WriteReceiptStatus


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
            repo=GovernedQuarterlyFinancialRepository(root/'quarterly.jsonl')
            item=repo.materialize(candidate,fact,evidence,assessment,created_at=now)
            self.assertEqual(item.figures_inr_crore['revenue'],'100')
            self.assertEqual(item.figures_inr_crore['pat'],'10')
            self.assertFalse(item.changes_verdict); self.assertFalse(item.authorizes_trade)
            receipt=repo.controlled_write_service.receipts()[-1]
            self.assertEqual(receipt.status,WriteReceiptStatus.ACCEPTED)
            self.assertEqual(item.controlled_write_receipt_id,receipt.receipt_id)
            controlled=repo.controlled_write_service.get_record(receipt.record_id)
            self.assertEqual(controlled.information_class,InformationClass.FACT)
            self.assertEqual(controlled.validation_status,ValidationStatus.VERIFIED)
            self.assertEqual(controlled.payload['value']['revenue'],'100')
            restored=GovernedQuarterlyFinancialRepository(root/'quarterly.jsonl')
            self.assertEqual(restored.read_all(),(item,))
            self.assertEqual(restored.controlled_write_service.get_record(receipt.record_id),controlled)

    def test_incomplete_checks_and_tampering_are_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); candidate,fact,evidence,assessment,now=self.inputs(root); repo=GovernedQuarterlyFinancialRepository(root/'q.jsonl')
            held={**assessment,'decision':'HOLD_FOR_REPORTING_NOTE_REVIEW'}
            with self.assertRaisesRegex(ValueError,'not cleared'): repo.materialize(candidate,fact,evidence,held,created_at=now)
            self.assertFalse((root/'controlled-intelligence-write-journal.jsonl').exists())
            evidence['values_inr_crore']['revenue']='999'
            with self.assertRaisesRegex(ValueError,'current evidence'): repo.materialize(candidate,fact,evidence,assessment,created_at=now)

    def test_duplicate_is_rejected(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); values=self.inputs(root); repo=GovernedQuarterlyFinancialRepository(root/'q.jsonl')
            repo.materialize(*values[:4],created_at=values[4])
            with self.assertRaisesRegex(ValueError,'already'): repo.materialize(*values[:4],created_at=values[4])

    def test_controlled_conflict_blocks_quarterly_materialization(self):
        with TemporaryDirectory() as directory:
            root=Path(directory); candidate,fact,evidence,assessment,now=self.inputs(root)
            repo=GovernedQuarterlyFinancialRepository(root/'q.jsonl')
            source=evidence['source_column']; figures=assessment['figures_for_review_inr_crore']
            normalized={name:repo._number(figures[name],name) for name in repo.REQUIRED}
            record_id=sha256(f'{fact.fact_id}\n{assessment["record_fingerprint"]}\nGOVERNED_QUARTERLY_V1'.encode()).hexdigest()
            command=repo.controlled_write_adapter.build_command(
                candidate=candidate,fact=fact,source=source,figures=normalized,
                record_id=record_id,created_at=now)
            conflicting=replace(
                command,command_id='seed-conflict',idempotency_key='seed-conflict',
                payload={**command.payload,'value':{**command.payload['value'],'revenue':'999'}})
            self.assertEqual(repo.controlled_write_service.submit(conflicting).status,WriteReceiptStatus.ACCEPTED)
            with self.assertRaisesRegex(ValueError,'controlled quarterly Fact write blocked'):
                repo.materialize(candidate,fact,evidence,assessment,created_at=now)
            self.assertFalse((root/'q.jsonl').exists())
            self.assertEqual(repo.controlled_write_service.trusted_records(),())


if __name__ == '__main__': unittest.main()
