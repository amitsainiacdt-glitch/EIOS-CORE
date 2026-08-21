"""Append-only receipts for explicit governed Evidence pack rescoring."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_entity_evidence_pack_preview import HistoricalComparisonEntityEvidencePackPreview
from modules.external_intelligence.historical_comparison_evidence_governance import HistoricalComparisonEvidenceGovernance
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.historical_comparison_governed_evidence_pack_analyzer import HistoricalComparisonGovernedEvidencePackAnalyzer
from modules.external_intelligence.historical_comparison_governed_scoring_receipt import HistoricalComparisonGovernedScoringReceipt


class HistoricalComparisonGovernedScoringLedger:
    SCHEMA_VERSION = 1

    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("governed scoring path must identify a file")

    def analyze(self, pack, governance, *, analyst, rescored_at, analyzer=None):
        if not isinstance(pack, HistoricalComparisonEntityEvidencePackPreview):
            raise ValueError("pack must be an entity Evidence pack preview")
        if not isinstance(governance, HistoricalComparisonEvidenceGovernance):
            raise ValueError("governance must be a human governance record")
        expected_pack = HistoricalComparisonEvidencePackScoringLedger.pack_fingerprint(pack)
        if governance.pack_fingerprint != expected_pack:
            raise ValueError("governance does not bind to the current exact pack")
        analyst = self._text(analyst, "analyst")
        rescored_at = self._datetime(rescored_at, "rescored_at")
        try:
            if rescored_at < governance.governed_at:
                raise ValueError("rescoring timestamp precedes governance")
        except TypeError as exc:
            raise ValueError("rescoring timestamps use inconsistent timezone awareness") from exc
        fingerprint = self.input_fingerprint(pack, governance)
        if any(item.governed_input_fingerprint == fingerprint for item in self.read_all()):
            raise ValueError("this exact governed pack was already rescored")
        result = (analyzer or HistoricalComparisonGovernedEvidencePackAnalyzer()).analyze(
            pack, governance
        )
        receipt = HistoricalComparisonGovernedScoringReceipt(
            schema_version=1,
            governed_input_fingerprint=fingerprint,
            pack_fingerprint=expected_pack,
            entity=pack.entity,
            evidence_score=result.evidence_score,
            confidence=result.confidence,
            sufficiently_supported=result.sufficiently_supported,
            evidence_gaps=tuple(result.evidence_gaps),
            strengths=tuple(result.strengths),
            weaknesses=tuple(result.weaknesses),
            warnings=tuple(result.warnings),
            analyst=analyst,
            rescored_at=rescored_at,
        )
        receipt = self._parse(self._payload(receipt))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return result, receipt

    def read_all(self):
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("governed scoring path must be a file")
        results, seen = [], set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid governed score at line {line_number}: {exc}") from exc
                if item.governed_input_fingerprint in seen:
                    raise ValueError(f"Duplicate governed score at line {line_number}")
                seen.add(item.governed_input_fingerprint)
                results.append(item)
        return tuple(results)

    @staticmethod
    def input_fingerprint(pack, governance):
        payload = {
            "pack_fingerprint": governance.pack_fingerprint,
            "entity": governance.entity,
            "assumptions": list(governance.assumptions),
            "kill_switches": [item.__dict__ for item in governance.kill_switches],
            "monitoring_signals": list(governance.monitoring_signals),
            "governance_analyst": governance.analyst,
            "governance_rationale": governance.rationale,
            "governed_at": governance.governed_at.isoformat(),
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict) or payload["schema_version"] != 1:
            raise ValueError("unsupported schema version")
        return HistoricalComparisonGovernedScoringReceipt(
            schema_version=1,
            governed_input_fingerprint=cls._sha(payload["governed_input_fingerprint"]),
            pack_fingerprint=cls._sha(payload["pack_fingerprint"]),
            entity=cls._text(payload["entity"], "entity"),
            evidence_score=cls._score(payload["evidence_score"], "evidence_score"),
            confidence=cls._score(payload["confidence"], "confidence"),
            sufficiently_supported=cls._bool(payload["sufficiently_supported"]),
            evidence_gaps=cls._texts(payload["evidence_gaps"]),
            strengths=cls._texts(payload["strengths"]),
            weaknesses=cls._texts(payload["weaknesses"]),
            warnings=cls._texts(payload["warnings"]),
            analyst=cls._text(payload["analyst"], "analyst"),
            rescored_at=cls._iso(payload["rescored_at"]),
        )

    @staticmethod
    def _payload(item):
        return {**item.__dict__, "evidence_gaps": list(item.evidence_gaps), "strengths": list(item.strengths), "weaknesses": list(item.weaknesses), "warnings": list(item.warnings), "rescored_at": item.rescored_at.isoformat()}

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _sha(cls, value):
        value = cls._text(value, "fingerprint")
        if len(value) != 64:
            raise ValueError("fingerprint must be SHA-256")
        int(value, 16)
        return value.casefold()

    @staticmethod
    def _score(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be numeric")
        value = float(value)
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"{name} must be between 0 and 100")
        return value

    @staticmethod
    def _bool(value):
        if not isinstance(value, bool):
            raise ValueError("sufficiently_supported must be boolean")
        return value

    @classmethod
    def _texts(cls, value):
        if not isinstance(value, list):
            raise ValueError("diagnostics must be lists")
        return tuple(cls._text(item, "diagnostic") for item in value)

    @staticmethod
    def _datetime(value, name):
        if not isinstance(value, datetime):
            raise ValueError(f"{name} must be datetime")
        return value

    @classmethod
    def _iso(cls, value):
        if not isinstance(value, str):
            raise ValueError("rescored_at must be ISO datetime")
        return cls._datetime(datetime.fromisoformat(value), "rescored_at")


__all__ = ["HistoricalComparisonGovernedScoringLedger"]
