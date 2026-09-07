from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from modules.company_intelligence.quarterly_note_human_review import QuarterlyNoteReviewLedger


def note(identifier='NOTE-1', passage='Limited review applies to these standalone results.'):
    return {'candidate_id': identifier, 'document_hash': 'a' * 64, 'pdf_page': 2,
            'topic': 'LIMITED_REVIEW', 'source_passage': passage,
            'review_question': 'Does this apply to the selected quarter?'}


class QuarterlyNoteHumanReviewTests(unittest.TestCase):
    def test_all_exact_context_decisions_clear_note_review_only(self):
        with TemporaryDirectory() as directory:
            ledger = QuarterlyNoteReviewLedger(Path(directory) / 'reviews.jsonl')
            now = datetime.now(timezone.utc)
            for index, item in enumerate((note(), note('NOTE-2', 'Historical impairment does not affect this quarter.')), 1):
                ledger.record(item, review_id=f'REV-{index}', document_hash='a' * 64,
                    company='Example Ltd', period_end='2026-06-30', basis='STANDALONE',
                    decision='APPLIES' if index == 1 else 'DOES_NOT_APPLY',
                    rationale='Checked the complete note against the selected column.', reviewed_at=now, reviewer='Reviewer')
            result = ledger.apply({'candidates': [note(), note('NOTE-2', 'Historical impairment does not affect this quarter.')]},
                document_hash='a' * 64, company='Example Ltd', period_end='2026-06-30', basis='STANDALONE')
            self.assertTrue(result['review_complete'])
            self.assertEqual(result['reviewed_count'], 2)

    def test_unresolved_or_missing_decision_keeps_hold(self):
        with TemporaryDirectory() as directory:
            ledger = QuarterlyNoteReviewLedger(Path(directory) / 'reviews.jsonl')
            ledger.record(note(), review_id='REV-1', document_hash='a' * 64, company='Example Ltd',
                period_end='2026-06-30', basis='STANDALONE', decision='UNRESOLVED',
                rationale='The passage scope is not clear enough to decide.', reviewed_at=datetime.now(timezone.utc), reviewer='Reviewer')
            result = ledger.apply({'candidates': [note(), note('NOTE-2')]}, document_hash='a' * 64,
                company='Example Ltd', period_end='2026-06-30', basis='STANDALONE')
            self.assertFalse(result['review_complete'])

    def test_period_basis_and_tampered_passage_do_not_transfer(self):
        with TemporaryDirectory() as directory:
            ledger = QuarterlyNoteReviewLedger(Path(directory) / 'reviews.jsonl'); now = datetime.now(timezone.utc)
            ledger.record(note(), review_id='REV-1', document_hash='a' * 64, company='Example Ltd',
                period_end='2026-06-30', basis='STANDALONE', decision='APPLIES',
                rationale='Checked the exact note and selected reporting column.', reviewed_at=now, reviewer='Reviewer')
            other = ledger.apply({'candidates': [note()]}, document_hash='a' * 64, company='Example Ltd',
                period_end='2026-06-30', basis='CONSOLIDATED')
            self.assertFalse(other['review_complete'])
            with self.assertRaisesRegex(ValueError, 'current note passage'):
                ledger.apply({'candidates': [note(passage='Changed passage')]}, document_hash='a' * 64,
                    company='Example Ltd', period_end='2026-06-30', basis='STANDALONE')

    def test_later_decision_supersedes_without_erasing_audit_history(self):
        with TemporaryDirectory() as directory:
            ledger = QuarterlyNoteReviewLedger(Path(directory) / 'reviews.jsonl'); now = datetime.now(timezone.utc)
            args = dict(review_id='REV-1', document_hash='a' * 64, company='Example Ltd', period_end='2026-06-30',
                        basis='STANDALONE', decision='APPLIES', rationale='Checked exact source context.', reviewed_at=now, reviewer='Reviewer')
            ledger.record(note(), **args)
            ledger.record(note(), **{**args, 'review_id': 'REV-2', 'decision': 'DOES_NOT_APPLY'})
            self.assertEqual(len(ledger.read_all()), 2)
            result = ledger.apply({'candidates': [note()]}, document_hash='a' * 64,
                company='Example Ltd', period_end='2026-06-30', basis='STANDALONE')
            self.assertEqual(result['candidates'][0]['human_review']['decision'], 'DOES_NOT_APPLY')


if __name__ == '__main__': unittest.main()
