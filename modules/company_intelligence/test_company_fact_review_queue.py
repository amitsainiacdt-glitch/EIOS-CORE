from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewQueueBuilder
from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry


class CompanyFactReviewQueueTests(unittest.TestCase):
    def test_company_primary_passage_becomes_page_aware_review_candidate(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            now = datetime(2026, 9, 1, tzinfo=timezone.utc)
            text = "[[PDF_PAGE_7]] Coromandel International received an order worth INR 125 crore on 28 August 2026."
            body = text.encode()
            registry = TrustedPublicSourceRegistry((
                TrustedPublicSourceDefinition("COROMANDEL", "Coromandel", ("coromandel.biz",), source_type="COMPANY_PRIMARY"),
            ))
            ledger = PublicSourceAcquisitionLedger(root / "acquisition.jsonl")
            receipt = ledger.record(
                acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="OFFICIAL_DOCUMENT_DISCOVERY",
                source_url="https://www.coromandel.biz/report.txt", status="RETRIEVED",
                requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
                document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="test",
            )
            acquisition = TrustedPublicAcquisitionResult(
                registry.resolve(receipt.source_url), receipt,
                RetrievedContent(receipt.source_url, 200, text, "text/plain", {}), body,
            )
            extraction = TrustedPublicDocumentExtractionAdapter(
                PublicDocumentExtractionLedger(root / "extraction.jsonl"), clock=lambda: now + timedelta(seconds=1),
            ).extract(acquisition, extraction_id="E1", recorder="test")
            admission = PublicObservationAdmissionGate(registry).preview(
                acquisition=acquisition, extraction=extraction, title="Official report",
                entity="Coromandel International", category="COMPANY_FILING", confidence=80,
            )
            self.assertTrue(admission.admissible)
            output = root / "queue.json"
            candidates = CompanyFactReviewQueueBuilder(output).build(
                acquisition=acquisition, extraction=extraction, admission=admission,
                company="Coromandel International", generated_at=now,
            )
            self.assertEqual(len(candidates), 1)
            self.assertEqual(candidates[0].pdf_page, 7)
            self.assertEqual(candidates[0].review_status, "PENDING_META_REVIEW")
            self.assertFalse(candidates[0].creates_evidence)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(payload["creates_evidence"])
            self.assertTrue(payload["requires_human_review"])


if __name__ == "__main__":
    unittest.main()
