import unittest
from datetime import date, timedelta
from modules.discovery.pre_inflection import Evidence, InflectionCase, assess, empty_scan_report

class TestPreInflection(unittest.TestCase):
    def case(self, **kwargs):
        d=date(2026,10,19)
        values=dict(ticker="TEST",sector="Industrials",asof=d,
            evidence=(Evidence("Commissioned facility","https://example.org/exchange",d,d,True),),
            causal_chain="Customer -> dispatch -> cash",next_2_to_4_quarter_trigger="Offtake",
            cash_earnings_bridge="Output x contribution less financing and working capital",
            expectation_gap="Capacity economics underappreciated",
            contradictions=("Customer concentration",),kill_tests=("No dispatches",),
            price_recognition_checked=True,materially_rerated=False,thesis_broken=False,
            temporary_imperfections_explained=True,
            scoring={"causal":.9,"cash_earnings":.9,"expectation_gap":.9,"valuation":.9,"resilience":.8,"timing":.8})
        values.update(kwargs)
        return InflectionCase(**values)
    def test_positive_research_never_trades(self):
        result=assess(self.case())
        self.assertEqual(result.classification,"Buy-zone Candidate")
        self.assertEqual(result.capital_action,"NOT_ASSESSED")
    def test_price_recognition_overrides(self):
        self.assertEqual(assess(self.case(materially_rerated=True)).classification,"Too Late")
    def test_thesis_break_overrides(self):
        self.assertEqual(assess(self.case(thesis_broken=True)).classification,"Reject")
    def test_future_data_excluded(self):
        d=date(2026,10,19)
        evidence=Evidence("Future event","https://example.org/future",d+timedelta(days=1),d+timedelta(days=1),True)
        self.assertEqual(assess(self.case(evidence=(evidence,))).classification,"Research Now")
    def test_no_corroboration_no_promotion(self):
        e=Evidence("Company says so","https://example.org/company",date(2026,10,19),date(2026,10,19),False)
        self.assertEqual(assess(self.case(evidence=(e,))).classification,"Research Now")
    def test_empty_scan(self):
        self.assertIn("No fresh high-conviction",empty_scan_report(date(2026,10,19),tuple())["summary"])
    def test_capital_action_forbidden(self):
        with self.assertRaises(ValueError): assess(self.case(capital_action="BUY"))
if __name__=="__main__": unittest.main()
