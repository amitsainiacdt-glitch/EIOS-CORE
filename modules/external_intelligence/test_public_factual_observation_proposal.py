"""Offline proposal and human-review tests using temporary ledgers only."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.http_retriever import RetrievedContent
from modules.external_intelligence.public_document_extraction_ledger import PublicDocumentExtractionLedger
from modules.external_intelligence.public_factual_candidate_extractor import PublicFactualCandidateExtractor
from modules.external_intelligence.public_factual_candidate_validator import PublicFactualCandidateValidator
from modules.external_intelligence.public_factual_candidate_validation import PublicFactualCandidateValidationDecision
from modules.external_intelligence.public_factual_observation_proposal_builder import PublicFactualObservationProposalBuilder
from modules.external_intelligence.public_factual_observation_review_package_builder import PublicFactualObservationReviewPackageBuilder
from modules.external_intelligence.public_factual_observation_review_ledger import PublicFactualObservationReviewLedger
from modules.external_intelligence.public_factual_observation_review_ledger import PublicFactualObservationReviewDecision
from modules.external_intelligence.public_observation_admission_gate import PublicObservationAdmissionGate
from modules.external_intelligence.public_observation_commit_audit import PublicObservationCommitAuditLedger
from modules.external_intelligence.public_source_acquisition_ledger import PublicSourceAcquisitionLedger
from modules.external_intelligence.trusted_public_acquisition_adapter import TrustedPublicAcquisitionResult
from modules.external_intelligence.trusted_public_document_extraction_adapter import TrustedPublicDocumentExtractionAdapter
from modules.external_intelligence.trusted_public_source_registry import TrustedPublicSourceDefinition, TrustedPublicSourceRegistry
from modules.external_intelligence.reviewed_public_factual_observation_commit_service import ReviewedPublicFactualObservationCommitService
from modules.external_intelligence.public_factual_controlled_write_adapter import PublicFactualControlledWriteAdapter
from modules.observation.observation_engine import ObservationEngine
from modules.observation.observation_persistence import ObservationPersistence
from modules.intelligence_write import ControlledIntelligenceWriteService, InformationClass, ValidationStatus, WriteReceiptStatus, verify_receipt_fingerprint


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        now = datetime(2026, 8, 29, 17, tzinfo=timezone.utc)
        text = "Alpha Engineering Limited received an order worth INR 125 crore on 28 August 2026 from Metro Rail Corporation."
        body = text.encode()
        registry = TrustedPublicSourceRegistry((TrustedPublicSourceDefinition("NSE", "NSE", ("nseindia.com",)),))
        receipt = PublicSourceAcquisitionLedger(root / "a.jsonl").record(
            acquisition_id="A1", cycle_id="C1", job_id="J1", research_intent="FACT_PROPOSAL",
            source_url="https://www.nseindia.com/announcement/1", access_classification="PUBLIC", status="RETRIEVED",
            requested_at=now, completed_at=now, http_status=200, content_type="text/plain",
            source_document_id="ANN-1", document_hash=sha256(body).hexdigest(), bytes_received=len(body), recorder="Acquirer",
        )
        acquisition = TrustedPublicAcquisitionResult(registry.resolve(receipt.source_url), receipt, RetrievedContent(receipt.source_url, 200, text, "text/plain", {}), body)
        extraction = TrustedPublicDocumentExtractionAdapter(PublicDocumentExtractionLedger(root / "e.jsonl"), clock=lambda: now + timedelta(seconds=1)).extract(acquisition, extraction_id="E1", recorder="Extractor")
        admission = PublicObservationAdmissionGate(registry).preview(acquisition=acquisition, extraction=extraction, observations=(), title="Filing", entity="Alpha Engineering Limited", category="EXCHANGE_FILING", confidence=80)
        candidate_preview = PublicFactualCandidateExtractor().extract(acquisition=acquisition, extraction=extraction, admission=admission, subject_entity="Alpha Engineering Limited")
        candidate = candidate_preview.candidates[0]
        validation = PublicFactualCandidateValidator().validate(candidate=candidate, acquisition=acquisition, extraction=extraction)
        proposal = PublicFactualObservationProposalBuilder().build(proposal_id="PROP-1", candidate=candidate, validation=validation, acquisition=acquisition, extraction=extraction)
        assert proposal.description == candidate.source_passage
        assert proposal.category == "PUBLIC_FACT_ORDER_CONTRACT"
        assert proposal.requires_human_review and not hasattr(proposal, "confidence")
        assert proposal.explicit_amounts == ("INR 125 crore",)
        package = PublicFactualObservationReviewPackageBuilder().build(
            package_id="PKG-1", candidate_preview=candidate_preview, validations=(validation,), acquisition=acquisition,
            extraction=extraction, included_event_types=("ORDER_CONTRACT",),
        )
        assert len(package.proposals) == 1 and package.proposals[0].description == candidate.source_passage
        assert package.package_status == "READY_FOR_HUMAN_PROPOSAL_REVIEW" and not package.deferred_candidates
        assert package.requires_human_review and not package.creates_observation
        assert PublicFactualObservationReviewPackageBuilder().build(
            package_id="PKG-1", candidate_preview=candidate_preview, validations=(validation,), acquisition=acquisition,
            extraction=extraction, included_event_types=("ORDER_CONTRACT",),
        ) == package
        deferred_validation = replace(
            validation, decision=PublicFactualCandidateValidationDecision.DEFER,
            reason_codes=("UNCERTAIN_STATEMENT_REQUIRES_CORROBORATION",), requires_corroboration=True,
        )
        held_package = PublicFactualObservationReviewPackageBuilder().build(
            package_id="PKG-HOLD", candidate_preview=candidate_preview, validations=(deferred_validation,),
            acquisition=acquisition, extraction=extraction, included_event_types=("ORDER_CONTRACT",),
        )
        assert held_package.package_status == "RESEARCH_HOLD_CORROBORATION"
        assert not held_package.proposals and len(held_package.deferred_candidates) == 1
        try:
            PublicFactualObservationReviewPackageBuilder().build(
                package_id="PKG-BLOCKED", candidate_preview=candidate_preview, validations=(validation,), acquisition=acquisition,
                extraction=extraction, included_event_types=("WEATHER_ANOMALY",),
            )
        except ValueError as exc:
            assert "at least one" in str(exc)
        else:
            raise AssertionError("empty review package accepted")

        ledger = PublicFactualObservationReviewLedger(root / "reviews.jsonl")
        approved = ledger.record(proposal, review_id="REV-1", decision="APPROVE", approved_confidence=82, notes="Exact exchange passage confirms the order; materiality requires later analysis.", reviewed_at=now + timedelta(minutes=1), reviewer="Human Reviewer")
        assert approved.approved_confidence == 82.0 and ledger.read_all() == (approved,)
        observation_path = root / "reviewed-observations.json"
        audit = PublicObservationCommitAuditLedger(root / "commit-audit.jsonl")
        reviewed_service = ReviewedPublicFactualObservationCommitService(
            PublicObservationAdmissionGate(registry),
            ObservationEngine(persistence=ObservationPersistence(observation_path)),
            audit, clock=lambda: now + timedelta(minutes=2),
        )
        committed = reviewed_service.commit(
            commit_id="COMMIT-PROP-1", proposal=proposal, review=approved,
            candidate=candidate, acquisition=acquisition, extraction=extraction,
            recorder="Reviewed Fact Commit",
        )
        assert committed.committed
        assert committed.observation.description == candidate.source_passage
        assert committed.observation.confidence == 82.0
        assert committed.observation.category == "PUBLIC_FACT_ORDER_CONTRACT"
        assert committed.observation.provenance.public_fact_candidate_id == candidate.candidate_id
        assert committed.observation.provenance.public_fact_event_type == "ORDER_CONTRACT"
        assert committed.observation.provenance.public_fact_statement_posture == "ASSERTED"
        assert committed.observation.provenance.public_fact_proposal_id == proposal.proposal_id
        assert committed.observation.provenance.public_fact_review_id == approved.review_id
        assert committed.controlled_write_receipt.status == WriteReceiptStatus.ACCEPTED
        assert verify_receipt_fingerprint(committed.controlled_write_receipt)
        controlled_record = reviewed_service.controlled_write_service.get_record(committed.controlled_write_receipt.record_id)
        assert controlled_record.information_class == InformationClass.FACT
        assert controlled_record.validation_status == ValidationStatus.VERIFIED
        assert controlled_record.payload["statement"] == candidate.source_passage
        assert controlled_record.source_references[0].document_hash == receipt.document_hash
        assert reviewed_service.controlled_write_service.trusted_records() == (controlled_record,)
        audit_events = audit.read_all()
        assert [item.status.value for item in audit_events] == ["AUTHORIZED", "COMMITTED"]
        assert all(item.proposal_id == proposal.proposal_id and item.review_id == approved.review_id for item in audit_events)
        assert len(ObservationPersistence(observation_path).load()) == 1
        conflict_write_service = ControlledIntelligenceWriteService(clock=lambda: now + timedelta(minutes=2))
        controlled_adapter = PublicFactualControlledWriteAdapter()
        seed = controlled_adapter.build_command(
            commit_id="SEED-CONFLICT", proposal=proposal, review=approved, candidate=candidate,
            acquisition=acquisition, extraction=extraction,
        )
        seed = replace(
            seed, command_id="seed-conflicting-fact", idempotency_key="seed-conflicting-fact",
            payload={**seed.payload, "statement": seed.payload["statement"] + " conflicting"},
        )
        assert conflict_write_service.submit(seed).status == WriteReceiptStatus.ACCEPTED
        conflict_observations = root / "controlled-conflict-observations.json"
        conflict_audit = PublicObservationCommitAuditLedger(root / "controlled-conflict-audit.jsonl")
        controlled_block = ReviewedPublicFactualObservationCommitService(
            PublicObservationAdmissionGate(registry),
            ObservationEngine(persistence=ObservationPersistence(conflict_observations)),
            conflict_audit, clock=lambda: now + timedelta(minutes=3),
            controlled_write_service=conflict_write_service,
        ).commit(
            commit_id="CONTROLLED-CONFLICT", proposal=proposal, review=approved,
            candidate=candidate, acquisition=acquisition, extraction=extraction,
            recorder="Reviewed Fact Commit",
        )
        assert not controlled_block.committed
        assert controlled_block.status == "NOT_COMMITTED_CONTROLLED_WRITE_REJECTED"
        assert controlled_block.controlled_write_receipt.status == WriteReceiptStatus.CONFLICT_RECORDED
        assert not conflict_observations.exists()
        assert [item.status.value for item in conflict_audit.read_all()] == ["BLOCKED"]
        deferred_review = replace(approved, decision=PublicFactualObservationReviewDecision.DEFER, approved_confidence=None)
        try:
            ReviewedPublicFactualObservationCommitService(
                PublicObservationAdmissionGate(registry), ObservationEngine(persistence=ObservationPersistence(root / "blocked.json")),
                PublicObservationCommitAuditLedger(root / "blocked-audit.jsonl"),
            ).commit(commit_id="BLOCKED", proposal=proposal, review=deferred_review, candidate=candidate, acquisition=acquisition, extraction=extraction, recorder="Committer")
        except ValueError as exc:
            assert "APPROVE" in str(exc)
        else:
            raise AssertionError("deferred human review reached commit")
        mismatched_review = replace(approved, proposal_fingerprint="0" * 64)
        try:
            ReviewedPublicFactualObservationCommitService(
                PublicObservationAdmissionGate(registry), ObservationEngine(persistence=ObservationPersistence(root / "mismatch.json")),
                PublicObservationCommitAuditLedger(root / "mismatch-audit.jsonl"),
            ).commit(commit_id="MISMATCH", proposal=proposal, review=mismatched_review, candidate=candidate, acquisition=acquisition, extraction=extraction, recorder="Committer")
        except ValueError as exc:
            assert "bind" in str(exc)
        else:
            raise AssertionError("mismatched review reached commit")
        tampered_proposal = replace(proposal, description=proposal.description + " altered")
        try:
            PublicFactualObservationReviewLedger(root / "tampered.jsonl").record(tampered_proposal, review_id="REV-TAMPER", decision="REJECT", notes="Tampered", reviewed_at=now, reviewer="Reviewer")
        except ValueError as exc:
            assert "fingerprint" in str(exc)
        else:
            raise AssertionError("tampered proposal accepted for review")
        try:
            ledger.record(proposal, review_id="REV-2", decision="REJECT", notes="Duplicate decision", reviewed_at=now, reviewer="Reviewer")
        except ValueError as exc:
            assert "already has" in str(exc)
        else:
            raise AssertionError("second review decision accepted")

        stale_validation = replace(validation, source_passage=validation.source_passage + " altered")
        try:
            PublicFactualObservationProposalBuilder().build(proposal_id="PROP-2", candidate=candidate, validation=stale_validation, acquisition=acquisition, extraction=extraction)
        except ValueError as exc:
            assert "stale" in str(exc)
        else:
            raise AssertionError("stale validation accepted")

        try:
            PublicFactualObservationReviewLedger(root / "bad.jsonl").record(proposal, review_id="REV-BAD", decision="APPROVE", notes="Missing confidence", reviewed_at=now, reviewer="Reviewer")
        except ValueError as exc:
            assert "approved_confidence" in str(exc)
        else:
            raise AssertionError("approval without confidence accepted")

    print("PUBLIC FACTUAL OBSERVATION PROPOSAL: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
