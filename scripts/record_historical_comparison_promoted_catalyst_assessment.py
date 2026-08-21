"""Record a human decision on one exact promoted-stage Catalyst preview."""
import argparse,json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Record human assessment of an exact promoted-stage Catalyst preview.");p.add_argument("--signal-chain-json",action="append",required=True);p.add_argument("--stage-review-ledger-path",required=True);p.add_argument("--decision-ledger-path",required=True)
 for n in ("theme","cluster-id","catalyst-id","trigger","description","economic-impact","earnings-impact","valuation-impact","disposition","reviewer","rationale","reviewed-at"):p.add_argument("--"+n,required=True)
 p.add_argument("--condition",action="append",default=[]);p.add_argument("--monitoring-requirement",action="append",default=[]);return p
def one(items,predicate,name):
 matches=[x for x in items if predicate(x)]
 if len(matches)!=1:raise ValueError(f"{name} was not found uniquely")
 return matches[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[];chains=[];review_path=Path(a.stage_review_ledger_path);destination=Path(a.decision_ledger_path)
 try:
  for raw in a.signal_chain_json:
   spec=json.loads(raw);signal_id=spec["signal_id"];current=[Path(spec[x]) for x in ("creation_path","interpretation_path","conversion_path","validation_decision_path")];paths.extend(current)
   creation=one(HistoricalComparisonSignalCreationLedger(current[0]).read_all(),lambda x:x.signal_id==signal_id,"Signal creation")
   interpretation=one(HistoricalComparisonSignalInterpretationLedger(current[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
   conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(current[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
   decision=one(HistoricalComparisonSignalValidationDecisionLedger(current[3]).read_all(),lambda x:x.signal_id==signal_id,"Signal validation decision")
   chains.append(HistoricalComparisonApprovedSignalInput(creation,interpretation,conversion,decision))
  all_sources=paths+[review_path]
  if destination.resolve() in {p.resolve() for p in all_sources}:raise ValueError("decision ledger must be distinct from every source ledger")
  before={p:p.read_bytes() for p in all_sources if p.is_file()}
  kwargs=dict(theme=a.theme,cluster_id=a.cluster_id,catalyst_id=a.catalyst_id,trigger=a.trigger,description=a.description,economic_impact=a.economic_impact,earnings_impact=a.earnings_impact,valuation_impact=a.valuation_impact)
  baseline=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(chains,**kwargs)
  reviews=[x for x in HistoricalComparisonSignalStageReviewLedger(review_path).read_all() if x.support_fingerprint==baseline.support_fingerprint]
  preview=HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(chains,reviews,**kwargs)
  decision=HistoricalComparisonPromotedCatalystAssessmentLedger(destination).record(preview,disposition=a.disposition,conditions=a.condition,monitoring_requirements=a.monitoring_requirement,reviewer=a.reviewer,rationale=a.rationale,reviewed_at=datetime.fromisoformat(a.reviewed_at))
 except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Promoted Catalyst assessment error: {exc}");return 1
 if any(p.read_bytes()!=value for p,value in before.items()):print("Promoted Catalyst assessment error: a source ledger changed.");return 1
 print(f"Catalyst: {decision.catalyst_id}");print(f"Decision: {decision.disposition.value}");print(f"Preview fingerprint: {decision.preview_fingerprint}");print("Decision appended. No Signal or Catalyst was persisted or rescored.");return 0
if __name__=="__main__":raise SystemExit(main())
