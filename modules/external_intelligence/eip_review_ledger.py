"""Append-only EIP review boundary; no downstream object creation."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.eip_classification import EIPStage
from modules.external_intelligence.eip_classification_service import EIPClassificationService
from modules.external_intelligence.eip_repository import EIPRepository, StoredEIPClassification
from modules.external_intelligence.eip_review import EIPReviewDecision, EIPReviewReceipt


class EIPReviewLedger:
    def __init__(self, path, service):
        self.path = Path(path)
        if not isinstance(service, EIPClassificationService): raise ValueError("service must be EIPClassificationService")
        self.service = service

    def record(self, stored, *, stored_pre_inflection, current_pre_inflection, stored_recognition, current_recognition, recognition_review, review_id, decision, notes, reviewed_at, reviewer):
        if not isinstance(stored, StoredEIPClassification): raise ValueError("stored must be StoredEIPClassification")
        expected = EIPRepository.fingerprint_payload(EIPRepository.classification_payload(stored.classification))
        if stored.classification_fingerprint != expected: raise ValueError("stored EIP fingerprint mismatch")
        current = self.service.classify(
            classification_id=stored.classification.classification_id,
            stored_pre_inflection=stored_pre_inflection, current_pre_inflection=current_pre_inflection,
            stored_recognition=stored_recognition, current_recognition=current_recognition,
            recognition_review=recognition_review, risk_disposition=stored.classification.risk_disposition,
            risk_rationale=stored.classification.risk_rationale, valuation_room=stored.classification.valuation_room,
            valuation_rationale=stored.classification.valuation_rationale,
        )
        if current != stored.classification: raise ValueError("stored EIP classification is stale")
        decision = decision if isinstance(decision, EIPReviewDecision) else EIPReviewDecision(decision)
        if any(item.review_id == review_id for item in self.all()): raise ValueError("review_id already exists")
        if any(item.classification_fingerprint == expected for item in self.all()): raise ValueError("EIP classification already reviewed")
        eligible_stages = {EIPStage.STAGE_3_EARLIEST_INVESTABLE_POINT, EIPStage.STAGE_4_EARLY_CONFIRMATION}
        if decision == EIPReviewDecision.AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW and (current.stage not in eligible_stages or not current.eligible_for_human_eip_review):
            raise ValueError("only eligible Stage 3 or Stage 4 may reach downstream Evidence review")
        if current.stage == EIPStage.STAGE_5_CONSENSUS_RECOVERY_POTENTIALLY_LATE and decision == EIPReviewDecision.HOLD_EIP_RESEARCH:
            raise ValueError("Stage 5 must be rejected, not held as an EIP candidate")
        receipt = EIPReviewReceipt(1, self._text(review_id), current.classification_id, expected, current.stage.value, decision, self._text(notes), self._datetime(reviewed_at), self._text(reviewer))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def all(self):
        if not self.path.exists(): return ()
        result, reviews, classifications = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid EIP review at line {number}: {exc}") from exc
                if item.review_id in reviews or item.classification_fingerprint in classifications: raise ValueError(f"Duplicate EIP review at line {number}")
                reviews.add(item.review_id); classifications.add(item.classification_fingerprint); result.append(item)
        return tuple(result)
    @staticmethod
    def _payload(item): return {**item.__dict__, "decision": item.decision.value, "reviewed_at": item.reviewed_at.isoformat()}
    @classmethod
    def _parse(cls, value):
        if value.get("schema_version") != 1: raise ValueError("unsupported EIP review schema")
        return EIPReviewReceipt(1, cls._text(value["review_id"]), cls._text(value["classification_id"]), EIPRepository._sha(value["classification_fingerprint"]), cls._text(value["stage"]), EIPReviewDecision(value["decision"]), cls._text(value["notes"]), datetime.fromisoformat(value["reviewed_at"]), cls._text(value["reviewer"]))
    @staticmethod
    def _text(value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("text must not be empty")
        return value.strip()
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("reviewed_at must be datetime")
        return value


__all__ = ["EIPReviewLedger"]
