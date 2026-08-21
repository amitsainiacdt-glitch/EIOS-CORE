from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.test_historical_comparison_signal_stage_review import support

def build(root):
 items,baseline=support(root);review_ledger=HistoricalComparisonSignalStageReviewLedger(root/"reviews.jsonl");reviews=[]
 for item in items:reviews.append(review_ledger.record(baseline,item.interpretation,item.validation_decision,target_stage="Validated Signal",disposition="Approved",reviewer="Stage Reviewer",rationale="Exact support reviewed.",reviewed_at=item.validation_decision.reviewed_at))
 kwargs=dict(theme="Entity Revenue Growth",cluster_id="HC-CLUSTER-001",catalyst_id="HC-CAT-MULTI-001",trigger="Independent revenue signals are strengthening.",description="Three approved Signals support one Catalyst.",economic_impact="Demand supports revenue growth.",earnings_impact="Revenue growth may support earnings.",valuation_impact="No valuation calculation is performed.")
 return HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(items,reviews,**kwargs)
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp)
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Expectation Gap forbidden")):
   preview=build(root)
  source=(root/"reviews.jsonl").read_bytes();ledger=HistoricalComparisonPromotedCatalystAssessmentLedger(root/"decisions.jsonl")
  decision=ledger.record(preview,disposition="Approved",conditions=["Maintain corroboration"],monitoring_requirements=["Review quarterly"],reviewer="Catalyst Reviewer",rationale="Promoted Signals clear the existing threshold.",reviewed_at=__import__('datetime').datetime(2026,8,21))
  assert decision.preview_fingerprint==ledger.preview_fingerprint(preview) and ledger.read_all()==(decision,)
  assert (root/"reviews.jsonl").read_bytes()==source
  try:ledger.record(preview,disposition="Deferred",reviewer="Other",rationale="Wait.",reviewed_at=__import__('datetime').datetime(2026,8,22))
  except ValueError as exc:assert "already exists" in str(exc)
  else:raise AssertionError("duplicate decision accepted")
  weak=replace(preview,promoted_meets_minimum=False)
  try:HistoricalComparisonPromotedCatalystAssessmentLedger(root/"weak.jsonl").record(weak,disposition="Approved",reviewer="Reviewer",rationale="Invalid approval.",reviewed_at=__import__('datetime').datetime(2026,8,21))
  except ValueError as exc:assert "below-threshold" in str(exc)
  else:raise AssertionError("below-threshold approval accepted")
  deferred=HistoricalComparisonPromotedCatalystAssessmentLedger(root/"deferred.jsonl").record(weak,disposition="Deferred",reviewer="Reviewer",rationale="More evidence required.",reviewed_at=__import__('datetime').datetime(2026,8,21))
  assert deferred.disposition.value=="Deferred"
 print("HISTORICAL PROMOTED CATALYST ASSESSMENT: ALL TESTS PASSED")
if __name__=="__main__":main()
