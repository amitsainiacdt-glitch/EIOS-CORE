"""Human column binding for official NSE iXBRL corroboration candidates."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path


@dataclass(frozen=True)
class ExchangeIxbrlColumnReview:
    review_id: str
    candidate_fingerprint: str
    decision: str
    selected_column: int | None
    reviewer: str
    rationale: str
    reviewed_at: datetime
    receipt_fingerprint: str


def candidate_fingerprint(candidate: dict) -> str:
    return sha256(json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def prepare_column_review(candidate: dict) -> dict:
    if candidate.get("status") != "EXCHANGE_CORROBORATION_CANDIDATE" or candidate.get("creates_approved_facts") is not False:
        raise ValueError("unsafe NSE iXBRL candidate")
    values = candidate.get("values_inr_lakh", {})
    lengths = {len(row) for row in values.values() if isinstance(row, list) and row}
    if not values or len(lengths) != 1:
        raise ValueError("NSE iXBRL metric columns are incomplete or inconsistent")
    count = lengths.pop()
    return {
        "schema_version": 1, "candidate_fingerprint": candidate_fingerprint(candidate),
        "ticker": candidate["metadata"]["ticker"], "company": candidate["metadata"]["company"],
        "period_start": candidate["metadata"]["period_start"], "period_end": candidate["metadata"]["period_end"],
        "basis": candidate["metadata"]["basis"], "column_count": count,
        "columns": [{"column_index": index, "values_inr_lakh": {metric: row[index] for metric, row in values.items()}}
                    for index in range(count)],
        "status": "AWAITING_HUMAN_COLUMN_BINDING", "creates_approved_facts": False,
    }


class ExchangeIxbrlColumnReviewLedger:
    def __init__(self, path: Path): self.path = Path(path)

    def record(self, candidate: dict, *, review_id: str, decision: str, selected_column: int | None,
               reviewer: str, rationale: str, reviewed_at: datetime):
        preview = prepare_column_review(candidate)
        if decision not in {"SELECT", "HOLD", "REJECT"}: raise ValueError("invalid column review decision")
        if decision == "SELECT":
            if isinstance(selected_column, bool) or not isinstance(selected_column, int) or not 0 <= selected_column < preview["column_count"]:
                raise ValueError("selected iXBRL column is outside the candidate")
        elif selected_column is not None: raise ValueError("only SELECT may bind a column")
        if not isinstance(reviewed_at, datetime): raise ValueError("reviewed_at must be a datetime")
        if any(not isinstance(value, str) or not value.strip() for value in (review_id, reviewer, rationale)):
            raise ValueError("review identity, reviewer and rationale are required")
        existing = self.read_all()
        if any(item.review_id == review_id or item.candidate_fingerprint == preview["candidate_fingerprint"] for item in existing):
            raise ValueError("iXBRL candidate already has a column decision")
        raw = ExchangeIxbrlColumnReview(review_id.strip(), preview["candidate_fingerprint"], decision,
            selected_column, reviewer.strip(), rationale.strip(), reviewed_at, "")
        item = ExchangeIxbrlColumnReview(**{**asdict(raw), "receipt_fingerprint": self.fingerprint(raw)})
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            payload=asdict(item); payload["reviewed_at"]=reviewed_at.isoformat()
            stream.write(json.dumps(payload,sort_keys=True,separators=(",", ":"))+"\n")
        return item

    def read_all(self):
        if not self.path.exists(): return ()
        result=[]; ids=set(); candidates=set()
        for number,line in enumerate(self.path.read_text(encoding="utf-8").splitlines(),1):
            try:
                payload=json.loads(line); payload["reviewed_at"]=datetime.fromisoformat(payload["reviewed_at"])
                item=ExchangeIxbrlColumnReview(**payload)
                if item.receipt_fingerprint != self.fingerprint(item): raise ValueError("invalid receipt fingerprint")
                if item.review_id in ids or item.candidate_fingerprint in candidates: raise ValueError("duplicate review")
                ids.add(item.review_id); candidates.add(item.candidate_fingerprint); result.append(item)
            except (KeyError,TypeError,ValueError) as exc: raise ValueError(f"invalid iXBRL column review at line {number}: {exc}") from exc
        return tuple(result)

    @staticmethod
    def fingerprint(review):
        payload=asdict(review); payload.pop("receipt_fingerprint",None); payload["reviewed_at"]=review.reviewed_at.isoformat()
        return sha256(json.dumps(payload,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def apply_column_review(candidate: dict, review: ExchangeIxbrlColumnReview) -> dict:
    if not isinstance(review, ExchangeIxbrlColumnReview) or review.receipt_fingerprint != ExchangeIxbrlColumnReviewLedger.fingerprint(review):
        raise ValueError("valid persisted iXBRL column review required")
    if review.candidate_fingerprint != candidate_fingerprint(candidate): raise ValueError("column review does not bind to candidate")
    if review.decision != "SELECT": raise ValueError("iXBRL column was not selected")
    preview=prepare_column_review(candidate)
    if review.selected_column is None or review.selected_column >= preview["column_count"]: raise ValueError("invalid selected column")
    result={**candidate, "values_inr_lakh": {metric:[row[review.selected_column]] for metric,row in candidate["values_inr_lakh"].items()},
            "column_binding": {"selected_column":review.selected_column,"review_id":review.review_id,
                               "review_receipt_fingerprint":review.receipt_fingerprint},
            "status":"EXCHANGE_CORROBORATION_CANDIDATE", "creates_approved_facts":False}
    return result


__all__=["ExchangeIxbrlColumnReview","ExchangeIxbrlColumnReviewLedger","prepare_column_review","apply_column_review"]
