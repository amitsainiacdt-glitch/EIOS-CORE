"""Final audited commit boundary for an approved factual Observation proposal."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from modules.external_intelligence.external_observation_adapter import ExternalObservationAdapter
from modules.external_intelligence.public_factual_candidate import PublicFactualCandidate
from modules.external_intelligence.public_factual_candidate_validator import PublicFactualCandidateValidator
from modules.external_intelligence.public_factual_observation_proposal import PublicFactualObservationProposal
from modules.external_intelligence.public_factual_observation_proposal_builder import PublicFactualObservationProposalBuilder
from modules.external_intelligence.public_factual_observation_review_ledger import PublicFactualObservationReviewDecision, PublicFactualObservationReviewReceipt
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_observation_commit_audit import PublicObservationCommitAuditLedger
from modules.external_intelligence.public_observation_commit_service import PublicObservationCommitResult
from modules.external_intelligence.public_factual_controlled_write_adapter import PublicFactualControlledWriteAdapter
from modules.intelligence_write import ControlledIntelligenceWriteService, WriteReceiptStatus
from modules.observation.observation_engine import ObservationEngine


class ReviewedPublicFactualObservationCommitService:
    """Commits exact reviewed fact text; never invokes downstream analysis."""

    def __init__(self, gate, observation_engine, audit_ledger, *, validator=None, clock=None,
                 controlled_write_service=None, controlled_write_adapter=None):
        if not isinstance(gate, PublicObservationAdmissionGate): raise ValueError("gate must be a PublicObservationAdmissionGate")
        if not isinstance(observation_engine, ObservationEngine): raise ValueError("observation_engine must be an ObservationEngine")
        if not isinstance(audit_ledger, PublicObservationCommitAuditLedger): raise ValueError("audit_ledger must be a PublicObservationCommitAuditLedger")
        self.gate, self.observation_engine, self.audit_ledger = gate, observation_engine, audit_ledger
        self.validator = validator or PublicFactualCandidateValidator()
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.adapter = ExternalObservationAdapter(observation_engine)
        self.controlled_write_service = controlled_write_service or ControlledIntelligenceWriteService(clock=self.clock)
        if not isinstance(self.controlled_write_service, ControlledIntelligenceWriteService):
            raise ValueError("controlled_write_service must be a ControlledIntelligenceWriteService")
        self.controlled_write_adapter = controlled_write_adapter or PublicFactualControlledWriteAdapter()
        if not isinstance(self.controlled_write_adapter, PublicFactualControlledWriteAdapter):
            raise ValueError("controlled_write_adapter must be a PublicFactualControlledWriteAdapter")

    def commit(self, *, commit_id, proposal, review, candidate, acquisition, extraction, recorder, published_at=None, filing_at=None):
        if not isinstance(proposal, PublicFactualObservationProposal): raise ValueError("proposal must be a PublicFactualObservationProposal")
        if not isinstance(review, PublicFactualObservationReviewReceipt): raise ValueError("review must be a PublicFactualObservationReviewReceipt")
        if not isinstance(candidate, PublicFactualCandidate): raise ValueError("candidate must be a PublicFactualCandidate")
        if not PublicFactualObservationProposalBuilder.verify_fingerprint(proposal): raise ValueError("proposal fingerprint does not match proposal content")
        if review.proposal_id != proposal.proposal_id or review.proposal_fingerprint != proposal.proposal_fingerprint: raise ValueError("review does not bind to proposal")
        if review.decision != PublicFactualObservationReviewDecision.APPROVE or review.approved_confidence is None: raise ValueError("commit requires an APPROVE review with confidence")
        validation = self.validator.validate(candidate=candidate, acquisition=acquisition, extraction=extraction)
        if not validation.validated: raise ValueError("candidate is no longer validated")
        rebuilt = PublicFactualObservationProposalBuilder(self.validator).build(
            proposal_id=proposal.proposal_id, candidate=candidate, validation=validation,
            acquisition=acquisition, extraction=extraction, title=proposal.title,
        )
        if rebuilt != proposal: raise ValueError("proposal no longer matches the validated candidate")
        admission = self.gate.preview(
            acquisition=acquisition, extraction=extraction, observations=tuple(self.observation_engine.registry.all()),
            title=proposal.title, entity=proposal.entity, category=proposal.category,
            confidence=review.approved_confidence,
        )
        if not admission.admissible:
            self.audit_ledger.block(commit_id=commit_id, admission=admission, proposal=proposal, review=review, recorded_at=self.clock(), recorder=recorder)
            return PublicObservationCommitResult(False, f"NOT_COMMITTED_{admission.decision.value}", admission, None)
        controlled_command = self.controlled_write_adapter.build_command(
            commit_id=commit_id, proposal=proposal, review=review, candidate=candidate,
            acquisition=acquisition, extraction=extraction,
            published_at=published_at, filing_at=filing_at,
        )
        controlled_receipt = self.controlled_write_service.submit(controlled_command)
        if controlled_receipt.status not in {WriteReceiptStatus.ACCEPTED, WriteReceiptStatus.DUPLICATE_NO_CHANGE}:
            self.audit_ledger.block(
                commit_id=commit_id, admission=admission, proposal=proposal, review=review,
                recorded_at=self.clock(), recorder=recorder,
            )
            return PublicObservationCommitResult(
                False, "NOT_COMMITTED_CONTROLLED_WRITE_REJECTED", admission, None, controlled_receipt,
            )
        self.audit_ledger.begin(commit_id=commit_id, admission=admission, proposal=proposal, review=review, recorded_at=self.clock(), recorder=recorder)
        acquired = acquisition.receipt
        observation = self.adapter.ingest(
            title=proposal.title, description=proposal.description, source=proposal.source_url,
            category=proposal.category, entity=proposal.entity, confidence=review.approved_confidence,
            cycle_id=acquired.cycle_id, job_id=acquired.job_id, research_intent=acquired.research_intent,
            retrieved_at=acquired.completed_at, published_at=published_at, filing_at=filing_at,
            content_type=acquired.content_type, source_document_id=acquired.source_document_id,
            document_hash=acquired.document_hash, extraction_method=proposal.extraction_method,
            public_fact_candidate_id=proposal.candidate_id,
            public_fact_event_type=proposal.event_type,
            public_fact_statement_posture=proposal.statement_posture,
            public_fact_proposal_id=proposal.proposal_id,
            public_fact_review_id=review.review_id,
        )
        status = "COMMITTED" if observation is not None else "FINAL_NOVELTY_REJECTION"
        fingerprint = observation.provenance.observation_fingerprint if observation is not None else None
        self.audit_ledger.complete(commit_id=commit_id, status=status, admission=admission, proposal=proposal, review=review, observation_fingerprint=fingerprint, recorded_at=self.clock(), recorder=recorder)
        return PublicObservationCommitResult(
            observation is not None,
            status if observation is not None else "NOT_COMMITTED_FINAL_NOVELTY_REJECTION",
            admission, observation, controlled_receipt,
        )


__all__ = ["ReviewedPublicFactualObservationCommitService"]
