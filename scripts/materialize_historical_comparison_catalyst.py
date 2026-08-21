"""Explicitly materialize one approved promoted-stage Catalyst."""
import argparse,json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Explicitly materialize one human-approved promoted-stage Catalyst.");p.add_argument("--signal-chain-json",action="append",required=True)
 for n in ("stage-review-ledger-path","assessment-ledger-path","creation-ledger-path","theme","cluster-id","catalyst-id","trigger","description","economic-impact","earnings-impact","valuation-impact","creator","rationale","created-at"):p.add_argument("--"+n,required=True)
 return p
def one(items,predicate,name):
 matches=[x for x in items if predicate(x)]
 if len(matches)!=1:raise ValueError(f"{name} was not found uniquely")
 return matches[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[];chains=[];review_path=Path(a.stage_review_ledger_path);assessment_path=Path(a.assessment_ledger_path);destination=Path(a.creation_ledger_path)
 try:
  for raw in a.signal_chain_json:
   spec=json.loads(raw);signal_id=spec["signal_id"];current=[Path(spec[x]) for x in ("creation_path","interpretation_path","conversion_path","validation_decision_path")];paths.extend(current)
   creation=one(HistoricalComparisonSignalCreationLedger(current[0]).read_all(),lambda x:x.signal_id==signal_id,"Signal creation")
   interpretation=one(HistoricalComparisonSignalInterpretationLedger(current[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
   conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(current[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
   decision=one(HistoricalComparisonSignalValidationDecisionLedger(current[3]).read_all(),lambda x:x.signal_id==signal_id,"Signal validation decision")
   chains.append(HistoricalComparisonApprovedSignalInput(creation,interpretation,conversion,decision))
  sources=paths+[review_path,assessment_path]
  if destination.resolve() in {p.resolve() for p in sources}:raise ValueError("creation ledger must be distinct from every source ledger")
  before={p:p.read_bytes() for p in sources if p.is_file()};kwargs=dict(theme=a.theme,cluster_id=a.cluster_id,catalyst_id=a.catalyst_id,trigger=a.trigger,description=a.description,economic_impact=a.economic_impact,earnings_impact=a.earnings_impact,valuation_impact=a.valuation_impact)
  baseline=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(chains,**kwargs);reviews=[x for x in HistoricalComparisonSignalStageReviewLedger(review_path).read_all() if x.support_fingerprint==baseline.support_fingerprint]
  preview=HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(chains,reviews,**kwargs);fingerprint=HistoricalComparisonPromotedCatalystAssessmentLedger.preview_fingerprint(preview)
  assessment=one(HistoricalComparisonPromotedCatalystAssessmentLedger(assessment_path).read_all(),lambda x:x.preview_fingerprint==fingerprint,"approved promoted Catalyst assessment")
  _,receipt=HistoricalComparisonCatalystCreationLedger(destination).materialize(chains,reviews,assessment,**kwargs,creator=a.creator,rationale=a.rationale,created_at=datetime.fromisoformat(a.created_at))
 except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Catalyst materialization error: {exc}");return 1
 if any(p.read_bytes()!=value for p,value in before.items()):print("Catalyst materialization error: a source ledger changed.");return 1
 print(f"Catalyst: {receipt.catalyst_id}");print(f"Score: {receipt.catalyst_score:.2f}");print(f"Catalyst fingerprint: {receipt.catalyst_fingerprint}");print("Creation receipt appended. No Signal was modified and no downstream engine was invoked.");return 0
if __name__=="__main__":raise SystemExit(main())
