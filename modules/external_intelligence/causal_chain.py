"""Passive five-link causal-chain contract for governed Pre-Inflection research."""

from dataclasses import dataclass
from enum import Enum


class CausalChainStage(str, Enum):
    ROOT_CAUSE_CHANGE = "ROOT_CAUSE_CHANGE"
    INTERMEDIATE_TRANSMISSION = "INTERMEDIATE_TRANSMISSION"
    COMPANY_OPERATING_EFFECT = "COMPANY_OPERATING_EFFECT"
    FINANCIAL_EFFECT = "FINANCIAL_EFFECT"
    EXPECTED_MARKET_EFFECT = "EXPECTED_MARKET_EFFECT"


@dataclass(frozen=True)
class CausalChainLink:
    stage: CausalChainStage
    statement: str
    mechanism: str
    temporal_evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class CausalChainAssessment:
    schema_version: int
    chain_id: str
    entity: str
    sector_id: str
    causal_indicator_ids: tuple[str, ...]
    input_temporal_evidence_ids: tuple[str, ...]
    links: tuple[CausalChainLink, ...]
    expected_lead_time_quarters: tuple[int, int]
    assumptions: tuple[str, ...]
    uncertainty_statement: str
    public_information_only: bool
    non_authority_statement: str


__all__ = ["CausalChainAssessment", "CausalChainLink", "CausalChainStage"]
