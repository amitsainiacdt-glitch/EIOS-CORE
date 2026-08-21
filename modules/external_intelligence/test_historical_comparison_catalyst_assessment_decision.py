from pathlib import Path
from tempfile import TemporaryDirectory
from dataclasses import replace
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_catalyst_analysis_preview_builder import HistoricalComparisonCatalystAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_catalyst_assessment_decision import HistoricalComparisonCatalystAssessmentDisposition
from modules.external_intelligence.historical_comparison_catalyst_assessment_decision_ledger import HistoricalComparisonCatalystAssessmentDecisionLedger
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.test_historical_comparison_catalyst_eligibility_preview import chain

def inputs(root):
 case,interpretation,creation,signal_decision=chain(root);_,classification=HistoricalComparisonCatalystClassificationLedger(root/"classifications.jsonl").classify(creation,interpretation,case.conversion,signal_decision,analyst="Classifier",rationale="Exact classification",classified_at=case.when);preview=HistoricalComparisonCatalystAnalysisPreviewBuilder().build(creation,interpretation,case.conversion,signal_decision,classification,catalyst_id="HC-CAT-ASSESS-001");return case,classification,preview
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);case,classification,preview=inputs(root);path=root/"assessment.jsonl";ledger=HistoricalComparisonCatalystAssessmentDecisionLedger(path)
  try:ledger.record(preview,classification,disposition="Approved",reviewer="Reviewer",rationale="Should fail",reviewed_at=case.when)
  except ValueError as exc:assert "below-threshold" in str(exc)
  else:raise AssertionError("below-threshold Catalyst approved")
  assert not path.exists()
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Expectation Gap forbidden")):
   deferred=ledger.record(preview,classification,disposition="Deferred",conditions=["Add independent Signal"],monitoring_requirements=["Monitor Catalyst score"],reviewer="Catalyst Reviewer",rationale="Below threshold; more support required.",reviewed_at=case.when)
  assert deferred.disposition==HistoricalComparisonCatalystAssessmentDisposition.DEFERRED and ledger.read_all()==(deferred,)
  try:ledger.record(preview,classification,disposition="Rejected",reviewer="Other",rationale="Duplicate",reviewed_at=case.when)
  except ValueError as exc:assert "already exists" in str(exc)
  else:raise AssertionError("duplicate decision accepted")
 with TemporaryDirectory() as temp:
  root=Path(temp);case,classification,preview=inputs(root);supported=replace(preview,catalyst_score=60.0,meets_minimum_score=True)
  approved=HistoricalComparisonCatalystAssessmentDecisionLedger(root/"assessment.jsonl").record(supported,classification,disposition="Approved",reviewer="Reviewer",rationale="Threshold met in exact preview.",reviewed_at=case.when)
  assert approved.disposition==HistoricalComparisonCatalystAssessmentDisposition.APPROVED
 print("HISTORICAL CATALYST ASSESSMENT DECISION: ALL TESTS PASSED")
if __name__=="__main__":main()
