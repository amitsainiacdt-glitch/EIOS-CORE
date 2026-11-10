"""BRAVO v4.8 pilot tests: independent discovery, completeness, and anti-hindsight."""
import unittest
from datetime import date
from modules.discovery.bravo_v48_pilot import (
    DiscoveryLane, DiscoveryLead, HistoricalReplay, discover, complete,
    audit_replay, measure_outcomes,
)
from modules.decision.bravo_v47_calibration import BravoEvidence, AddLane, BravoAction


def lead(name="FRESH", lane=DiscoveryLane.OPERATING_REPAIR, **kw):
    d = dict(ticker=name, lane=lane, observed_on="2026-11-05",
             source_urls=("https://www.bseindia.com/test",),
             what_broke="Underutilisation", repair_mechanism="New plant dispatches",
             leading_signals=("Verified commissioning",), next_trigger="Next dispatch report")
    d.update(kw)
    return DiscoveryLead(**d)


def evidence(**kw):
    d = dict(ticker="FRESH", lane=AddLane.EIP, as_of_date="2026-11-05",
             filing_urls=("https://www.nseindia.com/test",),
             causal_indicators=("Capacity commissioned", "Confirmed dispatches"),
             price=100.0, base_value=210.0, bear_value=65.0,
             bull_value=300.0, horizon_years=2.5,
             diluted_basis_verified=True, cash_financing_reviewed=True,
             governance_reviewed=True, permanent_loss_bounded=True)
    d.update(kw)
    return BravoEvidence(**d)


class PilotTests(unittest.TestCase):
    def test_unfamiliar_leads_before_anchors(self):
        report=discover((lead("OLD", familiar_registry_name=True),
                         lead("NEW")), date(2026,11,6))
        self.assertEqual(report.investigated[0].ticker, "NEW")
        self.assertEqual(report.novel_leads, 1)

    def test_three_lanes_measured(self):
        report=discover(tuple(lead(str(i), lane) for i,lane in enumerate(DiscoveryLane)),
                        date(2026,11,6))
        self.assertFalse(report.missing_lanes)

    def test_missing_lane_is_disclosed(self):
        report=discover((lead(),),date(2026,11,6))
        self.assertEqual(len(report.missing_lanes),2)

    def test_missing_cash_does_not_veto_discovery(self):
        self.assertEqual(len(discover((lead(),),date(2026,11,6)).investigated),1)

    def test_future_signal_rejected(self):
        r=discover((lead(observed_on="2027-01-01"),), date(2026,11,6))
        self.assertEqual(len(r.investigated),0)

    def test_duplicate_universe_is_counted(self):
        r=discover((lead("ABC"),lead("ABC")),date(2026,11,6))
        self.assertEqual(len(r.rejected_early),1)

    def test_no_price_only_recovery(self):
        r=discover((lead(repair_mechanism=""),),date(2026,11,6))
        self.assertEqual(len(r.investigated),0)

    def test_decision_completion_add_has_zero_deployment(self):
        p=complete(evidence(), "", "")
        self.assertEqual(p.decision.action,BravoAction.EIP_ADD)
        self.assertEqual(p.decision.capital_deployment_rupees,0)

    def test_wait_requires_specific_follow_up(self):
        with self.assertRaises(ValueError):
            complete(evidence(diluted_basis_verified=False), "", "")
        p=complete(evidence(diluted_basis_verified=False),
                   "Reconcile QIP shares", "2026-12-01")
        self.assertIn("diluted",p.incomplete_reason)

    def test_no_lookahead(self):
        r=HistoricalReplay("ABC","2026-11-05",("2026-11-06",),
                           "2026-11-05","2027-01-01",30)
        self.assertEqual(audit_replay(r),"INVALID_LOOKAHEAD_EVIDENCE")

    def test_pending_outcome_is_not_false_positive(self):
        r=HistoricalReplay("ABC","2026-11-05",("2026-11-04",),
                           "2026-11-05","2027-01-01",None)
        self.assertEqual(audit_replay(r),"PENDING_OUTCOME")
        self.assertIsNone(measure_outcomes((r,))["false_positives"])


if __name__=="__main__":
    unittest.main()
