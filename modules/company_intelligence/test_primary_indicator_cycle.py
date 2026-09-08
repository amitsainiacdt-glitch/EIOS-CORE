import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from modules.company_intelligence.primary_indicator_cycle import process_primary_indicator_results
from modules.company_intelligence.primary_indicator_ledger import PrimaryIndicatorLedger


class PrimaryIndicatorCycleTests(unittest.TestCase):
    def test_records_bound_official_observation_without_changing_decision_state(self):
        job_id = 'COROMANDEL-PRIMARY-INDICATOR-CORO-PHOSPHORIC-ACID-PRICE'
        provenance = SimpleNamespace(
            job_id=job_id,
            research_intent='PRIMARY_INDICATOR_MONITORING',
            source_quality_tier='TIER_1',
            source_domain='coromandel.biz',
            content_fingerprint='a' * 64,
        )
        observation = SimpleNamespace(
            description='Phosphoric acid settlement price was 1,050 USD/t for 2026-09-01 in the official update.',
            source='https://coromandel.biz/investors/official-update',
            provenance=provenance,
        )
        result = SimpleNamespace(job_id=job_id, observations=(observation,))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'records.jsonl'
            summary = process_primary_indicator_results(
                (result,), ledger_path=path, recorded_at=datetime(2026, 9, 8, tzinfo=timezone.utc)
            )
            records = PrimaryIndicatorLedger(path).read_all()

        self.assertEqual(summary['recorded'], 1)
        self.assertEqual(summary['held'], 0)
        self.assertFalse(summary['creates_catalyst'])
        self.assertFalse(summary['changes_verdict'])
        self.assertFalse(summary['authorizes_trade'])
        self.assertEqual(records[0].value, '1050')
        self.assertEqual(records[0].reporting_date, '2026-09-01')


if __name__ == '__main__':
    unittest.main()
