from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock
from modules.company_intelligence.quarterly_source_retry import run_source_retries


class SourceRetryTests(unittest.TestCase):
    def check(self, histories=(), *, execute=True, offline=False, changed=False, duplicate=False):
        now = datetime(2026, 9, 3, tzinfo=timezone.utc)
        body = b'%PDF-1.7 test'
        digest = sha256(body).hexdigest()
        url = 'https://issuer.example/report.pdf'
        with TemporaryDirectory() as folder:
            root = Path(folder)
            directory = root / 'data/runtime/quarterly_intake' / digest / 'run'
            directory.mkdir(parents=True)
            (directory / 'source.pdf').write_bytes(b'changed' if changed else body)
            candidate = {'candidate_id':'id', 'document_hash':digest, 'source_url':url, 'company':'Example'}
            packet = {'company':'Example', 'candidates':[candidate] * (2 if duplicate else 1),
                      'quarterly_record_evidence':{'id':{'source_column':{'document_hash':digest,'ticker':'TEST'}}}}
            (directory / 'quarterly-candidates.json').write_text(json.dumps(packet), encoding='utf-8')
            for index, (status, http, hours) in enumerate(histories):
                target = directory / 'source-verification' / str(index)
                target.mkdir(parents=True)
                (target / 'verification.json').write_text(json.dumps({'document_hash':digest, 'ticker':'TEST',
                    'source_url':url, 'checked_at':(now-timedelta(hours=hours)).isoformat(),
                    'status':status, 'http_status':http}), encoding='utf-8')
            verify = Mock(return_value={'status':'SOURCE_UNAVAILABLE','result_path':'saved'})
            result = run_source_retries(root, now=now, execute=execute, offline=offline, verifier=verify)
            return result, verify.call_count

    def test_due_attempt_once_for_duplicate_columns(self):
        result, count = self.check(duplicate=True)
        self.assertEqual(count, 1)
        self.assertFalse(result['creates_approved_facts'])

    def test_dry_run_never_downloads(self):
        self.assertEqual(self.check(execute=False)[1], 0)

    def test_offline_never_downloads(self):
        self.assertEqual(self.check(offline=True)[1], 0)

    def test_recent_transient_failure_waits(self):
        result, count = self.check([('SOURCE_UNAVAILABLE',503,1)])
        self.assertEqual(count, 0)
        self.assertEqual(result['items'][0]['status'], 'WAITING_RETRY_WINDOW')

    def test_old_transient_failure_retries(self):
        self.assertEqual(self.check([('SOURCE_UNAVAILABLE',503,25)])[1], 1)

    def test_access_refusal_does_not_repeat(self):
        result, count = self.check([('SOURCE_UNAVAILABLE',406,25)])
        self.assertEqual(count, 0)
        self.assertEqual(result['items'][0]['status'], 'SOURCE_ACCESS_REQUIRES_ATTENTION')

    def test_match_does_not_repeat(self):
        self.assertEqual(self.check([('EXACT_ISSUER_COPY_MATCH',200,25)])[1], 0)

    def test_attempt_limit(self):
        result, count = self.check([('SOURCE_UNAVAILABLE',503,h) for h in (75,50,25)])
        self.assertEqual(count, 0)
        self.assertEqual(result['items'][0]['status'], 'RETRY_LIMIT_REACHED')

    def test_changed_original_withheld(self):
        self.assertEqual(self.check(changed=True)[1], 0)
