"""Read-only governed Expectation Gap eligibility preview."""
import argparse,json
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_creation_ledger import HistoricalComparisonCatalystCreationLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_expectation_gap_eligibility_preview_builder import HistoricalComparisonExpectationGapEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_promoted_catalyst_assessment_ledger import HistoricalComparisonPromotedCatalystAssessmentLedger
from modules.external_intelligence.historical_comparison_promoted_stage_catalyst_preview_builder import HistoricalComparisonPromotedStageCatalystPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_stage_review_ledger import HistoricalComparisonSignalStageReviewLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Preview governed Catalyst eligibility for later Expectation Gap analysis.");p.add_argument("--signal-chain-json",action="append",required=True)
 for n in ("stage-review-ledger-path","assessment-ledger-path","catalyst-creation-ledger-path","theme","cluster-id","catalyst-id","trigger","description","economic-impact","earnings-impact","valuation-impact"):p.add_argument("--"+n,required=True)
 return p
def one(items,predicate,name):
 matches=[x for x in items if predicate(x)]
 if len(matches)!=1:raise ValueError(f"{name} was not found uniquely")
 return matches[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[];chains=[];review_path=Path(a.stage_review_ledger_path);assessment_path=Path(a.assessment_ledger_path);creation_path=Path(a.catalyst_creation_ledger_path)
 try:
  for raw in a.signal_chain_json:
   spec=json.loads(raw);signal_id=spec["signal_id"];current=[Path(spec[x]) for x in ("creation_path","interpretation_path","conversion_path","validation_decision_path")];paths.extend(current)
   signal_creation=one(HistoricalComparisonSignalCreationLedger(current[0]).read_all(),lambda x:x.signal_id==signal_id,"Signal creation")
   interpretation=one(HistoricalComparisonSignalInterpretationLedger(current[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(signal_creation.governed_input_fingerprint,signal_creation.evidence_id),"Signal interpretation")
   conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(current[2]).read_all(),lambda x:x.evidence_id==signal_creation.evidence_id,"Evidence conversion")
   decision=one(HistoricalComparisonSignalValidationDecisionLedger(current[3]).read_all(),lambda x:x.signal_id==signal_id,"Signal validation decision")
   chains.append(HistoricalComparisonApprovedSignalInput(signal_creation,interpretation,conversion,decision))
  sources=paths+[review_path,assessment_path,creation_path];before={p:p.read_bytes() for p in sources if p.is_file()};kwargs=dict(theme=a.theme,cluster_id=a.cluster_id,catalyst_id=a.catalyst_id,trigger=a.trigger,description=a.description,economic_impact=a.economic_impact,earnings_impact=a.earnings_impact,valuation_impact=a.valuation_impact)
  baseline=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(chains,**kwargs);reviews=[x for x in HistoricalComparisonSignalStageReviewLedger(review_path).read_all() if x.support_fingerprint==baseline.support_fingerprint]
  promoted=HistoricalComparisonPromotedStageCatalystPreviewBuilder().build(chains,reviews,**kwargs);preview_fingerprint=HistoricalComparisonPromotedCatalystAssessmentLedger.preview_fingerprint(promoted)
  assessment=one(HistoricalComparisonPromotedCatalystAssessmentLedger(assessment_path).read_all(),lambda x:x.preview_fingerprint==preview_fingerprint,"promoted Catalyst assessment")
  assessment_fingerprint=HistoricalComparisonCatalystCreationLedger._assessment_fingerprint(assessment);creation=one(HistoricalComparisonCatalystCreationLedger(creation_path).read_all(),lambda x:x.assessment_fingerprint==assessment_fingerprint,"Catalyst creation receipt")
  preview=HistoricalComparisonExpectationGapEligibilityPreviewBuilder().build(chains,reviews,assessment,creation,**kwargs)
 except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Expectation Gap eligibility error: {exc}");return 1
 if any(p.read_bytes()!=value for p,value in before.items()):print("Expectation Gap eligibility error: a source ledger changed.");return 1
 payload={**preview.__dict__}
 for key in ("signal_ids","promoted_signal_ids","required_analysis_inputs","blockers","warnings"):payload[key]=list(payload[key])
 print(json.dumps(payload,sort_keys=True,indent=2));print("Read-only eligibility preview: Expectation Gap analysis was not invoked.");return 0
if __name__=="__main__":raise SystemExit(main())
