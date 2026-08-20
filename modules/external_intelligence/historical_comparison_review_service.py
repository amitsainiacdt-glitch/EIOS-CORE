"""Explicit in-memory human decisions for comparison review candidates."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewCandidate,
    HistoricalComparisonReviewStatus,
)


class HistoricalComparisonReviewService:
    """Return a newly reviewed candidate without persistence or publication."""

    def review(
        self,
        candidate: HistoricalComparisonReviewCandidate,
        *,
        status: HistoricalComparisonReviewStatus,
        reviewer: str,
        reason: str,
        reviewed_at: datetime,
    ) -> HistoricalComparisonReviewCandidate:
        if not isinstance(candidate, HistoricalComparisonReviewCandidate):
            raise ValueError(
                "candidate must be a HistoricalComparisonReviewCandidate"
            )

        if candidate.status != HistoricalComparisonReviewStatus.PENDING:
            raise ValueError("candidate has already been reviewed")

        if (
            not isinstance(status, HistoricalComparisonReviewStatus)
            or status == HistoricalComparisonReviewStatus.PENDING
        ):
            raise ValueError("status must be an explicit review disposition")

        reviewer_value = self._required_text(reviewer, "reviewer")
        reason_value = self._required_text(reason, "reason")

        if not isinstance(reviewed_at, datetime):
            raise ValueError("reviewed_at must be a datetime")

        try:
            if reviewed_at < candidate.recorded_at:
                raise ValueError(
                    "reviewed_at must not precede the audit record"
                )
        except TypeError as exc:
            raise ValueError(
                "review and audit timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc

        return replace(
            candidate,
            status=status,
            reviewer=reviewer_value,
            reviewed_at=reviewed_at,
            review_reason=reason_value,
        )

    @staticmethod
    def _required_text(value, name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["HistoricalComparisonReviewService"]
