"""Human-reviewed annual statement Facts routed through the controlled write boundary."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from pathlib import Path

from modules.intelligence_write import (
    ActorOrigin, ActorType, AuthorityScope, ControlledIntelligenceWriteJournal,
    ControlledIntelligenceWriteService, InformationClass, OriginType,
    SourceReference, ValidationStatus, WriteCommand, WriteOperation,
    WriteReceiptStatus,
)


STATEMENT_TYPES = {"BALANCE_SHEET", "CASH_FLOW"}


@dataclass(frozen=True)
class AnnualFinancialHumanReview:
    review_id: str
    reviewer: str
    statement_fingerprint: str
    decision: str
    confidence: int
    rationale: str
    reviewed_at: datetime


@dataclass(frozen=True)
class GovernedAnnualFinancial:
    schema_version: int
    record_id: str
    ticker: str
    company: str
    statement_type: str
    period: str
    basis: str
    figures_inr_crore: dict[str, str]
    document_hash: str
    source_url: str
    source_pages: tuple[int, ...]
    statement_fingerprint: str
    human_review_id: str
    created_at: datetime
    controlled_write_receipt_id: str
    status: str = "GOVERNED_ANNUAL_FINANCIAL"
    changes_verdict: bool = False
    authorizes_trade: bool = False


class GovernedAnnualFinancialRepository:
    """Append-only store. Extraction and arithmetic checks cannot approve a statement."""

    def __init__(self, path: Path, *, controlled_write_service=None):
        self.path = Path(path)
        self.controlled_write_service = controlled_write_service or ControlledIntelligenceWriteService(
            journal=ControlledIntelligenceWriteJournal(
                self.path.parent / "controlled-intelligence-write-journal.jsonl"
            )
        )

    def materialize(self, statement: dict, review: AnnualFinancialHumanReview, *,
                    ticker: str, company: str, created_at: datetime):
        normalized, document_hash, source_url = self._validate_statement(statement)
        fingerprint = self.fingerprint(statement)
        if not isinstance(review, AnnualFinancialHumanReview):
            raise ValueError("annual statement requires a human review")
        if review.decision != "APPROVE" or review.statement_fingerprint != fingerprint:
            raise ValueError("human approval does not bind to the current annual statement")
        if not review.reviewer.strip() or not review.rationale.strip() or not 0 <= review.confidence <= 100:
            raise ValueError("human review identity, rationale and confidence are required")
        if statement.get("review_status") != "PENDING_META_REVIEW" or statement.get("creates_evidence") is not False:
            raise ValueError("only unchanged fail-closed extraction candidates may be reviewed")
        statement_type = statement["statement_type"]
        period, basis = statement["period"], statement["basis"]
        semantic_key = f"annual-{statement_type.lower().replace('_', '-')}|{period}|{basis}"
        record_id = sha256(f"{ticker}\n{semantic_key}\n{fingerprint}\nGOVERNED_ANNUAL_V1".encode()).hexdigest()
        source_pages = tuple(sorted({int(f["pdf_page"]) for f in statement["facts"].values()
                                     if f is not None and "pdf_page" in f}))
        command = WriteCommand(
            schema_version=1, command_id=f"controlled-annual:{record_id}",
            idempotency_key=f"governed-annual:{record_id}", operation=WriteOperation.PROPOSE_FACT,
            actor=ActorOrigin(
                actor_id=review.reviewer, actor_type=ActorType.HUMAN,
                actor_version="annual-financial-human-review-v1", origin_id=review.review_id,
                origin_type=OriginType.HUMAN_REVIEW,
                authority_scopes=(AuthorityScope.PROPOSE_FACT, AuthorityScope.VERIFY_FACT)),
            requested_at=created_at, company_id=ticker, entity=company,
            information_class=InformationClass.FACT, semantic_key=semantic_key,
            payload={"metric": f"ANNUAL_{statement_type}", "value": normalized,
                     "unit": "INR_CRORE", "period": period, "basis": basis,
                     "statement_fingerprint": fingerprint, "human_review_id": review.review_id},
            source_references=(SourceReference(
                source_id=fingerprint, source_type=f"GOVERNED_ANNUAL_{statement_type}",
                source_url=source_url, document_hash=document_hash,
                page_or_section=",".join(map(str, source_pages))),),
            confidence=review.confidence, requested_validation_status=ValidationStatus.VERIFIED,
            correlation_id=record_id, causation_id=review.review_id)
        receipt = self.controlled_write_service.submit(command)
        if receipt.status not in {WriteReceiptStatus.ACCEPTED, WriteReceiptStatus.DUPLICATE_NO_CHANGE}:
            raise ValueError("controlled annual Fact write blocked: " +
                             ", ".join(receipt.rejection_codes or receipt.validation_codes))
        item = GovernedAnnualFinancial(
            1, record_id, ticker, company, statement_type, period, basis, normalized,
            document_hash, source_url, source_pages, fingerprint,
            review.review_id, created_at, receipt.receipt_id)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            payload = asdict(item); payload["created_at"] = created_at.isoformat()
            stream.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        return item

    def read_all(self):
        if not self.path.exists():
            return ()
        receipt_ids = {receipt.receipt_id for receipt in self.controlled_write_service.receipts()}
        result, record_ids = [], set()
        for number, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line); value["created_at"] = datetime.fromisoformat(value["created_at"])
                value["source_pages"] = tuple(value["source_pages"])
                item = GovernedAnnualFinancial(**value)
                if item.record_id in record_ids or item.statement_type not in STATEMENT_TYPES:
                    raise ValueError("invalid or duplicate annual record")
                if item.controlled_write_receipt_id not in receipt_ids:
                    raise ValueError("controlled write receipt is missing")
                if item.changes_verdict or item.authorizes_trade:
                    raise ValueError("annual record exceeded its authority")
                record_ids.add(item.record_id); result.append(item)
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"invalid governed annual record at line {number}: {exc}") from exc
        return tuple(result)

    @staticmethod
    def fingerprint(statement: dict) -> str:
        return sha256(json.dumps(statement, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    @staticmethod
    def _validate_statement(statement: dict) -> tuple[dict[str, str], str, str]:
        if statement.get("statement_type") not in STATEMENT_TYPES:
            raise ValueError("unsupported annual statement type")
        for key in ("period", "basis", "facts"):
            if not statement.get(key):
                raise ValueError(f"annual statement requires {key}")
        sourced = [fact for fact in statement["facts"].values() if fact is not None]
        if not sourced:
            raise ValueError("annual statement contains no figures")
        document_hash = statement.get("document_hash") or sourced[0].get("document_hash")
        source_url = statement.get("source_url") or sourced[0].get("source_url")
        if not isinstance(document_hash, str) or len(document_hash) != 64 or not source_url:
            raise ValueError("annual statement requires source URL and SHA-256 document hash")
        normalized = {}
        for metric, fact in statement["facts"].items():
            if fact is None:
                continue
            if fact.get("document_hash") != document_hash or fact.get("source_url") != source_url:
                raise ValueError("all annual figures must bind to the same source")
            if fact.get("unit") != "INR_CRORE":
                raise ValueError("annual figure unit must be INR_CRORE")
            try:
                number = Decimal(str(fact["value"]))
            except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
                raise ValueError(f"invalid annual figure: {metric}") from exc
            if not number.is_finite():
                raise ValueError(f"invalid annual figure: {metric}")
            normalized[metric] = format(number, "f")
        return normalized, document_hash, source_url


__all__ = ["AnnualFinancialHumanReview", "GovernedAnnualFinancial", "GovernedAnnualFinancialRepository"]
