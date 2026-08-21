"""Reconstruct and validate an exact created Signal without persistence."""
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation
from modules.external_intelligence.historical_comparison_signal_validation_preview import HistoricalComparisonSignalValidationPreview
from modules.opportunity.evidence_engine import EvidenceItem
from modules.opportunity.signals.signal_interpretation_engine import SignalInterpretationEngine
from modules.opportunity.signals.signal_validation import SignalValidationEngine

class HistoricalComparisonSignalValidationPreviewBuilder:
 def build(self,creation,interpretation,conversion,*,interpretation_engine=None,validation_engine=None):
  if not isinstance(creation,HistoricalComparisonSignalCreationReceipt): raise ValueError("creation must be a Signal creation receipt")
  if not isinstance(interpretation,HistoricalComparisonSignalInterpretation): raise ValueError("interpretation must be an approved Signal interpretation")
  if not isinstance(conversion,HistoricalComparisonEvidenceConversionReceipt): raise ValueError("conversion must be an Evidence conversion receipt")
  if (creation.governed_input_fingerprint,creation.pack_fingerprint,creation.evidence_id)!=(interpretation.governed_input_fingerprint,interpretation.pack_fingerprint,interpretation.evidence_id): raise ValueError("creation receipt and interpretation provenance differ")
  if creation.evidence_id!=conversion.evidence_id: raise ValueError("creation receipt and conversion bind different EvidenceItems")
  evidence=EvidenceItem(evidence_id=conversion.evidence_id,statement=conversion.statement,source=conversion.source,category=conversion.category,direction=conversion.direction,strength=conversion.strength,confidence=conversion.confidence,independent_confirmation=conversion.independent_confirmation,is_primary_source=conversion.is_primary_source,is_time_sensitive=conversion.is_time_sensitive,notes=conversion.notes)
  result=(interpretation_engine or SignalInterpretationEngine()).create(evidence=evidence,interpretation=interpretation.interpretation,signal_id=creation.signal_id)
  if not result.accepted or result.signal is None: raise ValueError(f"Signal reconstruction rejected: {result.reason}")
  signal=result.signal
  fingerprint=HistoricalComparisonSignalCreationLedger._fingerprint(signal)
  if fingerprint!=creation.signal_fingerprint: raise ValueError("reconstructed Signal fingerprint differs from creation receipt")
  validation=(validation_engine or SignalValidationEngine()).validate(signal)
  return HistoricalComparisonSignalValidationPreview(signal.signal_id,fingerprint,creation.governed_input_fingerprint,creation.evidence_id,validation.valid,validation.score,validation.confidence,validation.source_quality,validation.evidence_quality,validation.relevance,validation.recency,validation.persistence,validation.corroboration,validation.contradiction_penalty,validation.independent_confirmation,tuple(validation.reasons),tuple(validation.warnings),tuple(validation.invalidation_reasons))

__all__=["HistoricalComparisonSignalValidationPreviewBuilder"]
