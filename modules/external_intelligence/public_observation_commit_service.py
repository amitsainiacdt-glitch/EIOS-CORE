"""Controlled conversion of an admissible public document into one Observation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from modules.external_intelligence.external_observation_adapter import ExternalObservationAdapter
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_observation_admission_preview import PublicObservationAdmissionPreview
from modules.external_intelligence.public_observation_commit_audit import PublicObservationCommitAuditLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionResult
from modules.observation.observation import Observation
from modules.observation.observation_engine import ObservationEngine


@dataclass(frozen=True)
class PublicObservationCommitResult:
    committed: bool
    status: str
    admission: PublicObservationAdmissionPreview
    observation: Observation | None


class PublicObservationCommitService:
    """Rechecks admission at write time and never creates downstream analysis."""

    def __init__(self, gate, observation_engine, audit_ledger, *, clock=None):
        if not isinstance(gate, PublicObservationAdmissionGate):
            raise ValueError("gate must be a PublicObservationAdmissionGate")
        if not isinstance(observation_engine, ObservationEngine):
            raise ValueError("observation_engine must be an ObservationEngine")
        if not isinstance(audit_ledger, PublicObservationCommitAuditLedger):
            raise ValueError("audit_ledger must be a PublicObservationCommitAuditLedger")
        self.gate = gate
        self.observation_engine = observation_engine
        self.audit_ledger = audit_ledger
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.adapter = ExternalObservationAdapter(observation_engine)

    def commit(
        self, *, commit_id, acquisition, extraction, title, entity, category, confidence, recorder,
        published_at: datetime | None = None, filing_at: datetime | None = None,
    ):
        if not isinstance(acquisition, TrustedPublicAcquisitionResult):
            raise ValueError("acquisition must be a TrustedPublicAcquisitionResult")
        if not isinstance(extraction, TrustedPublicDocumentExtractionResult):
            raise ValueError("extraction must be a TrustedPublicDocumentExtractionResult")
        admission = self.gate.preview(
            acquisition=acquisition, extraction=extraction,
            observations=tuple(self.observation_engine.registry.all()),
            title=title, entity=entity, category=category, confidence=confidence,
        )
        if not admission.admissible:
            self.audit_ledger.block(commit_id=commit_id, admission=admission, recorded_at=self.clock(), recorder=recorder)
            return PublicObservationCommitResult(False, f"NOT_COMMITTED_{admission.decision.value}", admission, None)

        self.audit_ledger.begin(commit_id=commit_id, admission=admission, recorded_at=self.clock(), recorder=recorder)

        acquired, extracted = acquisition.receipt, extraction.receipt
        observation = self.adapter.ingest(
            title=admission.title, description=extraction.extracted_text,
            source=acquired.source_url, category=admission.category,
            entity=admission.entity, confidence=admission.confidence,
            cycle_id=acquired.cycle_id, job_id=acquired.job_id,
            research_intent=acquired.research_intent, retrieved_at=acquired.completed_at,
            published_at=published_at, filing_at=filing_at,
            content_type=acquired.content_type,
            source_document_id=acquired.source_document_id,
            document_hash=acquired.document_hash,
            extraction_method=extracted.extraction_method,
        )
        if observation is None:
            self.audit_ledger.complete(commit_id=commit_id, status="FINAL_NOVELTY_REJECTION", admission=admission, observation_fingerprint=None, recorded_at=self.clock(), recorder=recorder)
            return PublicObservationCommitResult(False, "NOT_COMMITTED_FINAL_NOVELTY_REJECTION", admission, None)
        self.audit_ledger.complete(commit_id=commit_id, status="COMMITTED", admission=admission, observation_fingerprint=observation.provenance.observation_fingerprint, recorded_at=self.clock(), recorder=recorder)
        return PublicObservationCommitResult(True, "COMMITTED", admission, observation)


__all__ = ["PublicObservationCommitResult", "PublicObservationCommitService"]
