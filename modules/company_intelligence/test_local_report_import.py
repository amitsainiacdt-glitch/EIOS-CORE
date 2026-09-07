from datetime import datetime, timezone
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from modules.company_intelligence.local_report_import import import_local_report
from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaReviewEngine
from modules.company_intelligence.test_company_fact_human_review import candidate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter


class LocalReportImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'test.pdf'
        self.path.write_bytes(b'%PDF-1.4\nSynthetic import-envelope test only')
        self.registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition('TEST', 'Test', ('example.com',)),))
        self.ledger = PublicSourceAcquisitionLedger(self.root / 'ledger.jsonl')

    def run_import(self, **overrides):
        args = dict(workspace=self.root, source_url='https://example.com/report.pdf',
                    expected_sha256=sha256(self.path.read_bytes()).hexdigest(), registry=self.registry, ledger=self.ledger)
        args.update(overrides)
        return import_local_report(self.path, **args)

    def test_local_origin_is_explicit_without_fabricated_http_response(self):
        result = self.run_import()
        self.assertIsNone(result.receipt.http_status)
        self.assertEqual(result.receipt.research_intent, 'LOCAL_OFFICIAL_DOCUMENT_IMPORT')
        self.assertEqual(TrustedPublicDocumentExtractionAdapter._lineage_method(result.receipt, 'pypdf_text_layer_v1'), 'local_import_pypdf_text_layer_v1')

    def test_wrong_hash_untrusted_url_and_invalid_pdf_fail_before_receipt(self):
        for overrides in ({'expected_sha256': '0'*64}, {'source_url': 'https://untrusted.example/report.pdf'}, {'workspace': self.root / 'other'}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.run_import(**overrides)
        self.path.write_bytes(b'not a PDF')
        with self.assertRaises(ValueError):
            self.run_import()
        self.assertFalse(self.ledger.path.exists())

    def test_local_candidates_cannot_gain_primary_source_authority(self):
        item = replace(candidate(), extraction_method='local_import_pypdf_text_layer_v1')
        result = CompanyCandidateMetaReviewEngine().assess(item, reviewed_at=datetime.now(timezone.utc))
        self.assertEqual(result.decision, 'HOLD_FOR_RESEARCH')
        self.assertIn('LOCAL_IMPORT_ORIGIN_REQUIRES_INDEPENDENT_REVIEW', result.reason_codes)
        self.assertFalse(result.creates_evidence)
