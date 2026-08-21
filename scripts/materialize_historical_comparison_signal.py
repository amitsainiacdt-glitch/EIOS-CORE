"""Explicitly create one Signal and append its creation receipt."""
from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger

def parser():
 p=argparse.ArgumentParser(description="Create one Signal from an approved historical-comparison interpretation.")
 for n in ("interpretation-ledger-path","conversion-receipt-path","signal-creation-receipt-path","governed-input-fingerprint","evidence-id","signal-id","creator","created-at"): p.add_argument("--"+n,required=True)
 return p
def _one(items,predicate,name):
 matches=[x for x in items if predicate(x)]
 if len(matches)!=1: raise ValueError(f"{name} was not found uniquely")
 return matches[0]
def main(argv=None):
 a=parser().parse_args(argv); sources=[Path(a.interpretation_ledger_path),Path(a.conversion_receipt_path)]; destination=Path(a.signal_creation_receipt_path)
 if len({p.resolve() for p in sources+[destination]})!=3: print("Signal creation error: all source and destination paths must differ."); return 1
 before={p:p.read_bytes() for p in sources if p.is_file()}
 try:
  interpretation=_one(HistoricalComparisonSignalInterpretationLedger(sources[0]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(a.governed_input_fingerprint.casefold(),a.evidence_id),"approved interpretation")
  conversion=_one(HistoricalComparisonEvidenceConversionReceiptLedger(sources[1]).read_all(),lambda x:x.evidence_id==a.evidence_id,"Evidence conversion")
  signal,receipt=HistoricalComparisonSignalCreationLedger(destination).materialize(interpretation,conversion,signal_id=a.signal_id,creator=a.creator,created_at=datetime.fromisoformat(a.created_at))
 except (KeyError,TypeError,ValueError) as exc: print(f"Signal creation error: {exc}"); return 1
 if any(p.read_bytes()!=v for p,v in before.items()): print("Signal creation error: an input file changed."); return 1
 print(f"Signal created: {signal.signal_id}"); print(f"Signal fingerprint: {receipt.signal_fingerprint}"); print("Creation receipt appended."); print("No Signal registry was changed and no Catalyst was created."); print("No Intelligence was published, and no valuation or investment decision was performed."); return 0
if __name__=="__main__": raise SystemExit(main())
