from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.test_historical_comparison_catalyst_eligibility_preview import chain

class FailingClassifier:
 def classify(self,**kwargs):raise AssertionError("duplicate/ineligible reached classifier")
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);case,interpretation,creation,decision=chain(root);ledger=HistoricalComparisonCatalystClassificationLedger(root/"classifications.jsonl")
  with patch("modules.opportunity.catalyst_engine.CatalystEngine.analyze",side_effect=AssertionError("Catalyst creation forbidden")):
   result,receipt=ledger.classify(creation,interpretation,case.conversion,decision,analyst="Catalyst Analyst",rationale="Explicit taxonomy classification.",classified_at=case.when)
  assert result.is_classified and receipt.primary_catalyst_id=="CAT-REV-GROWTH"
  assert receipt.signal_id==creation.signal_id and ledger.read_all()==(receipt,)
  try:ledger.classify(creation,interpretation,case.conversion,decision,analyst="Other",rationale="Duplicate",classified_at=case.when,classifier=FailingClassifier())
  except ValueError as exc:assert "already classified" in str(exc)
  else:raise AssertionError("duplicate classification accepted")
 with TemporaryDirectory() as temp:
  root=Path(temp);case,interpretation,creation,decision=chain(root,"Deferred");path=root/"classifications.jsonl"
  try:HistoricalComparisonCatalystClassificationLedger(path).classify(creation,interpretation,case.conversion,decision,analyst="Analyst",rationale="Should fail",classified_at=case.when,classifier=FailingClassifier())
  except ValueError as exc:assert "not eligible" in str(exc)
  else:raise AssertionError("ineligible Signal classified")
  assert not path.exists()
 print("HISTORICAL CATALYST CLASSIFICATION: ALL TESTS PASSED")
if __name__=="__main__":main()
