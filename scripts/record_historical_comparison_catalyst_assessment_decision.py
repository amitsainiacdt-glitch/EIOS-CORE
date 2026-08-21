"""Record a human decision on one exact Catalyst analysis preview."""
import argparse
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_analysis_preview_builder import HistoricalComparisonCatalystAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_catalyst_assessment_decision_ledger import HistoricalComparisonCatalystAssessmentDecisionLedger
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Record a human decision for an exact Catalyst analysis preview.")
 for n in ("signal-creation-receipt-path","interpretation-ledger-path","conversion-receipt-path","signal-validation-decision-ledger-path","catalyst-classification-receipt-path","catalyst-assessment-decision-ledger-path","signal-id","catalyst-id","disposition","reviewer","rationale","reviewed-at"):p.add_argument("--"+n,required=True)
 p.add_argument("--condition",action="append",default=[]);p.add_argument("--monitoring-requirement",action="append",default=[]);return p
def one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1:raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv);sources=[Path(a.signal_creation_receipt_path),Path(a.interpretation_ledger_path),Path(a.conversion_receipt_path),Path(a.signal_validation_decision_ledger_path),Path(a.catalyst_classification_receipt_path)];destination=Path(a.catalyst_assessment_decision_ledger_path)
 if len({p.resolve() for p in sources+[destination]})!=6:print("Catalyst assessment decision error: all source and destination paths must differ.");return 1
 before={p:p.read_bytes() for p in sources if p.is_file()}
 try:
  creation=one(HistoricalComparisonSignalCreationLedger(sources[0]).read_all(),lambda x:x.signal_id==a.signal_id,"Signal creation receipt")
  interpretation=one(HistoricalComparisonSignalInterpretationLedger(sources[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
  conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(sources[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
  signal_decision=one(HistoricalComparisonSignalValidationDecisionLedger(sources[3]).read_all(),lambda x:x.signal_id==creation.signal_id,"Signal validation decision")
  classification=one(HistoricalComparisonCatalystClassificationLedger(sources[4]).read_all(),lambda x:x.signal_id==creation.signal_id,"Catalyst classification receipt")
  preview=HistoricalComparisonCatalystAnalysisPreviewBuilder().build(creation,interpretation,conversion,signal_decision,classification,catalyst_id=a.catalyst_id)
  decision=HistoricalComparisonCatalystAssessmentDecisionLedger(destination).record(preview,classification,disposition=a.disposition,conditions=a.condition,monitoring_requirements=a.monitoring_requirement,reviewer=a.reviewer,rationale=a.rationale,reviewed_at=datetime.fromisoformat(a.reviewed_at))
 except (KeyError,TypeError,ValueError) as exc:print(f"Catalyst assessment decision error: {exc}");return 1
 if any(p.read_bytes()!=v for p,v in before.items()):print("Catalyst assessment decision error: an input file changed.");return 1
 print(f"Catalyst preview: {decision.catalyst_id}");print(f"Decision: {decision.disposition.value}");print(f"Analysis fingerprint: {decision.analysis_fingerprint}");print("Decision appended. No Catalyst, Expectation Gap, Opportunity score, valuation, or investment action was persisted.");return 0
if __name__=="__main__":raise SystemExit(main())
