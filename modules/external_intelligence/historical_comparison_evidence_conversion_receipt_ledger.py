"""Append-only receipts for explicit historical EvidenceItem creation."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_accepted_observation_preview import (
    HistoricalComparisonAcceptedObservationPreview,
)
from modules.external_intelligence.historical_comparison_evidence_assessment import (
    HistoricalComparisonEvidenceAssessment,
)
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import (
    HistoricalComparisonEvidenceConversionReceipt,
)
from modules.external_intelligence.historical_comparison_evidence_materializer import (
    HistoricalComparisonEvidenceMaterializer,
)
from modules.opportunity.evidence_engine import EvidenceItem


class HistoricalComparisonEvidenceConversionReceiptLedger:
    """Create once and preserve an exact materialization receipt."""

    SCHEMA_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("conversion receipt path must identify a file")

    def materialize(
        self,
        preview: HistoricalComparisonAcceptedObservationPreview,
        assessment: HistoricalComparisonEvidenceAssessment,
        *,
        converter: str,
        converted_at: datetime,
        materializer: HistoricalComparisonEvidenceMaterializer | None = None,
    ) -> tuple[EvidenceItem, HistoricalComparisonEvidenceConversionReceipt]:
        if not isinstance(preview, HistoricalComparisonAcceptedObservationPreview):
            raise ValueError("preview must be an accepted observation preview")
        if not isinstance(assessment, HistoricalComparisonEvidenceAssessment):
            raise ValueError("assessment must be a historical Evidence assessment")
        converter = self._text(converter, "converter")
        converted_at = self._datetime(converted_at, "converted_at")
        try:
            if converted_at < assessment.assessed_at:
                raise ValueError("conversion timestamp precedes assessment")
        except TypeError as exc:
            raise ValueError(
                "conversion and assessment timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc

        existing = self.read_all()
        if any(item.candidate_id == preview.candidate_id for item in existing):
            raise ValueError(
                "Evidence conversion already exists for candidate "
                f"{preview.candidate_id}"
            )
        engine = materializer or HistoricalComparisonEvidenceMaterializer()
        evidence = engine.materialize(preview, assessment)
        receipt = self._receipt(
            preview, assessment, evidence, converter, converted_at
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                json.dumps(
                    self._payload(receipt),
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        return evidence, receipt

    def read_all(self) -> tuple[HistoricalComparisonEvidenceConversionReceipt, ...]:
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("conversion receipt path must be a file")
        receipts = []
        candidate_ids = set()
        evidence_ids = set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, start=1):
                if not line.strip():
                    continue
                try:
                    receipt = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(
                        "Invalid Evidence conversion receipt at line "
                        f"{line_number}: {exc}"
                    ) from exc
                if receipt.candidate_id in candidate_ids:
                    raise ValueError(
                        f"Duplicate candidate conversion at line {line_number}"
                    )
                if receipt.evidence_id in evidence_ids:
                    raise ValueError(
                        f"Duplicate Evidence identity at line {line_number}"
                    )
                candidate_ids.add(receipt.candidate_id)
                evidence_ids.add(receipt.evidence_id)
                receipts.append(receipt)
        return tuple(receipts)

    @classmethod
    def _receipt(cls, preview, assessment, evidence, converter, converted_at):
        if not isinstance(evidence, EvidenceItem):
            raise ValueError("materializer did not return an EvidenceItem")
        expected_id = f"HC-{preview.candidate_id}"
        if evidence.evidence_id != expected_id:
            raise ValueError("materialized Evidence identity mismatch")
        receipt = HistoricalComparisonEvidenceConversionReceipt(
            schema_version=cls.SCHEMA_VERSION,
            candidate_id=cls._sha256(preview.candidate_id, "candidate_id"),
            observation_fingerprint=cls._sha256(
                preview.content_fingerprint, "observation_fingerprint"
            ),
            evidence_id=evidence.evidence_id,
            statement=evidence.statement,
            source=evidence.source,
            category=evidence.category,
            direction=evidence.direction,
            strength=evidence.strength,
            confidence=evidence.confidence,
            independent_confirmation=evidence.independent_confirmation,
            is_primary_source=evidence.is_primary_source,
            is_time_sensitive=evidence.is_time_sensitive,
            notes=evidence.notes,
            reviewer=preview.reviewer,
            reviewed_at=preview.reviewed_at,
            assessor=assessment.assessor,
            assessed_at=assessment.assessed_at,
            converter=converter,
            converted_at=converted_at,
        )
        return receipt

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict):
            raise ValueError("record must be a JSON object")
        version = payload["schema_version"]
        if not isinstance(version, int) or isinstance(version, bool) or version != 1:
            raise ValueError(f"unsupported schema version {version!r}")
        candidate_id = cls._sha256(payload["candidate_id"], "candidate_id")
        evidence_id = cls._text(payload["evidence_id"], "evidence_id")
        if evidence_id != f"HC-{candidate_id}":
            raise ValueError("Evidence identity does not match candidate")
        receipt = HistoricalComparisonEvidenceConversionReceipt(
            schema_version=version,
            candidate_id=candidate_id,
            observation_fingerprint=cls._sha256(
                payload["observation_fingerprint"], "observation_fingerprint"
            ),
            evidence_id=evidence_id,
            statement=cls._text(payload["statement"], "statement"),
            source=cls._text(payload["source"], "source"),
            category=cls._text(payload["category"], "category"),
            direction=cls._text(payload["direction"], "direction"),
            strength=cls._number(payload["strength"], "strength"),
            confidence=cls._number(payload["confidence"], "confidence"),
            independent_confirmation=cls._integer(
                payload["independent_confirmation"]
            ),
            is_primary_source=cls._boolean(
                payload["is_primary_source"], "is_primary_source"
            ),
            is_time_sensitive=cls._boolean(
                payload["is_time_sensitive"], "is_time_sensitive"
            ),
            notes=cls._text(payload["notes"], "notes"),
            reviewer=cls._text(payload["reviewer"], "reviewer"),
            reviewed_at=cls._iso(payload["reviewed_at"], "reviewed_at"),
            assessor=cls._text(payload["assessor"], "assessor"),
            assessed_at=cls._iso(payload["assessed_at"], "assessed_at"),
            converter=cls._text(payload["converter"], "converter"),
            converted_at=cls._iso(payload["converted_at"], "converted_at"),
        )
        if receipt.direction not in {"Supporting", "Contradictory"}:
            raise ValueError("direction must be Supporting or Contradictory")
        try:
            if receipt.assessed_at < receipt.reviewed_at:
                raise ValueError("assessment timestamp precedes review")
            if receipt.converted_at < receipt.assessed_at:
                raise ValueError("conversion timestamp precedes assessment")
        except TypeError as exc:
            raise ValueError(
                "receipt timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc
        return receipt

    @staticmethod
    def _payload(item) -> dict:
        return {
            **item.__dict__,
            "reviewed_at": item.reviewed_at.isoformat(),
            "assessed_at": item.assessed_at.isoformat(),
            "converted_at": item.converted_at.isoformat(),
        }

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _sha256(cls, value, name):
        text = cls._text(value, name)
        if len(text) != 64:
            raise ValueError(f"{name} must be a SHA-256 identity")
        try:
            int(text, 16)
        except ValueError as exc:
            raise ValueError(f"{name} must be a SHA-256 identity") from exc
        return text.casefold()

    @staticmethod
    def _datetime(value, name):
        if not isinstance(value, datetime):
            raise ValueError(f"{name} must be a datetime")
        return value

    @classmethod
    def _iso(cls, value, name):
        if not isinstance(value, str):
            raise ValueError(f"{name} must be an ISO datetime")
        return cls._datetime(datetime.fromisoformat(value), name)

    @staticmethod
    def _number(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        number = float(value)
        if not 0.0 <= number <= 100.0:
            raise ValueError(f"{name} must be between 0 and 100")
        return number

    @staticmethod
    def _integer(value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("independent_confirmation must be non-negative")
        return value

    @staticmethod
    def _boolean(value, name):
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a boolean")
        return value


__all__ = ["HistoricalComparisonEvidenceConversionReceiptLedger"]
