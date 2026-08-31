"""Only readiness-qualified cases may create frozen research hypotheses."""

from enum import Enum

from modules.external_intelligence.evidence_confidence_ceiling import EvidenceConfidenceCeiling
from modules.external_intelligence.mandatory_meta_review import MandatoryMetaReviewDecision,MandatoryMetaReviewReceipt
from modules.external_intelligence.pre_inflection_assessment import PreInflectionAssessmentPreview
from modules.external_intelligence.pre_inflection_case_readiness import PreInflectionCaseReadiness
from modules.external_intelligence.pre_inflection_hypothesis_evaluation import FrozenPreInflectionHypothesis,HypothesisDirection


class HypothesisScope(str,Enum):
    SECTOR="SECTOR"
    COMPANY="COMPANY"


class PreInflectionHypothesisFreezingService:
    def freeze(self,*,readiness,confidence_ceiling,pre_inflection_preview,meta_review,scope,hypothesis_id,case_id,metric_id,geography_id,direction,threshold_value,baseline_value,target_date,frozen_at,confidence_percent,evidence_fingerprints):
        if not isinstance(readiness,PreInflectionCaseReadiness): raise ValueError("case readiness assessment is required")
        if not isinstance(confidence_ceiling,EvidenceConfidenceCeiling): raise ValueError("evidence confidence ceiling is required")
        if not isinstance(pre_inflection_preview,PreInflectionAssessmentPreview) or not isinstance(meta_review,MandatoryMetaReviewReceipt): raise ValueError("governed Pre-Inflection preview and Meta review are required")
        if not pre_inflection_preview.eligible_for_human_pre_inflection_review: raise ValueError("Pre-Inflection preview is not review-eligible")
        if meta_review.decision!=MandatoryMetaReviewDecision.AUTHORIZE_PRE_INFLECTION_REVIEW: raise ValueError("Meta review did not authorize Pre-Inflection review")
        if pre_inflection_preview.meta_review_id!=meta_review.review_id or pre_inflection_preview.meta_assessment_id!=meta_review.assessment_id or pre_inflection_preview.meta_assessment_fingerprint!=meta_review.assessment_fingerprint: raise ValueError("Pre-Inflection preview does not bind to authorized Meta review")
        scope=scope if isinstance(scope,HypothesisScope) else HypothesisScope(scope)
        if scope==HypothesisScope.SECTOR and not readiness.sector_transmission_ready: raise ValueError("sector hypothesis requires sector-transmission readiness")
        if scope==HypothesisScope.COMPANY and not readiness.company_case_ready: raise ValueError("company hypothesis requires company-case readiness")
        if scope==HypothesisScope.COMPANY and not pre_inflection_preview.entity_scope: raise ValueError("company hypothesis requires reviewed entity scope")
        if scope==HypothesisScope.SECTOR and not pre_inflection_preview.sector_scope: raise ValueError("sector hypothesis requires reviewed sector scope")
        if not confidence_ceiling.confidence_eligible: raise ValueError("evidence confidence is not eligible for hypothesis freezing")
        if isinstance(confidence_percent,bool) or not isinstance(confidence_percent,(int,float)) or not 0<confidence_percent<100: raise ValueError("confidence must be between zero and one hundred")
        if confidence_percent>confidence_ceiling.maximum_confidence_percent: raise ValueError("proposed confidence exceeds evidence ceiling")
        if frozen_at.tzinfo is None or target_date.tzinfo is None or frozen_at>=target_date: raise ValueError("hypothesis must be frozen before a timezone-aware target")
        if not evidence_fingerprints: raise ValueError("evidence fingerprints are required")
        values=dict(hypothesis_id=hypothesis_id,case_id=case_id,metric_id=metric_id,geography_id=geography_id,direction=direction if isinstance(direction,HypothesisDirection) else HypothesisDirection(direction),threshold_value=float(threshold_value),baseline_value=None if baseline_value is None else float(baseline_value),target_date=target_date,frozen_at=frozen_at,confidence_percent=float(confidence_percent),evidence_fingerprints=tuple(evidence_fingerprints))
        fingerprint=FrozenPreInflectionHypothesis.fingerprint(**values)
        return FrozenPreInflectionHypothesis(**values,hypothesis_fingerprint=fingerprint,non_authority_statement="Frozen research hypothesis only; not a Signal, Opportunity, recommendation, position, or trade.")


__all__=["HypothesisScope","PreInflectionHypothesisFreezingService"]
