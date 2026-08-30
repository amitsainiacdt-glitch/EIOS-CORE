"""Append-only audit events for controlled public Observation commits."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path


class PublicObservationCommitAuditStatus(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"
    COMMITTED = "COMMITTED"
    FINAL_NOVELTY_REJECTION = "FINAL_NOVELTY_REJECTION"


@dataclass(frozen=True)
class PublicObservationCommitAuditEvent:
    schema_version: int
    commit_id: str
    sequence: int
    status: PublicObservationCommitAuditStatus
    acquisition_id: str
    extraction_id: str
    admission_decision: str
    admission_reason_codes: tuple[str, ...]
    document_hash: str | None
    extracted_content_fingerprint: str | None
    observation_fingerprint: str | None
    proposal_id: str | None
    proposal_fingerprint: str | None
    review_id: str | None
    recorded_at: datetime
    recorder: str


class PublicObservationCommitAuditLedger:
    def __init__(self, path):
        self.path = Path(path)
        if str(self.path).strip() in {"", "."}:
            raise ValueError("commit audit ledger path must identify a file")

    def begin(self, *, commit_id, admission, recorded_at, recorder, proposal=None, review=None):
        existing = self.events_for(commit_id)
        if existing:
            raise ValueError("commit_id already exists")
        return self._append(commit_id, 1, "AUTHORIZED", admission, None, recorded_at, recorder, proposal, review)

    def block(self, *, commit_id, admission, recorded_at, recorder, proposal=None, review=None):
        existing = self.events_for(commit_id)
        if existing:
            raise ValueError("commit_id already exists")
        return self._append(commit_id, 1, "BLOCKED", admission, None, recorded_at, recorder, proposal, review)

    def complete(self, *, commit_id, status, admission, observation_fingerprint, recorded_at, recorder, proposal=None, review=None):
        existing = self.events_for(commit_id)
        if len(existing) != 1 or existing[0].status != PublicObservationCommitAuditStatus.AUTHORIZED:
            raise ValueError("commit must have exactly one AUTHORIZED event before completion")
        if status not in ("COMMITTED", "FINAL_NOVELTY_REJECTION"):
            raise ValueError("invalid terminal commit status")
        if status == "COMMITTED" and not observation_fingerprint:
            raise ValueError("COMMITTED event requires an observation fingerprint")
        if status != "COMMITTED" and observation_fingerprint:
            raise ValueError("non-committed event cannot have an observation fingerprint")
        expected = self._review_identity(proposal, review)
        if (existing[0].proposal_id, existing[0].proposal_fingerprint, existing[0].review_id) != expected:
            raise ValueError("terminal commit review identity differs from authorization")
        return self._append(commit_id, 2, status, admission, observation_fingerprint, recorded_at, recorder, proposal, review)

    def events_for(self, commit_id):
        commit_id = self._text(commit_id, "commit_id")
        return tuple(item for item in self.read_all() if item.commit_id == commit_id)

    def unresolved_commit_ids(self):
        grouped = {}
        for event in self.read_all():
            grouped.setdefault(event.commit_id, []).append(event)
        return tuple(sorted(key for key, values in grouped.items() if values[-1].status == PublicObservationCommitAuditStatus.AUTHORIZED))

    def read_all(self):
        if not self.path.exists():
            return ()
        result, state = [], {}
        with self.path.open("r", encoding="utf-8") as ledger:
            for number, line in enumerate(ledger, 1):
                if not line.strip():
                    continue
                try:
                    item = self._parse(json.loads(line))
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid commit audit event at line {number}: {exc}") from exc
                prior = state.get(item.commit_id)
                if item.sequence == 1:
                    if prior is not None:
                        raise ValueError(f"Duplicate commit start at line {number}")
                elif item.sequence == 2:
                    if prior is None or prior.status != PublicObservationCommitAuditStatus.AUTHORIZED:
                        raise ValueError(f"Commit terminal event has no authorization at line {number}")
                else:
                    raise ValueError(f"Invalid commit sequence at line {number}")
                state[item.commit_id] = item
                result.append(item)
        return tuple(result)

    def _append(self, commit_id, sequence, status, admission, observation_fingerprint, recorded_at, recorder, proposal=None, review=None):
        from modules.external_intelligence.public_observation_admission_preview import PublicObservationAdmissionPreview
        if not isinstance(admission, PublicObservationAdmissionPreview):
            raise ValueError("admission must be a PublicObservationAdmissionPreview")
        proposal_id, proposal_fingerprint, review_id = self._review_identity(proposal, review)
        item = PublicObservationCommitAuditEvent(
            1, self._text(commit_id, "commit_id"), sequence,
            PublicObservationCommitAuditStatus(status), admission.acquisition_id,
            admission.extraction_id, admission.decision.value, admission.reason_codes,
            admission.document_hash, admission.extracted_content_fingerprint,
            observation_fingerprint, proposal_id, proposal_fingerprint, review_id,
            self._datetime(recorded_at), self._text(recorder, "recorder"),
        )
        item = self._parse(self._payload(item))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(self._payload(item), sort_keys=True, separators=(",", ":")) + "\n")
        return item

    @classmethod
    def _parse(cls, value):
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError("unsupported commit audit schema")
        status = PublicObservationCommitAuditStatus(value["status"])
        sequence = value["sequence"]
        if isinstance(sequence, bool) or sequence not in (1, 2):
            raise ValueError("invalid commit audit sequence")
        reasons = tuple(cls._text(v, "reason_code") for v in value["admission_reason_codes"])
        fingerprint = value["observation_fingerprint"]
        if status == PublicObservationCommitAuditStatus.COMMITTED and not fingerprint:
            raise ValueError("COMMITTED event requires observation fingerprint")
        return PublicObservationCommitAuditEvent(
            1, cls._text(value["commit_id"], "commit_id"), sequence, status,
            cls._text(value["acquisition_id"], "acquisition_id"), cls._text(value["extraction_id"], "extraction_id"),
            cls._text(value["admission_decision"], "admission_decision"), reasons,
            value["document_hash"], value["extracted_content_fingerprint"], fingerprint,
            value.get("proposal_id"), value.get("proposal_fingerprint"), value.get("review_id"),
            datetime.fromisoformat(value["recorded_at"]), cls._text(value["recorder"], "recorder"),
        )

    @staticmethod
    def _review_identity(proposal, review):
        if proposal is None and review is None:
            return None, None, None
        from modules.external_intelligence.public_factual_observation_proposal import PublicFactualObservationProposal
        from modules.external_intelligence.public_factual_observation_review_ledger import PublicFactualObservationReviewReceipt
        if not isinstance(proposal, PublicFactualObservationProposal) or not isinstance(review, PublicFactualObservationReviewReceipt):
            raise ValueError("proposal and review must be supplied together")
        if review.proposal_id != proposal.proposal_id or review.proposal_fingerprint != proposal.proposal_fingerprint:
            raise ValueError("review does not bind to proposal")
        return proposal.proposal_id, proposal.proposal_fingerprint, review.review_id

    @staticmethod
    def _payload(item):
        return {**item.__dict__, "status": item.status.value, "admission_reason_codes": list(item.admission_reason_codes), "recorded_at": item.recorded_at.isoformat()}

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @staticmethod
    def _datetime(value):
        if not isinstance(value, datetime):
            raise ValueError("recorded_at must be a datetime")
        return value


__all__ = ["PublicObservationCommitAuditEvent", "PublicObservationCommitAuditLedger", "PublicObservationCommitAuditStatus"]
