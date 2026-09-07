import json
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from modules.company_intelligence.quarterly_source_intake import verify_intake_source


class SourceIntakeTests(unittest.TestCase):
    def run_check(self, company='Example', url='https://issuer.example/report.pdf', jobs=None, fail=False):
        job = SimpleNamespace(ticker='TEST', intent='OFFICIAL_DOCUMENT_DISCOVERY', company='Example', entity_domain='issuer.example')
        body = b'%PDF-1.7 test'
        factory = Mock()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            with patch('modules.company_intelligence.quarterly_source_intake.load_company_coverage_jobs', return_value=[job] if jobs is None else jobs), patch('modules.company_intelligence.quarterly_source_intake.match_quarterly_source') as compare:
                if fail:
                    compare.side_effect = OSError('Network unavailable')
                else:
                    compare.return_value = ({'status':'EXACT_ISSUER_COPY_MATCH', 'creates_approved_facts':False}, body)
                result = verify_intake_source(body, sha256(body).hexdigest(), workspace=root,
                    output_directory=root, ticker='TEST', company=company, source_url=url, adapter_factory=factory)
                saved = json.loads(Path(result['result_path']).read_text(encoding='utf-8'))
                self.assertEqual(saved, result)
                return result, compare.call_count, factory.call_count

    def test_success_fetches_once_and_does_not_approve(self):
        result, calls, factories = self.run_check()
        self.assertEqual((calls, factories), (1, 1))
        self.assertEqual(result['status'], 'EXACT_ISSUER_COPY_MATCH')
        self.assertFalse(result['creates_approved_facts'])
        self.assertFalse(result['changes_verdict'])

    def test_missing_context_skips_network(self):
        result, calls, factories = self.run_check(company=None)
        self.assertEqual(result['status'], 'HOLD_MISSING_COMPANY_SOURCE_CONTEXT')
        self.assertEqual((calls, factories), (0, 0))

    def test_wrong_company_skips_network(self):
        self.assertEqual(self.run_check(company='Other')[1:], (0, 0))

    def test_unknown_company_skips_network(self):
        self.assertEqual(self.run_check(jobs=[])[1:], (0, 0))

    def test_foreign_url_skips_network(self):
        self.assertEqual(self.run_check(url='https://foreign.example/report.pdf')[1:], (0, 0))

    def test_failure_is_persisted_not_raised(self):
        result, calls, _ = self.run_check(fail=True)
        self.assertEqual(result['status'], 'SOURCE_CHECK_FAILED_HOLD')
        self.assertFalse(result['creates_approved_facts'])
        self.assertEqual(calls, 1)

    def test_complete_intake_keeps_review_packet_for_success_and_storage_failure(self):
        from pypdf import PdfWriter
        from modules.company_intelligence.quarterly_pdf_intake import run_quarterly_intake
        for storage_failure in (False, True):
            with self.subTest(storage_failure=storage_failure), TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / 'test.pdf'
                writer = PdfWriter()
                writer.add_blank_page(width=100, height=100)
                with source.open('wb') as handle:
                    writer.write(handle)
                with patch('modules.company_intelligence.quarterly_pdf_intake.extract_pdf_layout', return_value={'pages': []}), patch('modules.company_intelligence.quarterly_pdf_intake.verify_intake_source') as verify:
                    if storage_failure:
                        verify.side_effect = OSError('Storage unavailable')
                    else:
                        verify.return_value = {'status':'EXACT_ISSUER_COPY_MATCH', 'creates_approved_facts':False}
                    report = run_quarterly_intake(source, workspace=root, ticker='TEST', company='Example',
                                                  source_url='https://issuer.example/report.pdf')
                    verify.assert_called_once()
                    queue = json.loads(Path(report['review_queue']['queue_path']).read_text(encoding='utf-8'))
                    self.assertEqual(queue['source_verification'], report['source_verification'])
                    self.assertTrue(queue['requires_human_review'])
                    self.assertFalse(report['creates_approved_facts'])
                    self.assertFalse(report['changes_verdict'])
                    self.assertEqual(report['status'], 'RESEARCH_HOLD')
                    self.assertEqual((Path(report['run_directory']) / 'source.pdf').read_bytes(), source.read_bytes())
