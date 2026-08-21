from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.test_historical_comparison_signal_stage_review import support

def inputs(root):
 items,baseline=support(root);reviews=[];review_ledger=HistoricalComparisonSignalStageReviewLedger(root/"reviews.jsonl")
 for item in items:reviews.append(review_ledger.record(baseline,item.interpretation,item.validation_decision,target_stage="Validated Signal",disposition="Approved",reviewer="Stage Reviewer",rationale="Exact support reviewed.",reviewed_at=item.validation_decision.reviewed_at))
 kwargs=dict(theme="Entity Revenue Growth",cluster_id="HC-CLUSTER-001",catalyst_id="HC-CAT-MULTI-001",trigger="Independent revenue signals are strengthening.",description="Three approved Signals support one Catalyst.",economic_impact="Demand supports revenue growth.",earnings_impact="Revenue growth may support earnings.",valuation_impact="No valuation calculation is performed.")
 preview=HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(items,reviews,**kwargs)
 assessment=HistoricalComparisonPromotedCatalystAssessmentLedger(root/"assessments.jsonl").record(preview,disposition="Approved",reviewer="Catalyst Reviewer",rationale="Exact promoted result approved.",reviewed_at=datetime(2026,8,21))
 return items,reviews,kwargs,assessment
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);items,reviews,kwargs,assessment=inputs(root);source_paths=list(root.glob("*.jsonl"));before={p:p.read_bytes() for p in source_paths};ledger=HistoricalComparisonCatalystCreationLedger(root/"catalyst-creations.jsonl")
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Expectation Gap forbidden")):
   catalyst,receipt=ledger.materialize(items,reviews,assessment,**kwargs,creator="Catalyst Steward",rationale="Explicit approved materialization.",created_at=datetime(2026,8,22))
  assert catalyst.catalyst_id==receipt.catalyst_id and receipt.catalyst_score>=50
  assert receipt.catalyst_fingerprint==ledger._fingerprint(catalyst) and ledger.read_all()==(receipt,)
  assert all(p.read_bytes()==value for p,value in before.items())
  assert all(item.interpretation.interpretation.stage.value=="Emerging Signal" for item in items)
  class FailingBuilder:
   def build_with_catalyst(self,*args,**kwargs):raise AssertionError("duplicate reached materializer")
  try:ledger.materialize(items,reviews,assessment,**kwargs,creator="Other",rationale="Duplicate.",created_at=datetime(2026,8,23),builder=FailingBuilder())
  except ValueError as exc:assert "already materialized" in str(exc) or "already has" in str(exc)
  else:raise AssertionError("duplicate materialization accepted")
  rejected=replace(assessment,disposition=assessment.disposition.__class__.REJECTED)
  try:HistoricalComparisonCatalystCreationLedger(root/"rejected.jsonl").materialize(items,reviews,rejected,**kwargs,creator="Creator",rationale="Forbidden.",created_at=datetime(2026,8,22))
  except ValueError as exc:assert "Approved" in str(exc)
  else:raise AssertionError("rejected assessment materialized")
  stale=replace(assessment,preview_fingerprint="0"*64)
  try:HistoricalComparisonCatalystCreationLedger(root/"stale.jsonl").materialize(items,reviews,stale,**kwargs,creator="Creator",rationale="Stale.",created_at=datetime(2026,8,22))
  except ValueError as exc:assert "does not bind" in str(exc)
  else:raise AssertionError("stale assessment materialized")
 print("HISTORICAL CATALYST CREATION: ALL TESTS PASSED")
if __name__=="__main__":main()
