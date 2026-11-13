"""Mechanics-only tests using synthetic prices, NOT predictive validation."""
import unittest
from datetime import date,timedelta
from modules.validation.fox_backtest import Event,PriceBar,replay_event,summarize

def case(action="INVESTIGATE",published="2025-01-02T19:00:00+05:30",cutoff=None):
    return Event("e1","TEST",published,"https://nsearchives.nseindia.com/test.pdf",
                 action,cutoff or published)
def prices(n=270):
    d=date(2025,1,2)
    return {"TEST":[PriceBar((d+timedelta(days=i)).isoformat(),100+i,100+i)
                    for i in range(n)]}

class FoxBacktestTests(unittest.TestCase):
    def test_next_session_for_after_hours(self):
        r=replay_event(case(),prices())
        self.assertEqual((r.entry_session,r.entry_price),("2025-01-03",101))
    def test_premarket_also_next_session_conservative(self):
        r=replay_event(case(published="2025-01-02T08:00:00+05:30"),prices())
        self.assertEqual(r.entry_session,"2025-01-03")
    def test_no_naive_publication(self):
        with self.assertRaisesRegex(ValueError,"timezone"):
            replay_event(case(published="2025-01-02T19:00:00"),prices())
    def test_evidence_cutoff_blocks_hindsight(self):
        with self.assertRaisesRegex(ValueError,"Look-ahead"):
            replay_event(case(cutoff="2025-01-04T12:00:00+05:30"),prices())
    def test_reject_unverified_adjustment(self):
        p=prices()
        p["TEST"][2]=PriceBar("2025-01-04",102,102,False)
        with self.assertRaisesRegex(ValueError,"Unverified"):
            replay_event(case(),p)
    def test_same_session_open_never_used(self):
        self.assertNotEqual(replay_event(case(),prices()).entry_session,"2025-01-02")
    def test_63_session_compound_return_cost(self):
        r=replay_event(case(),prices())
        self.assertAlmostEqual(r.returns_percent[63],100*((164/101)*0.996-1),places=3)
    def test_right_censor_not_failure(self):
        r=replay_event(case(),prices(70))
        self.assertIsNotNone(r.returns_percent[63])
        self.assertIsNone(r.returns_percent[126])
        self.assertEqual(r.status,"PARTIAL")
    def test_no_fabricated_price(self):
        r=replay_event(case(),{})
        self.assertEqual(r.status,"UNSCORABLE")
        self.assertIsNone(r.entry_price)
    def test_cutoff_prevents_future_outcome(self):
        r=replay_event(case(),prices(),as_of_session="2025-01-10")
        self.assertTrue(all(x is None for x in r.returns_percent.values()))
    def test_benchmark_requires_same_dates(self):
        p=prices()
        bench={"NIFTY500":[PriceBar(x.session,100,100) for x in p["TEST"]]}
        r=replay_event(case(),p,bench)
        self.assertAlmostEqual(r.excess_return_percent[63],62.127,delta=.01)
    def test_no_censored_false_failures(self):
        s=summarize([replay_event(case(),prices(70))],252)
        self.assertEqual(s["observed_total"],0)
        self.assertIsNone(s["flagged_hit_rate_percent"])
    def test_nonflagged_controls_retained(self):
        s=summarize([replay_event(case(action="NO NEW INFLECTION"),prices())],63)
        self.assertEqual((s["flagged_observed"],s["nonflagged_observed"]),(0,1))
    def test_zero_deployment_all_research_actions(self):
        for action in ("INVESTIGATE","NO NEW INFLECTION","REJECT"):
            self.assertEqual(replay_event(case(action=action),prices()).capital_deployment_rupees,0)

if __name__=="__main__":
    unittest.main()
