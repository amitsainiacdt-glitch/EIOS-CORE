"""Print a read-only validation preview for one exact created Signal."""
import argparse,json
from pathlib import Path
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_validation_preview_builder import HistoricalComparisonSignalValidationPreviewBuilder

def parser():
 p=argparse.ArgumentParser(description="Read-only validation preview for one historical-comparison Signal.")
 for n in ("signal-creation-receipt-path","interpretation-ledger-path","conversion-receipt-path","signal-id"): p.add_argument("--"+n,required=True)
 return p
def _one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1: raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv); paths=[Path(a.signal_creation_receipt_path),Path(a.interpretation_ledger_path),Path(a.conversion_receipt_path)]
 if len({p.resolve() for p in paths})!=3: print("Signal validation preview error: all input paths must differ."); return 1
 before={p:p.read_bytes() for p in paths if p.is_file()}
 try:
  creation=_one(HistoricalComparisonSignalCreationLedger(paths[0]).read_all(),lambda x:x.signal_id==a.signal_id,"Signal creation receipt")
  interpretation=_one(HistoricalComparisonSignalInterpretationLedger(paths[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"approved interpretation")
  conversion=_one(HistoricalComparisonEvidenceConversionReceiptLedger(paths[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
  preview=HistoricalComparisonSignalValidationPreviewBuilder().build(creation,interpretation,conversion)
 except (KeyError,TypeError,ValueError) as exc: print(f"Signal validation preview error: {exc}"); return 1
 if any(p.read_bytes()!=v for p,v in before.items()): print("Signal validation preview error: an input file changed."); return 1
 print(json.dumps({**preview.__dict__,"reasons":list(preview.reasons),"warnings":list(preview.warnings),"invalidation_reasons":list(preview.invalidation_reasons)},sort_keys=True,indent=2))
 print("Read-only preview: no registry, receipt, Catalyst, Intelligence, valuation, or investment state changed."); return 0
if __name__=="__main__": raise SystemExit(main())
