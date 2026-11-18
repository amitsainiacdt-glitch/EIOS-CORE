"""FOX research-only completion gate and accountable case queue.

Not connected to the Site, scheduler or brokerage. Never places trades.
No synthetic missing fundamentals, price targets, or implied research ADDs.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple

from modules.decision.fox_valuation_worksheet import Worksheet, evaluate_worksheet
from modules.decision.fox_add_engine import FoxUnderwriting, evaluate_fox, FoxAction


@dataclass(frozen=True)
class CompletionCase:
    ticker: str
    lane: str
    first_seen: str
    last_reviewed: str
    owner: str
    primary_source_urls: Tuple[str, ...]
    next_evidence_event: str
    review_due: str
    exact_missing_inputs: Tuple[str, ...]
    worksheet: Optional[Worksheet] = None
    underwriting: Optional[FoxUnderwriting] = None
    original_zone: Optional[Tuple[float, float]] = None
    proposed_zone: Optional[Tuple[float, float]] = None
    fundamental_revision_source: str = ""
    fundamental_revision_reason: str = ""
    closed: bool = False
    closure_reason: str = ""


@dataclass(frozen=True)
class CompletionResult:
    state: str
    blockers: Tuple[str, ...]
    next_action: str
    days_open: int
    valuation_completed: bool
    capital_deployment_rupees: int = 0


def complete_case(c: CompletionCase, as_of: str) -> CompletionResult:
    """Do not allow a good-looking scenario to become a fictional ADD.

    A scenario screen and a separate causal/risk underwriting must BOTH pass.
    Failed economics stay economic failures, not a generic missing-evidence WAIT.
    """
    today = date.fromisoformat(as_of)
    first = date.fromisoformat(c.first_seen)
    reviewed = date.fromisoformat(c.last_reviewed)
    due = date.fromisoformat(c.review_due)
    if first > today or reviewed > today or due < first:
        raise ValueError("Invalid point-in-time case dates")
    age = (today - first).days
    missing = list(c.exact_missing_inputs)
    if not c.owner.strip(): missing.append("Accountable research owner")
    if not c.primary_source_urls: missing.append("Dated primary source URLs")
    if not c.next_evidence_event.strip(): missing.append("Next falsifiable evidence event")
    if due < today and not c.closed: missing.append("Review overdue: record an updated dated action")
    if c.original_zone != c.proposed_zone and c.original_zone is not None:
        if not (c.fundamental_revision_source.startswith("https://")
                and c.fundamental_revision_reason.strip()):
            missing.append("Original buy-zone immutable: fundamental source and reason required")
    if c.closed:
        if not c.closure_reason.strip():
            raise ValueError("Cannot archive a case without a closure reason")
        return CompletionResult("ARCHIVED", tuple(missing), c.closure_reason, age, False)
    if c.worksheet is None:
        missing.append("Dated fully diluted attributable-owner valuation worksheet")
        return CompletionResult("UNDERWRITING_INCOMPLETE", tuple(dict.fromkeys(missing)),
                                c.next_evidence_event, age, False)
    v = evaluate_worksheet(c.worksheet)
    if v.state == "UNDERWRITING_INCOMPLETE":
        missing.extend(v.blockers)
        return CompletionResult("UNDERWRITING_INCOMPLETE", tuple(dict.fromkeys(missing)),
                                c.next_evidence_event, age, False)
    if v.state == "ECONOMIC_FAILURE":
        return CompletionResult("ECONOMIC_FAILURE", tuple(v.blockers) + tuple(dict.fromkeys(missing)),
                                c.next_evidence_event, age, True)
    if missing:
        return CompletionResult("UNDERWRITING_INCOMPLETE", tuple(dict.fromkeys(missing)),
                                c.next_evidence_event, age, True)
    if c.underwriting is None:
        return CompletionResult("UNDERWRITING_INCOMPLETE",
                                ("Independent causal, governance and funding underwriting missing",),
                                c.next_evidence_event, age, True)
    if c.worksheet.ticker != c.underwriting.ticker or c.worksheet.as_of != c.underwriting.as_of:
        return CompletionResult("UNDERWRITING_INCOMPLETE",
                                ("Worksheet and independent underwriting differ in ticker/date",),
                                c.next_evidence_event, age, True)
    d = evaluate_fox(c.underwriting)
    if d.review_state == "FATAL_RISK":
        return CompletionResult("FATAL_RISK", d.blockers, c.next_evidence_event, age, True)
    if d.review_state == "ECONOMIC_FAILURE":
        return CompletionResult("ECONOMIC_FAILURE", d.blockers, c.next_evidence_event, age, True)
    if d.action in (FoxAction.EIP_ADD, FoxAction.VALUE_ADD, FoxAction.SPECIAL_SITUATION_ADD):
        return CompletionResult("RESEARCH_ADD", (), "Human research review; no trade authorisation",
                                age, True)
    return CompletionResult("UNDERWRITING_INCOMPLETE", d.blockers,
                            c.next_evidence_event, age, True)


def queue_audit(cases: Tuple[CompletionCase, ...], as_of: str) -> dict:
    results = [(c.ticker, complete_case(c, as_of)) for c in cases]
    return {
        "issuers": len(results),
        "over_7_days_open": sum(r.days_open > 7 and r.state != "ARCHIVED" for _, r in results),
        "over_14_days_open": sum(r.days_open > 14 and r.state != "ARCHIVED" for _, r in results),
        "valuations_completed": sum(r.valuation_completed for _, r in results),
        "research_adds": sum(r.state == "RESEARCH_ADD" for _, r in results),
        "incomplete": [(ticker, r.blockers, r.next_action) for ticker, r in results
                       if r.state == "UNDERWRITING_INCOMPLETE"],
        "capital_deployment_rupees": 0,
    }
