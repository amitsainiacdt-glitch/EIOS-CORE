"""Builds a Pre-Inflection preview only after authorized mandatory Meta."""

from modules.external_intelligence.mandatory_meta_analysis import MetaAnalysisConclusion, MetaContradictionBurden
from modules.external_intelligence.mandatory_meta_analysis_gate import MandatoryMetaAnalysisGate, MandatoryMetaGateDecision
from modules.external_intelligence.mandatory_meta_analysis_repository import MandatoryMetaAnalysisRepository, StoredMandatoryMetaAnalysis
from modules.external_intelligence.mandatory_meta_review import MandatoryMetaReviewDecision, MandatoryMetaReviewReceipt
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview, PreInflectionStrength
from modules.external_intelligence.temporal_leading_indicator_preview import TemporalIndicatorStructuralState, TemporalLeadingIndicatorPreview


class PreInflectionAssessmentService:
    NON_AUTHORITY = "Research-stage Pre-Inflection preview; not a Signal, EIP state, Opportunity, recommendation, or trade decision."

    def __init__(self, meta_gate):
        if not isinstance(meta_gate, MandatoryMetaAnalysisGate): raise ValueError("meta_gate must be MandatoryMetaAnalysisGate")
        self.meta_gate = meta_gate

    def preview(
        self, *, preview_id, stored_meta, meta_review, temporal_evidence, indicator_previews,
        what_is_changing, why_now, confirmation_requirements, invalidation_conditions,
        balance_sheet_governance_risks,
    ):
        if not isinstance(stored_meta, StoredMandatoryMetaAnalysis): raise ValueError("stored_meta must be StoredMandatoryMetaAnalysis")
        if not isinstance(meta_review, MandatoryMetaReviewReceipt): raise ValueError("meta_review must be MandatoryMetaReviewReceipt")
        expected_fingerprint = MandatoryMetaAnalysisRepository.fingerprint_payload(MandatoryMetaAnalysisRepository.assessment_payload(stored_meta.assessment))
        if stored_meta.assessment_fingerprint != expected_fingerprint: raise ValueError("stored Meta fingerprint mismatch")
        if meta_review.assessment_id != stored_meta.assessment.assessment_id or meta_review.assessment_fingerprint != stored_meta.assessment_fingerprint: raise ValueError("Meta review does not bind to stored assessment")
        if meta_review.decision != MandatoryMetaReviewDecision.AUTHORIZE_PRE_INFLECTION_REVIEW: raise ValueError("Pre-Inflection preview requires authorized Meta review")
        previews = tuple(indicator_previews)
        if not previews or not all(isinstance(item, TemporalLeadingIndicatorPreview) for item in previews): raise ValueError("indicator_previews must not be empty")
        current_gate = self.meta_gate.evaluate(temporal_evidence=temporal_evidence, assessment=stored_meta.assessment, indicator_previews=previews)
        if current_gate.decision != MandatoryMetaGateDecision.READY_FOR_PRE_INFLECTION: raise ValueError("Meta is no longer ready for Pre-Inflection review")
        assessment = stored_meta.assessment
        all_ready = all(item.structural_state == TemporalIndicatorStructuralState.STRUCTURALLY_READY_FOR_META for item in previews)
        lead_min = min(item.expected_lead_time_quarters[0] for item in previews)
        lead_max = max(item.expected_lead_time_quarters[1] for item in previews)
        strength = self._strength(assessment, all_ready)
        return PreInflectionAssessmentPreview(
            1, self._text(preview_id, "preview_id"), assessment.assessment_id, stored_meta.assessment_fingerprint,
            meta_review.review_id, assessment.entity_scope, assessment.sector_scope, assessment.causal_indicator_ids,
            strength, len(set(assessment.independence_group_ids)), all_ready, (lead_min, lead_max),
            assessment.contradiction_burden.value, assessment.contradictions, assessment.missing_expected_evidence,
            assessment.coverage_gaps, assessment.research_gaps, assessment.uncertainty_statement,
            self._text(what_is_changing, "what_is_changing"), self._text(why_now, "why_now"),
            self._texts(confirmation_requirements, "confirmation_requirements"),
            self._texts(invalidation_conditions, "invalidation_conditions"),
            self._texts(balance_sheet_governance_risks, "balance_sheet_governance_risks"),
            "NOT_ASSESSED", True, self.NON_AUTHORITY,
        )

    @staticmethod
    def _strength(assessment, all_ready):
        if assessment.conclusion == MetaAnalysisConclusion.EMERGING: return PreInflectionStrength.EMERGING
        if assessment.conclusion != MetaAnalysisConclusion.COHERENT or not all_ready: return PreInflectionStrength.WEAK
        if assessment.contradiction_burden in (MetaContradictionBurden.NONE, MetaContradictionBurden.LOW) and not assessment.missing_expected_evidence and not assessment.coverage_gaps:
            return PreInflectionStrength.STRONG
        return PreInflectionStrength.CREDIBLE

    @staticmethod
    def _text(value, name):
        if not isinstance(value, str) or not value.strip(): raise ValueError(f"{name} must not be empty")
        return value.strip()
    @classmethod
    def _texts(cls, values, name):
        if not isinstance(values, (list, tuple)): raise ValueError(f"{name} must be a list")
        result = tuple(cls._text(value, name) for value in values)
        if not result: raise ValueError(f"{name} must not be empty")
        return result


__all__ = ["PreInflectionAssessmentService"]
