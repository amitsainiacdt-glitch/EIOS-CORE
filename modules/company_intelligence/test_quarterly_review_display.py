import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from modules.company_intelligence.quarterly_review_display import load_quarterly_review_display, display_reporting_notes


class QuarterlyDisplayTests(unittest.TestCase):
    def note(self):
        return {'candidate_id': 'note', 'document_hash': 'a'*64, 'pdf_page': 2, 'topic': 'COMPARABILITY',
                'source_passage': 'Figures may not be comparable.', 'review_question': 'Check the affected basis.'}

    def test_note_keeps_source_text_and_page(self):
        result = display_reporting_notes({'candidates': [self.note()]}, 'a'*64)
        self.assertEqual(result['items'][0]['page'], 2)
        self.assertEqual(result['items'][0]['passage'], self.note()['source_passage'])

    def test_foreign_document_note_is_withheld(self):
        result = display_reporting_notes({'candidates': [self.note()]}, 'b'*64)
        self.assertEqual(result['items'], [])
        self.assertEqual(result['invalidCount'], 1)

    def test_duplicate_note_not_repeated(self):
        self.assertEqual(len(display_reporting_notes({'candidates': [self.note(), self.note()]}, 'a'*64)['items']), 1)

    def test_empty_workspace_has_no_candidate_values(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(load_quarterly_review_display(Path(folder), 'EXAMPLE')['items'], [])

    def test_invalid_packet_does_not_crash_dashboard(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            packet = root / 'data/runtime/quarterly_intake/run/quarterly-candidates.json'
            packet.parent.mkdir(parents=True)
            packet.write_text('{broken', encoding='utf-8')
            result = load_quarterly_review_display(root, 'EXAMPLE')
            self.assertEqual(result['items'], [])
            self.assertEqual(result['invalidPacketCount'], 1)

    def test_another_company_never_leaks_into_panel(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            packet = root / 'data/runtime/quarterly_intake/run/quarterly-candidates.json'
            packet.parent.mkdir(parents=True)
            packet.write_text(json.dumps({'candidates': [{'candidate_id':'a'}], 'quarterly_record_evidence': {
                'a': {'source_column': {'ticker':'OTHER'}}}}), encoding='utf-8')
            result = load_quarterly_review_display(root, 'EXAMPLE')
            self.assertEqual(result['items'], [])
            self.assertEqual(result['invalidPacketCount'], 0)
