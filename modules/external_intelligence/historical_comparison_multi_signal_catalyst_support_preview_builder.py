"""Aggregate only exact, human-approved Signals into a read-only Catalyst preview."""
from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview_builder import HistoricalComparisonCatalystEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview import HistoricalComparisonMultiSignalCatalystSupportPreview
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision
from modules.opportunity.catalyst.signal_cluster_catalyst_bridge import SignalClusterCatalystBridge
from modules.opportunity.catalyst_engine import CatalystEngine
from modules.opportunity.evidence_engine import EvidenceItem
from modules.opportunity.signals.signal_aggregation import SignalAggregationEngine
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine

@dataclass(frozen=True)
class HistoricalComparisonApprovedSignalInput:
 creation:HistoricalComparisonSignalCreationReceipt
 interpretation:HistoricalComparisonSignalInterpretation
 conversion:HistoricalComparisonEvidenceConversionReceipt
 validation_decision:HistoricalComparisonSignalValidationDecision

class _FixedClassifier:
 def __init__(self,result):self.result=result
 def classify(self,**kwargs):return self.result

class HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder:
 def build(self,inputs,*,theme,cluster_id,catalyst_id,trigger,description,economic_impact,earnings_impact,valuation_impact,aggregation_engine=None,bridge=None,catalyst_engine=None):
  if not isinstance(inputs,(list,tuple)) or len(inputs)<2:raise ValueError("at least two approved Signal inputs are required")
  theme=self._text(theme,"theme");cluster_id=self._text(cluster_id,"cluster_id");catalyst_id=self._text(catalyst_id,"catalyst_id")
  ordered=sorted(inputs,key=lambda x:x.creation.signal_id if isinstance(x,HistoricalComparisonApprovedSignalInput) else "")
  signals=[];signal_fingerprints=[];validation_fingerprints=[];evidence_ids=set()
  for item in ordered:
   if not isinstance(item,HistoricalComparisonApprovedSignalInput):raise ValueError("inputs contain an invalid approved Signal chain")
   eligibility=HistoricalComparisonCatalystEligibilityPreviewBuilder().build(item.creation,item.interpretation,item.conversion,item.validation_decision)
   if not eligibility.eligible_for_catalyst_review:raise ValueError(f"Signal {item.creation.signal_id} is not approved for Catalyst review")
   if item.creation.signal_fingerprint in signal_fingerprints:raise ValueError("Signal fingerprints must be unique")
   if item.conversion.evidence_id in evidence_ids:raise ValueError("EvidenceItems must be unique across supporting Signals")
   evidence_ids.add(item.conversion.evidence_id);signal_fingerprints.append(item.creation.signal_fingerprint);validation_fingerprints.append(item.validation_decision.validation_fingerprint)
   evidence=EvidenceItem(evidence_id=item.conversion.evidence_id,statement=item.conversion.statement,source=item.conversion.source,category=item.conversion.category,direction=item.conversion.direction,strength=item.conversion.strength,confidence=item.conversion.confidence,independent_confirmation=item.conversion.independent_confirmation,is_primary_source=item.conversion.is_primary_source,is_time_sensitive=item.conversion.is_time_sensitive,notes=item.conversion.notes)
   result=SignalInterpretationEngine().create(evidence=evidence,interpretation=item.interpretation.interpretation,signal_id=item.creation.signal_id)
   if not result.accepted or result.signal is None:raise ValueError(f"Signal reconstruction rejected: {result.reason}")
   if HistoricalComparisonSignalCreationLedger._fingerprint(result.signal)!=item.creation.signal_fingerprint:raise ValueError("reconstructed Signal fingerprint differs from creation receipt")
   signals.append(result.signal)
  cluster=(aggregation_engine or SignalAggregationEngine()).aggregate(signals,theme=theme,cluster_id=cluster_id)
  classification=(bridge or SignalClusterCatalystBridge()).classify(cluster=cluster)
  engine=catalyst_engine or CatalystEngine();engine.classifier=_FixedClassifier(classification)
  assumptions=self._unique(x for item in ordered for x in item.validation_decision.conditions)
  invalidations=self._unique(x for signal in signals for x in signal.invalidation_conditions)
  catalyst=engine.analyze(catalyst_id=catalyst_id,title=theme,trigger=self._text(trigger,"trigger"),signals=list(cluster.signals),description=self._text(description,"description"),economic_impact=self._text(economic_impact,"economic_impact"),earnings_impact=self._text(earnings_impact,"earnings_impact"),valuation_impact=self._text(valuation_impact,"valuation_impact"),affected_sectors=cluster.sectors,affected_companies=cluster.companies,assumptions=list(assumptions),invalidation_conditions=list(invalidations))
  identity={"theme":theme,"cluster_id":cluster_id,"catalyst_id":catalyst_id,"signal_ids":[x.signal_id for x in signals],"signal_fingerprints":signal_fingerprints,"validation_fingerprints":validation_fingerprints}
  fingerprint=hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
  warnings=tuple(cluster.warnings)+tuple(catalyst.warnings)
  reasons=tuple(cluster.reasons)+tuple(catalyst.reasons)
  meets=catalyst.catalyst_score>=CatalystEngine.MINIMUM_CATALYST_SCORE
  independent=cluster.independent_sources>=2
  stage_promotion_required=independent and cluster.emerging and not meets
  if stage_promotion_required:warnings=warnings+("Independent multi-Signal support is strong, but canonical Signal stages remain below the Catalyst threshold.",)
  return HistoricalComparisonMultiSignalCatalystSupportPreview(fingerprint,cluster_id,theme,catalyst_id,tuple(x.signal_id for x in signals),tuple(signal_fingerprints),tuple(validation_fingerprints),cluster.signal_count,cluster.independent_sources,cluster.average_strength,cluster.average_confidence,cluster.contradiction_count,cluster.cluster_score,cluster.confidence,cluster.emerging,catalyst.primary_catalyst_id,catalyst.primary_catalyst_family,catalyst.classification_confidence,catalyst.catalyst_score,catalyst.confidence,meets,independent,stage_promotion_required,tuple(dict.fromkeys(reasons)),tuple(dict.fromkeys(warnings)))
 @staticmethod
 def _text(v,n):
  if not isinstance(v,str) or not v.strip():raise ValueError(f"{n} must not be empty")
  return v.strip()
 @staticmethod
 def _unique(values):return tuple(dict.fromkeys(x for x in values if x))

__all__=["HistoricalComparisonApprovedSignalInput","HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder"]
