"""Maps one approved public factual proposal to the controlled write contract."""

from __future__ import annotations

from modules.intelligence_write import (
    ActorOrigin, ActorType, AuthorityScope, InformationClass, OriginType,
    SourceReference, ValidationStatus, WriteCommand, WriteOperation,
)


class PublicFactualControlledWriteAdapter:
    """Pure mapping only; source validation and human approval remain upstream."""

    VERSION = "public-factual-controlled-write-adapter-v1"

    def build_command(self, *, commit_id, proposal, review, candidate, acquisition,
                      extraction, published_at=None, filing_at=None):
        acquired = acquisition.receipt
        extracted = extraction.receipt
        event_at = filing_at or published_at or acquired.completed_at
        actor = ActorOrigin(
            actor_id=review.reviewer,
            actor_type=ActorType.HUMAN,
            actor_version="public-fact-review-v1",
            origin_id=review.review_id,
            origin_type=OriginType.HUMAN_REVIEW,
            authority_scopes=(AuthorityScope.PROPOSE_FACT, AuthorityScope.VERIFY_FACT),
        )
        source = SourceReference(
            source_id=acquired.source_document_id or acquired.acquisition_id,
            source_type=f"TRUSTED_PUBLIC_{acquisition.source.source_id}",
            source_url=acquired.source_url,
            document_hash=acquired.document_hash,
            page_or_section=f"characters {candidate.passage_start}-{candidate.passage_end}",
        )
        return WriteCommand(
            schema_version=1,
            command_id=f"controlled-public-fact:{commit_id}",
            idempotency_key=f"public-fact:{proposal.proposal_fingerprint}:{review.review_id}",
            operation=WriteOperation.PROPOSE_FACT,
            actor=actor,
            requested_at=review.reviewed_at,
            company_id=proposal.entity,
            entity=proposal.entity,
            information_class=InformationClass.FACT,
            semantic_key=f"public-event|{proposal.event_type}|{candidate.candidate_id}",
            payload={
                "statement": proposal.description,
                "event_type": proposal.event_type,
                "event_at": event_at.isoformat(),
                "statement_posture": proposal.statement_posture,
                "explicit_amounts": proposal.explicit_amounts,
                "explicit_dates": proposal.explicit_dates,
                "acquisition_id": acquired.acquisition_id,
                "extraction_id": extracted.extraction_id,
                "proposal_id": proposal.proposal_id,
                "review_id": review.review_id,
            },
            source_references=(source,),
            confidence=review.approved_confidence,
            requested_validation_status=ValidationStatus.VERIFIED,
            correlation_id=commit_id,
            causation_id=proposal.proposal_id,
        )


__all__ = ["PublicFactualControlledWriteAdapter"]
