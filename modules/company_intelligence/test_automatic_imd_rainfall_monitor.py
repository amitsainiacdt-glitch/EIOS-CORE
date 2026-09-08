import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from modules.company_intelligence.automatic_imd_rainfall_monitor import run_automatic_imd_rainfall_monitor


class AutomaticImdRainfallMonitorTests(unittest.TestCase):
    def test_not_due_uses_persisted_weekly_cadence_without_network(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); path = root / 'data/runtime/primary_indicator_assets/imd_country_rainfall_state.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({'schema_version':1,'status':'SUCCESS','next_due_at':'2026-09-15T00:00:00+00:00'}), encoding='utf-8')
            class Forbidden:
                def acquire(self, **kwargs): raise AssertionError('network must not run before due time')
            result = run_automatic_imd_rainfall_monitor(root, now=datetime(2026,9,8,tzinfo=timezone.utc), acquirer=Forbidden())
            self.assertEqual('NOT_DUE', result['status'])
            self.assertFalse(result['changes_verdict'])

    def test_corrupt_state_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); path = root / 'data/runtime/primary_indicator_assets/imd_country_rainfall_state.json'
            path.parent.mkdir(parents=True); path.write_text('{"schema_version":2}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'invalid IMD rainfall monitor state'):
                run_automatic_imd_rainfall_monitor(root, now=datetime(2026,9,8,tzinfo=timezone.utc))


if __name__ == '__main__': unittest.main()
