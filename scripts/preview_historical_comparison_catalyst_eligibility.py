"""Print read-only Catalyst review eligibility for one governed Signal."""
import argparse,json
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_eligibility_preview_builder import HistoricalComparisonCatalystEligibilityPreviewBuilder
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Read-only Catalyst review eligibility for one approved governed Signal.")
 for n in ("signal-creation-receipt-path","interpretation-ledger-path","conversion-receipt-path","validation-decision-ledger-path","signal-id"):p.add_argument("--"+n,required=True)
 return p
def one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1:raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[Path(a.signal_creation_receipt_path),Path(a.interpretation_ledger_path),Path(a.conversion_receipt_path),Path(a.validation_decision_ledger_path)]
 if len({p.resolve() for p in paths})!=4:print("Catalyst eligibility preview error: all input paths must differ.");return 1
 before={p:p.read_bytes() for p in paths if p.is_file()}
 try:
  creation=one(HistoricalComparisonSignalCreationLedger(paths[0]).read_all(),lambda x:x.signal_id==a.signal_id,"Signal creation receipt")
  interpretation=one(HistoricalComparisonSignalInterpretationLedger(paths[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
  conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(paths[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
  decisions=[x for x in HistoricalComparisonSignalValidationDecisionLedger(paths[3]).read_all() if x.signal_id==creation.signal_id]
  if len(decisions)!=1:raise ValueError("Signal validation decision was not found uniquely")
  preview=HistoricalComparisonCatalystEligibilityPreviewBuilder().build(creation,interpretation,conversion,decisions[0])
 except (KeyError,TypeError,ValueError) as exc:print(f"Catalyst eligibility preview error: {exc}");return 1
 if any(p.read_bytes()!=v for p,v in before.items()):print("Catalyst eligibility preview error: an input file changed.");return 1
 print(json.dumps({**preview.__dict__,"blockers":list(preview.blockers),"conditions":list(preview.conditions),"monitoring_requirements":list(preview.monitoring_requirements)},sort_keys=True,indent=2));print("Read-only eligibility only: Catalyst classification was not invoked.");return 0
if __name__=="__main__":raise SystemExit(main())
