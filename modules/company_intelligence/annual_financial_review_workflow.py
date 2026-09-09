"""Operational queue for human review of extracted annual financial statements."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from modules.company_intelligence.governed_annual_financial import (
    AnnualFinancialHumanReviewLedger, GovernedAnnualFinancialRepository, STATEMENT_TYPES,
)


@dataclass(frozen=True)
class AnnualFinancialReviewItem:
    ticker: str
    company: str
    statement_type: str
    period: str
    basis: str
    figure_count: int
    source_url: str
    document_hash: str
    source_pages: tuple[int, ...]
    statement_fingerprint: str
    status: str = "AWAITING_HUMAN_DECISION"


class AnnualFinancialReviewWorkflow:
    def __init__(self, review_ledger: AnnualFinancialHumanReviewLedger,
                 governed_repository: GovernedAnnualFinancialRepository):
        self.review_ledger = review_ledger
        self.governed_repository = governed_repository

    def prepare(self, pack: dict, statement_type: str):
        if statement_type not in STATEMENT_TYPES:
            raise ValueError("unsupported annual statement type")
        ticker, company = pack.get("ticker"), pack.get("company")
        if not ticker or not company or pack.get("schema_version") != 1:
            raise ValueError("annual review pack requires schema, ticker and company")
        seen, result = set(), []
        decided = {item.statement_fingerprint for item in self.review_ledger.read_all()}
        for source_statement in pack.get("periods", []):
            statement = {**source_statement, "statement_type": statement_type}
            normalized, document_hash, source_url = self.governed_repository._validate_statement(statement)
            fingerprint = self.governed_repository.fingerprint(statement)
            identity = (statement["period"], statement["basis"])
            if identity in seen:
                raise ValueError("duplicate period and basis in annual review pack")
            seen.add(identity)
            pages = tuple(sorted({int(fact["pdf_page"]) for fact in statement["facts"].values()
                                  if fact is not None and "pdf_page" in fact}))
            result.append((AnnualFinancialReviewItem(
                ticker, company, statement_type, statement["period"], statement["basis"],
                len(normalized), source_url, document_hash, pages, fingerprint,
                "DECISION_RECORDED" if fingerprint in decided else "AWAITING_HUMAN_DECISION"), statement))
        return tuple(result)

    def decide(self, pack: dict, statement_type: str, *, period: str, basis: str,
               review_id: str, reviewer: str, decision: str, confidence: int | None,
               rationale: str, reviewed_at: datetime):
        matches = [(item, statement) for item, statement in self.prepare(pack, statement_type)
                   if item.period == period and item.basis == basis]
        if len(matches) != 1:
            raise ValueError("annual review selection must match exactly one statement")
        item, statement = matches[0]
        if item.status != "AWAITING_HUMAN_DECISION":
            raise ValueError("annual statement already has a human decision")
        review = self.review_ledger.record(
            statement, review_id=review_id, reviewer=reviewer, decision=decision,
            confidence=confidence, rationale=rationale, reviewed_at=reviewed_at)
        governed = None
        if decision == "APPROVE":
            governed = self.governed_repository.materialize(
                statement, review, ticker=item.ticker, company=item.company, created_at=reviewed_at)
        return review, governed


__all__ = ["AnnualFinancialReviewItem", "AnnualFinancialReviewWorkflow"]
