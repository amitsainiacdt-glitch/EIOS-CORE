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

    def test_volume_led_recovery_detected(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=None,
                                sequential_revenue_growth_pct=None,
                                operating_volume_growth_yoy_pct=24.58,
                                distribution_network_growth_yoy_pct=34))
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)
        self.assertEqual(r.capital_deployment_rupees,0)

    def test_missing_dated_zone_blocks_add_but_not_investigation(self):
        r=detect_inflection(case(fixed_zone_exists=False,
                                 verified_diluted_valuation=False))
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)
        self.assertTrue(any("Fixed dated research valuation zone" in b for b in r.blockers))
        self.assertEqual(r.capital_deployment_rupees,0)

    def test_exceptional_single_signal_triggers_investigation(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=35,
                sequential_revenue_growth_pct=None,
                exceptional_signal_verified=True,
                independent_exceptional_source_url="https://www.crisil.com/research/order-verified.pdf"))
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)
        self.assertEqual(r.capital_deployment_rupees,0)

    def test_single_signal_without_distinct_source_does_not_trigger(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=35,
                sequential_revenue_growth_pct=None,
                exceptional_signal_verified=True,
                independent_exceptional_source_url="https://nsearchives.nseindia.com/test.pdf"))
        self.assertEqual(r.action,InflectionAction.NO_NEW_INFLECTION)

    def test_network_expansion_alone_not_enough(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=None,
                                sequential_revenue_growth_pct=None,
                                distribution_network_growth_yoy_pct=34))
        self.assertEqual(r.action,InflectionAction.NO_NEW_INFLECTION)

    def test_sequential_signal_can_pair_with_milestone(self):
        r=detect_inflection(case(order_intake_growth_yoy_pct=None,
                                verified_capacity_or_customer_milestone=True))
        self.assertEqual(r.action,InflectionAction.INVESTIGATE)


if __name__=="__main__":
    unittest.main()
