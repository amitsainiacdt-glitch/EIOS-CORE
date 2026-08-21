from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview_builder import HistoricalComparisonCatalystEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDecision
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger
from modules.external_intelligence.test_historical_comparison_signal_creation import inputs
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_validation_preview_builder import HistoricalComparisonSignalValidationPreviewBuilder

def chain(root,disposition="Approved"):
 case,interpretation=inputs();_,creation=HistoricalComparisonSignalCreationLedger(root/"creation.jsonl").materialize(interpretation,case.conversion,signal_id="HC-SIG-CAT-001",creator="Creator",created_at=case.when);validation=HistoricalComparisonSignalValidationPreviewBuilder().build(creation,interpretation,case.conversion);decision=HistoricalComparisonSignalValidationDecisionLedger(root/"decisions.jsonl").record(validation,creation,disposition=disposition,conditions=["Preserve corroboration"],monitoring_requirements=["Monitor demand"],reviewer="Reviewer",rationale="Reviewed exact validation.",reviewed_at=case.when);return case,interpretation,creation,decision
def main():
 with TemporaryDirectory() as temp:
  case,interpretation,creation,decision=chain(Path(temp))
  with patch("modules.opportunity.catalyst.catalyst_classifier.CatalystClassifier.classify",side_effect=AssertionError("classification forbidden")):
   preview=HistoricalComparisonCatalystEligibilityPreviewBuilder().build(creation,interpretation,case.conversion,decision)
  assert preview.eligible_for_catalyst_review and not preview.blockers
  assert preview.conditions==("Preserve corroboration",)
 with TemporaryDirectory() as temp:
  case,interpretation,creation,decision=chain(Path(temp),"Deferred")
  preview=HistoricalComparisonCatalystEligibilityPreviewBuilder().build(creation,interpretation,case.conversion,decision)
  assert not preview.eligible_for_catalyst_review and "Deferred" in preview.blockers[0]
  altered=HistoricalComparisonSignalValidationDecision(**{**decision.__dict__,"validation_fingerprint":"f"*64})
  try:HistoricalComparisonCatalystEligibilityPreviewBuilder().build(creation,interpretation,case.conversion,altered)
  except ValueError as exc:assert "differs from the human decision" in str(exc)
  else:raise AssertionError("stale validation decision accepted")
 print("HISTORICAL CATALYST ELIGIBILITY PREVIEW: ALL TESTS PASSED")
if __name__=="__main__":main()
