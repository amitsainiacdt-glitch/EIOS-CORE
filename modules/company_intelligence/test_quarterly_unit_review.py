import copy
import unittest
from pathlib import Path
from modules.company_intelligence.quarterly_unit_review import apply_unit_reviews, validated_unit_reviews


class UnitReviewTests(unittest.TestCase):
    def fixture(self):
        digest = 'a' * 64
        base = {'document_hash': digest, 'pdf_page': 1, 'table_id': 't'}
        review = {**base, 'review_id': 'r', 'observed_text': '₹ in Crores',
                  'reviewer_kind': 'ASSISTANT_VISUAL_REVIEW', 'status': 'CANDIDATE_NOT_HUMAN_APPROVED'}
        page = {'pdf_page': 1, 'ruled_tables': [{'table_id': 't', 'columns': [
            {'column_index': 0, 'date_header_text': '30 June 2026'}]}]}
        binding = {'tables': [{'table_id': 't', 'unit_assessment': {'unit_candidates': ['crore'], 'issues': []},
            'spans': [{**base, 'kind': k, 'text': t, 'first_column': 0, 'last_column': 0}
                      for k,t in [('basis','STANDALONE'),('duration','Quarter ended')]],
            'columns': [{'column_index': 0, 'resolution': {'status': 'HOLD'},
                'date_comparison': {'status': 'DATE_READINGS_AGREE_PENDING_REVIEW',
                                    'native': {'date': '2026-06-30'}}}]}]}
        return binding, page, [review], digest

    def test_unit_candidate_not_approval_and_original_preserved(self):
        args = self.fixture()
        before = copy.deepcopy(args[0])
        result = apply_unit_reviews(*args)
        resolved = result['tables'][0]['columns'][0]['resolution']
        self.assertEqual(resolved['unit'], 'INR_CRORE')
        self.assertEqual(resolved['status'], 'HEADER_RECOGNIZED_PENDING_REVIEW')
        self.assertFalse(resolved['creates_approved_facts'])
        self.assertEqual(args[0], before)

    def test_different_document_never_inherits_unit(self):
        args = list(self.fixture())
        args[-1] = 'b' * 64
        self.assertEqual(apply_unit_reviews(*args), args[0])

    def test_duplicate_reviews_hold(self):
        args = self.fixture()
        args[2].append(copy.deepcopy(args[2][0]))
        self.assertEqual(apply_unit_reviews(*args), args[0])

    def test_currency_conflict_not_overridden(self):
        args = self.fixture()
        args[0]['tables'][0]['unit_assessment']['issues'] = ['FOREIGN_OR_CONFLICTING_CURRENCY']
        self.assertEqual(apply_unit_reviews(*args), args[0])

    def test_bad_date_stays_held(self):
        args = self.fixture()
        args[0]['tables'][0]['columns'][0]['date_comparison']['status'] = 'DATE_CONFLICT_HOLD'
        self.assertEqual(apply_unit_reviews(*args)['tables'][0]['columns'][0]['resolution']['status'], 'HOLD')

    def test_unrelated_document_has_no_saved_review(self):
        root = Path(__file__).resolve().parents[2]
        self.assertEqual(validated_unit_reviews(root, '0' * 64), [])
