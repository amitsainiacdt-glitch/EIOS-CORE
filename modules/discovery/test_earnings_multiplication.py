import unittest
from datetime import date, timedelta
from dataclasses import replace
from modules.discovery.earnings_multiplication import (
    EconomicScenario, LinkEvidence, MultiplicationCase, calculate,
    assess_multiplication, independently_verified_suppliers)
D=date(2026,10,19)
def econ(name,sales=100, margin=15, capex=5, nwc=2,shares=10,pe=15):
    return EconomicScenario(name,sales,margin,2,1,25,capex,nwc,shares,pe)
def case(**overrides):
    base=dict(ticker="ABC",asof=D,market_price=10,current=econ("current"),
       bear=econ("bear",70,10),base=econ("base",180,18),bull=econ("bull",250,23),
       existing_shareholder_dilution_checked=True,price_recognition_checked=True,
       causal_evidence_verified=True,thesis_kill_tests=("No customer qualification",))
    base.update(overrides)
    return MultiplicationCase(**base)
class MultiplicationTests(unittest.TestCase):
    def test_growth_capex_reduces_owner_cash(self):
        s=econ("test",capex=40)
        self.assertLess(calculate(s).owner_cash_after_growth,calculate(econ("test")).owner_cash_after_growth)
    def test_dilution_reduces_eps(self):
        self.assertLess(calculate(econ("diluted",shares=20)).eps,calculate(econ("normal",shares=10)).eps)
    def test_no_auto_trading(self):
        a=assess_multiplication(case())
        self.assertEqual(a.capital_action,"NOT_ASSESSED")
    def test_unknown_price_blocks(self):
        a=assess_multiplication(case(market_price=None))
        self.assertEqual(a.status,"RESEARCH_INCOMPLETE")
    def test_causal_gate(self):
        a=assess_multiplication(case(causal_evidence_verified=False))
        self.assertEqual(a.status,"RESEARCH_INCOMPLETE")
    def test_verified_supplier_only(self):
        a=LinkEvidence("Supplier A","Customer B","qualified","https://exchange.example/filing",D,D,True)
        b=replace(a,supplier="Rumour",independent=False)
        self.assertEqual(independently_verified_suppliers((a,b),D),("Supplier A",))
    def test_future_supplier_date_rejected(self):
        with self.assertRaises(ValueError):
            LinkEvidence("A","B","supply","https://example.org",D+timedelta(days=1),D,True)
if __name__=="__main__": unittest.main()
