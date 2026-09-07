import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from modules.company_intelligence.quarterly_note_draft_display import attach_note_drafts


class NoteDraftDisplayTests(unittest.TestCase):
    def display(self, **changes):
        draft = {'ticker': 'TEST', 'document_hash': 'a'*64, 'target_period_end': '2026-06-30',
                 'status': 'ASSISTANT_RESEARCH_DRAFT_NOT_HUMAN_APPROVED',
                 'creates_approved_facts': False, 'changes_verdict': False,
                 'assessments': [{'candidate_id': 'note', 'local_pdf_page': 2, 'explanation': 'Earlier quarter.'}]}
        draft.update(changes)
        with TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / 'data/company_intelligence'
            folder.mkdir(parents=True)
            (folder / 'test_quarterly_note_assessment_draft.json').write_text(json.dumps(draft), encoding='utf-8')
            notes = {'items': [{'id': 'note', 'page': 2}]}
            return attach_note_drafts(root, notes, ticker='TEST', document_hash='a'*64,
                                      period_end='2026-06-30')['items'][0]['assistantDraft']

    def test_matching_draft_is_labelled(self):
        self.assertEqual(self.display()['status'], 'ASSISTANT_DRAFT_NOT_APPROVED')

    def test_other_company_withheld(self):
        self.assertIsNone(self.display(ticker='OTHER'))

    def test_other_hash_withheld(self):
        self.assertIsNone(self.display(document_hash='b'*64))

    def test_other_period_withheld(self):
        self.assertIsNone(self.display(target_period_end='2026-03-31'))

    def test_approval_claim_withheld(self):
        self.assertIsNone(self.display(creates_approved_facts=True))

    def test_wrong_page_withheld(self):
        self.assertIsNone(self.display(assessments=[{'candidate_id':'note', 'local_pdf_page':3, 'explanation':'Wrong page'}]))

    def test_duplicates_withheld(self):
        entry = {'candidate_id':'note', 'local_pdf_page':2, 'explanation':'Duplicate'}
        self.assertIsNone(self.display(assessments=[entry, entry]))

    def test_malformed_assessments_do_not_crash(self):
        self.assertIsNone(self.display(assessments=None))
