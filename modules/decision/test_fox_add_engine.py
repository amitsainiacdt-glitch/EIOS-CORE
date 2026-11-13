"""FOX ADD decisions are research classifications only; synthetic fixtures test gates."""
import unittest
from dataclasses import replace
from modules.decision.fox_add_engine import (
 FoxAction,FoxUnderwriting,RiskClass,RiskItem,ValuationZone,evaluate_fox)

def case(**kw):
 z=ValuationZone(1,"2026-10-01",90,110,100,"thesis-v1",
                 "https://nsearchives.nseindia.com/corporate/example.pdf")
 e=FoxUnderwriting(
  ticker="TEST",lane="EIP",as_of="2026-11-10",price_as_of="2026-11-09",
  price=100,primary_urls=("https://nsearchives.nseindia.com/corporate/example.pdf",),
  causal_signals=("Orders rising","Sequential margins recovering"),
  horizon_years=2.5,bear_value=70,base_value=200,bull_value=260,
  diluted_share_count_verified=True,financing_survival_verified=True,
  governance_evaluated=True,cash_conversion_evaluated=True,
  valuation_evidence_verified=True,recovery_mechanism="Order execution in two quarters",
  next_kill_test="Order conversion under 50%",catalyst_date="2027-03-31",research_zone=z)
 return replace(e,**kw)

class FOXAddTests(unittest.TestCase):
 def test_eip_research_add_not_trade(self):
  d=evaluate_fox(case())
  self.assertEqual(d.action,FoxAction.EIP_ADD)
  self.assertEqual(d.capital_deployment_rupees,0)
 def test_bounded_temporary_risk_allows_smaller_add(self):
  risk=RiskItem("temporary working capital",RiskClass.BOUNDED_UNRESOLVED,8,
                "Receivables worsen beyond 120 days")
  d=evaluate_fox(case(risk_items=(risk,)))
  self.assertEqual(d.action,FoxAction.EIP_ADD)
  self.assertEqual(d.research_risk_budget_pct,1.0)
 def test_unbounded_governance_reject(self):
  d=evaluate_fox(case(risk_items=(RiskItem("unbounded RPT",RiskClass.THESIS_BREAKING),)))
  self.assertEqual(d.action,FoxAction.REJECT)
 def test_price_only_zone_revision_rejected(self):
  prior=case().research_zone
  changed=replace(prior,version=2,low=75,high=90)
  d=evaluate_fox(case(research_zone=changed,previous_zone=prior,price=80))
  self.assertEqual(d.action,FoxAction.WAIT)
  self.assertTrue(any("revision prohibited" in x for x in d.blockers))
 def test_fundamental_zone_revision_allowed(self):
  prior=case().research_zone
  changed=replace(prior,version=2,low=80,high=120,evidence_changed=True,
                  revision_reason="Audited EPS upgrade")
  self.assertEqual(evaluate_fox(case(research_zone=changed,previous_zone=prior)).action,FoxAction.EIP_ADD)
 def test_cheaper_price_improves_ratio_no_zone_movement(self):
  x=evaluate_fox(case(price=100))
  y=evaluate_fox(case(price=95))
  self.assertGreater(y.upside_downside_ratio,x.upside_downside_ratio)
  self.assertEqual(y.action,FoxAction.EIP_ADD)
 def test_below_fixed_zone_with_intact_thesis_can_add(self):
  d=evaluate_fox(case(price=80))
  self.assertEqual(d.action,FoxAction.EIP_ADD)
  self.assertEqual(d.capital_deployment_rupees,0)
 def test_below_zone_with_missing_evidence_still_waits(self):
  d=evaluate_fox(case(price=80,financing_survival_verified=False))
  self.assertEqual(d.action,FoxAction.WAIT)
  self.assertIn("Financing / survival bridge unverified",d.evidence_gaps)
 def test_evidence_and_economics_reported_separately(self):
  d=evaluate_fox(case(price=120,diluted_share_count_verified=False))
  self.assertEqual(d.action,FoxAction.WAIT)
  self.assertIn("Fully diluted equity denominator unverified",d.evidence_gaps)
  self.assertIn("Price above locked research zone ceiling",d.economic_failures)
 def test_below_zone_cannot_override_fatal_risk(self):
  r=RiskItem("Unbounded financing",RiskClass.THESIS_BREAKING)
  self.assertEqual(evaluate_fox(case(price=80,risk_items=(r,))).action,FoxAction.REJECT)
 def test_below_zone_poor_base_case_still_waits(self):
  d=evaluate_fox(case(price=80,bear_value=50,base_value=100,bull_value=130))
  self.assertEqual(d.action,FoxAction.WAIT)
  self.assertTrue(d.economic_failures)
 def test_outside_fixed_zone_wait(self):
  d=evaluate_fox(case(price=120))
  self.assertEqual(d.action,FoxAction.WAIT)
 def test_no_causal_signal_wait(self):
  self.assertEqual(evaluate_fox(case(causal_signals=("Orders",))).action,FoxAction.WAIT)
 def test_missing_diluted_denominator_wait(self):
  self.assertEqual(evaluate_fox(case(diluted_share_count_verified=False)).action,FoxAction.WAIT)
 def test_unquantified_bounded_risk_wait(self):
  risk=RiskItem("Cash conversion",RiskClass.BOUNDED_UNRESOLVED)
  self.assertEqual(evaluate_fox(case(risk_items=(risk,))).action,FoxAction.WAIT)
 def test_future_price_is_not_valid(self):
  self.assertEqual(evaluate_fox(case(price_as_of="2026-11-12")).action,FoxAction.WAIT)
 def test_weighted_value_gate(self):
  self.assertEqual(evaluate_fox(case(probabilities=(.95,.04,.01),
                                      bear_value=70,base_value=200,bull_value=260)).action,FoxAction.WAIT)
 def test_special_situation_lane(self):
  self.assertEqual(evaluate_fox(case(lane="SPECIAL SITUATION")).action,FoxAction.SPECIAL_SITUATION_ADD)
 def test_low_return_gate(self):
  self.assertEqual(evaluate_fox(case(base_value=125,bull_value=160)).action,FoxAction.WAIT)
 def test_missing_price_never_add(self):
  self.assertEqual(evaluate_fox(case(price=None)).action,FoxAction.WAIT)

if __name__=="__main__":unittest.main()
