"""Record a human decision on one exact governed Mispricing analysis."""
import json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_mispricing_assessment_ledger import HistoricalComparisonMispricingAssessmentLedger
from scripts.preview_historical_comparison_mispricing_analysis import build_mispricing_preview_from_args, parser as preview_parser

def parser():
 result=preview_parser();result.description="Record a human assessment of an exact governed Mispricing analysis."
 for name in ("decision-ledger-path","disposition","reviewer","rationale","reviewed-at"):result.add_argument("--"+name,required=True)
 result.add_argument("--condition",action="append",default=[]);result.add_argument("--monitoring-requirement",action="append",default=[]);return result
def main(argv=None):
 args=parser().parse_args(argv);destination=Path(args.decision_ledger_path)
 try:
  preview,before=build_mispricing_preview_from_args(args)
  if destination.resolve() in {path.resolve() for path in before}:raise ValueError("decision ledger must be distinct from every source file")
  decision=HistoricalComparisonMispricingAssessmentLedger(destination).record(preview,disposition=args.disposition,conditions=args.condition,monitoring_requirements=args.monitoring_requirement,reviewer=args.reviewer,rationale=args.rationale,reviewed_at=datetime.fromisoformat(args.reviewed_at))
 except (OSError,KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Mispricing assessment error: {exc}");return 1
 if any(path.read_bytes()!=value for path,value in before.items()):print("Mispricing assessment error: a source file changed.");return 1
 print(f"Company: {decision.company}");print(f"Decision: {decision.disposition.value}");print(f"Analysis fingerprint: {decision.analysis_fingerprint}");print("Decision appended. No downstream analysis or investment action was performed.");return 0
if __name__=="__main__":raise SystemExit(main())
