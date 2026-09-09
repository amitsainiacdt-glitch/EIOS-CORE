"""Fail-closed validation for explainable, non-probabilistic regime labels."""

from modules.external_intelligence.causal_chain import CausalChainAssessment
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.change_regime import ChangeRegime, ChangeRegimeAssessment, RegimeConfidence


class ChangeRegimeService:
    NON_AUTHORITY = "Research-stage regime classification; not a probability, Signal, Catalyst, EIP, recommendation, position, or trade instruction."

    def __init__(self, causal_chain_service):
        if not isinstance(causal_chain_service, CausalChainService):
            raise ValueError("causal_chain_service must be CausalChainService")
        self.causal_chain_service = causal_chain_service

    def validate(self, *, causal_chain, assessment):
        if not isinstance(causal_chain, CausalChainAssessment):
            raise ValueError("causal_chain must be CausalChainAssessment")
        self.causal_chain_service.validate(causal_chain)
        if not isinstance(assessment, ChangeRegimeAssessment):
            raise ValueError("assessment must be ChangeRegimeAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported change-regime schema")
        self._text(assessment.assessment_id, "assessment_id")
        if assessment.causal_chain_id != causal_chain.chain_id:
            raise ValueError("regime assessment does not bind to causal chain")
        if not isinstance(assessment.regime, ChangeRegime):
            raise ValueError("regime is invalid")
        if not isinstance(assessment.confidence, RegimeConfidence):
            raise ValueError("regime confidence is invalid")
        if not assessment.public_information_only:
            raise ValueError("regime assessment accepts public information only")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("regime assessment requires the canonical non-authority statement")
        evidence = self._unique_texts(assessment.input_temporal_evidence_ids, "input_temporal_evidence_ids")
        if set(evidence) != set(causal_chain.input_temporal_evidence_ids):
            raise ValueError("regime evidence does not exactly bind to causal-chain evidence")
        self._unique_texts(assessment.classification_basis, "classification_basis")
        self._unique_texts(assessment.alternative_explanations, "alternative_explanations")
        self._unique_texts(assessment.distinguishing_tests, "distinguishing_tests")
        self._text(assessment.uncertainty_statement, "uncertainty_statement")
        if assessment.regime in (ChangeRegime.STATISTICAL_NOISE, ChangeRegime.SPECULATIVE_NARRATIVE) and assessment.confidence == RegimeConfidence.HIGH:
            raise ValueError("noise or narrative cannot carry high causal confidence")
        return assessment

    def may_enter_meta_review(self, *, causal_chain, assessment):
        self.validate(causal_chain=causal_chain, assessment=assessment)
        return assessment.regime not in (ChangeRegime.STATISTICAL_NOISE, ChangeRegime.SPECULATIVE_NARRATIVE)

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _unique_texts(cls, values, name):
        if not isinstance(values, tuple) or not values:
            raise ValueError(f"{name} must be a non-empty tuple")
        result = tuple(cls._text(value, name) for value in values)
        if len(set(result)) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result


__all__ = ["ChangeRegimeService"]
