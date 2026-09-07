import unittest
from modules.company_intelligence import test_quarterly_record_candidates as fixtures
from modules.company_intelligence.quarterly_record_candidates import build_record_candidates
from modules.company_intelligence.quarterly_financial_review import assess_quarterly_financials


class QuarterlyFinancialReviewTests(unittest.TestCase):
    def record(self):
        return build_record_candidates(*fixtures.RecordCandidateTests().fixture())['records'][0]

    def test_checks_pass_but_origin_and_notes_stay_held(self):
        result = assess_quarterly_financials(self.record())
        self.assertTrue(result['technical_checks_passed'])
        self.assertEqual([c['status'] for c in result['checks']], ['PASS']*4 + ['HOLD']*2)
        self.assertFalse(result['creates_approved_facts'])

    def test_modified_header_caught(self):
        record = self.record()
        record['source_column']['header_text'] = 'STANDALONE Year ended INR crore 31 March 2026'
        self.assertFalse(assess_quarterly_financials(record)['technical_checks_passed'])

    def test_modified_image_reading_caught(self):
        record = self.record()
        record['source_column']['cells']['revenue']['source_reading']['ocr_text'] = '999'
        result = assess_quarterly_financials(record)
        self.assertFalse(result['technical_checks_passed'])
        self.assertEqual(result['figures_for_review_inr_crore'], {})

    def test_changed_cell_location_caught(self):
        record = self.record()
        record['source_column']['cells']['pat']['source_reading']['column_index'] = 7
        self.assertFalse(assess_quarterly_financials(record)['technical_checks_passed'])

    def test_missing_evidence_caught(self):
        result = assess_quarterly_financials({})
        self.assertFalse(result['technical_checks_passed'])

    def test_fingerprint_changes_with_evidence(self):
        record = self.record()
        before = assess_quarterly_financials(record)['record_fingerprint']
        record['source_column']['cells']['pat']['source_reading']['ocr_text'] = '100'
        self.assertNotEqual(before, assess_quarterly_financials(record)['record_fingerprint'])

    def test_corroborated_delivery_passes_source_but_notes_remain_held(self):
        record = self.record()
        source = record['source_column']
        result = assess_quarterly_financials(record, source_verification={
            'status': 'ACQUISITION_RECEIPT_PRESERVED_PENDING_REVIEW',
            'provider_id': 'EIOS_CORROBORATED_BROWSER_CAPTURE',
            'document_hash': source['document_hash'],
            'source_url': 'https://issuer.example/q1.pdf',
        }, reporting_notes={'review_complete': False, 'candidates': [{
            'topic': 'COMPARABILITY', 'source_passage': 'Standalone results for 30 June 2026 are not comparable.'
        }]})
        self.assertEqual(result['checks'][4]['status'], 'PASS')
        self.assertEqual(result['checks'][5]['status'], 'HOLD')
        self.assertEqual(result['decision'], 'HOLD_FOR_REPORTING_NOTE_REVIEW')
        self.assertEqual(result['reporting_note_assessments'][0]['applicability']['status'], 'APPLICABILITY_UNCONFIRMED')

    def test_unverified_local_inbox_does_not_pass_source(self):
        record = self.record()
        source = record['source_column']
        result = assess_quarterly_financials(record, source_verification={
            'status': 'ACQUISITION_RECEIPT_PRESERVED_PENDING_REVIEW',
            'provider_id': 'EIOS_GOVERNED_LOCAL_INBOX',
            'document_hash': source['document_hash'],
            'source_url': 'https://issuer.example/q1.pdf',
        })
        self.assertEqual(result['checks'][4]['status'], 'HOLD')
