"""Passive governed Pre-Inflection preview; never an investment decision."""

from dataclasses import dataclass
from enum import Enum


class PreInflectionStrength(str, Enum):
    WEAK = "WEAK"
    EMERGING = "EMERGING"
    CREDIBLE = "CREDIBLE"
    STRONG = "STRONG"


@dataclass(frozen=True)
class PreInflectionAssessmentPreview:
    schema_version: int
    preview_id: str
    meta_assessment_id: str
    meta_assessment_fingerprint: str
    meta_review_id: str
    entity_scope: tuple[str, ...]
    sector_scope: tuple[str, ...]
    causal_indicator_ids: tuple[str, ...]
    strength: PreInflectionStrength
    independent_support_count: int
    all_indicators_structurally_ready: bool
    expected_lead_time_quarters: tuple[int, int]
    contradiction_burden: str
    contradictions: tuple[str, ...]
    missing_expected_evidence: tuple[str, ...]
    coverage_gaps: tuple[str, ...]
    research_gaps: tuple[str, ...]
    uncertainty_statement: str
    what_is_changing: str
    why_now: str
    confirmation_requirements: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    balance_sheet_governance_risks: tuple[str, ...]
    market_recognition_status: str
    eligible_for_human_pre_inflection_review: bool
    non_authority_statement: str


__all__ = ["PreInflectionAssessmentPreview", "PreInflectionStrength"]
