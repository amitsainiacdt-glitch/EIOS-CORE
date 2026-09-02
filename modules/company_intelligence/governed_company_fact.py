"""Materialize approved company candidates as governed facts only."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from modules.company_intelligence.company_candidate_meta_review import CompanyCandidateMetaAssessment
from modules.company_intelligence.company_fact_human_review import CompanyFactHumanDecision, CompanyFactHumanReviewLedger, CompanyFactHumanReviewReceipt
from modules.company_intelligence.company_fact_review_queue import CompanyFactReviewCandidate


@dataclass(frozen=True)
class GovernedCompanyFact:
    schema_version: int
    fact_id: str
    candidate_id: str
    company: str
    event_type: str
    statement: str
    statement_posture: str
    explicit_amounts: tuple[str, ...]
    explicit_dates: tuple[str, ...]
    pdf_page: int | None
    source_url: str
    document_hash: str
    approved_confidence: float
    meta_assessment_id: str
    human_review_id: str
    created_at: datetime
    status: str = "GOVERNED_FACT"
    creates_evidence: bool = False
    creates_catalyst: bool = False
    changes_verdict: bool = False


class GovernedCompanyFactRepository:
    def __init__(self, path: Path): self.path = Path(path)

    def materialize(self, candidate, meta, review, *, created_at):
        CompanyFactHumanReviewLedger.validate_binding(candidate, meta, review)
        if review.decision != CompanyFactHumanDecision.APPROVE or review.approved_confidence is None:
            raise ValueError("governed fact requires an approved human review")
        if any(item.candidate_id == candidate.candidate_id for item in self.read_all()):
            raise ValueError("candidate is already materialized")
        fact_id = sha256(f"{candidate.candidate_id}\n{review.review_id}\nGOVERNED_FACT_V1".encode()).hexdigest()
        fact = GovernedCompanyFact(
            1, fact_id, candidate.candidate_id, candidate.company, candidate.event_type,
            candidate.source_passage, candidate.statement_posture, candidate.explicit_amounts,
            candidate.explicit_dates, candidate.pdf_page, candidate.source_url,
            candidate.document_hash, review.approved_confidence, meta.assessment_id,
            review.review_id, created_at,
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as ledger:
            payload = asdict(fact); payload["created_at"] = created_at.isoformat()
            ledger.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return fact

    def read_all(self):
        if not self.path.exists(): return ()
        result, ids, candidates = [], set(), set()
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                value = json.loads(line); value["created_at"] = datetime.fromisoformat(value["created_at"])
                fact = GovernedCompanyFact(**value)
                if fact.schema_version != 1 or fact.fact_id in ids or fact.candidate_id in candidates:
                    raise ValueError("invalid or duplicate governed fact")
                if fact.creates_evidence or fact.creates_catalyst or fact.changes_verdict:
                    raise ValueError("governed fact exceeded its authority")
                ids.add(fact.fact_id); candidates.add(fact.candidate_id); result.append(fact)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid governed company fact at line {number}: {exc}") from exc
        return tuple(result)


__all__ = ["GovernedCompanyFact", "GovernedCompanyFactRepository"]
