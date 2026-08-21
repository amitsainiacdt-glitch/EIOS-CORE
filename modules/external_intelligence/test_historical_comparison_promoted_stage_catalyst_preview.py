from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.test_historical_comparison_signal_stage_review import support

def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);items,baseline=support(root);ledger=HistoricalComparisonSignalStageReviewLedger(root/"reviews.jsonl");reviews=[]
  for item in items:
   reviews.append(ledger.record(baseline,item.interpretation,item.validation_decision,target_stage="Validated Signal",disposition="Approved",conditions=[f"Maintain support for {item.creation.signal_id}"],reviewer="Stage Reviewer",rationale="Exact strong cluster reviewed.",reviewed_at=item.validation_decision.reviewed_at))
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Expectation Gap forbidden")):
   preview=HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(items,reviews,theme="Entity Revenue Growth",cluster_id="HC-CLUSTER-001",catalyst_id="HC-CAT-MULTI-001",trigger="Independent revenue signals are strengthening.",description="Three approved Signals support the same revenue Catalyst.",economic_impact="Demand supports company revenue growth.",earnings_impact="Revenue growth may support earnings.",valuation_impact="No valuation calculation is performed.")
  assert preview.baseline_catalyst_score<50<=preview.promoted_catalyst_score
  assert preview.promoted_meets_minimum and not preview.baseline_meets_minimum
  assert preview.promoted_signal_ids==tuple(x.creation.signal_id for x in items)
  assert all(x.interpretation.interpretation.stage.value=="Emerging Signal" for x in items)
  try:HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(items,[reviews[0],reviews[0]],theme="Entity Revenue Growth",cluster_id="HC-CLUSTER-001",catalyst_id="HC-CAT-MULTI-001",trigger="Trigger",description="Description",economic_impact="Impact",earnings_impact="Earnings",valuation_impact="No valuation")
  except ValueError as exc:assert "unique Signal IDs" in str(exc)
  else:raise AssertionError("duplicate stage reviews accepted")
 print("HISTORICAL PROMOTED-STAGE CATALYST PREVIEW: ALL TESTS PASSED")
if __name__=="__main__":main()
