from datetime import datetime, timezone
from types import SimpleNamespace
import unittest
from modules.company_intelligence.official_report_discovery import ReportLinks, discover_official_reports
from modules.company_intelligence.automatic_official_document_pipeline import AutomaticOfficialDocumentPipeline
from modules.company_intelligence.test_automatic_official_document_pipeline import job


class OfficialReportDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.job = job()
        self.registry = AutomaticOfficialDocumentPipeline._registry(self.job)
        self.seed = 'https://www.coromandel.biz/investors/reports/'
        self.manifest = {'companies': {'COROMANDEL': {'sources': [{'url': self.seed, 'source_type': 'ANNUAL_REPORT', 'authority': 'ISSUER_OFFICIAL'}]}}}

    def test_relative_links_deduplicated_and_untrusted_links_rejected(self):
        parser = ReportLinks(self.seed, self.registry)
        parser.feed('<a href="/one.pdf#page=2">A</a><a href="/one.pdf">B</a><a href="http://www.coromandel.biz/no.pdf">C</a><a href="https://evil.example/no.pdf">D</a><a href="https://www.coromandel.biz.evil.example/no.pdf">E</a><a href="javascript:alert(1)">F</a>')
        self.assertEqual(parser.links, ['https://www.coromandel.biz/one.pdf'])

    def test_discovery_is_bounded_and_not_content_verification(self):
        adapter = SimpleNamespace(registry=self.registry, acquire=lambda **kwargs: SimpleNamespace(
            document_bytes=b'<a href="/one.pdf">A</a><a href="/two.pdf">B</a>',
            receipt=SimpleNamespace(source_url=self.seed), retrieved_content=SimpleNamespace(content_type='text/html')))
        report = discover_official_reports(self.job, self.manifest, adapter, acquired_at=datetime.now(timezone.utc), cycle_id='TEST', max_documents=1)
        self.assertEqual(report['pdf_links_found'], 2)
        self.assertEqual(len(report['selected_sources']), 1)
        self.assertIn('not yet verified', report['selected_sources'][0].result.snippet)

    def test_known_annual_does_not_hide_quarterly_page(self):
        sources = self.manifest['companies']['COROMANDEL']['sources']
        sources[0]['document_urls'] = ['https://www.coromandel.biz/annual.pdf']
        sources.append({'url': self.seed + 'presentations/', 'source_type': 'INVESTOR_PRESENTATION', 'authority': 'ISSUER_OFFICIAL'})
        quarterly = self.seed + 'quarterly/'
        sources.append({'url': quarterly, 'source_type': 'QUARTERLY_RESULTS', 'authority': 'ISSUER_OFFICIAL'})
        calls = []
        def acquire(**kwargs):
            calls.append(kwargs['url'])
            return SimpleNamespace(document_bytes=b'<a href="/annual.pdf">Duplicate</a><a href="/quarter.pdf">Quarter</a><a href="/extra.pdf">Extra</a>', receipt=SimpleNamespace(source_url=kwargs['url']), retrieved_content=SimpleNamespace(content_type='text/html'))
        report = discover_official_reports(self.job, self.manifest, SimpleNamespace(registry=self.registry, acquire=acquire), acquired_at=datetime.now(timezone.utc), cycle_id='TEST')
        self.assertEqual(calls, [quarterly])
        self.assertEqual([item.result.url for item in report['selected_sources']], ['https://www.coromandel.biz/annual.pdf', 'https://www.coromandel.biz/quarter.pdf'])

    def test_limit_applies_across_pages(self):
        self.manifest['companies']['COROMANDEL']['sources'].append({'url': self.seed + 'second/', 'source_type': 'QUARTERLY_RESULTS', 'authority': 'ISSUER_OFFICIAL'})
        calls = []
        def acquire(**kwargs):
            calls.append(kwargs['url'])
            return SimpleNamespace(document_bytes=b'<a href="one.pdf">One</a><a href="two.pdf">Two</a>', receipt=SimpleNamespace(source_url=kwargs['url']), retrieved_content=SimpleNamespace(content_type='text/html'))
        report = discover_official_reports(self.job, self.manifest, SimpleNamespace(registry=self.registry, acquire=acquire), acquired_at=datetime.now(timezone.utc), cycle_id='TEST', max_documents=1)
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(report['selected_sources']), 1)

    def test_http_failure_and_missing_seed_are_explicit(self):
        adapter = SimpleNamespace(registry=self.registry, acquire=lambda **kwargs: SimpleNamespace(document_bytes=None, receipt=SimpleNamespace(error_code='HTTP_403')))
        report = discover_official_reports(self.job, self.manifest, adapter, acquired_at=datetime.now(timezone.utc), cycle_id='TEST')
        self.assertEqual(report['pages_failed'], 1)
        self.assertEqual(report['errors'], ['HTTP_403'])
        self.assertEqual(discover_official_reports(self.job, {}, adapter, acquired_at=datetime.now(timezone.utc), cycle_id='TEST')['pages_checked'], 0)
