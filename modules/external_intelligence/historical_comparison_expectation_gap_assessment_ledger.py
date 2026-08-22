"""Append-only human decisions for exact Expectation Gap analyses."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_expectation_gap_analysis_preview import HistoricalComparisonExpectationGapAnalysisPreview
from modules.external_intelligence.historical_comparison_expectation_gap_assessment_decision import (
    HistoricalComparisonExpectationGapAssessmentDecision,
    HistoricalComparisonExpectationGapAssessmentDisposition,
)


class HistoricalComparisonExpectationGapAssessmentLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("Expectation Gap assessment path must identify a file")

    def record(self, preview, *, disposition, conditions=(), monitoring_requirements=(), reviewer, rationale, reviewed_at):
        if not isinstance(preview, HistoricalComparisonExpectationGapAnalysisPreview):
            raise ValueError("preview must be an Expectation Gap analysis preview")
        try:
            disposition = disposition if isinstance(disposition, HistoricalComparisonExpectationGapAssessmentDisposition) else HistoricalComparisonExpectationGapAssessmentDisposition(disposition)
        except (TypeError, ValueError) as exc:
            raise ValueError("disposition must be Approved, Rejected, or Deferred") from exc
        if disposition == HistoricalComparisonExpectationGapAssessmentDisposition.APPROVED and not preview.material_gap:
            raise ValueError("a non-material Expectation Gap analysis cannot be approved")
        if any(item.analysis_fingerprint == preview.analysis_fingerprint for item in self.read_all()):
            raise ValueError("a decision already exists for this exact Expectation Gap analysis")
        decision = HistoricalComparisonExpectationGapAssessmentDecision(
            1, self._sha(preview.analysis_fingerprint, "analysis_fingerprint"),
            self._sha(preview.eligibility_fingerprint, "eligibility_fingerprint"), preview.catalyst_id,
            self._sha(preview.catalyst_fingerprint, "catalyst_fingerprint"),
            self._sha(preview.creation_receipt_fingerprint, "creation_receipt_fingerprint"),
            preview.gap_id, preview.material_gap, preview.positive_gap, preview.negative_gap,
            preview.gap_score, preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
            disposition, self._texts(conditions, "conditions"),
            self._texts(monitoring_requirements, "monitoring_requirements"),
            self._text(reviewer, "reviewer"), self._text(rationale, "rationale"),
            self._datetime(reviewed_at),
        )
        decision = self._parse(self._payload(decision))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(decision), sort_keys=True, separators=(",", ":")) + "\n")
        return decision

    def read_all(self):
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("Expectation Gap assessment path must be a file")
        result, seen = [], set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid Expectation Gap assessment at line {number}: {exc}") from exc
                if item.analysis_fingerprint in seen:
                    raise ValueError(f"Duplicate Expectation Gap assessment at line {number}")
                seen.add(item.analysis_fingerprint)
                result.append(item)
        return tuple(result)

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ValueError("unsupported Expectation Gap assessment schema")
        try:
            disposition = HistoricalComparisonExpectationGapAssessmentDisposition(payload["disposition"])
        except (TypeError, ValueError) as exc:
            raise ValueError("invalid disposition") from exc
        material, positive, negative = (payload[name] for name in ("material_gap", "positive_gap", "negative_gap"))
        if not all(isinstance(value, bool) for value in (material, positive, negative)) or material != (positive or negative) or (positive and negative):
            raise ValueError("invalid Expectation Gap direction")
        if disposition == HistoricalComparisonExpectationGapAssessmentDisposition.APPROVED and not material:
            raise ValueError("a non-material Expectation Gap analysis cannot be approved")
        signal_ids = cls._texts(payload["signal_ids"], "signal_ids")
        promoted = cls._texts(payload["promoted_signal_ids"], "promoted_signal_ids")
        if not signal_ids or not promoted or not set(promoted).issubset(signal_ids):
            raise ValueError("promoted Signal IDs must be a non-empty subset of Signal IDs")
        return HistoricalComparisonExpectationGapAssessmentDecision(
            1, cls._sha(payload["analysis_fingerprint"], "analysis_fingerprint"),
            cls._sha(payload["eligibility_fingerprint"], "eligibility_fingerprint"),
            cls._text(payload["catalyst_id"], "catalyst_id"),
            cls._sha(payload["catalyst_fingerprint"], "catalyst_fingerprint"),
            cls._sha(payload["creation_receipt_fingerprint"], "creation_receipt_fingerprint"),
            cls._text(payload["gap_id"], "gap_id"), material, positive, negative,
            cls._score(payload["gap_score"], "gap_score"), cls._score(payload["confidence"], "confidence"),
            signal_ids, promoted, disposition, cls._texts(payload["conditions"], "conditions"),
            cls._texts(payload["monitoring_requirements"], "monitoring_requirements"),
            cls._text(payload["reviewer"], "reviewer"), cls._text(payload["rationale"], "rationale"),
            cls._iso(payload["reviewed_at"]),
        )

    @staticmethod
    def _payload(item):
        return {**item.__dict__, "signal_ids": list(item.signal_ids), "promoted_signal_ids": list(item.promoted_signal_ids), "disposition": item.disposition.value, "conditions": list(item.conditions), "monitoring_requirements": list(item.monitoring_requirements), "reviewed_at": item.reviewed_at.isoformat()}

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)):
            raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if len({value.casefold() for value in result}) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result

    @classmethod
    def _sha(cls, value, name):
        value = cls._text(value, name)
        if len(value) != 64:
            raise ValueError(f"{name} must be SHA-256")
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError(f"{name} must be SHA-256") from exc
        return value.casefold()

    @staticmethod
    def _score(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100:
            raise ValueError(f"{name} must be on the 0-100 scale")
        return float(value)

    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime):
            raise ValueError("reviewed_at must be a datetime")
        return value

    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str):
            raise ValueError("reviewed_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value))


__all__ = ["HistoricalComparisonExpectationGapAssessmentLedger"]
