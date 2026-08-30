"""Append-only, current-data review boundary before EIP."""

import json
from datetime import datetime
from pathlib import Path

from modules.external_intelligence.price_recognition_repository import PriceRecognitionRepository, StoredPriceRecognition
from modules.external_intelligence.price_recognition_review import PriceRecognitionReviewDecision, PriceRecognitionReviewReceipt
from modules.external_intelligence.price_recognition_service import PriceRecognitionService


class PriceRecognitionReviewLedger:
    def __init__(self, path, service):
        self.path = Path(path)
        if not isinstance(service, PriceRecognitionService): raise ValueError("service must be PriceRecognitionService")
        self.service = service

    def record(self, stored, *, stored_pre_inflection, current_pre_inflection, pre_inflection_review, market_snapshot, review_id, decision, notes, reviewed_at, reviewer):
        if not isinstance(stored, StoredPriceRecognition): raise ValueError("stored must be StoredPriceRecognition")
        expected = PriceRecognitionRepository.fingerprint_payload(PriceRecognitionRepository.preview_payload(stored.preview))
        if stored.recognition_fingerprint != expected: raise ValueError("stored Price Recognition fingerprint mismatch")
        rebuilt = self.service.preview(stored_pre_inflection=stored_pre_inflection, current_pre_inflection=current_pre_inflection, pre_inflection_review=pre_inflection_review, market_snapshot=market_snapshot)
        if rebuilt != stored.preview: raise ValueError("stored Price Recognition preview is stale")
        decision = decision if isinstance(decision, PriceRecognitionReviewDecision) else PriceRecognitionReviewDecision(decision)
        if any(item.review_id == review_id for item in self.all()): raise ValueError("review_id already exists")
        if any(item.recognition_fingerprint == stored.recognition_fingerprint for item in self.all()): raise ValueError("Price Recognition already reviewed")
        if decision == PriceRecognitionReviewDecision.AUTHORIZE_EIP_REVIEW and not rebuilt.eligible_for_eip_review: raise ValueError("recognition state is not eligible for EIP review")
        if decision == PriceRecognitionReviewDecision.HOLD_FOR_MARKET_DATA and rebuilt.state.value == "FULLY_RECOGNIZED_POTENTIALLY_LATE": raise ValueError("fully recognized cases must be rejected, not held for data")
        receipt = PriceRecognitionReviewReceipt(1, self._text(review_id), rebuilt.snapshot_id, stored.recognition_fingerprint, decision, rebuilt.state.value, self._text(notes), self._datetime(reviewed_at), self._text(reviewer))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream: stream.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def all(self):
        if not self.path.exists(): return ()
        result, reviews, recognitions = [], set(), set()
        with self.path.open("r", encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                if not line.strip(): continue
                try: item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc: raise ValueError(f"Invalid Price Recognition review at line {number}: {exc}") from exc
                if item.review_id in reviews or item.recognition_fingerprint in recognitions: raise ValueError(f"Duplicate Price Recognition review at line {number}")
                reviews.add(item.review_id); recognitions.add(item.recognition_fingerprint); result.append(item)
        return tuple(result)

    @staticmethod
    def _payload(item): return {**item.__dict__, "decision": item.decision.value, "reviewed_at": item.reviewed_at.isoformat()}
    @classmethod
    def _parse(cls, value):
        fingerprint = PriceRecognitionRepository._sha(value["recognition_fingerprint"])
        if value.get("schema_version") != 1: raise ValueError("unsupported Price Recognition review schema")
        return PriceRecognitionReviewReceipt(1, cls._text(value["review_id"]), cls._text(value["snapshot_id"]), fingerprint, PriceRecognitionReviewDecision(value["decision"]), cls._text(value["recognition_state"]), cls._text(value["notes"]), datetime.fromisoformat(value["reviewed_at"]), cls._text(value["reviewer"]))
    @staticmethod
    def _text(value):
        if not isinstance(value, str) or not value.strip(): raise ValueError("text must not be empty")
        return value.strip()
    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("reviewed_at must be datetime")
        return value


__all__ = ["PriceRecognitionReviewLedger"]
