from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_creation_receipt import HistoricalComparisonSignalCreationReceipt
from modules.external_intelligence.historical_comparison_signal_validation_preview_builder import HistoricalComparisonSignalValidationPreviewBuilder
from modules.external_intelligence.test_historical_comparison_signal_creation import inputs

class FailingValidation:
 def validate(self,signal): raise AssertionError("validation ran for altered Signal")
def main():
 case,approved=inputs()
 with TemporaryDirectory() as temp:
  signal,creation=HistoricalComparisonSignalCreationLedger(Path(temp)/"creation.jsonl").materialize(approved,case.conversion,signal_id="HC-SIG-VALIDATE-001",creator="Creator",created_at=case.when)
  before=(approved,case.conversion,creation)
  with patch("modules.opportunity.catalyst.catalyst_classifier.CatalystClassifier.classify",side_effect=AssertionError("Catalyst forbidden")):
   preview=HistoricalComparisonSignalValidationPreviewBuilder().build(creation,approved,case.conversion)
  assert preview.signal_id==signal.signal_id
  assert preview.signal_fingerprint==creation.signal_fingerprint
  assert preview.independent_confirmation==case.conversion.independent_confirmation
  assert (approved,case.conversion,creation)==before
  altered=HistoricalComparisonSignalCreationReceipt(**{**creation.__dict__,"signal_fingerprint":"f"*64})
  try: HistoricalComparisonSignalValidationPreviewBuilder().build(altered,approved,case.conversion,validation_engine=FailingValidation())
  except ValueError as exc: assert "fingerprint differs" in str(exc)
  else: raise AssertionError("altered Signal receipt accepted")
 print("HISTORICAL SIGNAL VALIDATION PREVIEW: ALL TESTS PASSED")
if __name__=="__main__": main()
