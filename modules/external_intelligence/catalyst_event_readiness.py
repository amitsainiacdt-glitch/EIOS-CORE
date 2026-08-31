"""Evidence and expectation gates before a candidate reaches catalyst classification."""

from dataclasses import dataclass
from datetime import datetime,timezone
from enum import Enum
import re

from modules.opportunity.catalyst.catalyst_taxonomy import CatalystFamily


class CatalystEventStatus(str,Enum):
    ANNOUNCED="ANNOUNCED"
    SCHEDULED="SCHEDULED"
    COMPLETED="COMPLETED"
    CONTINUING_TREND="CONTINUING_TREND"


@dataclass(frozen=True)
class PublicCatalystEventCandidate:
    candidate_id: str
    entity: str
    family: CatalystFamily
    event_status: CatalystEventStatus
    event_date: datetime | None
    authority_id: str
    source_document_id: str
    source_url: str
    document_hash: str
    exact_passage: str
    linked_fact_ids: tuple[str,...]
    quantified_event_value: float | None
    quantified_event_unit: str | None
    transmission_mechanism: str | None
    expectation_baseline_source_id: str | None
    expectation_gap_statement: str | None
    invalidation_condition: str | None
    public_information_only: bool=True


@dataclass(frozen=True)
class CatalystEventReadiness:
    status: str
    factual_event_ready: bool
    expectation_reset_ready: bool
    missing_controls: tuple[str,...]
    permitted_claim: str
    blocked_claims: tuple[str,...]


def assess_catalyst_event(candidate, *, assessed_at, max_event_age_days=180):
    if not isinstance(candidate,PublicCatalystEventCandidate): raise ValueError("public catalyst candidate is required")
    if assessed_at.tzinfo is None: raise ValueError("assessed_at must be timezone-aware")
    missing=[]
    if not candidate.public_information_only: missing.append("public-information-only evidence")
    if candidate.authority_id not in ("NSE","BSE","SEBI","PIB","RBI","DGFT","AGRI_MINISTRY","FERTILIZERS_DEPARTMENT","FOOD_DISTRIBUTION_DEPARTMENT"):
        missing.append("approved primary authority")
    if not re.fullmatch(r"[0-9a-f]{64}",candidate.document_hash): missing.append("valid SHA-256 source hash")
    if not candidate.source_document_id.strip() or not candidate.source_url.startswith("https://"): missing.append("traceable source document")
    if len(candidate.exact_passage.split())<8: missing.append("substantive exact source passage")
    status=candidate.event_status if isinstance(candidate.event_status,CatalystEventStatus) else CatalystEventStatus(candidate.event_status)
    if status==CatalystEventStatus.CONTINUING_TREND: missing.append("discrete announced, scheduled, or completed event")
    if candidate.event_date is None or candidate.event_date.tzinfo is None: missing.append("dated event")
    else:
        age=(assessed_at.astimezone(timezone.utc)-candidate.event_date.astimezone(timezone.utc)).days
        if status!=CatalystEventStatus.SCHEDULED and (age<0 or age>max_event_age_days): missing.append("current event date")
    if not candidate.linked_fact_ids: missing.append("governed fact linkage")
    if candidate.quantified_event_value is None or not candidate.quantified_event_unit: missing.append("quantified event magnitude and unit")
    if not candidate.transmission_mechanism or len(candidate.transmission_mechanism.split())<5: missing.append("explicit transmission mechanism")
    if not candidate.invalidation_condition or len(candidate.invalidation_condition.split())<4: missing.append("testable invalidation condition")
    factual=not missing
    expectation_missing=[]
    if not candidate.expectation_baseline_source_id: expectation_missing.append("public expectation baseline")
    if not candidate.expectation_gap_statement or len(candidate.expectation_gap_statement.split())<5: expectation_missing.append("explicit expectation gap")
    expectation=factual and not expectation_missing
    all_missing=tuple(dict.fromkeys(missing+expectation_missing))
    readiness="EXPECTATION_RESET_READY" if expectation else "FACTUAL_EVENT_READY" if factual else "RESEARCH_HOLD"
    claim=(f"A dated public event is eligible for {candidate.family.value} research and has an explicit public expectation comparator." if expectation else
           f"A dated public event is eligible for {candidate.family.value} research, but market-expectation reset is unproven." if factual else
           "The candidate is not yet a catalyst; it remains a research lead.")
    return CatalystEventReadiness(readiness,factual,expectation,all_missing,claim,(
        "the event will cause the proposed operating outcome",
        "announcement equals execution or cash realization",
        "event value equals revenue, profit, or free cash flow",
        "the event is surprising or unpriced without a public expectation baseline",
        "catalyst classification authorizes an Opportunity, recommendation, or trade",
    ))


__all__=["CatalystEventStatus","PublicCatalystEventCandidate","CatalystEventReadiness","assess_catalyst_event"]
