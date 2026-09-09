"""Passive post-EIP confirmation and thesis-lifecycle contracts."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PostEIPConfirmationType(str, Enum):
    OPERATING_RESULT = "OPERATING_RESULT"
    FINANCIAL_RESULT = "FINANCIAL_RESULT"
    MANAGEMENT_GUIDANCE = "MANAGEMENT_GUIDANCE"
    ANALYST_REVISION = "ANALYST_REVISION"
    CONSENSUS_REVISION = "CONSENSUS_REVISION"
    PRICE_REACTION = "PRICE_REACTION"
    CAUSAL_LEADING_INDICATOR = "CAUSAL_LEADING_INDICATOR"


class PostEIPRelationship(str, Enum):
    CONFIRMS = "CONFIRMS"
    CONTRADICTS = "CONTRADICTS"
    CONTEXT_ONLY = "CONTEXT_ONLY"


class PostEIPLifecycleAction(str, Enum):
    WAIT_FOR_CONFIRMATION = "WAIT_FOR_CONFIRMATION"
    SCALE_REVIEW = "SCALE_REVIEW"
    HOLD = "HOLD"
    KILL_THESIS_REVIEW = "KILL_THESIS_REVIEW"


@dataclass(frozen=True)
class PostEIPEvidence:
    evidence_id: str
    confirmation_type: PostEIPConfirmationType
    relationship: PostEIPRelationship
    observed_at: datetime
    source_ids: tuple[str, ...]
    independence_group_id: str
    explanation: str
    triggered_kill_test: str | None = None


@dataclass(frozen=True)
class PostEIPLifecycleAssessment:
    schema_version: int
    assessment_id: str
    reader_packet_fingerprint: str
    eip_identified_at: datetime
    evidence: tuple[PostEIPEvidence, ...]
    unresolved_uncertainties: tuple[str, ...]
    monitoring_requirements: tuple[str, ...]
    public_information_only: bool
    non_authority_statement: str


@dataclass(frozen=True)
class PostEIPLifecycleResult:
    assessment_id: str
    action: PostEIPLifecycleAction
    confirming_evidence_ids: tuple[str, ...]
    contradicting_evidence_ids: tuple[str, ...]
    independent_confirmation_groups: tuple[str, ...]
    triggered_kill_tests: tuple[str, ...]
    reason_codes: tuple[str, ...]
    changes_original_eip_date: bool
    authorizes_portfolio_action: bool
    non_authority_statement: str


__all__ = [
    "PostEIPConfirmationType", "PostEIPEvidence", "PostEIPLifecycleAction",
    "PostEIPLifecycleAssessment", "PostEIPLifecycleResult", "PostEIPRelationship",
]
