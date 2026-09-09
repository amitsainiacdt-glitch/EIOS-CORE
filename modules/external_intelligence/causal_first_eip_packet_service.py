"""Assembles existing governed outputs without blending them into one score."""

import dataclasses
import hashlib
import json
from datetime import datetime
from enum import Enum

from modules.external_intelligence.causal_chain import CausalChainAssessment
from modules.external_intelligence.causal_first_eip_packet import CausalFirstEIPDecisionPacket, CausalFirstEIPPacketDecision
from modules.external_intelligence.change_regime import ChangeRegime, ChangeRegimeAssessment
from modules.external_intelligence.eip_expectation_gap import EIPExpectationGapAssessment, EIPExpectationGapResult
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaGateDecision, MandatoryMetaGateResult
from modules.external_intelligence.normalized_valuation import NormalizedValuationAssessment, NormalizedValuationResult, NormalizedValuationRoom
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview
from modules.external_intelligence.survivability import SurvivabilityAssessment, SurvivabilityDecision, SurvivabilityGateResult
from modules.external_intelligence.thesis_price_recognition import ThesisPriceRecognitionAssessment, ThesisPriceRecognitionGateResult, ThesisRecognitionDecision


class CausalFirstEIPPacketService:
    NON_AUTHORITY = "Governed EIP input packet only; not an EIP classification, recommendation, position, or trade instruction."

    def assemble(
        self, *, packet_id, meta_gate, pre_inflection, causal_chain, regime_assessment,
        recognition_assessment, recognition_gate, expectation_gap_assessment,
        expectation_gap, normalized_valuation_assessment, normalized_valuation,
        survivability_assessment, survivability,
    ):
        self._text(packet_id, "packet_id")
        self._type(meta_gate, MandatoryMetaGateResult, "meta_gate")
        self._type(pre_inflection, PreInflectionAssessmentPreview, "pre_inflection")
        self._type(causal_chain, CausalChainAssessment, "causal_chain")
        self._type(regime_assessment, ChangeRegimeAssessment, "regime_assessment")
        self._type(recognition_assessment, ThesisPriceRecognitionAssessment, "recognition_assessment")
        self._type(recognition_gate, ThesisPriceRecognitionGateResult, "recognition_gate")
        self._type(expectation_gap_assessment, EIPExpectationGapAssessment, "expectation_gap_assessment")
        self._type(expectation_gap, EIPExpectationGapResult, "expectation_gap")
        self._type(normalized_valuation_assessment, NormalizedValuationAssessment, "normalized_valuation_assessment")
        self._type(normalized_valuation, NormalizedValuationResult, "normalized_valuation")
        self._type(survivability_assessment, SurvivabilityAssessment, "survivability_assessment")
        self._type(survivability, SurvivabilityGateResult, "survivability")
        if not meta_gate.assessment_id:
            raise ValueError("Mandatory Meta assessment identity is required")
        if pre_inflection.meta_assessment_id != meta_gate.assessment_id:
            raise ValueError("Pre-Inflection preview does not bind to Mandatory Meta")
        if causal_chain.entity.casefold() not in {item.casefold() for item in pre_inflection.entity_scope}:
            raise ValueError("causal-chain entity is outside Pre-Inflection scope")
        if causal_chain.sector_id.casefold() not in {item.casefold() for item in pre_inflection.sector_scope}:
            raise ValueError("causal-chain sector is outside Pre-Inflection scope")
        if set(causal_chain.causal_indicator_ids) != set(pre_inflection.causal_indicator_ids):
            raise ValueError("causal-chain indicators do not bind to Pre-Inflection preview")
        if set(meta_gate.expected_temporal_evidence_ids) != set(causal_chain.input_temporal_evidence_ids):
            raise ValueError("causal chain does not bind to Mandatory Meta evidence")
        bindings = (
            (regime_assessment.causal_chain_id, causal_chain.chain_id, "regime/causal chain"),
            (recognition_assessment.causal_chain_id, causal_chain.chain_id, "recognition/causal chain"),
            (recognition_assessment.regime_assessment_id, regime_assessment.assessment_id, "recognition/regime"),
            (recognition_gate.assessment_id, recognition_assessment.assessment_id, "recognition result"),
            (expectation_gap_assessment.causal_chain_id, causal_chain.chain_id, "gap/causal chain"),
            (expectation_gap_assessment.regime_assessment_id, regime_assessment.assessment_id, "gap/regime"),
            (expectation_gap_assessment.thesis_recognition_assessment_id, recognition_assessment.assessment_id, "gap/recognition"),
            (expectation_gap.assessment_id, expectation_gap_assessment.assessment_id, "gap result"),
            (normalized_valuation_assessment.expectation_gap_assessment_id, expectation_gap_assessment.assessment_id, "valuation/gap"),
            (normalized_valuation.assessment_id, normalized_valuation_assessment.assessment_id, "valuation result"),
            (survivability_assessment.causal_chain_id, causal_chain.chain_id, "survivability/causal chain"),
            (survivability_assessment.normalized_valuation_assessment_id, normalized_valuation_assessment.assessment_id, "survivability/valuation"),
            (survivability.assessment_id, survivability_assessment.assessment_id, "survivability result"),
        )
        for actual, expected, name in bindings:
            if actual != expected:
                raise ValueError(f"stale or mismatched {name} binding")

        reasons = []
        if survivability.hard_veto or survivability.decision == SurvivabilityDecision.VETO_SURVIVABILITY_FAILURE:
            decision = CausalFirstEIPPacketDecision.VETO_SURVIVABILITY_FAILURE
            reasons.append("SURVIVABILITY_HARD_VETO")
        elif recognition_gate.hard_veto or recognition_gate.decision == ThesisRecognitionDecision.VETO_TOO_LATE:
            decision = CausalFirstEIPPacketDecision.VETO_TOO_LATE
            reasons.append("PRICE_RECOGNITION_HARD_VETO")
        else:
            if meta_gate.decision != MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION:
                reasons.append("MANDATORY_META_NOT_READY")
            if regime_assessment.regime in (ChangeRegime.STATISTICAL_NOISE, ChangeRegime.SPECULATIVE_NARRATIVE):
                reasons.append("CHANGE_REGIME_NOT_EIP_ELIGIBLE")
            if recognition_gate.decision != ThesisRecognitionDecision.ALLOW_EIP_REVIEW:
                reasons.append("PRICE_RECOGNITION_NOT_READY")
            if not expectation_gap.eligible_for_eip_assembly:
                reasons.append("EXPECTATION_GAP_NOT_READY")
            if normalized_valuation.valuation_room != NormalizedValuationRoom.SUFFICIENT or not normalized_valuation.eligible_for_eip_assembly:
                reasons.append("NORMALIZED_VALUATION_NOT_READY")
            if survivability.decision not in (SurvivabilityDecision.CLEAR, SurvivabilityDecision.CONTAINED) or not survivability.eligible_for_eip_assembly:
                reasons.append("SURVIVABILITY_NOT_READY")
            decision = (CausalFirstEIPPacketDecision.HOLD_FOR_RESEARCH if reasons else
                        CausalFirstEIPPacketDecision.READY_FOR_GOVERNED_EIP_CLASSIFICATION)

        components = (
            ("mandatory_meta_gate", meta_gate), ("pre_inflection", pre_inflection), ("causal_chain", causal_chain),
            ("change_regime", regime_assessment), ("thesis_recognition_assessment", recognition_assessment),
            ("thesis_recognition_gate", recognition_gate), ("expectation_gap_assessment", expectation_gap_assessment),
            ("expectation_gap_result", expectation_gap), ("normalized_valuation_assessment", normalized_valuation_assessment),
            ("normalized_valuation_result", normalized_valuation), ("survivability_assessment", survivability_assessment),
            ("survivability_result", survivability),
        )
        fingerprints = tuple((name, self.fingerprint(value)) for name, value in components)
        ready = decision == CausalFirstEIPPacketDecision.READY_FOR_GOVERNED_EIP_CLASSIFICATION
        return CausalFirstEIPDecisionPacket(
            1, packet_id.strip(), meta_gate.assessment_id, pre_inflection.preview_id, causal_chain.chain_id, regime_assessment.assessment_id,
            recognition_assessment.assessment_id, expectation_gap_assessment.assessment_id,
            normalized_valuation_assessment.assessment_id, survivability_assessment.assessment_id,
            fingerprints, decision, tuple(reasons), ready, False, self.NON_AUTHORITY,
        )

    @classmethod
    def fingerprint(cls, value):
        payload = cls._canonical(value)
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

    @classmethod
    def _canonical(cls, value):
        if dataclasses.is_dataclass(value):
            return {field.name: cls._canonical(getattr(value, field.name)) for field in dataclasses.fields(value)}
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, datetime):
            if value.tzinfo is None:
                raise ValueError("fingerprinted datetime must be timezone-aware")
            return value.isoformat()
        if isinstance(value, tuple):
            return [cls._canonical(item) for item in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        raise ValueError(f"unsupported fingerprint value: {type(value).__name__}")

    @staticmethod
    def _type(value, expected, name):
        if not isinstance(value, expected):
            raise ValueError(f"{name} must be {expected.__name__}")

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must not be empty")
        return value.strip()


__all__ = ["CausalFirstEIPPacketService"]
