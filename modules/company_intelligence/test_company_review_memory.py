from dataclasses import replace
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine, CompanyCandidateMetaReviewWriter
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.test_company_fact_human_review import candidate


class CompanyReviewMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'reviews.jsonl'
        self.now = datetime(2026, 9, 2, tzinfo=timezone.utc)
        self.item = candidate()
        self.engine = CompanyCandidateMetaReviewEngine()

    def record(self, decision):
        meta = self.engine.assess(self.item, reviewed_at=self.now)
        return CompanyFactHumanReviewLedger(self.path).record(
            self.item, meta, review_id='review-1', decision=decision,
            rationale='Test feedback, not real financial approval.', reviewer='Test reviewer',
            reviewed_at=self.now, approved_confidence=80 if decision == 'APPROVE' else None)

    def assess(self, item=None, at=None):
        return self.engine.assess(item or self.item, reviewed_at=at or self.now, review_ledger_path=self.path)

    def test_rejected_fact_is_remembered_across_runs_and_restarts(self):
        self.record('REJECT')
        replay = replace(self.item, candidate_id='new-run', extraction_id='new-extraction')
        result = self.assess(replay)
        self.assertEqual(result.decision, 'HOLD_FOR_RESEARCH')
        self.assertIn('REVIEW_MEMORY_REJECT_SAME_SOURCE_FACT', result.reason_codes)
        self.assertFalse(result.changes_verdict)

    def test_hold_is_remembered(self):
        self.record('HOLD')
        self.assertEqual(self.assess().decision, 'HOLD_FOR_RESEARCH')

    def test_approval_is_context_not_automatic_authority(self):
        self.record('APPROVE')
        result = self.assess()
        self.assertIn('REVIEW_MEMORY_APPROVE_SAME_SOURCE_FACT', result.reason_codes)
        self.assertTrue(result.requires_human_review)
        self.assertTrue(result.requires_mandatory_meta)
        self.assertFalse(result.creates_evidence)
        self.assertFalse(result.creates_catalyst)
        self.assertFalse(result.changes_verdict)

    def test_no_cross_company_document_page_or_number_learning(self):
        self.record('REJECT')
        for change in ({'company': 'Other Company'}, {'document_hash': 'b'*64}, {'pdf_page': 8},
                       {'source_passage': self.item.source_passage.replace('125', '250')},
                       {'explicit_amounts': ('INR 250 crore',)}):
            with self.subTest(change=change):
                self.assertFalse(any(code.startswith('REVIEW_MEMORY_') for code in self.assess(replace(self.item, **change)).reason_codes))

    def test_future_feedback_is_not_used_in_historical_assessments(self):
        self.record('REJECT')
        self.assertFalse(any(code.startswith('REVIEW_MEMORY_') for code in self.assess(at=self.now - timedelta(days=1)).reason_codes))

    def test_tampered_snapshot_blocks_memory(self):
        self.record('REJECT')
        payload = json.loads(self.path.read_text())
        payload['candidate_snapshot']['source_passage'] = 'Changed source'
        self.path.write_text(json.dumps(payload) + '\n')
        with self.assertRaisesRegex(ValueError, 'snapshot'):
            self.assess()

    def test_legacy_reviews_still_load_but_do_not_invent_learning_context(self):
        self.record('REJECT')
        payload = json.loads(self.path.read_text())
        payload.pop('candidate_snapshot')
        self.path.write_text(json.dumps(payload) + '\n')
        self.assertEqual(len(CompanyFactHumanReviewLedger(self.path).read_all()), 1)
        self.assertFalse(any(code.startswith('REVIEW_MEMORY_') for code in self.assess().reason_codes))

    def test_production_writer_consults_memory(self):
        self.record('REJECT')
        output = Path(self.temp.name) / 'meta.json'
        results = CompanyCandidateMetaReviewWriter().write([self.item], output_path=output, reviewed_at=self.now, review_ledger_path=self.path)
        self.assertEqual(results[0].decision, 'HOLD_FOR_RESEARCH')
        self.assertIn('REVIEW_MEMORY_REJECT_SAME_SOURCE_FACT', json.loads(output.read_text())['assessments'][0]['reason_codes'])


if __name__ == '__main__':
    unittest.main()
