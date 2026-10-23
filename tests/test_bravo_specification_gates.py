"""BRAVO EIOS v3 specification-level gating fixtures. NOT production integration tests."""
from dataclasses import dataclass

@dataclass
class Candidate:
    source_primary: bool=True
    independent_corroboration: bool=True
    quote_current: bool=True
    shares_verified: bool=True
    event_known_at_decision: bool=True
    attributable_orders_verified: bool=True
    funding_verified: bool=True
    reasonable_downside: bool=True
    recoverable_working_capital: bool=True
    structural_kill: bool=False
    has_causal_event: bool=True

def evaluate(c):
    if c.structural_kill:
        return "REJECT"
    required = (c.source_primary,c.independent_corroboration,c.quote_current,
                c.shares_verified,c.event_known_at_decision,
                c.attributable_orders_verified,c.funding_verified,
                c.reasonable_downside,c.recoverable_working_capital,c.has_causal_event)
    return "ADD" if all(required) else "WAIT"

def test_specification_gates():
    fixtures = [
      ("verified", Candidate(), "ADD"),
      ("stale_quote", Candidate(quote_current=False), "WAIT"),
      ("unverified_dilution", Candidate(shares_verified=False), "WAIT"),
      ("lookahead", Candidate(event_known_at_decision=False), "WAIT"),
      ("joint_venture_order", Candidate(attributable_orders_verified=False), "WAIT"),
      ("unfunded_capex", Candidate(funding_verified=False), "WAIT"),
      ("poor_downside", Candidate(reasonable_downside=False), "WAIT"),
      ("uncollected_receivables", Candidate(recoverable_working_capital=False), "WAIT"),
      ("temporary_negative_cfo", Candidate(recoverable_working_capital=True), "ADD"),
      ("uncorroborated_press_release", Candidate(independent_corroboration=False), "WAIT"),
      ("thesis_kill", Candidate(structural_kill=True), "REJECT"),
      ("no_causal_evidence", Candidate(has_causal_event=False), "WAIT"),
    ]
    for name, candidate, expected in fixtures:
        actual = evaluate(candidate)
        assert actual == expected, f"{name}: {actual}, expected {expected}"

if __name__ == "__main__":
    test_specification_gates()
    print("12/12 specification gate fixtures passed; pipeline integration NOT tested")
