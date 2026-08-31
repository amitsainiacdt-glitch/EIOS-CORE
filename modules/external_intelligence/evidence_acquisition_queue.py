"""Deterministic, bounded research queue for unresolved evidence layers."""

from dataclasses import dataclass
from datetime import datetime,timedelta
from enum import Enum


class AcquisitionRouteState(str,Enum):
    READY="READY"
    TRANSIENT_FAILURE="TRANSIENT_FAILURE"
    ACCESS_REQUIRED="ACCESS_REQUIRED"
    SOURCE_BOUNDARY="SOURCE_BOUNDARY"
    STALE_ONLY="STALE_ONLY"


@dataclass(frozen=True)
class EvidenceAcquisitionNeed:
    need_id: str
    evidence_domain: str
    source_id: str
    route_state: AcquisitionRouteState
    blocks_sector_transmission: bool
    blocks_company_attribution: bool
    contradiction_value: int
    expected_information_gain: int
    attempt_count: int
    last_attempt_at: datetime | None
    minimum_retry_hours: int
    authorized_public_route: bool
    requires_user_credential_or_key: bool


@dataclass(frozen=True)
class EvidenceAcquisitionQueueItem:
    need_id: str
    priority: int
    action: str
    eligible_now: bool
    next_eligible_at: datetime | None
    reason_codes: tuple[str,...]


def build_evidence_acquisition_queue(needs, *, now, sector_transmission_ready=False):
    if now.tzinfo is None: raise ValueError("now must be timezone-aware")
    result=[]
    for need in needs:
        if not isinstance(need,EvidenceAcquisitionNeed): raise ValueError("queue requires EvidenceAcquisitionNeed items")
        state=need.route_state if isinstance(need.route_state,AcquisitionRouteState) else AcquisitionRouteState(need.route_state)
        reasons=[]; eligible=True; next_at=None
        if not need.authorized_public_route: eligible=False; reasons.append("NO_AUTHORIZED_PUBLIC_ROUTE")
        if need.requires_user_credential_or_key: eligible=False; reasons.append("USER_ACCESS_REQUIRED")
        if state==AcquisitionRouteState.SOURCE_BOUNDARY: eligible=False; reasons.append("SOURCE_BOUNDARY_RESPECTED")
        if state==AcquisitionRouteState.ACCESS_REQUIRED: eligible=False; reasons.append("ACCESS_REQUIRED")
        if need.last_attempt_at is not None:
            if need.last_attempt_at.tzinfo is None: raise ValueError("last_attempt_at must be timezone-aware")
            next_at=need.last_attempt_at+timedelta(hours=need.minimum_retry_hours*(2**min(need.attempt_count,4)))
            if now<next_at: eligible=False; reasons.append("RETRY_BACKOFF_ACTIVE")
        if need.blocks_company_attribution and not need.blocks_sector_transmission and not sector_transmission_ready:
            eligible=False; reasons.append("DEFER_UNTIL_SECTOR_TRANSMISSION_READY")
        priority=(40 if need.blocks_sector_transmission else 0)+(15 if need.blocks_company_attribution else 0)+need.contradiction_value+need.expected_information_gain-min(need.attempt_count*5,20)
        action=("ACQUIRE_AND_HASH" if eligible and state==AcquisitionRouteState.READY else
                "BOUNDED_RETRY" if eligible and state==AcquisitionRouteState.TRANSIENT_FAILURE else
                "FIND_SANCTIONED_ALTERNATIVE" if eligible and state==AcquisitionRouteState.STALE_ONLY else
                "WAIT")
        result.append(EvidenceAcquisitionQueueItem(need.need_id,priority,action,eligible,next_at,tuple(reasons)))
    return tuple(sorted(result,key=lambda item:(not item.eligible_now,-item.priority,item.need_id)))


__all__=["AcquisitionRouteState","EvidenceAcquisitionNeed","EvidenceAcquisitionQueueItem","build_evidence_acquisition_queue"]
