"""Record human Signal stage review against exact multi-Signal support."""
import argparse,json
from pathlib import Path
from datetime import datetime
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Record controlled Emerging-to-Validated Signal stage review.");p.add_argument("--signal-chain-json",action="append",required=True)
 for n in ("theme","cluster-id","catalyst-id","trigger","description","economic-impact","earnings-impact","valuation-impact","review-signal-id","target-stage","disposition","stage-review-ledger-path","reviewer","rationale","reviewed-at"):p.add_argument("--"+n,required=True)
 p.add_argument("--condition",action="append",default=[]);p.add_argument("--monitoring-requirement",action="append",default=[]);return p
def one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1:raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[];chains=[]
 try:
  for raw in a.signal_chain_json:
   spec=json.loads(raw);signal_id=spec["signal_id"];current=[Path(spec[x]) for x in ("creation_path","interpretation_path","conversion_path","validation_decision_path")];paths.extend(current)
   creation=one(HistoricalComparisonSignalCreationLedger(current[0]).read_all(),lambda x:x.signal_id==signal_id,"Signal creation")
   interpretation=one(HistoricalComparisonSignalInterpretationLedger(current[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
   conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(current[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
   decision=one(HistoricalComparisonSignalValidationDecisionLedger(current[3]).read_all(),lambda x:x.signal_id==signal_id,"Signal validation decision")
   chains.append(HistoricalComparisonApprovedSignalInput(creation,interpretation,conversion,decision))
  destination=Path(a.stage_review_ledger_path)
  if len({p.resolve() for p in paths+[destination]})!=len(paths)+1:raise ValueError("all source and destination paths must be distinct")
  before={p:p.read_bytes() for p in paths if p.is_file()}
  support=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(chains,theme=a.theme,cluster_id=a.cluster_id,catalyst_id=a.catalyst_id,trigger=a.trigger,description=a.description,economic_impact=a.economic_impact,earnings_impact=a.earnings_impact,valuation_impact=a.valuation_impact)
  selected=one(chains,lambda x:x.creation.signal_id==a.review_signal_id,"review Signal")
  review=HistoricalComparisonSignalStageReviewLedger(destination).record(support,selected.interpretation,selected.validation_decision,target_stage=a.target_stage,disposition=a.disposition,conditions=a.condition,monitoring_requirements=a.monitoring_requirement,reviewer=a.reviewer,rationale=a.rationale,reviewed_at=datetime.fromisoformat(a.reviewed_at))
 except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Signal stage review error: {exc}");return 1
 if any(p.read_bytes()!=v for p,v in before.items()):print("Signal stage review error: an input file changed.");return 1
 print(f"Signal: {review.signal_id}");print(f"Transition: {review.current_stage.value} -> {review.target_stage.value}");print(f"Decision: {review.disposition.value}");print("Review appended. No Signal was mutated and no Catalyst was recalculated or persisted.");return 0
if __name__=="__main__":raise SystemExit(main())
