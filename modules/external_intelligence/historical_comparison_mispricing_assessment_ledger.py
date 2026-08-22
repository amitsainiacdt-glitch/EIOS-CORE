"""Append-only human decisions for exact governed Mispricing analyses."""

from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_mispricing_analysis_preview import HistoricalComparisonMispricingAnalysisPreview
from modules.external_intelligence.historical_comparison_mispricing_assessment_decision import HistoricalComparisonMispricingAssessmentDecision, HistoricalComparisonMispricingAssessmentDisposition


class HistoricalComparisonMispricingAssessmentLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("Mispricing assessment path must identify a file")

    def record(self, preview, *, disposition, conditions=(), monitoring_requirements=(), reviewer, rationale, reviewed_at):
        if not isinstance(preview, HistoricalComparisonMispricingAnalysisPreview):
            raise ValueError("preview must be a Mispricing analysis preview")
        try:
            disposition = disposition if isinstance(disposition, HistoricalComparisonMispricingAssessmentDisposition) else HistoricalComparisonMispricingAssessmentDisposition(disposition)
        except (TypeError, ValueError) as exc:
            raise ValueError("disposition must be Approved, Rejected, or Deferred") from exc
        if disposition == HistoricalComparisonMispricingAssessmentDisposition.APPROVED and not preview.potential_mispricing:
            raise ValueError("an analysis without potential mispricing cannot be approved")
        if any(item.analysis_fingerprint == preview.analysis_fingerprint for item in self.read_all()):
            raise ValueError("a decision already exists for this exact Mispricing analysis")
        decision = HistoricalComparisonMispricingAssessmentDecision(
            1, preview.analysis_fingerprint, preview.eligibility_fingerprint,
            preview.valuation_fingerprint, preview.valuation_receipt_fingerprint,
            preview.expectation_gap_fingerprint, preview.catalyst_fingerprint,
            preview.company, preview.potential_mispricing, preview.mispricing_score,
            preview.confidence, preview.signal_ids, preview.promoted_signal_ids,
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
        if not self.path.exists(): return ()
        if not self.path.is_file(): raise ValueError("Mispricing assessment path must be a file")
        result, seen = [], set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Mispricing assessment at line {number}: {exc}") from exc
                if item.analysis_fingerprint in seen: raise ValueError(f"Duplicate Mispricing assessment at line {number}")
                seen.add(item.analysis_fingerprint); result.append(item)
        return tuple(result)

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict) or payload.get("schema_version") != 1: raise ValueError("unsupported Mispricing assessment schema")
        try: disposition = HistoricalComparisonMispricingAssessmentDisposition(payload["disposition"])
        except (TypeError, ValueError) as exc: raise ValueError("invalid disposition") from exc
        potential = payload["potential_mispricing"]
        if not isinstance(potential, bool): raise ValueError("potential_mispricing must be boolean")
        if disposition == HistoricalComparisonMispricingAssessmentDisposition.APPROVED and not potential: raise ValueError("an analysis without potential mispricing cannot be approved")
        signals, promoted = cls._texts(payload["signal_ids"], "signal_ids"), cls._texts(payload["promoted_signal_ids"], "promoted_signal_ids")
        if not signals or not promoted or not set(promoted).issubset(signals): raise ValueError("promoted Signal IDs must be a non-empty subset")
        return HistoricalComparisonMispricingAssessmentDecision(
            1, cls._sha(payload["analysis_fingerprint"]), cls._sha(payload["eligibility_fingerprint"]),
            cls._sha(payload["valuation_fingerprint"]), cls._sha(payload["valuation_receipt_fingerprint"]),
            cls._sha(payload["expectation_gap_fingerprint"]), cls._sha(payload["catalyst_fingerprint"]),
            cls._text(payload["company"], "company"), potential,
            cls._score(payload["mispricing_score"], "mispricing_score"), cls._score(payload["confidence"], "confidence"),
            signals, promoted, disposition, cls._texts(payload["conditions"], "conditions"),
            cls._texts(payload["monitoring_requirements"], "monitoring_requirements"),
            cls._text(payload["reviewer"], "reviewer"), cls._text(payload["rationale"], "rationale"), cls._iso(payload["reviewed_at"]),
        )

    @staticmethod
    def _payload(item): return {**item.__dict__, "signal_ids": list(item.signal_ids), "promoted_signal_ids": list(item.promoted_signal_ids), "disposition": item.disposition.value, "conditions": list(item.conditions), "monitoring_requirements": list(item.monitoring_requirements), "reviewed_at": item.reviewed_at.isoformat()}
    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if len({value.casefold() for value in result}) != len(result): raise ValueError(f"{name} must not contain duplicates")
        return result
    @classmethod
    def _sha(cls, value):
        value = cls._text(value, "fingerprint")
        if len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()
    @staticmethod
    def _score(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100: raise ValueError(f"{name} must be on the 0-100 scale")
        return float(value)
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("reviewed_at must be a datetime")
        return value
    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str): raise ValueError("reviewed_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value))


__all__ = ["HistoricalComparisonMispricingAssessmentLedger"]
