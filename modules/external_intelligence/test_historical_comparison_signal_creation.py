from datetime import datetime,timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_signal_creation_ledger import HistoricalComparisonSignalCreationLedger
from modules.external_intelligence.test_historical_comparison_signal_interpretation_ledger import SignalInterpretationLedgerTests
from modules.external_intelligence.historical_comparison_signal_interpretation import HistoricalComparisonSignalInterpretation

def inputs():
 case=SignalInterpretationLedgerTests(); case.setUp()
 approved=HistoricalComparisonSignalInterpretation(1,case.governed.governed_input_fingerprint,case.governed.pack_fingerprint,case.governed.entity,case.conversion.evidence_id,case.interpretation,"Human","Explicit review",case.when)
 return case,approved
class FailingEngine:
 def create(self,**kwargs): raise AssertionError("duplicate reached Signal engine")
def main():
 case,approved=inputs()
 with TemporaryDirectory() as temp:
  path=Path(temp)/"signal-receipts.jsonl"; ledger=HistoricalComparisonSignalCreationLedger(path)
  with patch("modules.opportunity.catalyst.catalyst_classifier.CatalystClassifier.classify",side_effect=AssertionError("Catalyst forbidden")):
   signal,receipt=ledger.materialize(approved,case.conversion,signal_id="HC-SIG-001",creator="Signal Analyst",created_at=case.when)
  assert signal.signal_id=="HC-SIG-001" and receipt.signal_fingerprint
  assert ledger.read_all()==(receipt,)
  try: ledger.materialize(approved,case.conversion,signal_id="HC-SIG-002",creator="Signal Analyst",created_at=case.when,engine=FailingEngine())
  except ValueError as exc: assert "already materialized" in str(exc)
  else: raise AssertionError("duplicate interpretation accepted")
  assert len(ledger.read_all())==1
 mismatched=HistoricalComparisonSignalInterpretation(**{**approved.__dict__,"evidence_id":"other"})
 with TemporaryDirectory() as temp:
  path=Path(temp)/"signal-receipts.jsonl"
  try: HistoricalComparisonSignalCreationLedger(path).materialize(mismatched,case.conversion,signal_id="HC-SIG-003",creator="Signal Analyst",created_at=case.when)
  except ValueError as exc: assert "different EvidenceItems" in str(exc)
  else: raise AssertionError("mismatched provenance accepted")
  assert not path.exists()
 print("HISTORICAL COMPARISON SIGNAL CREATION: ALL TESTS PASSED")
if __name__=="__main__": main()
