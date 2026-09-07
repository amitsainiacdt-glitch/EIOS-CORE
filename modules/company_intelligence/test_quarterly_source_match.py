from datetime import datetime, timezone
from hashlib import sha256
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
from modules.company_intelligence.quarterly_source_match import match_quarterly_source


class QuarterlySourceMatchTests(unittest.TestCase):
    local = b'%PDF-1.7 original test bytes'

    def run_match(self, body, status=200, receipt_hash=None, source_kind='ISSUER'):
        receipt = SimpleNamespace(acquisition_id='test', source_url='https://issuer.example/q.pdf',
            completed_at=datetime.now(timezone.utc), http_status=status,
            status=SimpleNamespace(value='RETRIEVED' if body else 'FAILED'),
            document_hash=receipt_hash or (sha256(body).hexdigest() if body else None),
            bytes_received=len(body or b''))
        adapter = Mock()
        adapter.acquire.return_value = SimpleNamespace(receipt=receipt, document_bytes=body)
        return match_quarterly_source(self.local, sha256(self.local).hexdigest(),
                                      source_url=receipt.source_url, adapter=adapter, source_kind=source_kind)

    def test_exchange_match_is_distinct_and_not_company_approval(self):
        result, _ = self.run_match(self.local, source_kind='EXCHANGE')
        self.assertEqual(result['status'], 'EXACT_EXCHANGE_COPY_MATCH')
        self.assertFalse(result['company_content_verified'])
        self.assertIn('exchange', result['explanation'])

    def test_exchange_failure_is_labelled_correctly(self):
        result, _ = self.run_match(None, 403, source_kind='EXCHANGE')
        self.assertIn('exchange', result['explanation'])

    def test_unknown_source_kind_rejected(self):
        with self.assertRaises(ValueError):
            self.run_match(self.local, source_kind='UNTRUSTED')

    def test_exact_match_is_not_approval(self):
        result, body = self.run_match(self.local)
        self.assertEqual(result['status'], 'EXACT_ISSUER_COPY_MATCH')
        self.assertEqual(body, self.local)
        self.assertFalse(result['creates_approved_facts'])
        self.assertFalse(result['company_content_verified'])
        self.assertFalse(result['reporting_notes_verified'])

    def test_changed_copy_preserved_but_not_substituted(self):
        result, body = self.run_match(b'%PDF-1.7 different')
        self.assertEqual(result['status'], 'DIFFERENT_DOCUMENT')
        self.assertNotEqual(body, self.local)

    def test_html_not_pdf(self):
        self.assertEqual(self.run_match(b'<html>blocked</html>')[0]['status'], 'SOURCE_NOT_PDF')

    def test_failed_download(self):
        self.assertEqual(self.run_match(None, 406)[0]['status'], 'SOURCE_UNAVAILABLE')

    def test_partial_response_not_match(self):
        self.assertEqual(self.run_match(self.local, 206)[0]['status'], 'SOURCE_UNAVAILABLE')

    def test_receipt_tampering(self):
        result, body = self.run_match(self.local, receipt_hash='0' * 64)
        self.assertEqual(result['status'], 'ACQUISITION_EVIDENCE_MISMATCH')
        self.assertIsNone(body)

    def test_changed_local_never_fetches(self):
        adapter = Mock()
        with self.assertRaises(ValueError):
            match_quarterly_source(self.local, '0' * 64, source_url='https://issuer.example/q.pdf', adapter=adapter)
        adapter.acquire.assert_not_called()
