"""Append-only receipts for authoritative typed valuation snapshots."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from enum import Enum
from pathlib import Path

from modules.external_intelligence.historical_comparison_valuation_snapshot_receipt import HistoricalComparisonValuationSnapshotReceipt
from modules.master_dossier.valuation_section import ValuationSection


class HistoricalComparisonValuationSnapshotLedger:
    AUTHORITATIVE_SOURCE = "ValuationEngine"

    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("valuation snapshot receipt path must identify a file")

    def record(self, valuation, *, entity, recorder, rationale, recorded_at):
        self.validate_valuation(valuation)
        entity = self._text(entity, "entity")
        recorder = self._text(recorder, "recorder")
        rationale = self._text(rationale, "rationale")
        recorded_at = self._datetime(recorded_at)
        fingerprint = self.valuation_fingerprint(valuation)
        if any(item.valuation_fingerprint == fingerprint for item in self.read_all()):
            raise ValueError("this exact valuation snapshot already has a receipt")
        receipt = HistoricalComparisonValuationSnapshotReceipt(
            1, entity, fingerprint, float(valuation.intrinsic_value),
            float(valuation.fair_value), valuation.valuation_method.strip(),
            float(valuation.confidence), valuation.source.strip(), recorder,
            rationale, recorded_at,
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def read_all(self):
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("valuation snapshot receipt path must be a file")
        result, seen = [], set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid valuation snapshot receipt at line {number}: {exc}") from exc
                if item.valuation_fingerprint in seen:
                    raise ValueError(f"Duplicate valuation snapshot receipt at line {number}")
                seen.add(item.valuation_fingerprint)
                result.append(item)
        return tuple(result)

    @classmethod
    def validate_valuation(cls, valuation):
        if not isinstance(valuation, ValuationSection):
            raise ValueError("valuation must be a typed ValuationSection")
        if valuation.source.strip() != cls.AUTHORITATIVE_SOURCE:
            raise ValueError("valuation source must be ValuationEngine")
        cls._text(valuation.valuation_method, "valuation_method")
        for name in ("intrinsic_value", "fair_value"):
            value = getattr(valuation, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be a positive finite number")
        confidence = valuation.confidence
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 <= confidence <= 100:
            raise ValueError("confidence must be on the 0-100 scale")

    @classmethod
    def valuation_fingerprint(cls, valuation):
        cls.validate_valuation(valuation)
        payload = cls._canonical(valuation)
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

    @classmethod
    def _canonical(cls, value):
        if is_dataclass(value):
            return cls._canonical(asdict(value))
        if isinstance(value, Enum):
            return cls._canonical(value.value)
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                raise ValueError("valuation metadata keys must be strings")
            return {key: cls._canonical(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [cls._canonical(item) for item in value]
        if value is None or isinstance(value, (str, int, float, bool)):
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("valuation snapshot contains a non-finite number")
            return value
        raise ValueError(f"valuation snapshot contains unsupported value type {type(value).__name__}")

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ValueError("unsupported valuation snapshot schema")
        if cls._text(payload["source"], "source") != cls.AUTHORITATIVE_SOURCE:
            raise ValueError("valuation source must be ValuationEngine")
        return HistoricalComparisonValuationSnapshotReceipt(
            1, cls._text(payload["entity"], "entity"), cls._sha(payload["valuation_fingerprint"]),
            cls._positive(payload["intrinsic_value"], "intrinsic_value"),
            cls._positive(payload["fair_value"], "fair_value"),
            cls._text(payload["valuation_method"], "valuation_method"),
            cls._score(payload["confidence"]), cls.AUTHORITATIVE_SOURCE,
            cls._text(payload["recorder"], "recorder"), cls._text(payload["rationale"], "rationale"),
            cls._iso(payload["recorded_at"]),
        )

    @staticmethod
    def _payload(item): return {**item.__dict__, "recorded_at": item.recorded_at.isoformat()}
    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @staticmethod
    def _positive(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0: raise ValueError(f"{name} must be positive")
        return float(value)
    @staticmethod
    def _score(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100: raise ValueError("confidence must be on the 0-100 scale")
        return float(value)
    @classmethod
    def _sha(cls, value):
        value = cls._text(value, "valuation_fingerprint")
        if len(value) != 64: raise ValueError("valuation_fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("valuation_fingerprint must be SHA-256") from exc
        return value.casefold()
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("recorded_at must be a datetime")
        return value
    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str): raise ValueError("recorded_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value))


__all__ = ["HistoricalComparisonValuationSnapshotLedger"]
