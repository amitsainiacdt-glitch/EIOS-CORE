"""Record explicit human interpretation without creating a Signal."""
from __future__ import annotations
import argparse, json
from datetime import datetime
from pathlib import Path
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_ledger import HistoricalComparisonEvidencePackScoringLedger
from modules.external_intelligence.historical_comparison_governed_scoring_ledger import HistoricalComparisonGovernedScoringLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger

def build_parser():
    p=argparse.ArgumentParser(description="Record a human Signal interpretation for governed historical Evidence.")
    for name in ("governed-scoring-path","initial-scoring-path","conversion-receipt-path","interpretation-ledger-path","governed-input-fingerprint","evidence-id","interpretation-json","analyst","rationale","interpreted-at"):
        p.add_argument("--"+name, required=True)
    return p

def _one(items, predicate, name):
    matches=[item for item in items if predicate(item)]
    if len(matches)!=1: raise ValueError(f"{name} was not found uniquely")
    return matches[0]

def main(argv=None):
    a=build_parser().parse_args(argv)
    sources=[Path(a.governed_scoring_path),Path(a.initial_scoring_path),Path(a.conversion_receipt_path)]
    destination=Path(a.interpretation_ledger_path)
    if len({p.resolve() for p in sources+[destination]})!=4:
        print("Signal interpretation error: all source and destination paths must differ."); return 1
    before={p:p.read_bytes() for p in sources if p.is_file()}
    try:
        governed=_one(HistoricalComparisonGovernedScoringLedger(sources[0]).read_all(),lambda x:x.governed_input_fingerprint==a.governed_input_fingerprint.casefold(),"governed input fingerprint")
        scoring=_one(HistoricalComparisonEvidencePackScoringLedger(sources[1]).read_all(),lambda x:x.pack_fingerprint==governed.pack_fingerprint,"initial scoring receipt")
        conversion=_one(HistoricalComparisonEvidenceConversionReceiptLedger(sources[2]).read_all(),lambda x:x.evidence_id==a.evidence_id,"Evidence conversion receipt")
        interpretation=HistoricalComparisonSignalInterpretationLedger._interpretation(json.loads(a.interpretation_json))
        record=HistoricalComparisonSignalInterpretationLedger(destination).record(governed,scoring,conversion,interpretation=interpretation,analyst=a.analyst,rationale=a.rationale,interpreted_at=datetime.fromisoformat(a.interpreted_at))
    except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:
        print(f"Signal interpretation error: {exc}"); return 1
    if any(p.read_bytes()!=content for p,content in before.items()):
        print("Signal interpretation error: an input receipt file changed."); return 1
    print(f"Governed input: {record.governed_input_fingerprint}")
    print(f"EvidenceItem: {record.evidence_id}")
    print("Human Signal interpretation appended.")
    print("No Signal or Catalyst was created.")
    print("No Intelligence was published, and no valuation or investment decision was performed.")
    return 0

if __name__=="__main__": raise SystemExit(main())
