"""Point-in-time regression checks for the v4.8 research triage helper."""
import unittest
from modules.decision.bravo_v48_inflection import InflectionEvidence, InflectionAction, detect_inflection


def case(**override):
    d=dict(ticker="TEST",as_of_date="2026-11-06",price_as_of_date="2026-11-06",
           price=1260,source_urls=("https://nsearchives.nseindia.com/test.pdf",),
           order_intake_growth_yoy_pct=35,sequential_revenue_growth_pct=46,
           share_drawdown_adjusted_pct=-40,funding_survival_reviewed=True,
           downside_bounded=True,verified_diluted_valuation=False,fixed_zone_exists=False)
    d.update(override)
    return InflectionEvidence(**d)


class InflectionTests(unittest.TestCase):
    def test_early_recovery_triggers_investigate_not_buy(self):
        r=detect_inflection(case())
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)
        self.assertEqual(r.capital_deployment_rupees,0)
        self.assertIn("Diluted valuation not verified: cannot issue ADD",r.blockers)

    def test_price_fall_alone_never_triggers(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=None,
                      sequential_revenue_growth_pct=None))
        self.assertEqual(r.action,InflectionAction.NO_NEW_INFLECTION)

    def test_fatal_risk_rejects(self):
        self.assertEqual(detect_inflection(case(fatal_contradiction=True,
                              fatal_reason="Unfinanceable debt")).action,InflectionAction.REJECT)

    def test_no_lookahead(self):
        r=detect_inflection(case(as_of_date="2026-11-06",price_as_of_date="2026-11-13"))
        self.assertEqual(r.action,InflectionAction.NO_NEW_INFLECTION)

    def test_unverified_sources_block(self):
        self.assertEqual(detect_inflection(case(source_urls=())).action,
                         InflectionAction.NO_NEW_INFLECTION)

    def test_irrelevant_bearer_doesnt_auto_add(self):
        r=detect_inflection(case(verified_diluted_valuation=True,fixed_zone_exists=True))
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)
        self.assertEqual(r.capital_deployment_rupees,0)

    def test_sequential_signal_can_pair_with_milestone(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=None,
                                verified_capacity_or_customer_milestone=True))
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)


if __name__=="__main__":
    unittest.main()
