"""Append-only explicit governance for exact scored Evidence packs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.historical_comparison_evidence_governance import (
    HistoricalComparisonEvidenceGovernance,
    HistoricalComparisonGovernanceKillSwitch,
)
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_receipt import (
    HistoricalComparisonEvidencePackScoringReceipt,
)


class HistoricalComparisonEvidenceGovernanceLedger:
    """Persist one human governance record per exact pack fingerprint."""

    SCHEMA_VERSION = 1
    SEVERITIES = ("Low", "Medium", "High", "Critical")

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("governance ledger path must identify a file")

    def record(
        self,
        scoring: HistoricalComparisonEvidencePackScoringReceipt,
        *,
        assumptions,
        kill_switches,
        monitoring_signals,
        analyst: str,
        rationale: str,
        governed_at: datetime,
    ) -> HistoricalComparisonEvidenceGovernance:
        if not isinstance(scoring, HistoricalComparisonEvidencePackScoringReceipt):
            raise ValueError("scoring must be an Evidence pack scoring receipt")
        governed_at = self._datetime(governed_at, "governed_at")
        try:
            if governed_at < scoring.analyzed_at:
                raise ValueError("governance timestamp precedes pack analysis")
        except TypeError as exc:
            raise ValueError(
                "governance and analysis timestamps must use a consistent "
                "timezone-awareness policy"
            ) from exc
        governance = HistoricalComparisonEvidenceGovernance(
            schema_version=self.SCHEMA_VERSION,
            pack_fingerprint=self._sha256(scoring.pack_fingerprint),
            entity=self._text(scoring.entity, "entity"),
            assumptions=self._unique_texts(assumptions, "assumptions"),
            kill_switches=self._kill_switches(kill_switches),
            monitoring_signals=self._unique_texts(
                monitoring_signals, "monitoring_signals"
            ),
            analyst=self._text(analyst, "analyst"),
            rationale=self._text(rationale, "rationale"),
            governed_at=governed_at,
        )
        existing = self.read_all()
        if any(
            item.pack_fingerprint == governance.pack_fingerprint
            for item in existing
        ):
            raise ValueError("governance already exists for this exact pack")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                json.dumps(
                    self._payload(governance),
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        return governance

    def read_all(self) -> tuple[HistoricalComparisonEvidenceGovernance, ...]:
        if not self.path.exists():
            return ()
        if not self.path.is_file():
            raise ValueError("governance ledger path must be a file")
        records = []
        fingerprints = set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for line_number, line in enumerate(ledger, start=1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(
                        f"Invalid Evidence governance at line {line_number}: {exc}"
                    ) from exc
                if item.pack_fingerprint in fingerprints:
                    raise ValueError(
                        f"Duplicate Evidence governance at line {line_number}"
                    )
                fingerprints.add(item.pack_fingerprint)
                records.append(item)
        return tuple(records)

    @classmethod
    def _parse(cls, payload):
        if not isinstance(payload, dict):
            raise ValueError("record must be a JSON object")
        version = payload["schema_version"]
        if not isinstance(version, int) or isinstance(version, bool) or version != 1:
            raise ValueError(f"unsupported schema version {version!r}")
        return HistoricalComparisonEvidenceGovernance(
            schema_version=version,
            pack_fingerprint=cls._sha256(payload["pack_fingerprint"]),
            entity=cls._text(payload["entity"], "entity"),
            assumptions=cls._unique_texts(payload["assumptions"], "assumptions"),
            kill_switches=cls._kill_switches(payload["kill_switches"]),
            monitoring_signals=cls._unique_texts(
                payload["monitoring_signals"], "monitoring_signals"
            ),
            analyst=cls._text(payload["analyst"], "analyst"),
            rationale=cls._text(payload["rationale"], "rationale"),
            governed_at=cls._iso(payload["governed_at"]),
        )

    @staticmethod
    def _payload(item):
        return {
            "schema_version": item.schema_version,
            "pack_fingerprint": item.pack_fingerprint,
            "entity": item.entity,
            "assumptions": list(item.assumptions),
            "kill_switches": [value.__dict__ for value in item.kill_switches],
            "monitoring_signals": list(item.monitoring_signals),
            "analyst": item.analyst,
            "rationale": item.rationale,
            "governed_at": item.governed_at.isoformat(),
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
    def _unique_texts(cls, values, name):
        if not isinstance(values, (list, tuple)) or not values:
            raise ValueError(f"{name} must contain at least one item")
        result = tuple(cls._text(item, name) for item in values)
        normalized = [item.casefold() for item in result]
        if len(set(normalized)) != len(normalized):
            raise ValueError(f"{name} must not contain duplicates")
        return result

    @classmethod
    def _kill_switches(cls, values):
        if not isinstance(values, (list, tuple)) or not values:
            raise ValueError("kill_switches must contain at least one item")
        result = []
        names = set()
        for value in values:
            if isinstance(value, HistoricalComparisonGovernanceKillSwitch):
                value = value.__dict__
                item = HistoricalComparisonGovernanceKillSwitch(
                    name=cls._text(value["name"], "kill switch name"),
                    condition=cls._text(value["condition"], "kill switch condition"),
                    severity=cls._severity(value["severity"]),
                    measurable=cls._boolean(value["measurable"], "measurable"),
                    threshold=cls._text(value["threshold"], "threshold"),
                    monitoring_frequency=cls._text(
                        value["monitoring_frequency"], "monitoring_frequency"
                    ),
                    rationale=cls._text(value["rationale"], "kill switch rationale"),
                    triggered=cls._boolean(value["triggered"], "triggered"),
                )
            elif isinstance(value, dict):
                item = HistoricalComparisonGovernanceKillSwitch(
                    name=cls._text(value["name"], "kill switch name"),
                    condition=cls._text(value["condition"], "kill switch condition"),
                    severity=cls._severity(value["severity"]),
                    measurable=cls._boolean(value["measurable"], "measurable"),
                    threshold=cls._text(value["threshold"], "threshold"),
                    monitoring_frequency=cls._text(
                        value["monitoring_frequency"], "monitoring_frequency"
                    ),
                    rationale=cls._text(value["rationale"], "kill switch rationale"),
                    triggered=cls._boolean(value["triggered"], "triggered"),
                )
            else:
                raise ValueError("kill_switches contain an invalid item")
            if not isinstance(item.measurable, bool) or not isinstance(item.triggered, bool):
                raise ValueError("kill switch flags must be booleans")
            if item.severity not in cls.SEVERITIES:
                raise ValueError("kill switch severity is invalid")
            key = item.name.casefold()
            if key in names:
                raise ValueError("kill switch names must be unique")
            names.add(key)
            result.append(item)
        return tuple(result)

    @classmethod
    def _severity(cls, value):
        text = cls._text(value, "severity")
        if text not in cls.SEVERITIES:
            raise ValueError("severity must be Low, Medium, High, or Critical")
        return text

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
            raise ValueError("governed_at must be an ISO datetime")
        return cls._datetime(datetime.fromisoformat(value), "governed_at")


__all__ = ["HistoricalComparisonEvidenceGovernanceLedger"]
