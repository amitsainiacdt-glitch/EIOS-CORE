"""Append-only fingerprinted storage for governed Pre-Inflection previews."""

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview, PreInflectionStrength


@dataclass(frozen=True)
class StoredPreInflectionAssessment:
    preview_fingerprint: str
    preview: PreInflectionAssessmentPreview


class PreInflectionRepository:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}: raise ValueError("Pre-Inflection repository path must identify a file")

    def add(self, preview):
        if not isinstance(preview, PreInflectionAssessmentPreview): raise ValueError("preview must be PreInflectionAssessmentPreview")
        if any(item.preview.preview_id == preview.preview_id for item in self.all()): raise ValueError("preview_id already exists")
        payload = self.preview_payload(preview); fingerprint = self.fingerprint_payload(payload)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"preview_fingerprint": fingerprint, "preview": payload}, sort_keys=True, separators=(",", ":")) + "\n")
        return StoredPreInflectionAssessment(fingerprint, preview)

    def all(self):
        if not self.path.exists(): return ()
        result, ids, fingerprints = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try:
                    envelope = json.loads(line); preview = self.parse_preview(envelope["preview"]); fingerprint = self._sha(envelope["preview_fingerprint"])
                    if fingerprint != self.fingerprint_payload(self.preview_payload(preview)): raise ValueError("preview fingerprint mismatch")
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Pre-Inflection preview at line {number}: {exc}") from exc
                if preview.preview_id in ids or fingerprint in fingerprints: raise ValueError(f"Duplicate Pre-Inflection preview at line {number}")
                ids.add(preview.preview_id); fingerprints.add(fingerprint); result.append(StoredPreInflectionAssessment(fingerprint, preview))
        return tuple(result)

    @staticmethod
    def preview_payload(item):
        payload = {**item.__dict__, "strength": item.strength.value}
        for name in ("entity_scope", "sector_scope", "causal_indicator_ids", "expected_lead_time_quarters", "contradictions", "missing_expected_evidence", "coverage_gaps", "research_gaps", "confirmation_requirements", "invalidation_conditions", "balance_sheet_governance_risks"):
            payload[name] = list(payload[name])
        return payload

    @staticmethod
    def parse_preview(value):
        if not isinstance(value, dict) or value.get("schema_version") != 1: raise ValueError("unsupported Pre-Inflection schema")
        kwargs = dict(value)
        for name in ("entity_scope", "sector_scope", "causal_indicator_ids", "expected_lead_time_quarters", "contradictions", "missing_expected_evidence", "coverage_gaps", "research_gaps", "confirmation_requirements", "invalidation_conditions", "balance_sheet_governance_risks"):
            if not isinstance(kwargs[name], list): raise ValueError(f"{name} must be a list")
            kwargs[name] = tuple(kwargs[name])
        kwargs["strength"] = PreInflectionStrength(kwargs["strength"])
        return PreInflectionAssessmentPreview(**kwargs)

    @staticmethod
    def fingerprint_payload(value): return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()


__all__ = ["PreInflectionRepository", "StoredPreInflectionAssessment"]
