from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from scripts import run_automatic_company_cycle as cycle


class CompanyCycleSourceOrderTests(unittest.TestCase):
    def test_governed_company_plan_supersedes_legacy_jobs(self):
        legacy = SimpleNamespace(job_id='ANUP-LEGACY', ticker='ANUP')
        governed = SimpleNamespace(job_id='ANUP-GOVERNED', ticker='ANUP')
        other = SimpleNamespace(job_id='OTHER-LEGACY', ticker='OTHER')
        with patch.object(cycle.ResearchJobConfiguration, 'all_jobs', return_value=[legacy, other]), \
             patch.object(cycle, 'load_company_coverage_jobs', return_value=[governed]), \
             patch.object(cycle, 'load_quarterly_monitoring_jobs', return_value=[]):
            self.assertEqual([job.job_id for job in cycle.all_automatic_jobs()],
                             ['OTHER-LEGACY', 'ANUP-GOVERNED'])

    def test_search_failure_does_not_skip_saved_document_retry(self):
        for offline in (False, True):
            with self.subTest(offline=offline), TemporaryDirectory() as folder, ExitStack() as stack:
                root = Path(folder)
                for name, value in {'ROOT':root, 'RUNTIME_DIR':root, 'LOCK_PATH':root/'lock',
                                    'STATUS_PATH':root/'status.json'}.items():
                    stack.enter_context(patch.object(cycle, name, value))
                stack.enter_context(patch.object(cycle.os, 'chdir'))
                stack.enter_context(patch.object(cycle, 'check_financial_sources', return_value={'issues':[]}))
                stack.enter_context(patch.object(cycle, 'build_review_memory_report', return_value={'failed_review_ids':[]}))
                config = SimpleNamespace(offline_mode=offline)
                stack.enter_context(patch.object(cycle.ResearchRuntimeBootstrapConfig, 'from_environment', return_value=config))
                bootstrap = stack.enter_context(patch.object(cycle, 'ResearchRuntimeBootstrap')).return_value
                bootstrap.validate.return_value = SimpleNamespace(ready=True, job_count=1)
                events = []
                retry = stack.enter_context(patch.object(cycle, 'run_source_retries',
                    side_effect=lambda *args, **kwargs: events.append('retry') or {'status':'OFFLINE' if offline else 'COMPLETED'}))
                def fail_search(**kwargs):
                    events.append('search')
                    raise RuntimeError('Search unavailable')
                bootstrap.run_once.side_effect = fail_search
                self.assertEqual(cycle.main(), 1)
                self.assertEqual(events, ['retry', 'search'])
                self.assertEqual(retry.call_args.kwargs['offline'], offline)
                import json
                saved = json.loads((root/'status.json').read_text())
                self.assertEqual(saved['status'], 'FAILED')
                self.assertIn('quarterly_source_retries', saved)
                self.assertFalse((root/'lock').exists())
