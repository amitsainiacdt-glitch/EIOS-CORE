import unittest
from types import SimpleNamespace
from scripts.verify_quarterly_source import resolve_source_url
from scripts.verify_quarterly_source import source_registry
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


class QuarterlySourceAlternativeTests(unittest.TestCase):
    def setUp(self):
        self.registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition(
            'ISSUER', 'Test Company', ('issuer.example',), source_type='COMPANY_PRIMARY'),))
        self.original = 'https://issuer.example/results.pdf'

    def test_original_is_default(self):
        self.assertEqual(resolve_source_url(self.original, None, self.registry), self.original)

    def test_alternate_issuer_path_supported(self):
        alternate = 'https://issuer.example/board-results.pdf'
        self.assertEqual(resolve_source_url(self.original, alternate, self.registry), alternate)

    def test_lookalike_domain_rejected(self):
        with self.assertRaises(ValueError):
            resolve_source_url(self.original, 'https://issuer.example.attacker.example/report.pdf', self.registry)

    def test_local_target_rejected(self):
        with self.assertRaises(ValueError):
            resolve_source_url(self.original, 'http://127.0.0.1/report.pdf', self.registry)

    def test_exchange_mode_accepts_bse_not_issuer_or_lookalike(self):
        registry = source_registry(SimpleNamespace(), exchange=True)
        registry.resolve('https://www.bseindia.com/xml-data/corpfiling/AttachLive/report.pdf')
        for url in ('https://issuer.example/report.pdf', 'https://bseindia.com.evil.example/report.pdf'):
            with self.assertRaises(ValueError):
                registry.resolve(url)

    def test_default_mode_does_not_expand_to_exchanges(self):
        registry = source_registry(SimpleNamespace(ticker='TEST', company='Example', entity_domain='issuer.example'))
        with self.assertRaises(ValueError):
            registry.resolve('https://www.bseindia.com/report.pdf')
