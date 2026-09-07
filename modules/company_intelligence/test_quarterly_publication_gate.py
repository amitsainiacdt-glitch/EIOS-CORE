from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence import test_quarterly_record_candidates as fixtures
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_review_bridge import quarterly_review_candidate
from modules.company_intelligence.quarterly_note_human_review import QuarterlyNoteReviewLedger
from modules.company_intelligence.quarterly_publication_gate import quarterly_approval_assessment


class QuarterlyPublicationGateTests(unittest.TestCase):
    def inputs(self):
        record = build_record_candidates(*fixtures.RecordCandidateTests().fixture())['records'][0]
        candidate = quarterly_review_candidate(record, company='Example Company', source_url='https://example.org/report.pdf')
        note = {'candidate_id': 'NOTE-1', 'document_hash': candidate.document_hash, 'pdf_page': 2,
                'topic': 'LIMITED_REVIEW', 'source_passage': 'Limited review applies to the standalone quarter.',
                'review_question': 'Does this apply?'}
        verification = {'status': 'ACQUISITION_RECEIPT_PRESERVED_PENDING_REVIEW',
            'provider_id': 'EIOS_CORROBORATED_BROWSER_CAPTURE', 'document_hash': candidate.document_hash,
            'source_url': candidate.source_url, 'creates_approved_facts': False}
        return candidate, {'quarterly_record_evidence': {candidate.candidate_id: record},
                           'reporting_notes': {'candidates': [note]}, 'source_verification': verification}, note

    def test_note_hold_blocks_quarterly_approval(self):
        with TemporaryDirectory() as directory:
            candidate, queue, _ = self.inputs()
            with self.assertRaisesRegex(ValueError, 'REPORTING_NOTES'):
                quarterly_approval_assessment(candidate, queue, Path(directory) / 'notes.jsonl')

    def test_all_six_checks_permit_human_fact_approval_stage_only(self):
        with TemporaryDirectory() as directory:
            candidate, queue, note = self.inputs(); path = Path(directory) / 'notes.jsonl'
            QuarterlyNoteReviewLedger(path).record(note, review_id='REV-1', document_hash=candidate.document_hash,
                company=candidate.company, period_end='2026-06-30', basis='STANDALONE', decision='APPLIES',
                rationale='Checked the exact note against the selected quarter.', reviewed_at=datetime.now(timezone.utc), reviewer='Reviewer')
            result = quarterly_approval_assessment(candidate, queue, path)
            self.assertEqual(result['decision'], 'READY_FOR_HUMAN_FACT_APPROVAL')
            self.assertFalse(result['creates_approved_facts'])
            self.assertFalse(result['changes_verdict'])

    def test_wrong_document_source_stays_blocked(self):
        with TemporaryDirectory() as directory:
            candidate, queue, _ = self.inputs(); queue['source_verification']['document_hash'] = 'b' * 64
            with self.assertRaisesRegex(ValueError, 'OFFICIAL_SOURCE'):
                quarterly_approval_assessment(candidate, queue, Path(directory) / 'notes.jsonl')


if __name__ == '__main__': unittest.main()
