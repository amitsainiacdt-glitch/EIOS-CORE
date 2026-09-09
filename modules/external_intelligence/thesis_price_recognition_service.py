"""Hard recognition veto bound to the same causal thesis; no EIP decision."""

from modules.external_intelligence.causal_chain import CausalChainAssessment
from modules.external_intelligence.change_regime import ChangeRegimeAssessment
from modules.external_intelligence.price_recognition import PriceRecognitionPreview, PriceRecognitionState
from modules.external_intelligence.thesis_price_recognition import (
    FundamentalChangeIncorporation, ThesisPriceRecognitionAssessment,
    ThesisPriceRecognitionGateResult, ThesisRecognitionDecision,
)


class ThesisPriceRecognitionService:
    NON_AUTHORITY = "Thesis-specific recognition review; not an EIP, recommendation, position, or trade instruction."
    RECOGNITION_DIMENSIONS = frozenset({
        "CATALYST_PRICE_REACTION", "RELATIVE_PERFORMANCE", "VALUATION_RERATING",
        "ABNORMAL_VOLUME", "ANALYST_REVISIONS", "CONSENSUS_REVISIONS",
        "INSTITUTIONAL_ATTENTION", "MEDIA_NARRATIVE", "MANAGEMENT_NARRATIVE",
    })

    def evaluate(self, *, causal_chain, regime_assessment, market_recognition, assessment):
        if not isinstance(causal_chain, CausalChainAssessment):
            raise ValueError("causal_chain must be CausalChainAssessment")
        if not isinstance(regime_assessment, ChangeRegimeAssessment):
            raise ValueError("regime_assessment must be ChangeRegimeAssessment")
        if not isinstance(market_recognition, PriceRecognitionPreview):
            raise ValueError("market_recognition must be PriceRecognitionPreview")
        if not isinstance(assessment, ThesisPriceRecognitionAssessment):
            raise ValueError("assessment must be ThesisPriceRecognitionAssessment")
        if assessment.schema_version != 1:
            raise ValueError("unsupported thesis-recognition schema")
        self._text(assessment.assessment_id, "assessment_id")
        if assessment.causal_chain_id != causal_chain.chain_id:
            raise ValueError("recognition assessment does not bind to causal chain")
        if assessment.regime_assessment_id != regime_assessment.assessment_id or regime_assessment.causal_chain_id != causal_chain.chain_id:
            raise ValueError("recognition assessment does not bind to regime assessment")
        if assessment.market_snapshot_id != market_recognition.snapshot_id:
            raise ValueError("recognition assessment does not bind to market snapshot")
        if not isinstance(assessment.incorporation, FundamentalChangeIncorporation):
            raise ValueError("fundamental-change incorporation is invalid")
        if not assessment.public_information_only:
            raise ValueError("thesis recognition accepts public information only")
        if assessment.non_authority_statement != self.NON_AUTHORITY:
            raise ValueError("thesis recognition requires the canonical non-authority statement")
        self._text(assessment.evidence_rationale, "evidence_rationale")
        self._text(assessment.uncertainty_statement, "uncertainty_statement")
        sources = self._unique_texts(assessment.thesis_related_source_ids, "thesis_related_source_ids", allow_empty=True)
        dimensions = self._unique_texts(assessment.thesis_related_dimensions, "thesis_related_dimensions", allow_empty=True)
        if not set(dimensions).issubset(self.RECOGNITION_DIMENSIONS):
            raise ValueError("unknown thesis-recognition dimension")
        if assessment.incorporation != FundamentalChangeIncorporation.INSUFFICIENT_EVIDENCE and (not sources or not dimensions):
            raise ValueError("a recognition conclusion requires thesis-related sources and dimensions")

        reasons = []
        insufficient = (
            market_recognition.state == PriceRecognitionState.INSUFFICIENT_DATA
            or assessment.incorporation == FundamentalChangeIncorporation.INSUFFICIENT_EVIDENCE
        )
        fully_recognized = (
            market_recognition.state == PriceRecognitionState.FULLY_RECOGNIZED_POTENTIALLY_LATE
            or assessment.incorporation == FundamentalChangeIncorporation.MOST_OR_ALL
        )
        if fully_recognized:
            decision = ThesisRecognitionDecision.VETO_TOO_LATE
            reasons.append("SAME_FUNDAMENTAL_CHANGE_MOSTLY_OR_FULLY_RECOGNIZED")
        elif insufficient:
            decision = ThesisRecognitionDecision.HOLD_INSUFFICIENT_EVIDENCE
            reasons.append("THESIS_RECOGNITION_EVIDENCE_INSUFFICIENT")
        else:
            decision = ThesisRecognitionDecision.ALLOW_EIP_REVIEW
            if assessment.incorporation == FundamentalChangeIncorporation.MATERIAL:
                reasons.append("MATERIAL_RECOGNITION_REMAINS_FOR_HUMAN_ASYMMETRY_REVIEW")
        return ThesisPriceRecognitionGateResult(
            decision, assessment.incorporation, tuple(reasons), assessment.assessment_id,
            decision == ThesisRecognitionDecision.VETO_TOO_LATE, self.NON_AUTHORITY,
        )

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()

    @classmethod
    def _unique_texts(cls, values, name, *, allow_empty=False):
        if not isinstance(values, tuple):
            raise ValueError(f"{name} must be a tuple")
        result = tuple(cls._text(value, name) for value in values)
        if not allow_empty and not result:
            raise ValueError(f"{name} must not be empty")
        if len(set(result)) != len(result):
            raise ValueError(f"{name} must not contain duplicates")
        return result


__all__ = ["ThesisPriceRecognitionService"]
