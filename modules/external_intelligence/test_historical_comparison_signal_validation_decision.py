from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision import HistoricalComparisonSignalValidationDisposition
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger
from modules.external_intelligence.historical_comparison_signal_validation_preview import HistoricalComparisonSignalValidationPreview
from modules.external_intelligence.historical_comparison_signal_validation_preview_builder import HistoricalComparisonSignalValidationPreviewBuilder
from modules.external_intelligence.test_historical_comparison_signal_creation import inputs

def chain(root):
 case,approved=inputs();_,creation=HistoricalComparisonSignalCreationLedger(root/"creation.jsonl").materialize(approved,case.conversion,signal_id="HC-SIG-DECIDE-001",creator="Creator",created_at=case.when);preview=HistoricalComparisonSignalValidationPreviewBuilder().build(creation,approved,case.conversion);return case,creation,preview
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);case,creation,preview=chain(root);ledger=HistoricalComparisonSignalValidationDecisionLedger(root/"decisions.jsonl")
  with patch("modules.opportunity.catalyst.catalyst_classifier.CatalystClassifier.classify",side_effect=AssertionError("Catalyst forbidden")):
   decision=ledger.record(preview,creation,disposition="Approved",conditions=["Maintain corroboration"],monitoring_requirements=["Monitor demand"],reviewer="Validation Analyst",rationale="Exact valid preview reviewed.",reviewed_at=case.when)
  assert decision.disposition==HistoricalComparisonSignalValidationDisposition.APPROVED
  assert ledger.read_all()==(decision,)
  try:ledger.record(preview,creation,disposition="Rejected",reviewer="Other",rationale="Duplicate",reviewed_at=case.when)
  except ValueError as exc:assert "already exists" in str(exc)
  else:raise AssertionError("duplicate decision accepted")
 with TemporaryDirectory() as temp:
  root=Path(temp);case,creation,preview=chain(root);invalid=HistoricalComparisonSignalValidationPreview(**{**preview.__dict__,"valid":False,"invalidation_reasons":("Below threshold",)})
  path=root/"decisions.jsonl"
  try:HistoricalComparisonSignalValidationDecisionLedger(path).record(invalid,creation,disposition="Approved",reviewer="Analyst",rationale="Should fail",reviewed_at=case.when)
  except ValueError as exc:assert "cannot be approved" in str(exc)
  else:raise AssertionError("invalid preview approved")
  assert not path.exists()
  deferred=HistoricalComparisonSignalValidationDecisionLedger(path).record(invalid,creation,disposition="Deferred",reviewer="Analyst",rationale="Needs corroboration",reviewed_at=case.when)
  assert deferred.disposition==HistoricalComparisonSignalValidationDisposition.DEFERRED
 print("HISTORICAL SIGNAL VALIDATION DECISION: ALL TESTS PASSED")
if __name__=="__main__":main()
