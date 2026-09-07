import unittest
from modules.company_intelligence.collection_outcome import describe_document_collection


class CollectionOutcomeTests(unittest.TestCase):
    def summary(self, **updates):
        return dict(candidates_seen=0, archived=0, unchanged=0, failed=0,
                    extracted=0, fact_candidates_queued=0, extraction_holds=0) | updates

    def test_zero_collection_is_explicit(self):
        self.assertEqual(describe_document_collection(self.summary())['status'], 'NO_DOCUMENTS_EXTRACTED')

    def test_unchanged_is_distinct_from_new_extraction(self):
        self.assertEqual(describe_document_collection(self.summary(unchanged=2))['status'], 'EXISTING_DOCUMENTS_UNCHANGED')

    def test_extraction_is_not_approval(self):
        report = describe_document_collection(self.summary(extracted=1, fact_candidates_queued=3))
        self.assertEqual(report['status'], 'FACT_CANDIDATES_AWAITING_REVIEW')
        self.assertFalse(report['new_facts_approved'])

    def test_partial_failures_remain_visible(self):
        self.assertEqual(describe_document_collection(self.summary(extracted=2, failed=1))['status'], 'COLLECTION_NEEDS_ATTENTION')

    def test_missing_or_invalid_counts_are_not_zero(self):
        self.assertEqual(describe_document_collection({})['status'], 'COLLECTION_RESULT_UNAVAILABLE')
        for value in (None, True, -1, '2'):
            self.assertEqual(describe_document_collection(self.summary(extracted=value))['status'], 'COLLECTION_RESULT_UNAVAILABLE')

    def test_documents_without_candidates_have_separate_status(self):
        self.assertEqual(describe_document_collection(self.summary(extracted=2))['status'], 'DOCUMENTS_EXTRACTED_NO_FACT_CANDIDATES')
