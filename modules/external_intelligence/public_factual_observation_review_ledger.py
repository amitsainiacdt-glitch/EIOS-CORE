"""Append-only human review decisions for factual Observation proposals."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

from modules.external_intelligence.public_factual_observation_proposal import PublicFactualObservationProposal
from modules.external_intelligence.public_factual_observation_proposal_builder import PublicFactualObservationProposalBuilder


class PublicFactualObservationReviewDecision(str, Enum):
    APPROVE = "APPROVE"
    DEFER = "DEFER"
    REJECT = "REJECT"


@dataclass(frozen=True)
class PublicFactualObservationReviewReceipt:
    schema_version: int
    review_id: str
    proposal_id: str
    proposal_fingerprint: str
    decision: PublicFactualObservationReviewDecision
    approved_confidence: float | None
    notes: str
    reviewed_at: datetime
    reviewer: str


class PublicFactualObservationReviewLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("review ledger path must identify a file")

    def record(self, proposal, *, review_id, decision, notes, reviewed_at, reviewer, approved_confidence=None):
        if not isinstance(proposal, PublicFactualObservationProposal):
            raise ValueError("proposal must be a PublicFactualObservationProposal")
        if not PublicFactualObservationProposalBuilder.verify_fingerprint(proposal):
            raise ValueError("proposal fingerprint does not match proposal content")
        decision = decision if isinstance(decision, PublicFactualObservationReviewDecision) else PublicFactualObservationReviewDecision(decision)
        if any(item.review_id == review_id for item in self.read_all()):
            raise ValueError("review_id already exists")
        if any(item.proposal_fingerprint == proposal.proposal_fingerprint for item in self.read_all()):
            raise ValueError("proposal already has a review decision")
        confidence = self._confidence(approved_confidence) if approved_confidence is not None else None
        if decision == PublicFactualObservationReviewDecision.APPROVE and confidence is None:
            raise ValueError("APPROVE requires approved_confidence")
        if decision != PublicFactualObservationReviewDecision.APPROVE and confidence is not None:
            raise ValueError("only APPROVE can set approved_confidence")
        receipt = PublicFactualObservationReviewReceipt(
            1, self._text(review_id, "review_id"), proposal.proposal_id,
            proposal.proposal_fingerprint, decision, confidence, self._text(notes, "notes"),
            self._datetime(reviewed_at), self._text(reviewer, "reviewer"),
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(receipt), sort_keys=True, separators=(",", ":")) + "\n")
        return receipt

    def read_all(self):
        if not self.path.exists():
            return ()
        result, reviews, proposals = [], set(), set()
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid proposal review at line {number}: {exc}") from exc
                if item.review_id in reviews or item.proposal_fingerprint in proposals:
                    raise ValueError(f"Duplicate proposal review at line {number}")
                reviews.add(item.review_id); proposals.add(item.proposal_fingerprint); result.append(item)
        return tuple(result)

    @classmethod
    def _parse(cls, value):
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError("unsupported proposal review schema")
        decision = PublicFactualObservationReviewDecision(value["decision"])
        confidence = value["approved_confidence"]
        confidence = cls._confidence(confidence) if confidence is not None else None
        if (decision == PublicFactualObservationReviewDecision.APPROVE) != (confidence is not None):
            raise ValueError("review confidence does not match decision")
        return PublicFactualObservationReviewReceipt(
            1, cls._text(value["review_id"], "review_id"), cls._text(value["proposal_id"], "proposal_id"),
            cls._sha(value["proposal_fingerprint"]), decision, confidence, cls._text(value["notes"], "notes"),
            datetime.fromisoformat(value["reviewed_at"]), cls._text(value["reviewer"], "reviewer"),
        )

    @staticmethod
    def _payload(item):
        return {**item.__dict__, "decision": item.decision.value, "reviewed_at": item.reviewed_at.isoformat()}

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @staticmethod
    def _sha(value):
        value = PublicFactualObservationReviewLedger._text(value, "proposal_fingerprint").casefold()
        if len(value) != 64:
            raise ValueError("proposal_fingerprint must be SHA-256")
        try: int(value, 16)
        except ValueError as exc: raise ValueError("proposal_fingerprint must be SHA-256") from exc
        return value

    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime):
            raise ValueError("reviewed_at must be a datetime")
        return value

    @staticmethod
    def _confidence(value):
        if isinstance(value, bool):
            raise ValueError("approved_confidence must be between 0 and 100")
        value = float(value)
        if not 0 <= value <= 100:
            raise ValueError("approved_confidence must be between 0 and 100")
        return value


__all__ = ["PublicFactualObservationReviewDecision", "PublicFactualObservationReviewLedger", "PublicFactualObservationReviewReceipt"]
