"""Build deterministic review candidates from explicit audit changes."""

from __future__ import annotations

import hashlib
import json
from typing import Iterable

from modules.external_intelligence.historical_comparison_audit_record import (
    HistoricalComparisonAuditRecord,
)
from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewCandidate,
)


class HistoricalComparisonReviewCandidateBuilder:
    """Create review candidates without financial interpretation."""

    ID_SCHEMA_VERSION = 1

    def build(
        self,
        records: Iterable[HistoricalComparisonAuditRecord],
    ) -> tuple[HistoricalComparisonReviewCandidate, ...]:
        if records is None:
            raise ValueError("records must not be None")

        candidates = []
        candidate_ids = set()

        for record in records:
            if not isinstance(record, HistoricalComparisonAuditRecord):
                raise ValueError(
                    "records must contain HistoricalComparisonAuditRecord"
                )

            if record.change_detected is not True:
                continue

            if (
                record.historical_observation is None
                or record.comparison_type is None
                or record.change_direction is None
                or record.materiality is None
                or record.comparison_provenance is None
            ):
                raise ValueError(
                    "detected-change record lacks comparison facts"
                )

            candidate_id = self._candidate_id(record)
            if candidate_id in candidate_ids:
                raise ValueError(
                    "duplicate historical comparison review candidate "
                    f"identity {candidate_id}"
                )

            candidate_ids.add(candidate_id)
            candidates.append(
                HistoricalComparisonReviewCandidate(
                    candidate_id=candidate_id,
                    recorded_at=record.recorded_at,
                    current_observation=record.current_observation,
                    historical_observation=(
                        record.historical_observation
                    ),
                    selection_basis=record.selection_basis,
                    comparison_type=record.comparison_type,
                    change_direction=record.change_direction,
                    materiality=record.materiality,
                    delta=record.delta,
                    comparison_provenance=(
                        record.comparison_provenance
                    ),
                )
            )

        try:
            candidates.sort(
                key=lambda candidate: (
                    candidate.recorded_at,
                    candidate.candidate_id,
                )
            )
        except TypeError as exc:
            raise ValueError(
                "candidate timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc

        return tuple(candidates)

    @classmethod
    def _candidate_id(cls, record) -> str:
        identity = {
            "schema_version": cls.ID_SCHEMA_VERSION,
            "recorded_at": record.recorded_at.isoformat(),
            "current": cls._observation_identity(
                record.current_observation
            ),
            "historical": cls._observation_identity(
                record.historical_observation
            ),
            "selection_basis": (
                record.selection_basis.value
                if record.selection_basis is not None
                else None
            ),
            "comparison_type": record.comparison_type.value,
            "comparison_provenance": record.comparison_provenance,
        }
        canonical = json.dumps(
            identity,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def _observation_identity(observation) -> dict:
        return {
            "content_fingerprint": observation.content_fingerprint,
            "title": observation.title,
            "entity": observation.entity,
            "category": observation.category,
            "timestamp": observation.timestamp.isoformat(),
            "job_id": observation.job_id,
            "research_intent": observation.research_intent,
        }


__all__ = ["HistoricalComparisonReviewCandidateBuilder"]
