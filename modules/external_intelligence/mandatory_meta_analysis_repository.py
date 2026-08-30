"""Append-only, fingerprint-verified repository for mandatory Meta assessments."""

import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.external_intelligence.mandatory_meta_analysis import MandatoryMetaAnalysisAssessment, MetaAnalysisConclusion, MetaContradictionBurden, MetaKillTestResult, MetaKillTestStatus


@dataclass(frozen=True)
class StoredMandatoryMetaAnalysis:
    assessment_fingerprint: str
    assessment: MandatoryMetaAnalysisAssessment


class MandatoryMetaAnalysisRepository:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}: raise ValueError("Meta repository path must identify a file")

    def add(self, assessment):
        if not isinstance(assessment, MandatoryMetaAnalysisAssessment): raise ValueError("assessment must be MandatoryMetaAnalysisAssessment")
        if any(item.assessment.assessment_id == assessment.assessment_id for item in self.all()): raise ValueError("assessment_id already exists")
        payload = self.assessment_payload(assessment)
        fingerprint = self.fingerprint_payload(payload)
        envelope = {"assessment_fingerprint": fingerprint, "assessment": payload}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(envelope, sort_keys=True, separators=(",", ":")) + "\n")
        return StoredMandatoryMetaAnalysis(fingerprint, assessment)

    def all(self):
        if not self.path.exists(): return ()
        result, ids, fingerprints = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try:
                    envelope = json.loads(line); assessment = self.parse_assessment(envelope["assessment"])
                    fingerprint = self._sha(envelope["assessment_fingerprint"])
                    if fingerprint != self.fingerprint_payload(self.assessment_payload(assessment)): raise ValueError("assessment fingerprint mismatch")
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Meta assessment at line {number}: {exc}") from exc
                if assessment.assessment_id in ids or fingerprint in fingerprints: raise ValueError(f"Duplicate Meta assessment at line {number}")
                ids.add(assessment.assessment_id); fingerprints.add(fingerprint); result.append(StoredMandatoryMetaAnalysis(fingerprint, assessment))
        return tuple(result)

    @staticmethod
    def assessment_payload(item):
        payload = {**item.__dict__}
        for name in ("entity_scope", "sector_scope", "input_temporal_evidence_ids", "input_observation_fingerprints", "input_indicator_preview_fingerprints", "causal_indicator_ids", "causal_hypotheses", "independence_group_ids", "contradictions", "missing_expected_evidence", "coverage_gaps", "syndication_findings", "cross_scope_transmissions", "research_gaps"):
            payload[name] = list(payload[name])
        payload["kill_test_results"] = [{**value.__dict__, "status": value.status.value, "evidence_ids": list(value.evidence_ids)} for value in item.kill_test_results]
        payload["conclusion"] = item.conclusion.value; payload["contradiction_burden"] = item.contradiction_burden.value
        payload["assessed_at"] = item.assessed_at.isoformat()
        return payload

    @staticmethod
    def parse_assessment(value):
        if not isinstance(value, dict) or value.get("schema_version") != 1: raise ValueError("unsupported Meta schema")
        kwargs = dict(value)
        tuple_fields = ("entity_scope", "sector_scope", "input_temporal_evidence_ids", "input_observation_fingerprints", "input_indicator_preview_fingerprints", "causal_indicator_ids", "causal_hypotheses", "independence_group_ids", "contradictions", "missing_expected_evidence", "coverage_gaps", "syndication_findings", "cross_scope_transmissions", "research_gaps")
        for name in tuple_fields:
            if not isinstance(kwargs[name], list): raise ValueError(f"{name} must be a list")
            kwargs[name] = tuple(kwargs[name])
        kwargs["kill_test_results"] = tuple(MetaKillTestResult(item["indicator_id"], item["kill_test"], MetaKillTestStatus(item["status"]), tuple(item["evidence_ids"]), item["rationale"]) for item in kwargs["kill_test_results"])
        kwargs["conclusion"] = MetaAnalysisConclusion(kwargs["conclusion"])
        kwargs["contradiction_burden"] = MetaContradictionBurden(kwargs["contradiction_burden"])
        kwargs["assessed_at"] = datetime.fromisoformat(kwargs["assessed_at"])
        return MandatoryMetaAnalysisAssessment(**kwargs)

    @staticmethod
    def fingerprint_payload(payload): return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or len(value) != 64: raise ValueError("fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("fingerprint must be SHA-256") from exc
        return value.casefold()


__all__ = ["MandatoryMetaAnalysisRepository", "StoredMandatoryMetaAnalysis"]
