"""Synthetic worksheet tests: these are not company forecasts or live signals."""
import unittest
from dataclasses import replace
from modules.decision.fox_valuation_worksheet import Scenario, Worksheet, evaluate_worksheet

def case(**kw):
    return replace(Worksheet(
        ticker="SYNTHETIC",as_of="2026-11-16",price_as_of="2026-11-13",
        market_price=100.0,fully_diluted_shares_cr=10.0,horizon_years=2.0,
        evidence=(("https://nsearchives.nseindia.com/corporate/example.pdf","2026-11-12"),),
        scenarios=(Scenario("bear",50,12,.25,"Stress earnings"),
                   Scenario("base",100,18,.5,"Sustainable earnings"),
                   Scenario("bull",140,20,.25,"Faster conversion")),
        share_count_source="Fully diluted reconciliation",
        profit_bridge="Operating earnings less taxes and minorities",
        cash_conversion_bridge="Receivables and capital spending stressed",
        financing_and_governance_review="Funding and related-party reviewed",
        source_inputs_verified=True),**kw)

class ValuationWorksheetTests(unittest.TestCase):
    def test_scenario_screen_not_trading_add(self):
        d=evaluate_worksheet(case())
        self.assertEqual(d.state,"SCENARIO_SCREEN_PASSED_NOT_ADD")
        self.assertEqual(d.prices,(("bear",60.0),("base",180.0),("bull",280.0)))
        self.assertEqual(d.capital_deployment_rupees,0)
    def test_missing_diluted_share_count_never_estimated(self):
        d=evaluate_worksheet(case(fully_diluted_shares_cr=None))
        self.assertEqual(d.state,"UNDERWRITING_INCOMPLETE")
        self.assertEqual(d.prices,())
    def test_dated_filing_after_decision_rejected(self):
        d=evaluate_worksheet(case(evidence=(("https://example.org/f.pdf","2026-11-17"),)))
        self.assertIn("Look-ahead filing publication date",d.blockers)
    def test_unverified_inputs_cannot_pass(self):
        self.assertEqual(evaluate_worksheet(case(source_inputs_verified=False)).state,"UNDERWRITING_INCOMPLETE")
    def test_economic_failure_is_quantified_not_missing(self):
        low=(Scenario("bear",30,10,.25,"Bear"),Scenario("base",55,12,.5,"Base"),
             Scenario("bull",80,14,.25,"Bull"))
        d=evaluate_worksheet(case(scenarios=low))
        self.assertEqual(d.state,"ECONOMIC_FAILURE")
        self.assertTrue(d.blockers)
    def test_price_fall_can_improve_economics_without_rewriting_assumptions(self):
        high=evaluate_worksheet(case(market_price=160))
        low=evaluate_worksheet(case(market_price=90))
        self.assertGreater(low.base_cagr_pct,high.base_cagr_pct)
        self.assertEqual(high.prices,low.prices)
    def test_missing_rationale_blocks_model(self):
        sc=(Scenario("bear",50,12,.25,""),)+case().scenarios[1:]
        self.assertIn("Unexplained scenario assumptions",evaluate_worksheet(case(scenarios=sc)).blockers)
    def test_probability_error_blocks_model(self):
        sc=(Scenario("bear",50,12,.35,"Bear"),)+case().scenarios[1:]
        self.assertEqual(evaluate_worksheet(case(scenarios=sc)).state,"UNDERWRITING_INCOMPLETE")
if __name__=="__main__":unittest.main()
