"""Validates a complete causal chain without inferring, scoring, or promoting it."""

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry


class CausalChainService:
    NON_AUTHORITY = "Research-stage causal chain; not a Signal, Catalyst, EIP, recommendation, position, or trade instruction."
    REQUIRED_STAGES = tuple(CausalChainStage)

    def __init__(self, indicator_registry):
        if not isinstance(indicator_registry, SectorCausalIndicatorRegistry):
            raise ValueError("indicator_registry must be SectorCausalIndicatorRegistry")
        self.indicator_registry = indicator_registry

    def validate(self, assessment):
        if not isinstance(assessment, CausalChainAssessment):
            raise ValueError("assessment must be CausalChainAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported causal-chain schema")
        self._text(assessment.chain_id, "chain_id")
        self._text(assessment.entity, "entity")
        self._text(assessment.sector_id, "sector_id")
        self._text(assessment.uncertainty_statement, "uncertainty_statement")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("causal chain requires the canonical non-authority statement")
        if not assessment.public_information_only:
            raise ValueError("causal chain accepts public information only")

        evidence_ids = self._unique_texts(assessment.input_temporal_evidence_ids, "input_temporal_evidence_ids")
        indicator_ids = self._unique_texts(assessment.causal_indicator_ids, "causal_indicator_ids")
        sector = assessment.sector_id.casefold()
        for indicator_id in indicator_ids:
            definition = self.indicator_registry.get(indicator_id)
            if sector not in {value.casefold() for value in definition.sector_ids}:
                raise ValueError("causal indicator is outside chain sector scope")

        if tuple(link.stage for link in assessment.links) != self.REQUIRED_STAGES:
            raise ValueError("causal chain must contain each required stage exactly once and in order")
        used_evidence = set()
        for link in assessment.links:
            if not isinstance(link, CausalChainLink):
                raise ValueError("links must contain CausalChainLink values")
            self._text(link.statement, "link statement")
            self._text(link.mechanism, "link mechanism")
            linked = self._unique_texts(link.temporal_evidence_ids, "link temporal_evidence_ids", allow_empty=True)
            if not set(linked).issubset(set(evidence_ids)):
                raise ValueError("causal-chain link cites evidence outside the governed inputs")
            used_evidence.update(linked)
        if used_evidence != set(evidence_ids):
            raise ValueError("every governed evidence input must be used by the causal chain")

        if (not isinstance(assessment.expected_lead_time_quarters, tuple)
                or len(assessment.expected_lead_time_quarters) != 2):
            raise ValueError("expected_lead_time_quarters must contain minimum and maximum")
        lead_min, lead_max = assessment.expected_lead_time_quarters
        if isinstance(lead_min, bool) or isinstance(lead_max, bool) or not isinstance(lead_min, int) or not isinstance(lead_max, int):
            raise ValueError("causal-chain lead time must use whole quarters")
        if lead_min < 0 or lead_max < lead_min:
            raise ValueError("causal-chain lead-time range is invalid")
        self._unique_texts(assessment.assumptions, "assumptions")
        return assessment

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _unique_texts(cls, values, name, *, allow_empty=False):
        if not isinstance(values, tuple):
            raise ValueError(f"{name} must be a tuple")
        normalized = tuple(cls._text(value, name) for value in values)
        if not allow_empty and not normalized:
            raise ValueError(f"{name} must not be empty")
        if len(set(normalized)) != len(normalized):
            raise ValueError(f"{name} must not contain duplicates")
        return normalized


__all__ = ["CausalChainService"]
