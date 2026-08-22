"""Run governed Mispricing analysis without persistence."""
import json
from dataclasses import fields
from pathlib import Path
from modules.external_intelligence.historical_comparison_expectation_gap_assessment_ledger import HistoricalComparisonExpectationGapAssessmentLedger
from modules.external_intelligence.historical_comparison_expectation_gap_creation_ledger import HistoricalComparisonExpectationGapCreationLedger
from modules.external_intelligence.historical_comparison_mispricing_analysis_preview_builder import HistoricalComparisonMispricingAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_valuation_snapshot_ledger import HistoricalComparisonValuationSnapshotLedger
from modules.master_dossier.valuation_section import ValuationSection
from scripts.preview_historical_comparison_expectation_gap_analysis import build_preview_from_args, parser as analysis_parser

def parser():
 result=analysis_parser();result.description="Run governed read-only Mispricing analysis."
 for name in ("gap-assessment-ledger-path","gap-creation-ledger-path","valuation-json-path","valuation-receipt-ledger-path"):result.add_argument("--"+name,required=True)
 result.add_argument("--cmp",required=True,type=float);result.add_argument("--mispricing-assumption",action="append",default=[]);result.add_argument("--mispricing-invalidation-condition",action="append",default=[]);return result
def one(items,predicate,name):
 matches=[item for item in items if predicate(item)]
 if len(matches)!=1:raise ValueError(f"{name} was not found uniquely")
 return matches[0]
def build_mispricing_preview_from_args(args, include_context=False):
 gap_assessment_path=Path(args.gap_assessment_ledger_path);gap_creation_path=Path(args.gap_creation_ledger_path);valuation_path=Path(args.valuation_json_path);valuation_receipt_path=Path(args.valuation_receipt_ledger_path)
 analysis,before,context=build_preview_from_args(args,include_context=True)
 for path in (gap_assessment_path,gap_creation_path,valuation_path,valuation_receipt_path):before[path]=path.read_bytes()
 gap_assessment=one(HistoricalComparisonExpectationGapAssessmentLedger(gap_assessment_path).read_all(),lambda item:item.analysis_fingerprint==analysis.analysis_fingerprint,"Expectation Gap assessment")
 assessment_fingerprint=HistoricalComparisonExpectationGapCreationLedger.assessment_fingerprint(gap_assessment)
 gap_creation=one(HistoricalComparisonExpectationGapCreationLedger(gap_creation_path).read_all(),lambda item:item.assessment_fingerprint==assessment_fingerprint,"Expectation Gap creation receipt")
 valuation_payload=json.loads(before[valuation_path])
 if not isinstance(valuation_payload,dict):raise ValueError("valuation JSON must contain one object")
 allowed={field.name for field in fields(ValuationSection)}
 if set(valuation_payload)-allowed:raise ValueError("valuation JSON contains unknown fields")
 valuation=ValuationSection(**valuation_payload);valuation_fingerprint=HistoricalComparisonValuationSnapshotLedger.valuation_fingerprint(valuation)
 valuation_receipt=one(HistoricalComparisonValuationSnapshotLedger(valuation_receipt_path).read_all(),lambda item:item.valuation_fingerprint==valuation_fingerprint,"valuation snapshot receipt")
 preview=HistoricalComparisonMispricingAnalysisPreviewBuilder().build(context["inputs"],context["reviews"],context["catalyst_assessment"],context["catalyst_creation"],gap_assessment,gap_creation,valuation,valuation_receipt,cmp=args.cmp,mispricing_assumptions=args.mispricing_assumption,mispricing_invalidation_conditions=args.mispricing_invalidation_condition,**context["analysis_kwargs"])
 if include_context:
  return preview,before,{"inputs":context["inputs"],"reviews":context["reviews"],"catalyst_assessment":context["catalyst_assessment"],"catalyst_creation":context["catalyst_creation"],"gap_assessment":gap_assessment,"gap_creation":gap_creation,"valuation":valuation,"valuation_receipt":valuation_receipt,"analysis_kwargs":context["analysis_kwargs"]}
 return preview,before
def main(argv=None):
 args=parser().parse_args(argv)
 try:
  preview,before=build_mispricing_preview_from_args(args)
 except (OSError,KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Mispricing analysis error: {exc}");return 1
 if any(path.read_bytes()!=value for path,value in before.items()):print("Mispricing analysis error: a source file changed.");return 1
 payload={key:list(value) if isinstance(value,tuple) else value for key,value in preview.__dict__.items()};print(json.dumps(payload,sort_keys=True,indent=2));print("Read-only analysis preview: no receipt was appended and no downstream engine was invoked.");return 0
if __name__=="__main__":raise SystemExit(main())
