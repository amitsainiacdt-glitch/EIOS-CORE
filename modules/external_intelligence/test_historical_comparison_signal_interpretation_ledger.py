from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from modules.external_intelligence.historical_comparison_evidence_conversion_receipt import HistoricalComparisonEvidenceConversionReceipt
from modules.external_intelligence.historical_comparison_evidence_pack_scoring_receipt import HistoricalComparisonEvidencePackScoringReceipt
from modules.external_intelligence.historical_comparison_governed_scoring_receipt import HistoricalComparisonGovernedScoringReceipt
from modules.external_intelligence.historical_comparison_signal_interpretation_ledger import HistoricalComparisonSignalInterpretationLedger
from modules.opportunity.signals.signal_interpretation import SignalInterpretation
from modules.opportunity.signals.signal_model import SignalDirection,SignalDomain,SignalStage,SignalType,TimeHorizon

class SignalInterpretationLedgerTests(unittest.TestCase):
 def setUp(self):
  self.when=datetime(2026,8,21,10,tzinfo=timezone.utc)
  self.scoring=HistoricalComparisonEvidencePackScoringReceipt(1,"a"*64,"Entity A",("ev-1",),(),80.0,.8,True,(),("strong",),(),(),"Analyst",self.when)
  self.governed=HistoricalComparisonGovernedScoringReceipt(1,"b"*64,"a"*64,"Entity A",85.0,.85,True,(),("governed",),(),(),"Analyst",self.when)
  self.conversion=HistoricalComparisonEvidenceConversionReceipt(1,"candidate-1","c"*64,"ev-1","Statement","Source","Historical Comparison","Supportive",90.0,.9,2,True,False,"Notes","Reviewer",self.when,"Assessor",self.when,"Converter",self.when)
  self.interpretation=SignalInterpretation(title="Revenue inflection",description="A governed comparison supports an emerging revenue inflection.",detected_date="2026-08-21",domain=SignalDomain.EARNINGS,signal_type=SignalType.INFLECTION,direction=SignalDirection.POSITIVE,stage=SignalStage.EMERGING,horizon=TimeHorizon.MEDIUM_TERM,companies=["Entity A"],economic_mechanism="Demand supports revenue growth.",supply_demand_impact="Demand improves.",earnings_impact="Revenue may improve.",valuation_impact="No valuation conclusion.",magnitude=.7,probability=.75,persistence=.6,relevance=.9,market_expectation="Not assessed automatically.",market_recognition=.2,price_reaction="Not assessed automatically.",causal_chain=["Demand","Revenue"],beneficiaries=["Entity A"],historical_precedent="Governed historical comparison.",invalidation_conditions=["Demand weakens"])
 def test_round_trip_without_signal_creation(self):
  with TemporaryDirectory() as temp:
   ledger=HistoricalComparisonSignalInterpretationLedger(Path(temp)/"ledger.jsonl")
   with patch("modules.opportunity.signals.signal_interpretation_engine.SignalInterpretationEngine.create",side_effect=AssertionError("forbidden")):
    record=ledger.record(self.governed,self.scoring,self.conversion,interpretation=self.interpretation,analyst="Human",rationale="Explicit review.",interpreted_at=self.when)
   self.assertEqual(record,ledger.read_all()[0])
 def test_rejects_unsupported_before_write(self):
  unsupported=HistoricalComparisonGovernedScoringReceipt(**{**self.governed.__dict__,"sufficiently_supported":False})
  with TemporaryDirectory() as temp:
   path=Path(temp)/"ledger.jsonl"
   with self.assertRaisesRegex(ValueError,"not sufficiently supported"):
    HistoricalComparisonSignalInterpretationLedger(path).record(unsupported,self.scoring,self.conversion,interpretation=self.interpretation,analyst="Human",rationale="Review",interpreted_at=self.when)
   self.assertFalse(path.exists())
 def test_rejects_wrong_evidence_and_duplicate(self):
  wrong=HistoricalComparisonEvidenceConversionReceipt(**{**self.conversion.__dict__,"evidence_id":"other"})
  with TemporaryDirectory() as temp:
   ledger=HistoricalComparisonSignalInterpretationLedger(Path(temp)/"ledger.jsonl")
   with self.assertRaisesRegex(ValueError,"does not belong"):
    ledger.record(self.governed,self.scoring,wrong,interpretation=self.interpretation,analyst="Human",rationale="Review",interpreted_at=self.when)
   ledger.record(self.governed,self.scoring,self.conversion,interpretation=self.interpretation,analyst="Human",rationale="Review",interpreted_at=self.when)
   with self.assertRaisesRegex(ValueError,"already exists"):
    ledger.record(self.governed,self.scoring,self.conversion,interpretation=self.interpretation,analyst="Human",rationale="Review",interpreted_at=self.when)

if __name__=="__main__": unittest.main()
