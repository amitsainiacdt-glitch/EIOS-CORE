from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from modules.company_intelligence.financial_review_examples import build_cash_flow_review_examples
from modules.company_intelligence.source_review_regression import check_source_review_regression


class SourceReviewRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.document = self.root / 'sample.pdf'
        self.document.write_bytes(b'synthetic source bytes for fingerprint test only')
        digest = sha256(self.document.read_bytes()).hexdigest()
        fact = dict(unit='INR_CRORE', raw_unit='INR_LAKH', document_hash=digest,
                    pdf_page=1, column=1, column_periods=['FY2024-25', 'FY2023-24'],
                    source_passage='Synthetic test row', source_url='https://example.com/sample.pdf')
        self.pack = {'company': 'Test Company', 'periods': [{'period': 'FY2024-25', 'basis': 'STANDALONE',
            'review_status': 'PENDING_META_REVIEW', 'creates_evidence': False,
            'facts': {'operating_cash_flow': {**fact, 'value': 2, 'raw_value': '200'},
                      'cash_capex': {**fact, 'value': 3, 'raw_value': '(300)'}},
            'derived': {'free_cash_flow': -1, 'free_cash_flow_definition': 'Test definition'}}]}
        example = build_cash_flow_review_examples(self.pack)['examples'][0]
        self.review = {'schema_version': 1, 'reviewer_type': 'AI_ASSISTANT',
            **{flag: False for flag in ('human_approval', 'meta_approval', 'creates_evidence', 'changes_verdict', 'counts_as_human_learning_feedback')},
            'checks': [{'example_id': example['example_id'], 'period': 'FY2024-25',
                'local_document': 'sample.pdf', 'document_hash': digest, 'pdf_page': 1, 'column': 1,
                'operating_cash_crore': 2, 'fixed_asset_spending_magnitude_crore': 3, 'calculated_free_cash_flow_crore': -1}]}
        self.pack_path = self.root / 'pack.json'
        self.review_path = self.root / 'review.json'

    def check(self):
        self.pack_path.write_text(json.dumps(self.pack))
        self.review_path.write_text(json.dumps(self.review))
        return check_source_review_regression(self.root, self.review_path, self.pack_path)

    def test_unchanged_references_pass_without_approval(self):
        report = self.check()
        self.assertEqual(report['status'], 'SAVED_EXAMPLES_UNCHANGED')
        self.assertEqual(report['checked_examples'], 1)
        self.assertFalse(report['human_approval'])

    def test_changed_and_missing_documents_trigger_review(self):
        self.document.write_bytes(b'changed')
        self.assertEqual(self.check()['status'], 'RECHECK_REQUIRED')
        self.document.unlink()
        self.assertEqual(self.check()['issues'][0]['reason'], 'SOURCE_FILE_MISSING')

    def test_changed_extracted_values_trigger_review(self):
        self.pack['periods'][0]['facts']['operating_cash_flow']['value'] = 100
        self.assertEqual(self.check()['status'], 'RECHECK_REQUIRED')

    def test_reference_cannot_claim_human_approval(self):
        self.review['human_approval'] = True
        self.assertEqual(self.check()['status'], 'RECHECK_REQUIRED')

    def test_document_path_cannot_escape_workspace(self):
        self.review['checks'][0]['local_document'] = '../outside.pdf'
        self.assertEqual(self.check()['status'], 'RECHECK_REQUIRED')

    def test_no_reference_is_not_a_successful_check(self):
        report = check_source_review_regression(self.root, self.review_path, self.pack_path)
        self.assertEqual(report['status'], 'NO_REFERENCE_CHECKS')
        self.assertEqual(report['checked_examples'], 0)
