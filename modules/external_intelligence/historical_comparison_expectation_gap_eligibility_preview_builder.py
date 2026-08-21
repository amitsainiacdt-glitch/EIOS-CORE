"""Verify a governed Catalyst before any Expectation Gap analysis."""
from __future__ import annotations
import hashlib,json
from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_catalyst_creation_receipt import HistoricalComparisonCatalystCreationReceipt
from modules.external_intelligence.historical_comparison_expectation_gap_eligibility_preview import HistoricalComparisonExpectationGapEligibilityPreview
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_decision import HistoricalComparisonPromotedCatalystAssessmentDecision,HistoricalComparisonPromotedCatalystAssessmentDisposition
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.opportunity.catalyst_engine import CatalystEngine

class HistoricalComparisonExpectationGapEligibilityPreviewBuilder:
 REQUIRED_INPUTS=("gap_id","company","sector","market_expectation","eios_expectation","market_earnings_expectation","eios_earnings_expectation")
 def build(self,inputs,reviews,assessment,creation,*,theme,cluster_id,catalyst_id,trigger,description,economic_impact,earnings_impact,valuation_impact):
  if not isinstance(assessment,HistoricalComparisonPromotedCatalystAssessmentDecision):raise ValueError("assessment must be a promoted Catalyst assessment")
  if not isinstance(creation,HistoricalComparisonCatalystCreationReceipt):raise ValueError("creation must be a Catalyst creation receipt")
  preview,catalyst=HistoricalComparisonPromotedStageCatalystPreviewBuilder().build_with_catalyst(inputs,reviews,theme=theme,cluster_id=cluster_id,catalyst_id=catalyst_id,trigger=trigger,description=description,economic_impact=economic_impact,earnings_impact=earnings_impact,valuation_impact=valuation_impact)
  preview_fingerprint=HistoricalComparisonPromotedCatalystAssessmentLedger.preview_fingerprint(preview);assessment_fingerprint=HistoricalComparisonCatalystCreationLedger._assessment_fingerprint(assessment);catalyst_fingerprint=HistoricalComparisonCatalystCreationLedger._fingerprint(catalyst);creation_fingerprint=self.creation_receipt_fingerprint(creation)
  if (assessment.preview_fingerprint,assessment.promotion_fingerprint,assessment.support_fingerprint,assessment.catalyst_id,assessment.signal_ids,assessment.promoted_signal_ids)!=(preview_fingerprint,preview.promotion_fingerprint,preview.support_fingerprint,preview.catalyst_id,preview.signal_ids,preview.promoted_signal_ids):raise ValueError("assessment does not bind to the exact promoted Catalyst preview")
  if (creation.preview_fingerprint,creation.assessment_fingerprint,creation.promotion_fingerprint,creation.support_fingerprint,creation.catalyst_id,creation.catalyst_fingerprint,creation.signal_ids,creation.promoted_signal_ids)!=(preview_fingerprint,assessment_fingerprint,preview.promotion_fingerprint,preview.support_fingerprint,catalyst.catalyst_id,catalyst_fingerprint,preview.signal_ids,preview.promoted_signal_ids):raise ValueError("creation receipt does not bind to the exact approved Catalyst")
  if (creation.primary_catalyst_id,creation.primary_family,creation.catalyst_score,creation.confidence)!=(catalyst.primary_catalyst_id,catalyst.primary_catalyst_family,catalyst.catalyst_score,catalyst.confidence):raise ValueError("creation receipt Catalyst summary differs from reconstruction")
  blockers=[]
  if assessment.disposition!=HistoricalComparisonPromotedCatalystAssessmentDisposition.APPROVED:blockers.append("Promoted Catalyst assessment is not Approved.")
  if not preview.promoted_meets_minimum or catalyst.catalyst_score<CatalystEngine.MINIMUM_CATALYST_SCORE:blockers.append("Catalyst no longer meets the minimum score.")
  if not catalyst.economic_impact.strip():blockers.append("Catalyst economic impact is missing.")
  if not catalyst.earnings_impact.strip():blockers.append("Catalyst earnings impact is missing.")
  warnings=tuple(catalyst.warnings);identity={"creation_receipt_fingerprint":creation_fingerprint,"catalyst_fingerprint":catalyst_fingerprint,"required_analysis_inputs":self.REQUIRED_INPUTS}
  eligibility_fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
  return HistoricalComparisonExpectationGapEligibilityPreview(eligibility_fingerprint,not blockers,catalyst.catalyst_id,catalyst_fingerprint,creation_fingerprint,assessment_fingerprint,preview_fingerprint,preview.promotion_fingerprint,preview.support_fingerprint,preview.signal_ids,preview.promoted_signal_ids,catalyst.primary_catalyst_id,catalyst.primary_catalyst_family,catalyst.catalyst_score,catalyst.confidence,self.REQUIRED_INPUTS,tuple(blockers),warnings)
 @staticmethod
 def creation_receipt_fingerprint(receipt):
  if not isinstance(receipt,HistoricalComparisonCatalystCreationReceipt):raise ValueError("creation must be a Catalyst creation receipt")
  payload={**receipt.__dict__,"signal_ids":list(receipt.signal_ids),"promoted_signal_ids":list(receipt.promoted_signal_ids),"created_at":receipt.created_at.isoformat()}
  return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

__all__=["HistoricalComparisonExpectationGapEligibilityPreviewBuilder"]
