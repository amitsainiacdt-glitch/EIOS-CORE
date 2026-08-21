"""Explicitly classify one eligible Signal and append a taxonomy receipt."""
import argparse
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Classify one eligible governed Signal into the Catalyst taxonomy.")
 for n in ("signal-creation-receipt-path","interpretation-ledger-path","conversion-receipt-path","validation-decision-ledger-path","catalyst-classification-receipt-path","signal-id","analyst","rationale","classified-at"):p.add_argument("--"+n,required=True)
 return p
def one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1:raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv);sources=[Path(a.signal_creation_receipt_path),Path(a.interpretation_ledger_path),Path(a.conversion_receipt_path),Path(a.validation_decision_ledger_path)];destination=Path(a.catalyst_classification_receipt_path)
 if len({p.resolve() for p in sources+[destination]})!=5:print("Catalyst classification error: all source and destination paths must differ.");return 1
 before={p:p.read_bytes() for p in sources if p.is_file()}
 try:
  creation=one(HistoricalComparisonSignalCreationLedger(sources[0]).read_all(),lambda x:x.signal_id==a.signal_id,"Signal creation receipt")
  interpretation=one(HistoricalComparisonSignalInterpretationLedger(sources[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
  conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(sources[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
  decision=one(HistoricalComparisonSignalValidationDecisionLedger(sources[3]).read_all(),lambda x:x.signal_id==creation.signal_id,"Signal validation decision")
  result,receipt=HistoricalComparisonCatalystClassificationLedger(destination).classify(creation,interpretation,conversion,decision,analyst=a.analyst,rationale=a.rationale,classified_at=datetime.fromisoformat(a.classified_at))
 except (KeyError,TypeError,ValueError) as exc:print(f"Catalyst classification error: {exc}");return 1
 if any(p.read_bytes()!=v for p,v in before.items()):print("Catalyst classification error: an input file changed.");return 1
 print(f"Signal: {receipt.signal_id}");print(f"Primary family: {receipt.primary_family or 'Unclassified'}");print(f"Confidence: {receipt.confidence:.2f}");print("Classification receipt appended. No Catalyst object, Opportunity score, valuation, or investment action was created.");return 0
if __name__=="__main__":raise SystemExit(main())
