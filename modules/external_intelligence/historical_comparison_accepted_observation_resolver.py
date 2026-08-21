"""Exact read-only resolution of accepted reviews to persisted observations."""

from __future__ import annotations

from typing import Iterable

from modules.external_intelligence.historical_comparison_accepted_observation_preview import (
    HistoricalComparisonAcceptedObservationPreview,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewCandidate,
    HistoricalComparisonReviewStatus,
)
from modules.observation.observation import Observation


class HistoricalComparisonAcceptedObservationResolver:
    """Resolve accepted candidates without returning mutable source objects."""

    def resolve(
        self,
        candidate: HistoricalComparisonReviewCandidate,
        observations: Iterable[Observation],
    ) -> HistoricalComparisonAcceptedObservationPreview:
        if not isinstance(candidate, HistoricalComparisonReviewCandidate):
            raise ValueError("candidate must be a review candidate")
        if candidate.status != HistoricalComparisonReviewStatus.ACCEPTED:
            raise ValueError("candidate must have ACCEPTED status")
        if observations is None:
            raise ValueError("observations must not be None")
        if (
            candidate.reviewer is None
            or candidate.review_reason is None
            or candidate.reviewed_at is None
        ):
            raise ValueError("accepted candidate lacks review metadata")

        reference = candidate.current_observation
        fingerprint = self._fingerprint(reference.content_fingerprint)
        matches = []
        for observation in observations:
            if not isinstance(observation, Observation):
                raise ValueError("observations contain an invalid item")
            provenance = observation.provenance
            if (
                provenance is not None
                and provenance.content_fingerprint == fingerprint
            ):
                matches.append(observation)

        if not matches:
            raise ValueError(
                "accepted candidate source observation is missing for "
                f"fingerprint {fingerprint}"
            )
        if len(matches) > 1:
            raise ValueError(
                "accepted candidate source observation is ambiguous for "
                f"fingerprint {fingerprint}"
            )

        observation = matches[0]
        self._validate_identity(reference, observation)
        provenance = observation.provenance
        return HistoricalComparisonAcceptedObservationPreview(
            candidate_id=candidate.candidate_id,
            audit_recorded_at=candidate.recorded_at,
            reviewer=candidate.reviewer,
            review_reason=candidate.review_reason,
            reviewed_at=candidate.reviewed_at,
            title=observation.title,
            description=observation.description,
            source=observation.source,
            category=observation.category,
            entity=observation.entity,
            confidence=observation.confidence,
            timestamp=observation.timestamp,
            cycle_id=provenance.cycle_id,
            job_id=provenance.job_id,
            research_intent=provenance.research_intent,
            retrieved_at=provenance.retrieved_at,
            source_url=provenance.source_url,
            source_domain=provenance.source_domain,
            source_type=provenance.source_type,
            content_fingerprint=fingerprint,
        )

    @staticmethod
    def _fingerprint(value) -> str:
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError("audit content fingerprint must be SHA-256")
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError(
                "audit content fingerprint must be SHA-256"
            ) from exc
        return value.casefold()

    @staticmethod
    def _validate_identity(reference, observation) -> None:
        provenance = observation.provenance
        if provenance is None:
            raise ValueError("resolved observation lacks provenance")
        comparisons = (
            ("title", reference.title, observation.title),
            ("entity", reference.entity, observation.entity),
            ("category", reference.category, observation.category),
            ("timestamp", reference.timestamp, observation.timestamp),
            ("source", reference.source, observation.source),
            ("job_id", reference.job_id, provenance.job_id),
            (
                "research_intent",
                reference.research_intent,
                provenance.research_intent,
            ),
        )
        for name, expected, actual in comparisons:
            if expected != actual:
                raise ValueError(
                    "resolved observation provenance mismatch: " + name
                )


__all__ = ["HistoricalComparisonAcceptedObservationResolver"]
