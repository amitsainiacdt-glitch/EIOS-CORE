"""Append-only receipts for explicit entity Evidence pack scoring."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_entity_evidence_pack_analyzer import (
    HistoricalComparisonEntityEvidencePackAnalyzer,
)
from modules.external_intelligence.historical_comparison_entity_evidence_pack_preview import (
    HistoricalComparisonEntityEvidencePackPreview,
)
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_receipt import (
    HistoricalComparisonEvidencePackScoringReceipt,
)


class HistoricalComparisonEvidencePackScoringLedger:
    """Score each exact entity pack version at most once."""

    SCHEMA_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("scoring receipt path must identify a file")

    def analyze(
        self,
        pack: HistoricalComparisonEntityEvidencePackPreview,
        *,
        analyst: str,
        analyzed_at: datetime,
        analyzer: HistoricalComparisonEntityEvidencePackAnalyzer | None = None,
    ):
        if not isinstance(pack, HistoricalComparisonEntityEvidencePackPreview):
            raise ValueError("pack must be an entity Evidence pack preview")
        analyst = self._text(analyst, "analyst")
        analyzed_at = self._datetime(analyzed_at, "analyzed_at")
        fingerprint = self.pack_fingerprint(pack)
        existing = self.read_all()
        if any(item.pack_fingerprint == fingerprint for item in existing):
            raise ValueError("this exact entity Evidence pack was already scored")
        if pack.materialized_receipts:
            try:
                latest_conversion = max(
                    item.converted_at for item in pack.materialized_receipts
                )
                if analyzed_at < latest_conversion:
                    raise ValueError("analysis timestamp precedes materialization")
            except TypeError as exc:
                raise ValueError(
                    "analysis and conversion timestamps must use a consistent "
                    "timezone-awareness policy"
                ) from exc

        engine = analyzer or HistoricalComparisonEntityEvidencePackAnalyzer()
        result = engine.analyze(pack)
        receipt = HistoricalComparisonEvidencePackScoringReceipt(
            schema_version=self.SCHEMA_VERSION,
            pack_fingerprint=fingerprint,
            entity=pack.entity,
            supporting_evidence_ids=tuple(pack.supporting_evidence_ids),
            contradictory_evidence_ids=tuple(pack.contradictory_evidence_ids),
            evidence_score=result.evidence_score,
            confidence=result.confidence,
            sufficiently_supported=result.sufficiently_supported,
            evidence_gaps=tuple(result.evidence_gaps),
            strengths=tuple(result.strengths),
            weaknesses=tuple(result.weaknesses),
            warnings=tuple(result.warnings),
            analyst=analyst,
            analyzed_at=analyzed_at,
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                json.dumps(
                    self._payload(receipt), sort_keys=True, separators=(",", ":")
                )
                + "\n"
            )
        return result, receipt

    def read_all(self) -> tuple[HistoricalComparisonEvidencePackScoringReceipt, ...]:
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("scoring receipt path must be a file")
        receipts = []
        fingerprints = set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, start=1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(
                        f"Invalid Evidence scoring receipt at line {line_number}: {exc}"
                    ) from exc
                if item.pack_fingerprint in fingerprints:
                    raise ValueError(
                        f"Duplicate Evidence pack score at line {line_number}"
                    )
                fingerprints.add(item.pack_fingerprint)
                receipts.append(item)
        return tuple(receipts)

    @classmethod
    def pack_fingerprint(cls, pack) -> str:
        payload = {
            "schema_version": 1,
            "entity": pack.entity,
            "receipts": [
                {
                    **item.__dict__,
                    "reviewed_at": item.reviewed_at.isoformat(),
                    "assessed_at": item.assessed_at.isoformat(),
                    "converted_at": item.converted_at.isoformat(),
                }
                for item in sorted(
                    pack.materialized_receipts,
                    key=lambda value: value.candidate_id,
                )
            ],
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict):
            raise ValueError("record must be a JSON object")
        version = payload["schema_version"]
        if not isinstance(version, int) or isinstance(version, bool) or version != 1:
            raise ValueError(f"unsupported schema version {version!r}")
        return HistoricalComparisonEvidencePackScoringReceipt(
            schema_version=version,
            pack_fingerprint=cls._sha256(payload["pack_fingerprint"]),
            entity=cls._text(payload["entity"], "entity"),
            supporting_evidence_ids=cls._text_tuple(
                payload["supporting_evidence_ids"], "supporting_evidence_ids"
            ),
            contradictory_evidence_ids=cls._text_tuple(
                payload["contradictory_evidence_ids"],
                "contradictory_evidence_ids",
            ),
            evidence_score=cls._score(payload["evidence_score"], "evidence_score"),
            confidence=cls._score(payload["confidence"], "confidence"),
            sufficiently_supported=cls._boolean(
                payload["sufficiently_supported"], "sufficiently_supported"
            ),
            evidence_gaps=cls._text_tuple(payload["evidence_gaps"], "evidence_gaps"),
            strengths=cls._text_tuple(payload["strengths"], "strengths"),
            weaknesses=cls._text_tuple(payload["weaknesses"], "weaknesses"),
            warnings=cls._text_tuple(payload["warnings"], "warnings"),
            analyst=cls._text(payload["analyst"], "analyst"),
            analyzed_at=cls._iso(payload["analyzed_at"]),
        )

    @staticmethod
    def _payload(item):
        return {
            **item.__dict__,
            "supporting_evidence_ids": list(item.supporting_evidence_ids),
            "contradictory_evidence_ids": list(item.contradictory_evidence_ids),
            "evidence_gaps": list(item.evidence_gaps),
            "strengths": list(item.strengths),
            "weaknesses": list(item.weaknesses),
            "warnings": list(item.warnings),
            "analyzed_at": item.analyzed_at.isoformat(),
        }

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _sha256(cls, value):
        text = cls._text(value, "pack_fingerprint")
        if len(text) != 64:
            raise ValueError("pack_fingerprint must be SHA-256")
        try:
            int(text, 16)
        except ValueError as exc:
            raise ValueError("pack_fingerprint must be SHA-256") from exc
        return text.casefold()

    @classmethod
    def _text_tuple(cls, value, name):
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"{name} must be a list")
        return tuple(cls._text(item, name) for item in value)

    @staticmethod
    def _score(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        number = float(value)
        if not math.isfinite(number) or not 0.0 <= number <= 100.0:
            raise ValueError(f"{name} must be between 0 and 100")
        return number

    @staticmethod
    def _boolean(value, name):
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a boolean")
        return value

    @staticmethod
    def _datetime(value, name):
        if not isinstance(value, datetime):
            raise ValueError(f"{name} must be a datetime")
        return value

    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str):
            raise ValueError("analyzed_at must be an ISO datetime")
        return cls._datetime(datetime.fromisoformat(value), "analyzed_at")


__all__ = ["HistoricalComparisonEvidencePackScoringLedger"]
