from datetime import datetime, timezone, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from modules.company_intelligence.review_memory_report import build_review_memory_report
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanReviewLedger
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.test_company_fact_human_review import candidate


class ReviewMemoryReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'reviews.jsonl'
        self.now = datetime(2026, 9, 2, tzinfo=timezone.utc)

    def record(self, when=None):
        when = when or self.now
        item = candidate()
        meta = CompanyCandidateMetaReviewEngine().assess(item, reviewed_at=when)
        CompanyFactHumanReviewLedger(self.path).record(item, meta, review_id='R1', decision='REJECT',
            rationale='Synthetic test rejection', reviewer='Test', reviewed_at=when)

    def report(self):
        return build_review_memory_report(self.path, evaluated_at=self.now)

    def test_empty_memory_is_not_reported_as_successful_learning(self):
        report = self.report()
        self.assertEqual(report['status'], 'AWAITING_REVIEW_FEEDBACK')
        self.assertEqual(report['replayed_records'], 0)
        self.assertIsNone(report['investment_prediction_accuracy'])
        self.assertIsNone(report['unseen_fact_accuracy'])
        self.assertFalse(self.path.exists())

    def test_replay_measures_known_feedback_without_mutating_ledger(self):
        self.record()
        before = self.path.read_bytes()
        report = self.report()
        self.assertEqual(report['recorded_reviews'], 1)
        self.assertEqual(report['passed_replays'], 1)
        self.assertEqual(report['checks'][0]['baseline_decision'], 'READY_FOR_HUMAN_REVIEW')
        self.assertEqual(report['checks'][0]['memory_decision'], 'HOLD_FOR_RESEARCH')
        self.assertEqual(self.path.read_bytes(), before)
        self.assertIsNone(report['unseen_fact_accuracy'])

    def test_future_reviews_are_excluded(self):
        self.record(self.now + timedelta(days=1))
        report = self.report()
        self.assertEqual(report['excluded_future_reviews'], 1)
        self.assertEqual(report['replayed_records'], 0)

    def test_unknown_timezone_does_not_crash_or_leak_into_replay(self):
        self.record(self.now.replace(tzinfo=None))
        self.assertEqual(self.report()['excluded_timezone_unknown_reviews'], 1)
        result = CompanyCandidateMetaReviewEngine().assess(candidate(), reviewed_at=self.now, review_ledger_path=self.path)
        self.assertIn('REVIEW_MEMORY_TIMEZONE_UNKNOWN_NOT_APPLIED', result.reason_codes)

    def test_legacy_records_have_separate_coverage(self):
        self.record()
        payload = json.loads(self.path.read_text())
        payload.pop('candidate_snapshot')
        self.path.write_text(json.dumps(payload) + '\n')
        report = self.report()
        self.assertEqual(report['legacy_records_without_snapshot'], 1)
        self.assertEqual(report['usable_memory_records'], 0)

    def test_invalid_ledger_fails_closed(self):
        self.path.write_text('not json\n')
        with self.assertRaises(ValueError):
            self.report()


if __name__ == '__main__':
    unittest.main()
