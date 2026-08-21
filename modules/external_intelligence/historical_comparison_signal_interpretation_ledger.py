"""Append-only human interpretations; this module never creates Signals."""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path

from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_receipt import HistoricalComparisonEvidencePackScoringReceipt
from modules.external_intelligence.historical_comparison_governed_scoring_receipt import HistoricalComparisonGovernedScoringReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.opportunity.signals.signal_interpretation import SignalInterpretation
from modules.opportunity.signals.signal_model import SignalDirection, SignalDomain, SignalStage, SignalType, TimeHorizon


class HistoricalComparisonSignalInterpretationLedger:
    SCHEMA_VERSION = 1
    ENUMS = {
        "domain": SignalDomain,
        "signal_type": SignalType,
        "direction": SignalDirection,
        "stage": SignalStage,
        "horizon": TimeHorizon,
    }
    LIST_FIELDS = (
        "countries", "sectors", "companies", "commodities", "themes",
        "causal_chain", "beneficiaries", "adversely_affected",
        "invalidation_conditions",
    )
    FLOAT_FIELDS = (
        "magnitude", "probability", "persistence", "relevance",
        "market_recognition",
    )

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("Signal interpretation ledger path must identify a file")

    def record(self, governed, scoring, conversion, *, interpretation, analyst, rationale, interpreted_at):
        if not isinstance(governed, HistoricalComparisonGovernedScoringReceipt):
            raise ValueError("governed must be a governed scoring receipt")
        if not isinstance(scoring, HistoricalComparisonEvidencePackScoringReceipt):
            raise ValueError("scoring must be an Evidence pack scoring receipt")
        if not isinstance(conversion, HistoricalComparisonEvidenceConversionReceipt):
            raise ValueError("conversion must be an Evidence conversion receipt")
        if not isinstance(interpretation, SignalInterpretation):
            raise ValueError("interpretation must be a SignalInterpretation")
        if not governed.sufficiently_supported:
            raise ValueError("governed Evidence pack is not sufficiently supported")
        if governed.pack_fingerprint != scoring.pack_fingerprint:
            raise ValueError("governed and initial scoring receipts bind different packs")
        if governed.entity != scoring.entity:
            raise ValueError("governed and initial scoring receipts bind different entities")
        evidence_ids = scoring.supporting_evidence_ids + scoring.contradictory_evidence_ids
        if conversion.evidence_id not in evidence_ids:
            raise ValueError("Evidence conversion does not belong to the scored pack")
        interpreted_at = self._datetime(interpreted_at, "interpreted_at")
        try:
            if interpreted_at < governed.rescored_at or interpreted_at < conversion.converted_at:
                raise ValueError("interpretation timestamp precedes its governed Evidence inputs")
        except TypeError as exc:
            raise ValueError("interpretation timestamps use inconsistent timezone awareness") from exc
        interpretation = self._interpretation(self._interpretation_payload(interpretation))
        record = HistoricalComparisonSignalInterpretation(
            schema_version=1,
            governed_input_fingerprint=self._sha256(governed.governed_input_fingerprint, "governed_input_fingerprint"),
            pack_fingerprint=self._sha256(governed.pack_fingerprint, "pack_fingerprint"),
            entity=self._text(governed.entity, "entity"),
            evidence_id=self._text(conversion.evidence_id, "evidence_id"),
            interpretation=interpretation,
            analyst=self._text(analyst, "analyst"),
            rationale=self._text(rationale, "rationale"),
            interpreted_at=interpreted_at,
        )
        existing = self.read_all()
        if any((item.governed_input_fingerprint, item.evidence_id) == (record.governed_input_fingerprint, record.evidence_id) for item in existing):
            raise ValueError("interpretation already exists for this governed pack and EvidenceItem")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(record), sort_keys=True, separators=(",", ":")) + "\n")
        return record

    def read_all(self):
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("Signal interpretation ledger path must be a file")
        records, seen = [], set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid Signal interpretation at line {line_number}: {exc}") from exc
                key = item.governed_input_fingerprint, item.evidence_id
                if key in seen:
                    raise ValueError(f"Duplicate Signal interpretation at line {line_number}")
                seen.add(key)
                records.append(item)
        return tuple(records)

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ValueError("unsupported Signal interpretation schema")
        return HistoricalComparisonSignalInterpretation(
            schema_version=1,
            governed_input_fingerprint=cls._sha256(payload["governed_input_fingerprint"], "governed_input_fingerprint"),
            pack_fingerprint=cls._sha256(payload["pack_fingerprint"], "pack_fingerprint"),
            entity=cls._text(payload["entity"], "entity"),
            evidence_id=cls._text(payload["evidence_id"], "evidence_id"),
            interpretation=cls._interpretation(payload["interpretation"]),
            analyst=cls._text(payload["analyst"], "analyst"),
            rationale=cls._text(payload["rationale"], "rationale"),
            interpreted_at=cls._iso(payload["interpreted_at"]),
        )

    @classmethod
    def _interpretation(cls, payload):
        if not isinstance(payload, dict):
            raise ValueError("interpretation must be an object")
        expected = set(SignalInterpretation.__dataclass_fields__)
        if set(payload) != expected:
            raise ValueError("interpretation fields do not match the canonical contract")
        values = dict(payload)
        for name, enum_type in cls.ENUMS.items():
            try:
                values[name] = enum_type(values[name])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"interpretation {name} is invalid") from exc
        for name in cls.LIST_FIELDS:
            values[name] = list(cls._texts(values[name], name, allow_empty=True))
        for name in cls.FLOAT_FIELDS:
            value = values[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"interpretation {name} must be between 0 and 1")
            values[name] = float(value)
        for name in ("title", "description", "detected_date", "economic_mechanism", "supply_demand_impact", "earnings_impact", "valuation_impact", "market_expectation", "price_reaction", "historical_precedent"):
            values[name] = cls._text(values[name], name)
        return SignalInterpretation(**values)

    @classmethod
    def _interpretation_payload(cls, item):
        return {name: (value.value if isinstance(value, Enum) else list(value) if isinstance(value, (list, tuple)) else value) for name, value in item.__dict__.items()}

    @classmethod
    def _payload(cls, item):
        return {
            "schema_version": item.schema_version,
            "governed_input_fingerprint": item.governed_input_fingerprint,
            "pack_fingerprint": item.pack_fingerprint,
            "entity": item.entity,
            "evidence_id": item.evidence_id,
            "interpretation": cls._interpretation_payload(item.interpretation),
            "analyst": item.analyst,
            "rationale": item.rationale,
            "interpreted_at": item.interpreted_at.isoformat(),
        }

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _texts(cls, values, name, *, allow_empty=False):
        if not isinstance(values, (list, tuple)):
            raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if not allow_empty and not result:
            raise ValueError(f"{name} must not be empty")
        if len({value.casefold() for value in result}) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result

    @classmethod
    def _sha256(cls, value, name):
        value = cls._text(value, name)
        if len(value) != 64:
            raise ValueError(f"{name} must be SHA-256")
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError(f"{name} must be SHA-256") from exc
        return value.casefold()

    @staticmethod
    def _datetime(value, name):
        if not isinstance(value, datetime):
            raise ValueError(f"{name} must be a datetime")
        return value

    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str):
            raise ValueError("interpreted_at must be an ISO datetime")
        return cls._datetime(datetime.fromisoformat(value), "interpreted_at")


__all__ = ["HistoricalComparisonSignalInterpretationLedger"]
