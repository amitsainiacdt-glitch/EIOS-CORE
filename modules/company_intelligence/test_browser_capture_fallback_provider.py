from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from modules.company_intelligence.browser_capture_fallback_provider import BrowserCaptureFallbackProvider
from modules.company_intelligence.official_document_fallback import validate_fallback_delivery
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition

class BrowserCaptureFallbackTests(unittest.TestCase):
    def test_corroborated_capture_is_reused_without_approval(self):
        with TemporaryDirectory(dir=".") as temporary:
            root=Path(temporary).resolve(); capture=root/'data/runtime/browser_source_capture/case'; capture.mkdir(parents=True)
            body=b'%PDF-1.4 capture'; (capture/'source.pdf').write_bytes(body); url='https://issuer.example/q1.pdf'
            (capture/'provenance.json').write_text(json.dumps({'schema_version':1,'source_url':url,'status':'BROWSER_COPY_CORROBORATED_PENDING_REVIEW','creates_approved_facts':False,'preserved_file':'source.pdf','document_hash':sha256(body).hexdigest()}),encoding='utf-8')
            source=TrustedPublicSourceDefinition('ISSUER','Issuer',('issuer.example',),source_type='COMPANY_PRIMARY')
            provider=BrowserCaptureFallbackProvider(capture.parent,workspace=root,ledger=PublicSourceAcquisitionLedger(root/'ledger.jsonl'))
            result=provider.acquire_after_failure(SimpleNamespace(source=source),url=url)
            self.assertIs(validate_fallback_delivery(result,requested_url=url),result)
            self.assertFalse(json.loads((capture/'provenance.json').read_text())['creates_approved_facts'])

if __name__ == '__main__': unittest.main()
