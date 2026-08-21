"""Append-only human assessment ledger without Evidence creation."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_accepted_observation_preview import (
    HistoricalComparisonAcceptedObservationPreview,
)
from modules.external_intelligence.historical_comparison_evidence_assessment import (
    HistoricalComparisonEvidenceAssessment,
)


class HistoricalComparisonEvidenceAssessmentLedger:
    """Persist at most one explicit assessment for each accepted candidate."""

    SCHEMA_VERSION = 1
    DIRECTIONS = ("Supporting", "Contradictory")

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("Evidence assessment ledger path must identify a file")

    def record(
        self,
        preview: HistoricalComparisonAcceptedObservationPreview,
        *,
        category: str,
        direction: str,
        strength: float,
        confidence: float,
        independent_confirmation: int,
        is_primary_source: bool,
        is_time_sensitive: bool,
        assessor: str,
        rationale: str,
        assessed_at: datetime,
    ) -> HistoricalComparisonEvidenceAssessment:
        if not isinstance(preview, HistoricalComparisonAcceptedObservationPreview):
            raise ValueError("preview must be an accepted observation preview")
        try:
            if assessed_at < preview.reviewed_at:
                raise ValueError("assessment timestamp precedes accepted review")
        except TypeError as exc:
            raise ValueError(
                "assessment and review timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc

        assessment = HistoricalComparisonEvidenceAssessment(
            schema_version=self.SCHEMA_VERSION,
            candidate_id=self._sha256(preview.candidate_id, "candidate_id"),
            observation_fingerprint=self._sha256(
                preview.content_fingerprint, "observation_fingerprint"
            ),
            category=self._text(category, "category"),
            direction=self._direction(direction),
            strength=self._percentage(strength, "strength"),
            confidence=self._percentage(confidence, "confidence"),
            independent_confirmation=self._confirmation(
                independent_confirmation
            ),
            is_primary_source=self._boolean(
                is_primary_source, "is_primary_source"
            ),
            is_time_sensitive=self._boolean(
                is_time_sensitive, "is_time_sensitive"
            ),
            assessor=self._text(assessor, "assessor"),
            rationale=self._text(rationale, "rationale"),
            assessed_at=self._datetime(assessed_at, "assessed_at"),
        )
        existing = self.read_all()
        if any(
            item.candidate_id == assessment.candidate_id for item in existing
        ):
            raise ValueError(
                "Evidence assessment already exists for candidate "
                f"{assessment.candidate_id}"
            )

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                json.dumps(
                    self._payload(assessment),
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        return assessment

    def read_all(self) -> tuple[HistoricalComparisonEvidenceAssessment, ...]:
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("Evidence assessment ledger path must be a file")
        assessments = []
        candidate_ids = set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, start=1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(
                        "Invalid Evidence assessment ledger record at line "
                        f"{line_number}: {exc}"
                    ) from exc
                if item.candidate_id in candidate_ids:
                    raise ValueError(
                        "Duplicate Evidence assessment at line "
                        f"{line_number} for candidate {item.candidate_id}"
                    )
                candidate_ids.add(item.candidate_id)
                assessments.append(item)
        return tuple(assessments)

    @classmethod
    def _parse(cls, payload) -> HistoricalComparisonEvidenceAssessment:
        if not isinstance(payload, dict):
            raise ValueError("record must be a JSON object")
        version = payload["schema_version"]
        if not isinstance(version, int) or isinstance(version, bool) or version != 1:
            raise ValueError(f"unsupported schema version {version!r}")
        return HistoricalComparisonEvidenceAssessment(
            schema_version=version,
            candidate_id=cls._sha256(payload["candidate_id"], "candidate_id"),
            observation_fingerprint=cls._sha256(
                payload["observation_fingerprint"], "observation_fingerprint"
            ),
            category=cls._text(payload["category"], "category"),
            direction=cls._direction(payload["direction"]),
            strength=cls._percentage(payload["strength"], "strength"),
            confidence=cls._percentage(payload["confidence"], "confidence"),
            independent_confirmation=cls._confirmation(
                payload["independent_confirmation"]
            ),
            is_primary_source=cls._boolean(
                payload["is_primary_source"], "is_primary_source"
            ),
            is_time_sensitive=cls._boolean(
                payload["is_time_sensitive"], "is_time_sensitive"
            ),
            assessor=cls._text(payload["assessor"], "assessor"),
            rationale=cls._text(payload["rationale"], "rationale"),
            assessed_at=cls._datetime(
                datetime.fromisoformat(payload["assessed_at"]), "assessed_at"
            ),
        )

    @staticmethod
    def _payload(item) -> dict:
        return {
            "schema_version": item.schema_version,
            "candidate_id": item.candidate_id,
            "observation_fingerprint": item.observation_fingerprint,
            "category": item.category,
            "direction": item.direction,
            "strength": item.strength,
            "confidence": item.confidence,
            "independent_confirmation": item.independent_confirmation,
            "is_primary_source": item.is_primary_source,
            "is_time_sensitive": item.is_time_sensitive,
            "assessor": item.assessor,
            "rationale": item.rationale,
            "assessed_at": item.assessed_at.isoformat(),
        }

    @staticmethod
    def _text(value, name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _sha256(cls, value, name: str) -> str:
        text = cls._text(value, name)
        if len(text) != 64:
            raise ValueError(f"{name} must be a SHA-256 identity")
        try:
            int(text, 16)
        except ValueError as exc:
            raise ValueError(f"{name} must be a SHA-256 identity") from exc
        return text.casefold()

    @classmethod
    def _direction(cls, value) -> str:
        text = cls._text(value, "direction")
        if text not in cls.DIRECTIONS:
            raise ValueError(
                "direction must be Supporting or Contradictory"
            )
        return text

    @staticmethod
    def _percentage(value, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        number = float(value)
        if not math.isfinite(number) or not 0.0 <= number <= 100.0:
            raise ValueError(f"{name} must be between 0 and 100")
        return number

    @staticmethod
    def _confirmation(value) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(
                "independent_confirmation must be a non-negative integer"
            )
        return value

    @staticmethod
    def _boolean(value, name: str) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a boolean")
        return value

    @staticmethod
    def _datetime(value, name: str) -> datetime:
        if not isinstance(value, datetime):
            raise ValueError(f"{name} must be a datetime")
        return value


__all__ = ["HistoricalComparisonEvidenceAssessmentLedger"]
