"""Read-only multi-Signal Catalyst support from approved Signal-chain manifests."""
import argparse,json
from pathlib import Path
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_multi_signal_catalyst_support_preview_builder import HistoricalComparisonApprovedSignalInput,HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Read-only multi-Signal Catalyst support preview.");p.add_argument("--signal-chain-json",action="append",required=True)
 for n in ("theme","cluster-id","catalyst-id","trigger","description","economic-impact","earnings-impact","valuation-impact"):p.add_argument("--"+n,required=True)
 return p
def one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1:raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[];chains=[]
 try:
  for raw in a.signal_chain_json:
   spec=json.loads(raw);signal_id=spec["signal_id"];current=[Path(spec[x]) for x in ("creation_path","interpretation_path","conversion_path","validation_decision_path")];paths.extend(current)
   creation=one(HistoricalComparisonSignalCreationLedger(current[0]).read_all(),lambda x:x.signal_id==signal_id,"Signal creation")
   interpretation=one(HistoricalComparisonSignalInterpretationLedger(current[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
   conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(current[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
   decision=one(HistoricalComparisonSignalValidationDecisionLedger(current[3]).read_all(),lambda x:x.signal_id==signal_id,"Signal validation decision")
   chains.append(HistoricalComparisonApprovedSignalInput(creation,interpretation,conversion,decision))
  if len({p.resolve() for p in paths})!=len(paths):raise ValueError("all source ledger paths must be distinct")
  before={p:p.read_bytes() for p in paths if p.is_file()}
  preview=HistoricalComparisonMultiSignalCatalystSupportPreviewBuilder().build(chains,theme=a.theme,cluster_id=a.cluster_id,catalyst_id=a.catalyst_id,trigger=a.trigger,description=a.description,economic_impact=a.economic_impact,earnings_impact=a.earnings_impact,valuation_impact=a.valuation_impact)
 except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:print(f"Multi-Signal Catalyst preview error: {exc}");return 1
 if any(p.read_bytes()!=v for p,v in before.items()):print("Multi-Signal Catalyst preview error: an input file changed.");return 1
 payload={**preview.__dict__}
 for key in ("signal_ids","signal_fingerprints","validation_fingerprints","reasons","warnings"):payload[key]=list(payload[key])
 print(json.dumps(payload,sort_keys=True,indent=2));print("Read-only preview: no Catalyst, Opportunity, valuation, portfolio, or investment state was persisted.");return 0
if __name__=="__main__":raise SystemExit(main())
