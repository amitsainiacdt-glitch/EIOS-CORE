"""Builds a review-only package from currently validated public facts."""

from __future__ import annotations

import hashlib
import json

from modules.external_intelligence.public_factual_candidate import PublicFactualCandidatePreview
from modules.external_intelligence.public_factual_candidate_validation import PublicFactualCandidateValidation
from modules.external_intelligence.public_factual_observation_proposal_builder import PublicFactualObservationProposalBuilder
from modules.external_intelligence.public_factual_observation_review_package import DeferredPublicFactualCandidate, PublicFactualObservationReviewPackage


class PublicFactualObservationReviewPackageBuilder:
    def __init__(self, proposal_builder=None):
        self.proposal_builder = proposal_builder or PublicFactualObservationProposalBuilder()

    def build(self, *, package_id, candidate_preview, validations, acquisition, extraction, included_event_types):
        package_id = self._text(package_id, "package_id")
        if not isinstance(candidate_preview, PublicFactualCandidatePreview):
            raise ValueError("candidate_preview must be a PublicFactualCandidatePreview")
        if not isinstance(validations, (list, tuple)) or any(not isinstance(item, PublicFactualCandidateValidation) for item in validations):
            raise ValueError("validations must contain PublicFactualCandidateValidation records")
        event_types = self._event_types(included_event_types)
        by_id = {item.candidate_id: item for item in validations}
        if len(by_id) != len(validations):
            raise ValueError("validations contain duplicate candidate IDs")
        proposals, deferred, excluded = [], [], []
        for candidate in candidate_preview.candidates:
            validation = by_id.get(candidate.candidate_id)
            if candidate.event_type not in event_types or validation is None:
                excluded.append(candidate.candidate_id)
                continue
            if not validation.validated:
                if validation.decision.value == "DEFER":
                    deferred.append(DeferredPublicFactualCandidate(
                        candidate.candidate_id, candidate.event_type, candidate.statement_posture,
                        candidate.source_passage, validation.decision.value, validation.reason_codes,
                        validation.requires_corroboration,
                    ))
                else:
                    excluded.append(candidate.candidate_id)
                continue
            proposals.append(self.proposal_builder.build(
                proposal_id=f"{package_id}-P{len(proposals) + 1:02d}", candidate=candidate,
                validation=validation, acquisition=acquisition, extraction=extraction,
            ))
        unused = set(by_id).difference(item.candidate_id for item in candidate_preview.candidates)
        if unused:
            raise ValueError("validation does not belong to the candidate preview")
        if not proposals and not deferred:
            raise ValueError("review package requires at least one included candidate")
        status = "READY_FOR_HUMAN_PROPOSAL_REVIEW" if proposals and not deferred else "RESEARCH_HOLD_CORROBORATION"
        values = {
            "package_id": package_id,
            "acquisition_id": acquisition.receipt.acquisition_id,
            "extraction_id": extraction.receipt.extraction_id,
            "document_hash": acquisition.receipt.document_hash,
            "source_url": acquisition.receipt.source_url,
            "proposal_fingerprints": tuple(item.proposal_fingerprint for item in proposals),
            "deferred_candidates": tuple((item.candidate_id, item.validation_decision, item.reason_codes) for item in deferred),
            "excluded_candidate_ids": tuple(excluded),
            "package_status": status,
        }
        fingerprint = hashlib.sha256(json.dumps(values, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return PublicFactualObservationReviewPackage(
            1, package_id, fingerprint, values["acquisition_id"], values["extraction_id"],
            values["document_hash"], values["source_url"], tuple(proposals), tuple(deferred), tuple(excluded), status,
        )

    @staticmethod
    def to_payload(package):
        if not isinstance(package, PublicFactualObservationReviewPackage):
            raise ValueError("package must be a PublicFactualObservationReviewPackage")
        return {
            **{key: value for key, value in package.__dict__.items() if key not in {"proposals", "deferred_candidates"}},
            "proposals": [item.__dict__ for item in package.proposals],
            "deferred_candidates": [{**item.__dict__, "reason_codes": list(item.reason_codes)} for item in package.deferred_candidates],
            "excluded_candidate_ids": list(package.excluded_candidate_ids),
        }

    @staticmethod
    def _event_types(values):
        if not isinstance(values, (list, tuple)) or not values:
            raise ValueError("included_event_types must be a non-empty list")
        result = tuple(PublicFactualObservationReviewPackageBuilder._text(value, "event_type") for value in values)
        if len(set(result)) != len(result):
            raise ValueError("included_event_types must be unique")
        return frozenset(result)

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["PublicFactualObservationReviewPackageBuilder"]
