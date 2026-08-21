"""Print a read-only Catalyst Engine analysis for one classified Signal."""
import argparse,json
from pathlib import Path
from modules.external_intelligence.historical_comparison_catalyst_analysis_preview_builder import HistoricalComparisonCatalystAnalysisPreviewBuilder
from modules.external_intelligence.historical_comparison_catalyst_classification_ledger import HistoricalComparisonCatalystClassificationLedger
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt_ledger import HistoricalComparisonEvidenceConversionReceiptLedger
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.external_intelligence.historical_comparison_signal_validation_decision_ledger import HistoricalComparisonSignalValidationDecisionLedger

def parser():
 p=argparse.ArgumentParser(description="Read-only Catalyst analysis for one classified governed Signal.")
 for n in ("signal-creation-receipt-path","interpretation-ledger-path","conversion-receipt-path","validation-decision-ledger-path","catalyst-classification-receipt-path","signal-id","catalyst-id"):p.add_argument("--"+n,required=True)
 return p
def one(items,predicate,name):
 m=[x for x in items if predicate(x)]
 if len(m)!=1:raise ValueError(f"{name} was not found uniquely")
 return m[0]
def main(argv=None):
 a=parser().parse_args(argv);paths=[Path(a.signal_creation_receipt_path),Path(a.interpretation_ledger_path),Path(a.conversion_receipt_path),Path(a.validation_decision_ledger_path),Path(a.catalyst_classification_receipt_path)]
 if len({p.resolve() for p in paths})!=5:print("Catalyst analysis preview error: all input paths must differ.");return 1
 before={p:p.read_bytes() for p in paths if p.is_file()}
 try:
  creation=one(HistoricalComparisonSignalCreationLedger(paths[0]).read_all(),lambda x:x.signal_id==a.signal_id,"Signal creation receipt")
  interpretation=one(HistoricalComparisonSignalInterpretationLedger(paths[1]).read_all(),lambda x:(x.governed_input_fingerprint,x.evidence_id)==(creation.governed_input_fingerprint,creation.evidence_id),"Signal interpretation")
  conversion=one(HistoricalComparisonEvidenceConversionReceiptLedger(paths[2]).read_all(),lambda x:x.evidence_id==creation.evidence_id,"Evidence conversion")
  decision=one(HistoricalComparisonSignalValidationDecisionLedger(paths[3]).read_all(),lambda x:x.signal_id==creation.signal_id,"Signal validation decision")
  receipt=one(HistoricalComparisonCatalystClassificationLedger(paths[4]).read_all(),lambda x:x.signal_id==creation.signal_id,"Catalyst classification receipt")
  preview=HistoricalComparisonCatalystAnalysisPreviewBuilder().build(creation,interpretation,conversion,decision,receipt,catalyst_id=a.catalyst_id)
 except (KeyError,TypeError,ValueError) as exc:print(f"Catalyst analysis preview error: {exc}");return 1
 if any(p.read_bytes()!=v for p,v in before.items()):print("Catalyst analysis preview error: an input file changed.");return 1
 payload={**preview.__dict__};
 for key in ("secondary_catalyst_ids","secondary_families","evidence","assumptions","contradictory_evidence","invalidation_conditions","reasons","warnings"):payload[key]=list(payload[key])
 print(json.dumps(payload,sort_keys=True,indent=2));print("Read-only preview: no Catalyst, Opportunity, valuation, portfolio, or investment state was persisted.");return 0
if __name__=="__main__":raise SystemExit(main())
