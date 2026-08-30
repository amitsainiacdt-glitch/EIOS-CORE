"""Offline tests for the read-only public Observation admission gate."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry
from modules.observation.observation import Observation, ObservationProvenance


def main():
    with TemporaryDirectory() as directory:
        now = datetime(2026, 8, 29, 13, tzinfo=timezone.utc)
        root = Path(directory)
        registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("RBI", "RBI", ("rbi.org.in",)),))
        acquisitions = PublicSourceAcquisitionLedger(root / "a.jsonl")
        extractions = PublicDocumentExtractionLedger(root / "e.jsonl")
        body = b"Official public regulatory announcement with enough deterministic content for admission testing."
        receipt = acquisitions.record(
            acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="EARLY_HINT",
            source_url="https://www.rbi.org.in/notice", access_classification="PUBLIC", status="RETRIEVED",
            requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
            document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="Acquirer",
        )
        acquired = TrustedPublicAcquisitionResult(
            registry.resolve(receipt.source_url), receipt,
            RetrievedContent(receipt.source_url, 200, body.decode(), "text/plain", {}), body,
        )
        extraction = TrustedPublicDocumentExtractionAdapter(extractions, clock=lambda: now + timedelta(seconds=1)).extract(
            acquired, extraction_id="E1", recorder="Extractor"
        )
        gate = PublicObservationAdmissionGate(registry)
        values = dict(acquisition=acquired, extraction=extraction, title="Policy notice", entity="Banking", category="REGULATORY", confidence=85)
        admitted = gate.preview(observations=(), **values)
        assert admitted.admissible and admitted.reason_codes == () and admitted.source_id == "RBI"

        duplicate = Observation("Old", extraction.extracted_text, receipt.source_url, "REGULATORY", "Banking", 80, now, ObservationProvenance(document_hash=receipt.document_hash, content_fingerprint=extraction.receipt.extracted_content_fingerprint))
        rejected = gate.preview(observations=(duplicate,), **values)
        assert rejected.decision.value == "REJECT" and rejected.duplicate_observation_indexes == (0,)

        partial_receipt = replace(extraction.receipt, status=type(extraction.receipt.status).PARTIAL, warnings=("Incomplete",))
        partial = replace(extraction, receipt=partial_receipt)
        deferred = gate.preview(acquisition=acquired, extraction=partial, observations=(), title="Policy", entity="Banking", category="REGULATORY", confidence=50)
        assert deferred.decision.value == "DEFER" and "EXTRACTION_PARTIAL" in deferred.reason_codes

        mismatched = replace(extraction, receipt=replace(extraction.receipt, acquisition_fingerprint="0" * 64))
        invalid = gate.preview(acquisition=acquired, extraction=mismatched, observations=(), title="Policy", entity="Banking", category="REGULATORY", confidence=50)
        assert invalid.decision.value == "REJECT" and "EXTRACTION_ACQUISITION_MISMATCH" in invalid.reason_codes
        assert extractions.read_all() == (extraction.receipt,)

    print("PUBLIC OBSERVATION ADMISSION GATE: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
