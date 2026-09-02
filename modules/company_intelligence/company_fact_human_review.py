"""Append-only human decisions bound to company candidate META assessments."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaAssessment
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate


class CompanyFactHumanDecision(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    HOLD = "HOLD"


@dataclass(frozen=True)
class CompanyFactHumanReviewReceipt:
    schema_version: int
    review_id: str
    candidate_id: str
    candidate_fingerprint: str
    meta_assessment_id: str
    meta_assessment_fingerprint: str
    decision: CompanyFactHumanDecision
    approved_confidence: float | None
    rationale: str
    reviewed_at: datetime
    reviewer: str


class CompanyFactHumanReviewLedger:
    def __init__(self, path: Path):
        self.path = Path(path)

    def record(self, candidate, meta, *, review_id, decision, rationale, reviewed_at, reviewer, approved_confidence=None):
        self._validate_pair(candidate, meta)
        decision = decision if isinstance(decision, CompanyFactHumanDecision) else CompanyFactHumanDecision(decision)
        if any(item.candidate_id == candidate.candidate_id for item in self.read_all()):
            raise ValueError("candidate already has a human review decision")
        if decision == CompanyFactHumanDecision.APPROVE:
            if meta.decision != "READY_FOR_HUMAN_REVIEW":
                raise ValueError("approval requires META readiness for human review")
            confidence = self._confidence(approved_confidence)
        else:
            if approved_confidence is not None:
                raise ValueError("only approval may set approved confidence")
            confidence = None
        receipt = CompanyFactHumanReviewReceipt(
            1, self._text(review_id, "review_id"), candidate.candidate_id,
            self.candidate_fingerprint(candidate), meta.assessment_id,
            self.meta_fingerprint(meta), decision, confidence,
            self._text(rationale, "rationale"), self._datetime(reviewed_at),
            self._text(reviewer, "reviewer"),
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def read_all(self):
        if not self.path.exists():
            return ()
        result, candidates, reviews = [], set(), set()
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                if value.get("schema_version") != 1:
                    raise ValueError("unsupported schema")
                value["decision"] = CompanyFactHumanDecision(value["decision"])
                value["reviewed_at"] = datetime.fromisoformat(value["reviewed_at"])
                item = CompanyFactHumanReviewReceipt(**value)
                self._sha(item.candidate_fingerprint)
                self._sha(item.meta_assessment_fingerprint)
                if item.candidate_id in candidates or item.review_id in reviews:
                    raise ValueError("duplicate review identity")
                if (item.decision == CompanyFactHumanDecision.APPROVE) != (item.approved_confidence is not None):
                    raise ValueError("decision and confidence are inconsistent")
                candidates.add(item.candidate_id); reviews.add(item.review_id); result.append(item)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid company fact review at line {number}: {exc}") from exc
        return tuple(result)

    @classmethod
    def validate_binding(cls, candidate, meta, review):
        cls._validate_pair(candidate, meta)
        if not isinstance(review, CompanyFactHumanReviewReceipt):
            raise ValueError("review must be a CompanyFactHumanReviewReceipt")
        if review.candidate_id != candidate.candidate_id or review.candidate_fingerprint != cls.candidate_fingerprint(candidate):
            raise ValueError("review does not bind to the current candidate")
        if review.meta_assessment_id != meta.assessment_id or review.meta_assessment_fingerprint != cls.meta_fingerprint(meta):
            raise ValueError("review does not bind to the current META assessment")

    @classmethod
    def _validate_pair(cls, candidate, meta):
        if not isinstance(candidate, CompanyFactReviewCandidate):
            raise ValueError("candidate must be a CompanyFactReviewCandidate")
        if not isinstance(meta, CompanyCandidateMetaAssessment):
            raise ValueError("meta must be a CompanyCandidateMetaAssessment")
        if meta.candidate_id != candidate.candidate_id or meta.company != candidate.company:
            raise ValueError("META assessment does not bind to candidate")

    @staticmethod
    def candidate_fingerprint(candidate):
        return sha256(json.dumps(asdict(candidate), sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    @staticmethod
    def meta_fingerprint(meta):
        payload = asdict(meta); payload["reviewed_at"] = meta.reviewed_at.isoformat()
        return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    @staticmethod
    def _payload(item):
        return {**asdict(item), "decision": item.decision.value, "reviewed_at": item.reviewed_at.isoformat()}

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()

    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime): raise ValueError("reviewed_at must be a datetime")
        return value

    @staticmethod
    def _confidence(value):
        if isinstance(value, bool): raise ValueError("approved confidence must be between 0 and 100")
        try: value = float(value)
        except (TypeError, ValueError) as exc: raise ValueError("approved confidence must be between 0 and 100") from exc
        if not 0 <= value <= 100: raise ValueError("approved confidence must be between 0 and 100")
        return value

    @staticmethod
    def _sha(value):
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError("fingerprint must be SHA-256")
        int(value, 16)


__all__ = ["CompanyFactHumanDecision", "CompanyFactHumanReviewLedger", "CompanyFactHumanReviewReceipt"]
