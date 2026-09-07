import unittest
from modules.company_intelligence.quarterly_reporting_notes import extract_reporting_notes


class ReportingNoteTests(unittest.TestCase):
    def test_page_and_original_passage_preserved(self):
        text = '3 Consolidated figures may not be comparable due to an acquisition.'
        result = extract_reporting_notes(['First page',text], 'a'*64)
        item = result['candidates'][0]
        self.assertEqual(item['pdf_page'], 2)
        self.assertEqual(item['source_passage'], text)
        self.assertEqual(item['topic'], 'COMPARABILITY')
        self.assertFalse(result['review_complete'])

    def test_audit_word_alone_is_not_a_review(self):
        result = extract_reporting_notes(['Audited figures. Audit committee.'], 'a'*64)
        self.assertEqual(result['candidates'], [])

    def test_review_disclaimer_detected(self):
        result = extract_reporting_notes(['We do not express an audit opinion.'], 'a'*64)
        self.assertEqual(result['candidates'][0]['topic'], 'LIMITED_REVIEW')

    def test_negation_not_converted_to_restatement_claim(self):
        result = extract_reporting_notes(['No figures were restated.'], 'a'*64)
        self.assertEqual(result['candidates'][0]['source_passage'], 'No figures were restated.')
        self.assertIn('keyword alone', result['candidates'][0]['review_question'])

    def test_missing_text_not_clean_bill_of_health(self):
        result = extract_reporting_notes([''], 'a'*64)
        self.assertEqual(result['pages_without_text'], [1])
        self.assertFalse(result['absence_proves_no_issue'])

    def test_notes_separated(self):
        result = extract_reporting_notes(['2 An impairment was recognised.\n5 These are balancing figures.'], 'a'*64)
        self.assertEqual(len(result['candidates']), 2)
        self.assertNotEqual(result['candidates'][0]['candidate_id'], result['candidates'][1]['candidate_id'])
