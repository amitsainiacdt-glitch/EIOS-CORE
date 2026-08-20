"""Append-only audit reporting for runtime historical comparisons."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.runtime_historical_comparison import (
    RuntimeHistoricalComparison,
)


class HistoricalComparisonAuditReporter:
    """Serialize passive runtime comparison records as JSON Lines."""

    SCHEMA_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

        if str(self.path).strip() in {"", "."}:
            raise ValueError("audit path must identify a file")

    def report(
        self,
        record: RuntimeHistoricalComparison,
        *,
        recorded_at: datetime,
    ) -> None:
        if not isinstance(record, RuntimeHistoricalComparison):
            raise ValueError(
                "record must be a RuntimeHistoricalComparison"
            )

        if not isinstance(recorded_at, datetime):
            raise ValueError("recorded_at must be a datetime")

        payload = self._payload(record, recorded_at)
        line = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open("a", encoding="utf-8") as audit_file:
            audit_file.write(line + "\n")

    @classmethod
    def _payload(
        cls,
        record: RuntimeHistoricalComparison,
        recorded_at: datetime,
    ) -> dict:
        selection = record.selection
        comparison = record.comparison

        return {
            "schema_version": cls.SCHEMA_VERSION,
            "recorded_at": recorded_at.isoformat(),
            "current_observation": cls._observation_reference(
                record.current_observation
            ),
            "historical_observation": (
                cls._observation_reference(
                    selection.selected_observation
                )
                if selection.selected_observation is not None
                else None
            ),
            "selection": {
                "basis": (
                    selection.selection_basis.value
                    if selection.selection_basis is not None
                    else None
                ),
                "eligible_count": selection.eligible_count,
                "reason": selection.reason,
            },
            "comparison": (
                {
                    "type": comparison.comparison_type.value,
                    "change_detected": comparison.change_detected,
                    "change_direction": (
                        comparison.change_direction.value
                    ),
                    "materiality": comparison.materiality.value,
                    "delta": comparison.delta,
                    "provenance": comparison.provenance,
                }
                if comparison is not None
                else None
            ),
        }

    @staticmethod
    def _observation_reference(observation) -> dict:
        provenance = observation.provenance

        return {
            "title": observation.title,
            "entity": observation.entity,
            "category": observation.category,
            "timestamp": observation.timestamp.isoformat(),
            "source": observation.source,
            "job_id": (
                provenance.job_id if provenance is not None else None
            ),
            "research_intent": (
                provenance.research_intent
                if provenance is not None
                else None
            ),
            "content_fingerprint": (
                provenance.content_fingerprint
                if provenance is not None
                else None
            ),
        }


__all__ = ["HistoricalComparisonAuditReporter"]
