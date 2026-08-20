"""Strict read-only parser for historical comparison JSON Lines."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_audit_record import (
    HistoricalComparisonAuditObservation,
    HistoricalComparisonAuditRecord,
)
from modules.observation.historical_comparison import (
    ChangeDirection,
    ComparisonType,
    Materiality,
)
from modules.observation.historical_observation_selector import (
    HistoricalSelectionBasis,
)


class HistoricalComparisonAuditReader:
    """Read and validate audit records without modifying their source."""

    SUPPORTED_SCHEMA_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

        if str(self.path).strip() in {"", "."}:
            raise ValueError("audit path must identify a file")

    def read_all(self) -> tuple[HistoricalComparisonAuditRecord, ...]:
        if not self.path.exists():
            return ()

        if not self.path.is_file():
            raise ValueError("audit path must identify a file")

        records = []

        with self.path.open("r", encoding="utf-8") as audit_file:
            for line_number, line in enumerate(audit_file, start=1):
                if not line.strip():
                    continue

                try:
                    payload = json.loads(line)
                    records.append(self._parse_record(payload))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(
                        "Invalid historical comparison audit record "
                        f"at line {line_number}: {exc}"
                    ) from exc

        return tuple(records)

    def read_cycle(
        self,
        recorded_at: datetime,
    ) -> tuple[HistoricalComparisonAuditRecord, ...]:
        if not isinstance(recorded_at, datetime):
            raise ValueError("recorded_at must be a datetime")

        return tuple(
            record
            for record in self.read_all()
            if record.recorded_at == recorded_at
        )

    @classmethod
    def _parse_record(cls, payload) -> HistoricalComparisonAuditRecord:
        if not isinstance(payload, dict):
            raise ValueError("record must be a JSON object")

        schema_version = payload["schema_version"]
        if (
            not isinstance(schema_version, int)
            or isinstance(schema_version, bool)
            or schema_version != cls.SUPPORTED_SCHEMA_VERSION
        ):
            raise ValueError(
                f"unsupported schema version {schema_version!r}"
            )

        selection = cls._mapping(payload["selection"], "selection")
        comparison = payload["comparison"]

        if comparison is not None:
            comparison = cls._mapping(comparison, "comparison")

        if (
            comparison is not None
            and payload["historical_observation"] is None
        ):
            raise ValueError(
                "comparison requires a historical observation"
            )

        eligible_count = selection["eligible_count"]
        if (
            not isinstance(eligible_count, int)
            or isinstance(eligible_count, bool)
            or eligible_count < 0
        ):
            raise ValueError(
                "selection eligible_count must be a non-negative integer"
            )

        delta = comparison.get("delta") if comparison is not None else None
        if (
            delta is not None
            and (
                not isinstance(delta, (int, float))
                or isinstance(delta, bool)
            )
        ):
            raise ValueError("comparison delta must be numeric or null")

        return HistoricalComparisonAuditRecord(
            schema_version=schema_version,
            recorded_at=cls._datetime(
                payload["recorded_at"],
                "recorded_at",
            ),
            current_observation=cls._observation(
                payload["current_observation"],
                "current_observation",
            ),
            historical_observation=(
                cls._observation(
                    payload["historical_observation"],
                    "historical_observation",
                )
                if payload["historical_observation"] is not None
                else None
            ),
            selection_basis=cls._optional_enum(
                HistoricalSelectionBasis,
                selection["basis"],
                "selection basis",
            ),
            eligible_count=eligible_count,
            selection_reason=cls._string(
                selection["reason"],
                "selection reason",
            ),
            comparison_type=(
                cls._required_enum(
                    ComparisonType,
                    comparison["type"],
                    "comparison type",
                )
                if comparison is not None
                else None
            ),
            change_detected=(
                cls._boolean(
                    comparison["change_detected"],
                    "comparison change_detected",
                )
                if comparison is not None
                else None
            ),
            change_direction=(
                cls._required_enum(
                    ChangeDirection,
                    comparison["change_direction"],
                    "comparison change_direction",
                )
                if comparison is not None
                else None
            ),
            materiality=(
                cls._required_enum(
                    Materiality,
                    comparison["materiality"],
                    "comparison materiality",
                )
                if comparison is not None
                else None
            ),
            delta=(float(delta) if delta is not None else None),
            comparison_provenance=(
                cls._string(
                    comparison["provenance"],
                    "comparison provenance",
                )
                if comparison is not None
                else None
            ),
        )

    @classmethod
    def _observation(
        cls,
        value,
        name: str,
    ) -> HistoricalComparisonAuditObservation:
        item = cls._mapping(value, name)

        return HistoricalComparisonAuditObservation(
            title=cls._string(item["title"], f"{name} title"),
            entity=cls._string(item["entity"], f"{name} entity"),
            category=cls._string(item["category"], f"{name} category"),
            timestamp=cls._datetime(
                item["timestamp"],
                f"{name} timestamp",
            ),
            source=cls._string(item["source"], f"{name} source"),
            job_id=cls._optional_string(
                item["job_id"],
                f"{name} job_id",
            ),
            research_intent=cls._optional_string(
                item["research_intent"],
                f"{name} research_intent",
            ),
            content_fingerprint=cls._optional_string(
                item["content_fingerprint"],
                f"{name} content_fingerprint",
            ),
        )

    @staticmethod
    def _mapping(value, name: str) -> dict:
        if not isinstance(value, dict):
            raise ValueError(f"{name} must be a JSON object")
        return value

    @staticmethod
    def _string(value, name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string")
        return value

    @classmethod
    def _optional_string(cls, value, name: str) -> str | None:
        if value is None:
            return None
        return cls._string(value, name)

    @staticmethod
    def _boolean(value, name: str) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a boolean")
        return value

    @staticmethod
    def _datetime(value, name: str) -> datetime:
        if not isinstance(value, str):
            raise ValueError(f"{name} must be an ISO datetime string")
        try:
            return datetime.fromisoformat(value)
        except ValueError as exc:
            raise ValueError(
                f"{name} must be an ISO datetime string"
            ) from exc

    @staticmethod
    def _required_enum(enum_type, value, name: str):
        try:
            return enum_type(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} is invalid") from exc

    @classmethod
    def _optional_enum(cls, enum_type, value, name: str):
        if value is None:
            return None
        return cls._required_enum(enum_type, value, name)


__all__ = ["HistoricalComparisonAuditReader"]
