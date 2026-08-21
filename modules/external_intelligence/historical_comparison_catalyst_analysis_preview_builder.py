"""Run the Catalyst Engine in memory after exact receipt verification."""
from modules.external_intelligence.historical_comparison_catalyst_analysis_preview import HistoricalComparisonCatalystAnalysisPreview
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.historical_comparison_catalyst_classification_receipt import HistoricalComparisonCatalystClassificationReceipt
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview_builder import HistoricalComparisonCatalystEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision
from modules.opportunity.catalyst.catalyst_classifier import CatalystClassifier
from modules.opportunity.catalyst_engine import CatalystEngine
from modules.opportunity.evidence_engine import EvidenceItem
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine

class _FixedClassifier:
 def __init__(self,result):self.result=result
 def classify(self,**kwargs):return self.result

class HistoricalComparisonCatalystAnalysisPreviewBuilder:
 def build(self,creation,interpretation,conversion,decision,classification_receipt,*,catalyst_id,engine=None,classifier=None):
  if not isinstance(classification_receipt,HistoricalComparisonCatalystClassificationReceipt):raise ValueError("classification_receipt must be a Catalyst classification receipt")
  catalyst_id=self._text(catalyst_id,"catalyst_id")
  eligibility=HistoricalComparisonCatalystEligibilityPreviewBuilder().build(creation,interpretation,conversion,decision)
  eligibility_fingerprint=HistoricalComparisonCatalystClassificationLedger.eligibility_fingerprint(eligibility)
  if eligibility_fingerprint!=classification_receipt.eligibility_fingerprint:raise ValueError("current eligibility differs from the classification receipt")
  if (classification_receipt.signal_id,classification_receipt.signal_fingerprint,classification_receipt.validation_fingerprint)!=(creation.signal_id,creation.signal_fingerprint,decision.validation_fingerprint):raise ValueError("classification receipt and governed Signal provenance differ")
  evidence=EvidenceItem(evidence_id=conversion.evidence_id,statement=conversion.statement,source=conversion.source,category=conversion.category,direction=conversion.direction,strength=conversion.strength,confidence=conversion.confidence,independent_confirmation=conversion.independent_confirmation,is_primary_source=conversion.is_primary_source,is_time_sensitive=conversion.is_time_sensitive,notes=conversion.notes)
  result=SignalInterpretationEngine().create(evidence=evidence,interpretation=interpretation.interpretation,signal_id=creation.signal_id)
  if not result.accepted or result.signal is None:raise ValueError(f"Signal reconstruction rejected: {result.reason}")
  signal=result.signal
  classified=(classifier or CatalystClassifier()).classify(signals=[signal],causal_chain=signal.causal_chain)
  if HistoricalComparisonCatalystClassificationLedger.classification_fingerprint(classified)!=classification_receipt.classification_fingerprint:raise ValueError("current taxonomy classification differs from the receipt")
  catalyst_engine=engine or CatalystEngine();catalyst_engine.classifier=_FixedClassifier(classified)
  catalyst=catalyst_engine.analyze(catalyst_id=catalyst_id,title=signal.title,trigger=signal.description,signals=[signal],description=signal.description,economic_impact=signal.economic_mechanism,earnings_impact=signal.earnings_impact,valuation_impact=signal.valuation_impact,affected_sectors=signal.sectors,affected_companies=signal.companies,assumptions=list(decision.conditions),invalidation_conditions=signal.invalidation_conditions)
  return HistoricalComparisonCatalystAnalysisPreview(catalyst.catalyst_id,signal.signal_id,creation.signal_fingerprint,classification_receipt.classification_fingerprint,catalyst.primary_catalyst_id,catalyst.primary_catalyst_family,tuple(catalyst.secondary_catalyst_ids),tuple(catalyst.secondary_catalyst_families),catalyst.direction.value,catalyst.horizon.value,catalyst.magnitude,catalyst.probability,catalyst.persistence,catalyst.market_recognition,catalyst.catalyst_score,catalyst.confidence,catalyst.catalyst_score>=CatalystEngine.MINIMUM_CATALYST_SCORE,tuple(catalyst.evidence),tuple(catalyst.assumptions),tuple(catalyst.contradictory_evidence),tuple(catalyst.invalidation_conditions),tuple(catalyst.reasons),tuple(catalyst.warnings))
 @staticmethod
 def _text(v,n):
  if not isinstance(v,str) or not v.strip():raise ValueError(f"{n} must not be empty")
  return v.strip()

__all__=["HistoricalComparisonCatalystAnalysisPreviewBuilder"]
