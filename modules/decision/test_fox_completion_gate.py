"""Synthetic FOX completion tests: no live investment decisions."""
import unittest
from dataclasses import replace
from modules.decision.fox_completion_gate import CompletionCase, complete_case, queue_audit
from modules.decision.fox_valuation_worksheet import Worksheet, Scenario


def sample_case(**changes):
    w = Worksheet(
        ticker="SYNTH", as_of="2026-11-18", price_as_of="2026-11-17",
        market_price=100, fully_diluted_shares_cr=10, horizon_years=2,
        evidence=(("https://nsearchives.nseindia.com/corporate/synthetic.pdf","2026-11-16"),),
        scenarios=(Scenario("bear",50,12,.25,"Cash stress"),
                   Scenario("base",100,18,.5,"Normalised operating cash"),
                   Scenario("bull",140,20,.25,"Faster operating ramp")),
        share_count_source="Issued plus all outstanding options",
        profit_bridge="Parent PAT less minority and non-recurring gains",
        cash_conversion_bridge="Receivables, capex and leases tested",
        financing_and_governance_review="Funding, governance and guarantees evaluated",
        source_inputs_verified=True)
    base=CompletionCase(
        ticker="SYNTH",lane="EIP",first_seen="2026-11-01",
        last_reviewed="2026-11-18",owner="FOX research",
        primary_source_urls=("https://nsearchives.nseindia.com/corporate/synthetic.pdf",),
        next_evidence_event="Confirm customer cash collection",
        review_due="2026-11-20",exact_missing_inputs=(),
        worksheet=w)
    return replace(base,**changes)


class CompletionGateTests(unittest.TestCase):
    def test_math_pass_alone_cannot_issue_add(self):
        result=complete_case(sample_case(),"2026-11-18")
        self.assertEqual(result.state,"UNDERWRITING_INCOMPLETE")
        self.assertTrue(result.valuation_completed)
        self.assertIn("Independent causal", " ".join(result.blockers))
        self.assertEqual(result.capital_deployment_rupees,0)

    def test_no_worksheet_never_invents_target(self):
        result=complete_case(sample_case(worksheet=None),"2026-11-18")
        self.assertEqual(result.state,"UNDERWRITING_INCOMPLETE")
        self.assertFalse(result.valuation_completed)

    def test_quantified_economic_failure_not_generic_wait(self):
        weak=(Scenario("bear",25,10,.25,"Downside"),
              Scenario("base",50,12,.5,"Base"),
              Scenario("bull",70,15,.25,"Bull"))
        c=sample_case(worksheet=replace(sample_case().worksheet,scenarios=weak))
        result=complete_case(c,"2026-11-18")
        self.assertEqual(result.state,"ECONOMIC_FAILURE")
        self.assertTrue(result.valuation_completed)

    def test_locked_zone_cannot_move_without_fundamental_source(self):
        c=sample_case(original_zone=(80,90),proposed_zone=(65,75))
        r=complete_case(c,"2026-11-18")
        self.assertEqual(r.state,"UNDERWRITING_INCOMPLETE")
        self.assertIn("Original buy-zone immutable", " ".join(r.blockers))

    def test_price_drop_alone_preserves_zone_and_improves_cagr(self):
        from modules.decision.fox_valuation_worksheet import evaluate_worksheet
        base=sample_case()
        cheaper=replace(base.worksheet,market_price=80)
        self.assertGreater(evaluate_worksheet(cheaper).base_cagr_pct,
                           evaluate_worksheet(base.worksheet).base_cagr_pct)
        self.assertEqual(base.original_zone,base.proposed_zone)

    def test_overdue_and_stale_audit(self):
        c=sample_case()
        a=queue_audit((c,),"2026-11-18")
        self.assertEqual(a["issuers"],1)
        self.assertEqual(a["over_7_days_open"],1)
        self.assertEqual(a["over_14_days_open"],1)
        self.assertEqual(a["research_adds"],0)
        self.assertEqual(a["capital_deployment_rupees"],0)

    def test_expired_review_requires_accountability(self):
        c=sample_case(review_due="2026-11-10")
        r=complete_case(c,"2026-11-18")
        self.assertEqual(r.state,"UNDERWRITING_INCOMPLETE")
        self.assertIn("Review overdue", " ".join(r.blockers))


if __name__ == "__main__":
    unittest.main()
