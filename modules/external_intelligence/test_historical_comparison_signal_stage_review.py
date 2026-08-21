from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_stage_review import HistoricalComparisonSignalStageReviewDisposition
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.test_historical_comparison_multi_signal_catalyst_support import approved_input

def support(root):
 items=[approved_input(root,"1","Revenue growth acceleration","Revenue and customer demand are accelerating.","Company Filing"),approved_input(root,"2","Sales order growth","Sales orders support revenue growth.","Industry Data"),approved_input(root,"3","Customer demand expansion","Customer demand supports higher revenue.","Channel Survey")]
 preview=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(items,theme="Entity Revenue Growth",cluster_id="HC-CLUSTER-001",catalyst_id="HC-CAT-MULTI-001",trigger="Independent revenue signals are strengthening.",description="Three approved Signals support the same revenue Catalyst.",economic_impact="Demand supports company revenue growth.",earnings_impact="Revenue growth may support earnings.",valuation_impact="No valuation calculation is performed.")
 return items,preview
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);items,preview=support(root);ledger=HistoricalComparisonSignalStageReviewLedger(root/"stage-reviews.jsonl");item=items[0]
  with patch("modules.opportunity.catalyst_engine.CatalystEngine.analyze",side_effect=AssertionError("Catalyst recalculation forbidden")):
   review=ledger.record(preview,item.interpretation,item.validation_decision,target_stage="Validated Signal",disposition="Approved",conditions=["Maintain independent corroboration"],monitoring_requirements=["Watch demand reversal"],reviewer="Stage Reviewer",rationale="Strong emerging cluster supports controlled promotion.",reviewed_at=item.validation_decision.reviewed_at)
  assert review.disposition==HistoricalComparisonSignalStageReviewDisposition.APPROVED and ledger.read_all()==(review,)
  assert item.interpretation.interpretation.stage.value=="Emerging Signal"
  try:ledger.record(preview,item.interpretation,item.validation_decision,target_stage="Validated Signal",disposition="Approved",reviewer="Other",rationale="Duplicate",reviewed_at=item.validation_decision.reviewed_at)
  except ValueError as exc:assert "already exists" in str(exc)
  else:raise AssertionError("duplicate review accepted")
  weak=replace(preview,cluster_emerging=False)
  try:HistoricalComparisonSignalStageReviewLedger(root/"weak.jsonl").record(weak,items[1].interpretation,items[1].validation_decision,target_stage="Validated Signal",disposition="Approved",reviewer="Reviewer",rationale="Should fail",reviewed_at=items[1].validation_decision.reviewed_at)
  except ValueError as exc:assert "does not justify" in str(exc)
  else:raise AssertionError("weak support approved")
 print("HISTORICAL SIGNAL STAGE REVIEW: ALL TESTS PASSED")
if __name__=="__main__":main()
