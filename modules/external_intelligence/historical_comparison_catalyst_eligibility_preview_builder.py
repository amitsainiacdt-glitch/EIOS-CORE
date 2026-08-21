"""Fail-closed Catalyst review gate; never invokes Catalyst classification."""
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview import HistoricalComparisonCatalystEligibilityPreview
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision,HistoricalComparisonSignalValidationDisposition
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger
from modules.external_intelligence.historical_comparison_signal_validation_preview_builder import HistoricalComparisonSignalValidationPreviewBuilder
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt

class HistoricalComparisonCatalystEligibilityPreviewBuilder:
 def build(self,creation,interpretation,conversion,decision,*,validation_builder=None):
  if not isinstance(creation,HistoricalComparisonSignalCreationReceipt):raise ValueError("creation must be a Signal creation receipt")
  if not isinstance(interpretation,HistoricalComparisonSignalInterpretation):raise ValueError("interpretation must be an approved Signal interpretation")
  if not isinstance(conversion,HistoricalComparisonEvidenceConversionReceipt):raise ValueError("conversion must be an Evidence conversion receipt")
  if not isinstance(decision,HistoricalComparisonSignalValidationDecision):raise ValueError("decision must be a human Signal validation decision")
  preview=(validation_builder or HistoricalComparisonSignalValidationPreviewBuilder()).build(creation,interpretation,conversion)
  fingerprint=HistoricalComparisonSignalValidationDecisionLedger.validation_fingerprint(preview)
  if fingerprint!=decision.validation_fingerprint:raise ValueError("current validation result differs from the human decision")
  if (decision.signal_id,decision.signal_fingerprint,decision.governed_input_fingerprint,decision.evidence_id)!=(preview.signal_id,preview.signal_fingerprint,preview.governed_input_fingerprint,preview.evidence_id):raise ValueError("human decision and current Signal provenance differ")
  blockers=[]
  if not preview.valid:blockers.append("Signal validation is not valid.")
  if preview.invalidation_reasons:blockers.extend(preview.invalidation_reasons)
  if decision.disposition!=HistoricalComparisonSignalValidationDisposition.APPROVED:blockers.append(f"Human validation disposition is {decision.disposition.value}.")
  return HistoricalComparisonCatalystEligibilityPreview(preview.signal_id,preview.signal_fingerprint,fingerprint,preview.governed_input_fingerprint,preview.evidence_id,preview.valid,decision.disposition.value,not blockers,tuple(dict.fromkeys(blockers)),decision.conditions,decision.monitoring_requirements)

__all__=["HistoricalComparisonCatalystEligibilityPreviewBuilder"]
