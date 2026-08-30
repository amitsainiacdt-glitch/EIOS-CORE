"""Append-only repository for reviewed public Temporal Evidence records."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.public_temporal_evidence import PublicTemporalEvidenceRecord


class PublicTemporalEvidenceRepository:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}: raise ValueError("temporal repository path must identify a file")

    def add(self, record):
        if not isinstance(record, PublicTemporalEvidenceRecord): raise ValueError("record must be PublicTemporalEvidenceRecord")
        existing = self.all()
        if any(item.temporal_evidence_id == record.temporal_evidence_id or item.observation_fingerprint == record.observation_fingerprint for item in existing):
            raise ValueError("Temporal Evidence record already exists")
        record = self._parse(self._payload(record))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(self._payload(record), sort_keys=True, separators=(",", ":")) + "\n")
        return record

    def all(self):
        if not self.path.exists(): return ()
        result, ids, observations = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Temporal Evidence at line {number}: {exc}") from exc
                if item.temporal_evidence_id in ids or item.observation_fingerprint in observations: raise ValueError(f"Duplicate Temporal Evidence at line {number}")
                ids.add(item.temporal_evidence_id); observations.add(item.observation_fingerprint); result.append(item)
        return tuple(result)

    @staticmethod
    def _payload(item):
        return {**item.__dict__, "event_at": item.event_at.isoformat(), "known_at": item.known_at.isoformat()}

    @staticmethod
    def _parse(value):
        if not isinstance(value, dict) or value.get("schema_version") != 1: raise ValueError("unsupported Temporal Evidence schema")
        fields = ("temporal_evidence_id", "observation_fingerprint", "entity", "event_type", "statement_posture", "time_basis", "source_url", "document_hash", "candidate_id", "proposal_id", "review_id", "observation_title", "observation_description")
        values = []
        for field in fields:
            item = value[field]
            if not isinstance(item, str) or not item.strip(): raise ValueError(f"{field} must not be empty")
            values.append(item.strip())
        return PublicTemporalEvidenceRecord(1, values[0], values[1], values[2], values[3], values[4], datetime.fromisoformat(value["event_at"]), datetime.fromisoformat(value["known_at"]), *values[5:])


__all__ = ["PublicTemporalEvidenceRepository"]
