"""Append-only review boundary before Price Recognition."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.pre_inflection_assessment_service import PreInflectionAssessmentService
from modules.external_intelligence.pre_inflection_repository import PreInflectionRepository, StoredPreInflectionAssessment
from modules.external_intelligence.pre_inflection_review import PreInflectionReviewDecision, PreInflectionReviewReceipt


class PreInflectionReviewLedger:
    def __init__(self, path, service):
        self.path = Path(path)
        if not isinstance(service, PreInflectionAssessmentService): raise ValueError("service must be PreInflectionAssessmentService")
        self.service = service

    def record(self, stored, *, stored_meta, meta_review, temporal_evidence, indicator_previews, review_id, decision, notes, reviewed_at, reviewer):
        if not isinstance(stored, StoredPreInflectionAssessment): raise ValueError("stored must be StoredPreInflectionAssessment")
        expected = PreInflectionRepository.fingerprint_payload(PreInflectionRepository.preview_payload(stored.preview))
        if stored.preview_fingerprint != expected: raise ValueError("stored Pre-Inflection fingerprint mismatch")
        rebuilt = self.service.preview(
            preview_id=stored.preview.preview_id, stored_meta=stored_meta, meta_review=meta_review,
            temporal_evidence=temporal_evidence, indicator_previews=indicator_previews,
            what_is_changing=stored.preview.what_is_changing, why_now=stored.preview.why_now,
            confirmation_requirements=stored.preview.confirmation_requirements,
            invalidation_conditions=stored.preview.invalidation_conditions,
            balance_sheet_governance_risks=stored.preview.balance_sheet_governance_risks,
        )
        if rebuilt != stored.preview: raise ValueError("stored Pre-Inflection preview is stale")
        decision = decision if isinstance(decision, PreInflectionReviewDecision) else PreInflectionReviewDecision(decision)
        if any(item.review_id == review_id for item in self.all()): raise ValueError("review_id already exists")
        if any(item.preview_fingerprint == stored.preview_fingerprint for item in self.all()): raise ValueError("Pre-Inflection preview already reviewed")
        if decision == PreInflectionReviewDecision.AUTHORIZE_PRICE_RECOGNITION_REVIEW and (not rebuilt.eligible_for_human_pre_inflection_review or rebuilt.market_recognition_status != "NOT_ASSESSED"):
            raise ValueError("Pre-Inflection preview cannot authorize Price Recognition review")
        receipt = PreInflectionReviewReceipt(1, self._text(review_id), rebuilt.preview_id, stored.preview_fingerprint, decision, self._text(notes), self._datetime(reviewed_at), self._text(reviewer))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def all(self):
        if not self.path.exists(): return ()
        result, reviews, previews = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Pre-Inflection review at line {number}: {exc}") from exc
                if item.review_id in reviews or item.preview_fingerprint in previews: raise ValueError(f"Duplicate Pre-Inflection review at line {number}")
                reviews.add(item.review_id); previews.add(item.preview_fingerprint); result.append(item)
        return tuple(result)

    @staticmethod
    def _payload(item): return {**item.__dict__, "decision": item.decision.value, "reviewed_at": item.reviewed_at.isoformat()}
    @classmethod
    def _parse(cls, value):
        if value.get("schema_version") != 1: raise ValueError("unsupported Pre-Inflection review schema")
        fingerprint = PreInflectionRepository._sha(value["preview_fingerprint"])
        return PreInflectionReviewReceipt(1, cls._text(value["review_id"]), cls._text(value["preview_id"]), fingerprint, PreInflectionReviewDecision(value["decision"]), cls._text(value["notes"]), datetime.fromisoformat(value["reviewed_at"]), cls._text(value["reviewer"]))
    @staticmethod
    def _text(value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("text must not be empty")
        return value.strip()
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("reviewed_at must be datetime")
        return value


__all__ = ["PreInflectionReviewLedger"]
