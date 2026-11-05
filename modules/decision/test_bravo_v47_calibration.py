"""Regression tests for BRAVO v4.7 decision calibration."""
import unittest
from modules.decision.bravo_v47_calibration import (
    AddLane, BravoAction, BravoEvidence, evaluate_bravo,
)


def case(**overrides):
    data = dict(ticker="EXAMPLE", lane=AddLane.EIP, as_of_date="2026-11-05",
                filing_urls=("https://www.nseindia.com/example",),
                causal_indicators=("Commissioning verified", "Dispatches verified"),
                price=100, base_value=200, bear_value=60, bull_value=260,
                horizon_years=2.5, diluted_basis_verified=True,
                cash_financing_reviewed=True, governance_reviewed=True,
                permanent_loss_bounded=True)
    data.update(overrides)
    return BravoEvidence(**data)


class BravoCalibrationTests(unittest.TestCase):
    def test_repairable_cash_weakness_does_not_auto_veto(self):
        x = evaluate_bravo(case(temporary_weaknesses=("Working capital absorption",),
                                weakness_repair_mechanism="Receivables collection in two quarters"))
        self.assertEqual(x.action, BravoAction.EIP_ADD)
        self.assertEqual(x.capital_deployment_rupees, 0)

    def test_governance_fatal_risk_rejects(self):
        x = evaluate_bravo(case(fatal_risk=True, fatal_risk_reason="Unfinanceable debt"))
        self.assertEqual(x.action, BravoAction.REJECT)

    def test_missing_dilution_blocks_add(self):
        x = evaluate_bravo(case(diluted_basis_verified=False))
        self.assertEqual(x.action, BravoAction.WAIT)
        self.assertTrue(any("diluted" in s for s in x.blockers))

    def test_weak_asymmetry_blocks_add(self):
        x = evaluate_bravo(case(base_value=120, bear_value=60))
        self.assertEqual(x.action, BravoAction.WAIT)

    def test_not_enough_leading_signals_blocks(self):
        x = evaluate_bravo(case(causal_indicators=("Orders",)))
        self.assertEqual(x.action, BravoAction.WAIT)

    def test_no_fabricated_valuation(self):
        x = evaluate_bravo(case(base_value=None))
        self.assertEqual(x.action, BravoAction.WAIT)
        self.assertIsNone(x.base_cagr_percent)

    def test_value_and_special_situation_lanes(self):
        for lane, expected in ((AddLane.VALUE, BravoAction.VALUE_ADD),
                               (AddLane.SPECIAL_SITUATION, BravoAction.SPECIAL_SITUATION_ADD)):
            self.assertEqual(evaluate_bravo(case(lane=lane)).action, expected)

    def test_research_never_deploys_capital(self):
        self.assertEqual(evaluate_bravo(case(approval_to_trade=True)).capital_deployment_rupees, 0)


if __name__ == "__main__":
    unittest.main()
