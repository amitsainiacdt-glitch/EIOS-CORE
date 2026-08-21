from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger
from modules.external_intelligence.historical_comparison_signal_validation_preview_builder import HistoricalComparisonSignalValidationPreviewBuilder
from modules.external_intelligence.test_historical_comparison_signal_interpretation_ledger import SignalInterpretationLedgerTests

def approved_input(root,index,title,description,source):
 case=SignalInterpretationLedgerTests();case.setUp();conversion=replace(case.conversion,candidate_id=f"candidate-{index}",evidence_id=f"ev-{index}",source=source);canonical=replace(case.interpretation,title=title,description=description);interpretation=replace(__import__('modules.external_intelligence.historical_comparison_signal_interpretation',fromlist=['HistoricalComparisonSignalInterpretation']).HistoricalComparisonSignalInterpretation(1,case.governed.governed_input_fingerprint,case.governed.pack_fingerprint,case.governed.entity,conversion.evidence_id,canonical,"Human","Reviewed",case.when),governed_input_fingerprint=f"{index}"*64)
 _,creation=HistoricalComparisonSignalCreationLedger(root/f"creation-{index}.jsonl").materialize(interpretation,conversion,signal_id=f"HC-MULTI-{index}",creator="Creator",created_at=case.when)
 validation=HistoricalComparisonSignalValidationPreviewBuilder().build(creation,interpretation,conversion)
 decision=HistoricalComparisonSignalValidationDecisionLedger(root/f"decision-{index}.jsonl").record(validation,creation,disposition="Approved",conditions=[f"Condition {index}"],reviewer="Reviewer",rationale="Valid exact Signal.",reviewed_at=case.when)
 return HistoricalComparisonApprovedSignalInput(creation,interpretation,conversion,decision)
def main():
 with TemporaryDirectory() as temp:
  root=Path(temp);items=[approved_input(root,"1","Revenue growth acceleration","Revenue and customer demand are accelerating.","Company Filing"),approved_input(root,"2","Sales order growth","Sales orders support revenue growth.","Industry Data"),approved_input(root,"3","Customer demand expansion","Customer demand supports higher revenue.","Channel Survey")]
  with patch("modules.opportunity.expectation_gap_engine.ExpectationGapEngine.analyze",side_effect=AssertionError("Expectation Gap forbidden")):
   preview=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(items,theme="Entity Revenue Growth",cluster_id="HC-CLUSTER-001",catalyst_id="HC-CAT-MULTI-001",trigger="Independent revenue signals are strengthening.",description="Three approved Signals support the same revenue Catalyst.",economic_impact="Demand supports company revenue growth.",earnings_impact="Revenue growth may support earnings.",valuation_impact="No valuation calculation is performed.")
  assert preview.signal_count==3 and preview.independent_sources==3
  assert preview.independently_supported and preview.cluster_emerging
  assert not preview.meets_minimum_catalyst_score and preview.stage_promotion_required
  assert preview.cluster_score>=60 and preview.catalyst_score<50
  duplicate=items[0]
  try:HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build([items[0],duplicate],theme="Duplicate",cluster_id="DUP",catalyst_id="DUP",trigger="Duplicate",description="Duplicate",economic_impact="Duplicate",earnings_impact="Duplicate",valuation_impact="Duplicate")
  except ValueError as exc:assert "fingerprints must be unique" in str(exc)
  else:raise AssertionError("duplicate Evidence accepted")
 print("HISTORICAL MULTI-SIGNAL CATALYST SUPPORT: ALL TESTS PASSED")
if __name__=="__main__":main()
