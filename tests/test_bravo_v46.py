import unittest
from datetime import date
from bravo_v46.decision import Scenario, Evidence, Verdict, evaluate

class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.s = Scenario(300, 650, 900, .2, .55, .25)
        self.e = Evidence(2, True, True, True, trigger="Next quarterly results", review_date=date(2026, 11, 15))
    def test_add_never_authorizes_trade(self):
        d = evaluate(400, self.s, self.e)
        self.assertEqual(d.verdict, Verdict.ADD)
        self.assertFalse(d.capital_authorized)
    def test_unverified_wait(self):
        e = Evidence(2, False, True, True, trigger="Verify filing", review_date=date(2026, 11, 15))
        self.assertEqual(evaluate(400, self.s, e).verdict, Verdict.WAIT)
    def test_hard_stop_reject(self):
        e = Evidence(2, True, True, True, governance_hard_stop=True)
        self.assertEqual(evaluate(400, self.s, e).verdict, Verdict.REJECT)
    def test_weak_asymmetry_reject(self):
        self.assertEqual(evaluate(620, self.s, self.e).verdict, Verdict.REJECT)
    def test_probabilities_validated(self):
        with self.assertRaises(ValueError):
            evaluate(400, Scenario(300, 650, 900, .5, .5, .5), self.e)
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(float("nan"), self.s, self.e)
    def test_pending_wait(self):
        e = Evidence(2, True, True, True, material_pending=True, trigger="Results", review_date=date(2026, 11, 15))
        self.assertEqual(evaluate(400, self.s, e).verdict, Verdict.WAIT)
    def test_no_causal_evidence_reject(self):
        e = Evidence(0, True, True, True)
        self.assertEqual(evaluate(400, self.s, e).verdict, Verdict.REJECT)

if __name__ == "__main__":
    unittest.main()
