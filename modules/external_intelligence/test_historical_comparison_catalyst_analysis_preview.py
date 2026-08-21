from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_catalyst_analysis_preview_builder import HistoricalComparisonCatalystAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.historical_comparison_catalyst_classification_receipt import HistoricalComparisonCatalystClassificationReceipt
from modules.external_intelligence.test_historical_comparison_catalyst_eligibility_preview import chain

class FailingEngine:
 def analyze(self,**kwargs):raise AssertionError("stale receipt reached Catalyst Engine")
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);case,interpretation,creation,decision=chain(root);_,receipt=HistoricalComparisonCatalystClassificationLedger(root/"classifications.jsonl").classify(creation,interpretation,case.conversion,decision,analyst="Classifier",rationale="Exact classification",classified_at=case.when)
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Opportunity analysis forbidden")):
   preview=HistoricalComparisonCatalystAnalysisPreviewBuilder().build(creation,interpretation,case.conversion,decision,receipt,catalyst_id="HC-CAT-PREVIEW-001")
  assert preview.primary_catalyst_id==receipt.primary_catalyst_id
  assert preview.signal_fingerprint==creation.signal_fingerprint
  assert 0<=preview.catalyst_score<=100 and 0<=preview.confidence<=100
  altered=HistoricalComparisonCatalystClassificationReceipt(**{**receipt.__dict__,"classification_fingerprint":"f"*64})
  try:HistoricalComparisonCatalystAnalysisPreviewBuilder().build(creation,interpretation,case.conversion,decision,altered,catalyst_id="HC-CAT-PREVIEW-002",engine=FailingEngine())
  except ValueError as exc:assert "classification differs" in str(exc)
  else:raise AssertionError("stale classification receipt accepted")
 print("HISTORICAL CATALYST ANALYSIS PREVIEW: ALL TESTS PASSED")
if __name__=="__main__":main()
