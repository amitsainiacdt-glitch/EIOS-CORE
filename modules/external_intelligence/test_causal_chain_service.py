import unittest

from modules.external_intelligence.causal_chain import CausalChainAssessment, CausalChainLink, CausalChainStage
from modules.external_intelligence.causal_chain_service import CausalChainService
from modules.external_intelligence.sector_causal_indicator import CausalEffectDirection, SectorCausalIndicatorDefinition
from modules.external_intelligence.sector_causal_indicator_registry import SectorCausalIndicatorRegistry


class CausalChainServiceTests(unittest.TestCase):
    def setUp(self):
        definition = SectorCausalIndicatorDefinition(
            1, "CHEMICAL-SPREAD", 1, "Chemical spread", ("CHEMICALS",), ("PRICE",),
            "product spread", CausalEffectDirection.SUPPORTIVE, 2, 4,
            "Input cost falls faster than selling price", ("margin",), ("PROCESS_MANUFACTURER",),
            ("commodity exchange",), ("industry association",), "source family", 2, 2, 60,
            ("temporary outage",), ("selling price declines faster",), ("spread reverses",), True, (),
        )
        registry = SectorCausalIndicatorRegistry()
        registry.register(definition)
        self.service = CausalChainService(registry)

    def assessment(self, **changes):
        stages = tuple(CausalChainStage)
        links = tuple(
            CausalChainLink(stage, f"Statement for {stage.value}", f"Mechanism for {stage.value}",
                            ("TE-1",) if index == 0 else ())
            for index, stage in enumerate(stages)
        )
        values = dict(
            schema_version=1, chain_id="CHAIN-1", entity="Example Chemicals", sector_id="CHEMICALS",
            causal_indicator_ids=("CHEMICAL-SPREAD",), input_temporal_evidence_ids=("TE-1",),
            links=links, expected_lead_time_quarters=(2, 4), assumptions=("Selling prices remain broadly stable",),
            uncertainty_statement="Transmission may be delayed by existing inventory.", public_information_only=True,
            non_authority_statement=CausalChainService.NON_AUTHORITY,
        )
        values.update(changes)
        return CausalChainAssessment(**values)

    def test_accepts_complete_ordered_public_chain(self):
        self.assertEqual(self.service.validate(self.assessment()).chain_id, "CHAIN-1")

    def test_rejects_missing_or_reordered_stage(self):
        links = self.assessment().links
        with self.assertRaisesRegex(ValueError, "each required stage"):
            self.service.validate(self.assessment(links=links[:-1]))
        with self.assertRaisesRegex(ValueError, "each required stage"):
            self.service.validate(self.assessment(links=(links[1], links[0], *links[2:])))

    def test_rejects_out_of_scope_or_unused_evidence(self):
        links = list(self.assessment().links)
        links[0] = CausalChainLink(links[0].stage, links[0].statement, links[0].mechanism, ("TE-OTHER",))
        with self.assertRaisesRegex(ValueError, "outside the governed inputs"):
            self.service.validate(self.assessment(links=tuple(links)))
        with self.assertRaisesRegex(ValueError, "must be used"):
            self.service.validate(self.assessment(input_temporal_evidence_ids=("TE-1", "TE-2")))

    def test_rejects_non_public_or_cross_sector_chain(self):
        with self.assertRaisesRegex(ValueError, "public information only"):
            self.service.validate(self.assessment(public_information_only=False))
        with self.assertRaisesRegex(ValueError, "outside chain sector"):
            self.service.validate(self.assessment(sector_id="BANKING"))

    def test_does_not_accept_empty_reasoning_or_invalid_lead_time(self):
        links = list(self.assessment().links)
        links[2] = CausalChainLink(links[2].stage, " ", links[2].mechanism, ())
        with self.assertRaisesRegex(ValueError, "statement"):
            self.service.validate(self.assessment(links=tuple(links)))
        with self.assertRaisesRegex(ValueError, "lead-time range"):
            self.service.validate(self.assessment(expected_lead_time_quarters=(4, 2)))


if __name__ == "__main__":
    unittest.main()
