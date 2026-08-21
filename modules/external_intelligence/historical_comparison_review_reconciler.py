"""Read-only reconciliation of review candidates and persisted decisions."""

from dataclasses import replace
from typing import Iterable

from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewCandidate,
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence.historical_comparison_review_decision import (
    HistoricalComparisonReviewDecision,
)


class HistoricalComparisonReviewReconciler:
    """Overlay valid decisions without modifying candidates or ledgers."""

    def reconcile(
        self,
        candidates: Iterable[HistoricalComparisonReviewCandidate],
        decisions: Iterable[HistoricalComparisonReviewDecision],
    ) -> tuple[HistoricalComparisonReviewCandidate, ...]:
        if candidates is None or decisions is None:
            raise ValueError("candidates and decisions must not be None")

        candidate_list = tuple(candidates)
        decision_list = tuple(decisions)
        candidate_ids = set()
        for candidate in candidate_list:
            if not isinstance(candidate, HistoricalComparisonReviewCandidate):
                raise ValueError("candidates contain an invalid item")
            if candidate.status != HistoricalComparisonReviewStatus.PENDING:
                raise ValueError("source candidates must be pending")
            if candidate.candidate_id in candidate_ids:
                raise ValueError("candidate identities must be unique")
            candidate_ids.add(candidate.candidate_id)

        decision_by_id = {}
        for decision in decision_list:
            if not isinstance(decision, HistoricalComparisonReviewDecision):
                raise ValueError("decisions contain an invalid item")
            if decision.candidate_id not in candidate_ids:
                raise ValueError(
                    "decision references unknown candidate "
                    f"{decision.candidate_id}"
                )
            if decision.candidate_id in decision_by_id:
                raise ValueError("candidate has multiple decisions")
            decision_by_id[decision.candidate_id] = decision

        reconciled = []
        for candidate in candidate_list:
            decision = decision_by_id.get(candidate.candidate_id)
            if decision is None:
                reconciled.append(candidate)
                continue
            try:
                if decision.reviewed_at < candidate.recorded_at:
                    raise ValueError(
                        "decision timestamp precedes candidate audit time"
                    )
            except TypeError as exc:
                raise ValueError(
                    "candidate and decision timestamps must use a "
                    "consistent timezone-awareness policy"
                ) from exc
            reconciled.append(
                replace(
                    candidate,
                    status=decision.status,
                    reviewer=decision.reviewer,
                    reviewed_at=decision.reviewed_at,
                    review_reason=decision.reason,
                )
            )
        return tuple(reconciled)


__all__ = ["HistoricalComparisonReviewReconciler"]
