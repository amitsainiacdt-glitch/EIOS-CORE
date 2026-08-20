"""Append-only persistence for explicit human review decisions."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_review_candidate import (
    HistoricalComparisonReviewCandidate,
    HistoricalComparisonReviewStatus,
)
from modules.external_intelligence.historical_comparison_review_decision import (
    HistoricalComparisonReviewDecision,
)


class HistoricalComparisonReviewDecisionLedger:
    """Persist at most one explicit decision for each candidate ID."""

    SCHEMA_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("review decision ledger path must identify a file")

    def record(
        self,
        candidate: HistoricalComparisonReviewCandidate,
    ) -> HistoricalComparisonReviewDecision:
        if not isinstance(candidate, HistoricalComparisonReviewCandidate):
            raise ValueError(
                "candidate must be a HistoricalComparisonReviewCandidate"
            )
        if not candidate.reviewed:
            raise ValueError("candidate must have an explicit review decision")
        self._candidate_id(candidate.candidate_id)
        if (
            candidate.reviewer is None
            or candidate.review_reason is None
            or candidate.reviewed_at is None
        ):
            raise ValueError("reviewed candidate lacks decision metadata")

        existing = self.read_all()
        if any(
            decision.candidate_id == candidate.candidate_id
            for decision in existing
        ):
            raise ValueError(
                "review decision already exists for candidate "
                f"{candidate.candidate_id}"
            )

        decision = HistoricalComparisonReviewDecision(
            schema_version=self.SCHEMA_VERSION,
            candidate_id=candidate.candidate_id,
            status=candidate.status,
            reviewer=candidate.reviewer,
            reason=candidate.review_reason,
            reviewed_at=candidate.reviewed_at,
        )
        payload = {
            "schema_version": decision.schema_version,
            "candidate_id": decision.candidate_id,
            "status": decision.status.value,
            "reviewer": decision.reviewer,
            "reason": decision.reason,
            "reviewed_at": decision.reviewed_at.isoformat(),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                json.dumps(
                    payload,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        return decision

    def read_all(
        self,
    ) -> tuple[HistoricalComparisonReviewDecision, ...]:
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("review decision ledger path must be a file")

        decisions = []
        candidate_ids = set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, start=1):
                if not line.strip():
                    continue
                try:
                    payload = json.loads(line)
                    decision = self._parse(payload)
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(
                        "Invalid review decision ledger record at line "
                        f"{line_number}: {exc}"
                    ) from exc
                if decision.candidate_id in candidate_ids:
                    raise ValueError(
                        "Duplicate review decision at line "
                        f"{line_number} for candidate "
                        f"{decision.candidate_id}"
                    )
                candidate_ids.add(decision.candidate_id)
                decisions.append(decision)
        return tuple(decisions)

    @classmethod
    def _parse(cls, payload) -> HistoricalComparisonReviewDecision:
        if not isinstance(payload, dict):
            raise ValueError("record must be a JSON object")
        version = payload["schema_version"]
        if not isinstance(version, int) or isinstance(version, bool) or version != 1:
            raise ValueError(f"unsupported schema version {version!r}")
        candidate_id = cls._candidate_id(payload["candidate_id"])
        status = HistoricalComparisonReviewStatus(payload["status"])
        if status == HistoricalComparisonReviewStatus.PENDING:
            raise ValueError("persisted status must be a review disposition")
        return HistoricalComparisonReviewDecision(
            schema_version=version,
            candidate_id=candidate_id,
            status=status,
            reviewer=cls._text(payload["reviewer"], "reviewer"),
            reason=cls._text(payload["reason"], "reason"),
            reviewed_at=datetime.fromisoformat(payload["reviewed_at"]),
        )

    @staticmethod
    def _text(value, name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _candidate_id(cls, value) -> str:
        candidate_id = cls._text(value, "candidate_id")
        if len(candidate_id) != 64:
            raise ValueError("candidate_id must be a SHA-256 identity")
        try:
            int(candidate_id, 16)
        except ValueError as exc:
            raise ValueError(
                "candidate_id must be a SHA-256 identity"
            ) from exc
        return candidate_id.casefold()


__all__ = ["HistoricalComparisonReviewDecisionLedger"]
