"""Offline, temporary-store tests for controlled public Observation commits."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_observation_commit_service import PublicObservationCommitService
from modules.external_intelligence.public_observation_commit_audit import PublicObservationCommitAuditLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        production = root / "production-observations.json"
        production.write_bytes(b'{"preserve":"exactly"}')
        test_store = root / "test-observations.json"
        now = datetime(2026, 8, 29, 14, tzinfo=timezone.utc)
        registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("RBI", "RBI", ("rbi.org.in",)),))
        body = b"Official public policy change that is sufficiently complete for controlled Observation admission."
        acquisition_receipt = PublicSourceAcquisitionLedger(root / "a.jsonl").record(
            acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="EARLY_HINT",
            source_url="https://www.rbi.org.in/notice", access_classification="PUBLIC", status="RETRIEVED",
            requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
            source_document_id="NOTICE-1", document_hash=sha256(body).hexdigest(),
            bytes_received=len(body), recorder="Acquirer",
        )
        acquired = TrustedPublicAcquisitionResult(
            registry.resolve(acquisition_receipt.source_url), acquisition_receipt,
            RetrievedContent(acquisition_receipt.source_url, 200, body.decode(), "text/plain", {}), body,
        )
        extracted = TrustedPublicDocumentExtractionAdapter(
            PublicDocumentExtractionLedger(root / "e.jsonl"), clock=lambda: now + timedelta(seconds=1)
        ).extract(acquired, extraction_id="E1", recorder="Extractor")
        engine = ObservationEngine(persistence=ObservationPersistence(test_store))
        audit = PublicObservationCommitAuditLedger(root / "commit-audit.jsonl")
        service = PublicObservationCommitService(PublicObservationAdmissionGate(registry), engine, audit, clock=lambda: now + timedelta(seconds=2))
        committed = service.commit(
            commit_id="COMMIT-1", recorder="Commit Service",
            acquisition=acquired, extraction=extracted, title="Policy change",
            entity="Banking", category="REGULATORY", confidence=88,
            published_at=now - timedelta(hours=1), filing_at=now - timedelta(minutes=30),
        )
        assert committed.committed and committed.status == "COMMITTED"
        assert committed.observation.provenance.document_hash == acquisition_receipt.document_hash
        assert committed.observation.provenance.extraction_method == extracted.receipt.extraction_method
        assert committed.observation.provenance.source_document_id == "NOTICE-1"
        assert len(ObservationPersistence(test_store).load()) == 1

        repeated = service.commit(
            commit_id="COMMIT-2", recorder="Commit Service",
            acquisition=acquired, extraction=extracted, title="Policy change",
            entity="Banking", category="REGULATORY", confidence=88,
        )
        assert not repeated.committed and repeated.status == "NOT_COMMITTED_REJECT"
        assert "DUPLICATE_EXISTING_OBSERVATION" in repeated.admission.reason_codes
        assert len(ObservationPersistence(test_store).load()) == 1

        partial = replace(extracted, receipt=replace(extracted.receipt, status=type(extracted.receipt.status).PARTIAL, warnings=("Incomplete",)))
        deferred = PublicObservationCommitService(
            PublicObservationAdmissionGate(registry), ObservationEngine(persistence=ObservationPersistence(root / "partial.json")), audit, clock=lambda: now + timedelta(seconds=3)
        ).commit(commit_id="COMMIT-3", recorder="Commit Service", acquisition=acquired, extraction=partial, title="Partial", entity="Banking", category="REGULATORY", confidence=40)
        assert not deferred.committed and deferred.status == "NOT_COMMITTED_DEFER"
        assert not (root / "partial.json").exists()
        events = audit.read_all()
        assert [event.status.value for event in events] == ["AUTHORIZED", "COMMITTED", "BLOCKED", "BLOCKED"]
        assert audit.unresolved_commit_ids() == ()
        audit.begin(commit_id="COMMIT-INTERRUPTED", admission=committed.admission, recorded_at=now + timedelta(seconds=4), recorder="Commit Service")
        assert audit.unresolved_commit_ids() == ("COMMIT-INTERRUPTED",)
        assert production.read_bytes() == b'{"preserve":"exactly"}'

    print("PUBLIC OBSERVATION COMMIT SERVICE: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
