import unittest
import hashlib

from modules.external_intelligence.neutral_discovery import (
    NeutralDiscoveryCandidate, NeutralDiscoveryFactor, NeutralDiscoveryFactorKind, NeutralDiscoveryUniverse,
)
from modules.external_intelligence.neutral_discovery_service import NeutralDiscoveryService


class NeutralDiscoveryServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = NeutralDiscoveryService()

    @staticmethod
    def candidate(ticker, sector, points, *, holding=False, watch=False, discussed=False):
        return NeutralDiscoveryCandidate(
            ticker, f"{ticker} Limited", sector, hashlib.sha256(ticker.encode()).hexdigest(),
            (NeutralDiscoveryFactor(NeutralDiscoveryFactorKind.EXPECTED_INFORMATION_GAIN, points,
                                    "Public causal evidence could materially resolve the research question."),),
            holding, watch, discussed)

    def universe(self, candidates, sectors=("AUTOS", "CHEMICALS"), **changes):
        values = dict(schema_version=1, universe_id="INDIA-EQUITY", target_sector_ids=sectors,
                      candidates=tuple(candidates), selection_limit=2, public_information_only=True,
                      non_authority_statement=NeutralDiscoveryService.NON_AUTHORITY)
        values.update(changes)
        return NeutralDiscoveryUniverse(**values)

    def test_unfamiliar_company_outranks_holding_on_objective_evidence(self):
        result = self.service.select(self.universe((
            self.candidate("OWNED", "AUTOS", 20, holding=True, watch=True, discussed=True),
            self.candidate("NEWCO", "CHEMICALS", 80),
        )))
        self.assertEqual(result.selected_tickers[0], "NEWCO")
        self.assertEqual(result.anchor_context_tickers, ("OWNED",))
        self.assertFalse(result.creates_opportunity)

    def test_flipping_all_anchor_flags_cannot_change_selection_or_fingerprint(self):
        plain = (self.candidate("AUTO", "AUTOS", 60), self.candidate("CHEM", "CHEMICALS", 70))
        anchored = (self.candidate("AUTO", "AUTOS", 60, holding=True, discussed=True),
                    self.candidate("CHEM", "CHEMICALS", 70, watch=True))
        first = self.service.select(self.universe(plain))
        second = self.service.select(self.universe(anchored))
        self.assertEqual(first.selected_tickers, second.selected_tickers)
        self.assertEqual(first.priority_by_ticker, second.priority_by_ticker)
        self.assertEqual(first.selection_fingerprint, second.selection_fingerprint)

    def test_missing_declared_sector_is_visible_and_holds_universe_readiness(self):
        result = self.service.select(self.universe((self.candidate("AUTO", "AUTOS", 60),)))
        self.assertEqual(result.status, "HOLD_INCOMPLETE_UNIVERSE")
        self.assertEqual(result.missing_sector_ids, ("CHEMICALS",))

    def test_candidates_outside_declared_universe_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the declared universe"):
            self.service.select(self.universe((self.candidate("BANK", "BANKING", 50),)))

    def test_only_predeclared_objective_factor_types_are_accepted(self):
        invalid = NeutralDiscoveryCandidate(
            "FAV", "Favourite Limited", "AUTOS", "f" * 64,
            (("PORTFOLIO_HOLDING", 100, "Familiar company"),), True, False, True)
        with self.assertRaisesRegex(ValueError, "factor is invalid"):
            self.service.select(self.universe((invalid, self.candidate("CHEM", "CHEMICALS", 20))))

    def test_ties_are_deterministic_not_based_on_input_or_familiarity(self):
        a = self.candidate("AAA", "AUTOS", 50, holding=True)
        z = self.candidate("ZZZ", "CHEMICALS", 50)
        first = self.service.select(self.universe((z, a)))
        second = self.service.select(self.universe((a, z)))
        self.assertEqual(first.selected_tickers, ("AAA", "ZZZ"))
        self.assertEqual(first.selected_tickers, second.selected_tickers)
        self.assertEqual(first.selection_fingerprint, second.selection_fingerprint)


if __name__ == "__main__":
    unittest.main()
