from dataclasses import replace
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_expectation_gap_eligibility_preview_builder import HistoricalComparisonExpectationGapEligibilityPreviewBuilder
from modules.external_intelligence.test_historical_comparison_catalyst_creation import inputs

def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);items,reviews,kwargs,assessment=inputs(root);creation_ledger=HistoricalComparisonCatalystCreationLedger(root/"creations.jsonl");_,creation=creation_ledger.materialize(items,reviews,assessment,**kwargs,creator="Catalyst Steward",rationale="Explicit materialization.",created_at=datetime(2026,8,22));sources={p:p.read_bytes() for p in root.glob("*.jsonl")}
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Expectation Gap forbidden")):
   preview=HistoricalComparisonExpectationGapEligibilityPreviewBuilder().build(items,reviews,assessment,creation,**kwargs)
  assert preview.eligible and not preview.blockers and len(preview.required_analysis_inputs)==7
  assert all(p.read_bytes()==value for p,value in sources.items())
  assert all(item.interpretation.interpretation.stage.value=="Emerging Signal" for item in items)
  stale=replace(creation,catalyst_fingerprint="0"*64)
  try:HistoricalComparisonExpectationGapEligibilityPreviewBuilder().build(items,reviews,assessment,stale,**kwargs)
  except ValueError as exc:assert "does not bind" in str(exc)
  else:raise AssertionError("stale Catalyst receipt accepted")
  rejected=replace(assessment,disposition=assessment.disposition.__class__.REJECTED)
  rejected_fingerprint=HistoricalComparisonCatalystCreationLedger._assessment_fingerprint(rejected);rejected_creation=replace(creation,assessment_fingerprint=rejected_fingerprint)
  blocked=HistoricalComparisonExpectationGapEligibilityPreviewBuilder().build(items,reviews,rejected,rejected_creation,**kwargs)
  assert not blocked.eligible and "not Approved" in blocked.blockers[0]
 print("HISTORICAL EXPECTATION GAP ELIGIBILITY PREVIEW: ALL TESTS PASSED")
if __name__=="__main__":main()
