"""Apply approved stage reviews to fresh Signal copies for read-only comparison."""
from __future__ import annotations
import hashlib,json
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview import HistoricalComparisonPromotedStageCatalystPreview
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_stage_review import HistoricalComparisonSignalStageReview,HistoricalComparisonSignalStageReviewDisposition
from modules.opportunity.catalyst.signal_cluster_catalyst_bridge import SignalClusterCatalystBridge
from modules.opportunity.catalyst_engine import CatalystEngine
from modules.opportunity.evidence_engine import EvidenceItem
from modules.opportunity.signals.signal_aggregation import SignalAggregationEngine
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine

class _FixedClassifier:
 def __init__(self,result):self.result=result
 def classify(self,**kwargs):return self.result

class HistoricalComparisonPromotedStageCatalystPreviewBuilder:
 def build(self,inputs,reviews,*,theme,cluster_id,catalyst_id,trigger,description,economic_impact,earnings_impact,valuation_impact):
  baseline=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(inputs,theme=theme,cluster_id=cluster_id,catalyst_id=catalyst_id,trigger=trigger,description=description,economic_impact=economic_impact,earnings_impact=earnings_impact,valuation_impact=valuation_impact)
  if not isinstance(reviews,(list,tuple)) or not reviews:raise ValueError("at least one approved stage review is required")
  review_by_signal={}
  for review in reviews:
   if not isinstance(review,HistoricalComparisonSignalStageReview):raise ValueError("reviews contain an invalid stage review")
   if review.support_fingerprint!=baseline.support_fingerprint:raise ValueError("stage review binds a different support fingerprint")
   if review.disposition!=HistoricalComparisonSignalStageReviewDisposition.APPROVED:raise ValueError("only Approved stage reviews may be applied")
   if review.signal_id in review_by_signal:raise ValueError("stage reviews must contain unique Signal IDs")
   review_by_signal[review.signal_id]=review
  ordered=sorted(inputs,key=lambda x:x.creation.signal_id if isinstance(x,HistoricalComparisonApprovedSignalInput) else "")
  signals=[];original=[];effective=[];promoted=[];assumptions=[];invalidations=[]
  for item in ordered:
   if not isinstance(item,HistoricalComparisonApprovedSignalInput):raise ValueError("inputs contain an invalid approved Signal chain")
   evidence=EvidenceItem(evidence_id=item.conversion.evidence_id,statement=item.conversion.statement,source=item.conversion.source,category=item.conversion.category,direction=item.conversion.direction,strength=item.conversion.strength,confidence=item.conversion.confidence,independent_confirmation=item.conversion.independent_confirmation,is_primary_source=item.conversion.is_primary_source,is_time_sensitive=item.conversion.is_time_sensitive,notes=item.conversion.notes)
   result=SignalInterpretationEngine().create(evidence=evidence,interpretation=item.interpretation.interpretation,signal_id=item.creation.signal_id)
   if not result.accepted or result.signal is None:raise ValueError(f"Signal reconstruction rejected: {result.reason}")
   signal=result.signal
   if HistoricalComparisonSignalCreationLedger._fingerprint(signal)!=item.creation.signal_fingerprint:raise ValueError("reconstructed Signal fingerprint differs from creation receipt")
   original.append(signal.stage.value)
   review=review_by_signal.get(signal.signal_id)
   if review:
    if (review.signal_fingerprint,review.validation_fingerprint)!=(item.creation.signal_fingerprint,item.validation_decision.validation_fingerprint):raise ValueError("stage review and Signal provenance differ")
    if signal.stage!=review.current_stage:raise ValueError("current Signal stage differs from stage review")
    signal.stage=review.target_stage;promoted.append(signal.signal_id);assumptions.extend(review.conditions)
   assumptions.extend(item.validation_decision.conditions);invalidations.extend(signal.invalidation_conditions);effective.append(signal.stage.value);signals.append(signal)
  unknown=set(review_by_signal)-{x.signal_id for x in signals}
  if unknown:raise ValueError("stage review references a Signal outside the support set")
  cluster=SignalAggregationEngine().aggregate(signals,theme=theme,cluster_id=cluster_id);classification=SignalClusterCatalystBridge().classify(cluster=cluster);engine=CatalystEngine();engine.classifier=_FixedClassifier(classification)
  catalyst=engine.analyze(catalyst_id=catalyst_id,title=theme,trigger=trigger,signals=list(cluster.signals),description=description,economic_impact=economic_impact,earnings_impact=earnings_impact,valuation_impact=valuation_impact,affected_sectors=cluster.sectors,affected_companies=cluster.companies,assumptions=list(dict.fromkeys(assumptions)),invalidation_conditions=list(dict.fromkeys(invalidations)))
  identity={"support_fingerprint":baseline.support_fingerprint,"reviews":[{"signal_id":x.signal_id,"signal_fingerprint":x.signal_fingerprint,"target_stage":x.target_stage.value,"reviewed_at":x.reviewed_at.isoformat()} for x in sorted(reviews,key=lambda x:x.signal_id)]}
  fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
  return HistoricalComparisonPromotedStageCatalystPreview(fingerprint,baseline.support_fingerprint,cluster_id,catalyst_id,tuple(x.signal_id for x in signals),tuple(promoted),tuple(original),tuple(effective),baseline.catalyst_score,catalyst.catalyst_score,round(catalyst.catalyst_score-baseline.catalyst_score,2),baseline.catalyst_confidence,catalyst.confidence,baseline.meets_minimum_catalyst_score,catalyst.catalyst_score>=CatalystEngine.MINIMUM_CATALYST_SCORE,catalyst.primary_catalyst_id,catalyst.primary_catalyst_family,catalyst.classification_confidence,tuple(catalyst.reasons),tuple(catalyst.warnings))

__all__=["HistoricalComparisonPromotedStageCatalystPreviewBuilder"]
