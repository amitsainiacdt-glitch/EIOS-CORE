"""Builds a non-persistent Observation proposal from one validated fact."""

from __future__ import annotations

import json
from hashlib import sha256

from modules.external_intelligence.public_factual_candidate import PublicFactualCandidate
from modules.external_intelligence.public_factual_candidate_validation import PublicFactualCandidateValidation
from modules.external_intelligence.public_factual_candidate_validator import PublicFactualCandidateValidator
from modules.external_intelligence.public_factual_observation_proposal import PublicFactualObservationProposal


class PublicFactualObservationProposalBuilder:
    def __init__(self, validator=None):
        self.validator = validator or PublicFactualCandidateValidator()

    def build(self, *, proposal_id, candidate, validation, acquisition, extraction, title=None):
        proposal_id = self._text(proposal_id, "proposal_id")
        if not isinstance(candidate, PublicFactualCandidate):
            raise ValueError("candidate must be a PublicFactualCandidate")
        if not isinstance(validation, PublicFactualCandidateValidation) or not validation.validated:
            raise ValueError("proposal requires a VALIDATED factual candidate")
        current = self.validator.validate(candidate=candidate, acquisition=acquisition, extraction=extraction)
        if not current.validated or current != validation:
            raise ValueError("candidate validation is stale or does not match current source data")
        title = self._text(title, "title") if title is not None else self._default_title(candidate)
        values = {
            "candidate_id": candidate.candidate_id,
            "title": title,
            "description": candidate.source_passage,
            "entity": candidate.subject_entity,
            "category": f"PUBLIC_FACT_{candidate.event_type}",
            "source_url": candidate.source_url,
            "event_type": candidate.event_type,
            "statement_posture": candidate.statement_posture,
            "acquisition_id": candidate.acquisition_id,
            "extraction_id": candidate.extraction_id,
            "document_hash": candidate.document_hash,
            "extracted_content_fingerprint": candidate.extracted_content_fingerprint,
            "extraction_method": candidate.extraction_method,
            "explicit_amounts": candidate.explicit_amounts,
            "explicit_dates": candidate.explicit_dates,
        }
        fingerprint = self.fingerprint_values(values)
        return PublicFactualObservationProposal(1, proposal_id, fingerprint, **values)

    @staticmethod
    def fingerprint_values(values):
        return sha256(json.dumps(values, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    @classmethod
    def verify_fingerprint(cls, proposal):
        values = {
            key: value for key, value in proposal.__dict__.items()
            if key not in {"schema_version", "proposal_id", "proposal_fingerprint", "requires_human_review"}
        }
        return cls.fingerprint_values(values) == proposal.proposal_fingerprint

    @staticmethod
    def _default_title(candidate):
        label = candidate.event_type.replace("_", " ").title()
        posture = "Negative " if candidate.statement_posture == "NEGATED" else ("Proposed " if candidate.statement_posture == "UNCERTAIN" else "")
        return f"{candidate.subject_entity}: {posture}{label}"

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["PublicFactualObservationProposalBuilder"]
