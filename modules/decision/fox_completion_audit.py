"""FOX completion audit: research helper, not production integration/trading."""
from dataclasses import dataclass
from datetime import date
from typing import Tuple

PENDING = frozenset(("INVESTIGATE", "UNDERWRITING_INCOMPLETE"))
CLOSED = frozenset(("RESEARCH_ADD", "ECONOMIC_FAILURE", "FATAL_RISK"))
VALID_DECISIONS = PENDING | CLOSED

@dataclass(frozen=True)
class Case:
    ticker: str
    discovered: str
    last_review: str
    decision: str
    owner: str
    missing_facts: Tuple[str, ...]
    next_event: str
    due: str
    valuation_complete: bool
    evidence_urls: Tuple[str, ...]
    portfolio: bool = False

def audit(cases: Tuple[Case, ...], as_of: str):
    """Return named case audit and accurate 7/14-day stale totals."""
    today = date.fromisoformat(as_of)
    output, seen = [], set()
    for c in cases:
        start, reviewed = date.fromisoformat(c.discovered), date.fromisoformat(c.last_review)
        if c.decision not in VALID_DECISIONS:
            raise ValueError("Unknown FOX decision: cannot silently close case")
        if not c.ticker or c.ticker in seen or start > reviewed or reviewed > today:
            raise ValueError("duplicate/invalid case or dates")
        seen.add(c.ticker)
        pending = c.decision in PENDING
        age = (today-start).days
        days_unreviewed = (today-reviewed).days
        gaps = []
        if not c.owner: gaps.append("missing owner")
        if not c.evidence_urls or not all(u.startswith("https://") for u in c.evidence_urls):
            gaps.append("missing primary evidence")
        if pending:
            if not c.missing_facts: gaps.append("missing named blocker")
            if not c.next_event: gaps.append("missing next event")
            if not c.due: gaps.append("missing due date")
        else:
            if not c.valuation_complete: gaps.append("closed without valuation")
        overdue = pending and (not c.due or date.fromisoformat(c.due) < today)
        output.append(dict(ticker=c.ticker, decision=c.decision, age_days=age,
                           days_unreviewed=days_unreviewed,
                           unreviewed_7=pending and days_unreviewed>7,
                           unreviewed_14=pending and days_unreviewed>14,
                           stale_7=pending and age>7, stale_14=pending and age>14,
                           overdue=overdue, missing=tuple(gaps),
                           priority="P0" if pending and (overdue or c.portfolio) else
                                    "P1" if pending else "CLOSED"))
    return dict(cases=output, stale_7=sum(x["stale_7"] for x in output),
                stale_14=sum(x["stale_14"] for x in output),
                unreviewed_7=sum(x["unreviewed_7"] for x in output),
                unreviewed_14=sum(x["unreviewed_14"] for x in output),
                incomplete=sum(x["decision"] in PENDING for x in output),
                completed=sum(x["decision"] not in PENDING for x in output),
                capital_deployment_rupees=0)
