from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from modules.company_intelligence import test_quarterly_record_candidates as record_tests
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_review_bridge import quarterly_review_candidate, write_quarterly_review_queue
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger


class QuarterlyReviewBridgeTests(unittest.TestCase):
    def record(self):
        return build_record_candidates(*record_tests.RecordCandidateTests().fixture())['records'][0]

    def candidate(self):
        return quarterly_review_candidate(self.record(), company='Example Company', source_url='https://example.org/report.pdf')

    def test_local_origin_and_event_type_preserved(self):
        candidate = self.candidate()
        meta = CompanyCandidateMetaReviewEngine().assess(candidate, reviewed_at=datetime.now(timezone.utc))
        self.assertEqual(candidate.event_type, 'QUARTERLY_FINANCIAL_RESULT')
        self.assertIn('LOCAL_IMPORT_ORIGIN_REQUIRES_INDEPENDENT_REVIEW', meta.reason_codes)
        self.assertEqual(meta.decision, 'HOLD_FOR_RESEARCH')

    def test_changed_company_changes_identity(self):
        candidate = quarterly_review_candidate(self.record(), company='Another Company', source_url='https://example.org/report.pdf')
        self.assertNotEqual(candidate.candidate_id, self.candidate().candidate_id)
        self.assertEqual(self.candidate().candidate_id, self.candidate().candidate_id)

    def test_altered_values_rejected(self):
        record = self.record()
        record['values_inr_crore']['revenue'] = '999'
        with self.assertRaises(ValueError):
            quarterly_review_candidate(record, company='Example Company', source_url='https://example.org/report.pdf')

    def test_held_record_not_queued(self):
        record = self.record()
        record['status'] = 'HOLD'
        self.assertIsNone(quarterly_review_candidate(record, company='Example Company', source_url=''))

    def test_queue_contains_meta_and_evidence_but_no_approval(self):
        with TemporaryDirectory() as directory:
            report = {'ocr_pages': [{'record_candidates': {'records': [self.record(), self.record()]}}]}
            result = write_quarterly_review_queue(report, output_directory=directory,
                company='Example Company', source_url='https://example.org/report.pdf')
            self.assertEqual(result['candidate_count'], 1)
            self.assertEqual(result['meta_held_count'], 1)
            self.assertEqual(result['human_review_ready'], 0)
            self.assertTrue(Path(result['meta_path']).exists())

    def test_existing_human_ledger_blocks_approval(self):
        candidate = self.candidate()
        now = datetime.now(timezone.utc)
        meta = CompanyCandidateMetaReviewEngine().assess(candidate, reviewed_at=now)
        with TemporaryDirectory() as directory:
            ledger = CompanyFactHumanReviewLedger(Path(directory) / 'reviews.jsonl')
            with self.assertRaises(ValueError):
                ledger.record(candidate, meta, review_id='test', decision='APPROVE',
                    rationale='Arithmetic is not enough', reviewed_at=now, reviewer='TEST', approved_confidence=90)
            self.assertFalse(ledger.path.exists())
