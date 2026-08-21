"""Read-only aggregation of reconciled historical review candidates."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Iterable

from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewCandidate,
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence.historical_comparison_review_decision_summary import (
    HistoricalComparisonReviewCount,
    HistoricalComparisonReviewDecisionSummary,
)


class HistoricalComparisonReviewDecisionSummarizer:
    """Summarize explicit review facts without interpreting their meaning."""

    def summarize(
        self,
        candidates: Iterable[HistoricalComparisonReviewCandidate],
    ) -> HistoricalComparisonReviewDecisionSummary:
        if candidates is None:
            raise ValueError("candidates must not be None")

        candidate_list = tuple(candidates)
        candidate_ids = set()
        reviewed_at_values = []
        for candidate in candidate_list:
            if not isinstance(candidate, HistoricalComparisonReviewCandidate):
                raise ValueError("candidates contain an invalid item")
            if candidate.candidate_id in candidate_ids:
                raise ValueError("candidate identities must be unique")
            candidate_ids.add(candidate.candidate_id)
            if not isinstance(candidate.status, HistoricalComparisonReviewStatus):
                raise ValueError("candidate contains an invalid review status")
            self._validate_review_metadata(candidate)
            if candidate.reviewed_at is not None:
                reviewed_at_values.append(candidate.reviewed_at)

        try:
            earliest_reviewed_at = (
                min(reviewed_at_values) if reviewed_at_values else None
            )
            latest_reviewed_at = (
                max(reviewed_at_values) if reviewed_at_values else None
            )
        except TypeError as exc:
            raise ValueError(
                "review timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc

        status_counts = Counter(candidate.status for candidate in candidate_list)
        pending = tuple(
            sorted(
                candidate.candidate_id
                for candidate in candidate_list
                if candidate.status == HistoricalComparisonReviewStatus.PENDING
            )
        )
        decided = tuple(candidate for candidate in candidate_list if candidate.reviewed)

        return HistoricalComparisonReviewDecisionSummary(
            candidate_count=len(candidate_list),
            pending_count=len(pending),
            decided_count=len(decided),
            reviewed_count=status_counts[HistoricalComparisonReviewStatus.REVIEWED],
            accepted_count=status_counts[HistoricalComparisonReviewStatus.ACCEPTED],
            rejected_count=status_counts[HistoricalComparisonReviewStatus.REJECTED],
            deferred_count=status_counts[HistoricalComparisonReviewStatus.DEFERRED],
            by_entity=self._counts(
                candidate.current_observation.entity for candidate in candidate_list
            ),
            by_category=self._counts(
                candidate.current_observation.category for candidate in candidate_list
            ),
            by_comparison_type=self._counts(
                candidate.comparison_type.value for candidate in candidate_list
            ),
            by_reviewer=self._counts(
                candidate.reviewer for candidate in decided
            ),
            by_review_date=self._counts(
                candidate.reviewed_at.date().isoformat() for candidate in decided
            ),
            unresolved_candidate_ids=pending,
            earliest_reviewed_at=earliest_reviewed_at,
            latest_reviewed_at=latest_reviewed_at,
        )

    @staticmethod
    def _validate_review_metadata(candidate) -> None:
        metadata = (
            candidate.reviewer,
            candidate.reviewed_at,
            candidate.review_reason,
        )
        if candidate.status == HistoricalComparisonReviewStatus.PENDING:
            if any(value is not None for value in metadata):
                raise ValueError("pending candidate contains review metadata")
            return
        if any(value is None for value in metadata):
            raise ValueError("decided candidate lacks review metadata")
        if (
            not isinstance(candidate.reviewer, str)
            or not candidate.reviewer.strip()
            or not isinstance(candidate.review_reason, str)
            or not candidate.review_reason.strip()
            or not isinstance(candidate.reviewed_at, datetime)
        ):
            raise ValueError("decided candidate contains empty review metadata")

    @staticmethod
    def _counts(values) -> tuple[HistoricalComparisonReviewCount, ...]:
        counter = Counter(values)
        if None in counter:
            raise ValueError("summary dimension must not be None")
        if any(not isinstance(value, str) or not value for value in counter):
            raise ValueError("summary dimensions must be non-empty text")
        return tuple(
            HistoricalComparisonReviewCount(label=label, count=counter[label])
            for label in sorted(counter, key=lambda value: value.casefold())
        )


__all__ = ["HistoricalComparisonReviewDecisionSummarizer"]
