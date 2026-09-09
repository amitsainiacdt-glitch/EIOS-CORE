"""Fingerprint-bound assembly result for the causal-first EIP path."""

from dataclasses import dataclass
from enum import Enum


class CausalFirstEIPPacketDecision(str, Enum):
    READY_FOR_GOVERNED_EIP_CLASSIFICATION = "READY_FOR_GOVERNED_EIP_CLASSIFICATION"
    HOLD_FOR_RESEARCH = "HOLD_FOR_RESEARCH"
    VETO_TOO_LATE = "VETO_TOO_LATE"
    VETO_SURVIVABILITY_FAILURE = "VETO_SURVIVABILITY_FAILURE"


@dataclass(frozen=True)
class CausalFirstEIPDecisionPacket:
    schema_version: int
    packet_id: str
    meta_assessment_id: str
    causal_chain_id: str
    regime_assessment_id: str
    recognition_assessment_id: str
    expectation_gap_assessment_id: str
    normalized_valuation_assessment_id: str
    survivability_assessment_id: str
    component_fingerprints: tuple[tuple[str, str], ...]
    decision: CausalFirstEIPPacketDecision
    reason_codes: tuple[str, ...]
    all_components_ready: bool
    creates_eip: bool
    non_authority_statement: str


__all__ = ["CausalFirstEIPDecisionPacket", "CausalFirstEIPPacketDecision"]
