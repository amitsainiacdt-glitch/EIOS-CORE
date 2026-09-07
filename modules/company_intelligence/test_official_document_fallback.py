from datetime import datetime, timezone
from hashlib import sha256
from types import SimpleNamespace
import unittest

from modules.company_intelligence.official_document_fallback import (
    OfficialDocumentDeliveryProvenance,
    validate_fallback_delivery,
)


class OfficialDocumentFallbackTests(unittest.TestCase):
    def result(self, *, requested_url="https://issuer.example/report.pdf", delivery_url="https://provider.example/file"):
        body = b"%PDF governed copy"
        return SimpleNamespace(
            document_bytes=body,
            retrieved_content=SimpleNamespace(content_type="application/pdf"),
            receipt=SimpleNamespace(requested_url=requested_url, document_hash=sha256(body).hexdigest(), bytes_received=len(body)),
            delivery_provenance=OfficialDocumentDeliveryProvenance("APPROVED_PROVIDER", delivery_url, requested_url),
        )

    def test_valid_delivery_preserves_official_identity(self):
        result = self.result()
        self.assertIs(validate_fallback_delivery(result, requested_url=result.receipt.requested_url), result)

    def test_missing_provenance_is_rejected(self):
        result = self.result()
        del result.delivery_provenance
        with self.assertRaises(ValueError):
            validate_fallback_delivery(result, requested_url=result.receipt.requested_url)

    def test_changed_official_url_and_insecure_delivery_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_fallback_delivery(self.result(), requested_url="https://issuer.example/other.pdf")
        result = self.result(delivery_url="http://provider.example/file")
        with self.assertRaises(ValueError):
            validate_fallback_delivery(result, requested_url=result.receipt.requested_url)

    def test_tampered_bytes_are_rejected(self):
        result = self.result()
        result.document_bytes = b"changed"
        with self.assertRaises(ValueError):
            validate_fallback_delivery(result, requested_url=result.receipt.requested_url)


if __name__ == "__main__":
    unittest.main()
