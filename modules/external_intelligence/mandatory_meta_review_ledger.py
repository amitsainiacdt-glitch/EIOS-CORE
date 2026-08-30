"""Durable human-review boundary above mandatory Meta."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaAnalysisGate, MandatoryMetaGateDecision
from modules.external_intelligence.mandatory_meta_analysis_repository import MandatoryMetaAnalysisRepository, StoredMandatoryMetaAnalysis
from modules.external_intelligence.mandatory_meta_review import MandatoryMetaReviewDecision, MandatoryMetaReviewReceipt


class MandatoryMetaReviewLedger:
    def __init__(self, path, gate):
        self.path = Path(path)
        if not isinstance(gate, MandatoryMetaAnalysisGate): raise ValueError("gate must be MandatoryMetaAnalysisGate")
        self.gate = gate

    def record(self, stored, *, temporal_evidence, indicator_previews, review_id, decision, notes, reviewed_at, reviewer):
        if not isinstance(stored, StoredMandatoryMetaAnalysis): raise ValueError("stored must be StoredMandatoryMetaAnalysis")
        expected_fingerprint = MandatoryMetaAnalysisRepository.fingerprint_payload(MandatoryMetaAnalysisRepository.assessment_payload(stored.assessment))
        if stored.assessment_fingerprint != expected_fingerprint: raise ValueError("stored Meta assessment fingerprint mismatch")
        decision = decision if isinstance(decision, MandatoryMetaReviewDecision) else MandatoryMetaReviewDecision(decision)
        if any(item.review_id == review_id for item in self.all()): raise ValueError("review_id already exists")
        if any(item.assessment_fingerprint == stored.assessment_fingerprint for item in self.all()): raise ValueError("Meta assessment already reviewed")
        gate_result = self.gate.evaluate(temporal_evidence=temporal_evidence, assessment=stored.assessment, indicator_previews=indicator_previews)
        if decision == MandatoryMetaReviewDecision.AUTHORIZE_PRE_INFLECTION_REVIEW and gate_result.decision != MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION:
            raise ValueError("human review cannot authorize a Meta assessment that is not ready")
        if gate_result.decision == MandatoryMetaGateDecision.BLOCKED and decision == MandatoryMetaReviewDecision.HOLD_FOR_RESEARCH:
            raise ValueError("technically blocked Meta must be rejected and rebuilt, not held")
        receipt = MandatoryMetaReviewReceipt(1, self._text(review_id), stored.assessment.assessment_id, stored.assessment_fingerprint, decision, gate_result.decision.value, gate_result.reason_codes, self._text(notes), self._datetime(reviewed_at), self._text(reviewer))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def all(self):
        if not self.path.exists(): return ()
        result, reviews, assessments = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Meta review at line {number}: {exc}") from exc
                if item.review_id in reviews or item.assessment_fingerprint in assessments: raise ValueError(f"Duplicate Meta review at line {number}")
                reviews.add(item.review_id); assessments.add(item.assessment_fingerprint); result.append(item)
        return tuple(result)

    @staticmethod
    def _payload(item): return {**item.__dict__, "decision": item.decision.value, "gate_reason_codes": list(item.gate_reason_codes), "reviewed_at": item.reviewed_at.isoformat()}
    @classmethod
    def _parse(cls, value):
        if value.get("schema_version") != 1: raise ValueError("unsupported Meta review schema")
        fingerprint = cls._text(value["assessment_fingerprint"])
        if len(fingerprint) != 64:
            raise ValueError("assessment_fingerprint must be SHA-256")
        try: int(fingerprint, 16)
        except ValueError as exc: raise ValueError("assessment_fingerprint must be SHA-256") from exc
        return MandatoryMetaReviewReceipt(1, cls._text(value["review_id"]), cls._text(value["assessment_id"]), fingerprint.casefold(), MandatoryMetaReviewDecision(value["decision"]), cls._text(value["gate_decision"]), tuple(value["gate_reason_codes"]), cls._text(value["notes"]), datetime.fromisoformat(value["reviewed_at"]), cls._text(value["reviewer"]))
    @staticmethod
    def _text(value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("text must not be empty")
        return value.strip()
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("reviewed_at must be datetime")
        return value


__all__ = ["MandatoryMetaReviewLedger"]
