"""Passive contract for mandatory read-only Meta-Analysis."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MetaAnalysisConclusion(str, Enum):
    INSUFFICIENT = "INSUFFICIENT"
    EMERGING = "EMERGING"
    COHERENT = "COHERENT"
    CONTRADICTED = "CONTRADICTED"


class MetaContradictionBurden(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"


class MetaKillTestStatus(str, Enum):
    NOT_TRIGGERED = "NOT_TRIGGERED"
    TRIGGERED = "TRIGGERED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class MetaKillTestResult:
    indicator_id: str
    kill_test: str
    status: MetaKillTestStatus
    evidence_ids: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class MandatoryMetaAnalysisAssessment:
    schema_version: int
    assessment_id: str
    entity_scope: tuple[str, ...]
    sector_scope: tuple[str, ...]
    input_temporal_evidence_ids: tuple[str, ...]
    input_observation_fingerprints: tuple[str, ...]
    input_indicator_preview_fingerprints: tuple[str, ...]
    causal_indicator_ids: tuple[str, ...]
    causal_hypotheses: tuple[str, ...]
    independence_group_ids: tuple[str, ...]
    contradictions: tuple[str, ...]
    missing_expected_evidence: tuple[str, ...]
    coverage_gaps: tuple[str, ...]
    syndication_findings: tuple[str, ...]
    cross_scope_transmissions: tuple[str, ...]
    research_gaps: tuple[str, ...]
    kill_test_results: tuple[MetaKillTestResult, ...]
    conclusion: MetaAnalysisConclusion
    contradiction_burden: MetaContradictionBurden
    independence_checked: bool
    contradictions_checked: bool
    missing_evidence_checked: bool
    coverage_checked: bool
    kill_tests_checked: bool
    public_information_only: bool
    uncertainty_statement: str
    non_authority_statement: str
    assessed_at: datetime
    assessor: str


__all__ = ["MandatoryMetaAnalysisAssessment", "MetaAnalysisConclusion", "MetaContradictionBurden", "MetaKillTestResult", "MetaKillTestStatus"]
