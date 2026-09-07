from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from modules.company_intelligence.local_document_fallback_provider import LocalDocumentFallbackProvider
from modules.company_intelligence.official_document_fallback import validate_fallback_delivery
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition


class LocalDocumentFallbackProviderTests(unittest.TestCase):
    def test_exact_hash_bound_mapping_delivers_blocked_official_url(self):
        with TemporaryDirectory(dir=".") as temporary:
            root = Path(temporary).resolve()
            inbox = root / "data/runtime/official_document_inbox"
            inbox.mkdir(parents=True)
            body = b"%PDF-1.4 governed local copy"
            (inbox / "report.pdf").write_bytes(body)
            url = "https://issuer.example/report.pdf"
            (inbox / "report.json").write_text(json.dumps({
                "schema_version": 1, "file": "report.pdf", "source_url": url,
                "sha256": sha256(body).hexdigest(),
            }), encoding="utf-8")
            source = TrustedPublicSourceDefinition("ISSUER", "Issuer", ("issuer.example",), source_type="COMPANY_PRIMARY")
            blocked = SimpleNamespace(source=source, document_bytes=None)
            provider = LocalDocumentFallbackProvider(inbox, workspace=root, ledger=PublicSourceAcquisitionLedger(root / "ledger.jsonl"))
            result = provider.acquire_after_failure(blocked, url=url)
            self.assertEqual(result.document_bytes, body)
            self.assertIs(validate_fallback_delivery(result, requested_url=url), result)

    def test_no_or_ambiguous_mapping_fails_closed(self):
        with TemporaryDirectory(dir=".") as temporary:
            root = Path(temporary).resolve()
            inbox = root / "data/runtime/official_document_inbox"
            inbox.mkdir(parents=True)
            source = TrustedPublicSourceDefinition("ISSUER", "Issuer", ("issuer.example",), source_type="COMPANY_PRIMARY")
            provider = LocalDocumentFallbackProvider(inbox, workspace=root, ledger=PublicSourceAcquisitionLedger(root / "ledger.jsonl"))
            self.assertIsNone(provider.acquire_after_failure(SimpleNamespace(source=source), url="https://issuer.example/report.pdf"))


if __name__ == "__main__":
    unittest.main()
