"""
EIOS
Everest Investment Operating System

External Intelligence Duplicate Boundary Test
==============================================

Validates that duplicate external information is rejected
at the Observation layer before reaching IntelligenceMesh.

Architecture:

External Research
        ↓
ObservationEngine
        ↓
ObservationNoveltyEngine
        ↓
NEW observation only
        ↓
ExternalIntelligenceAdapter
        ↓
IntelligenceMesh
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.external_intelligence_adapter import (
    ExternalIntelligenceAdapter,
)

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.observation.observation_persistence import (
    ObservationPersistence,
)

from modules.observation.observation_registry import (
    ObservationRegistry,
)

from modules.research_context.research_context import (
    ResearchContext,
)


def main():

    print("=" * 60)
    print(
        "EIOS EXTERNAL INTELLIGENCE "
        "DUPLICATE BOUNDARY TEST"
    )
    print("=" * 60)

    # ======================================================
    # ISOLATED TEST ENVIRONMENT
    # ======================================================

    with TemporaryDirectory() as temp_dir:

        observation_path = (
            Path(temp_dir)
            / "observations.json"
        )

        persistence = ObservationPersistence(
            observation_path
        )

        # ==================================================
        # SETUP
        # ==================================================

        context = ResearchContext()

        registry = ObservationRegistry()

        observation_engine = ObservationEngine(
            registry=registry,
            persistence=persistence,
        )

        adapter = ExternalIntelligenceAdapter(
            context
        )

        # ==================================================
        # TEST 1 — FIRST OBSERVATION
        # ==================================================

        first = observation_engine.observe(
            title="Industrial capacity expansion",
            description=(
                "The company announced expansion "
                "of manufacturing capacity."
            ),
            source="Synthetic External Source",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=80.0,
        )

        assert first is not None

        assert (
            observation_engine.registry.count()
            == 1
        )

        print(
            "Test 1 — First Observation          : PASS"
        )

        # ==================================================
        # TEST 2 — FIRST INTELLIGENCE
        # ==================================================

        intelligence = adapter.publish(
            first
        )

        assert intelligence is not None

        assert (
            context.get_intelligence_mesh().count()
            == 1
        )

        print(
            "Test 2 — First Intelligence          : PASS"
        )

        # ==================================================
        # TEST 3 — EXACT DUPLICATE
        # ==================================================

        duplicate = observation_engine.observe(
            title="Industrial capacity expansion",
            description=(
                "The company announced expansion "
                "of manufacturing capacity."
            ),
            source="Synthetic External Source",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=80.0,
        )

        assert duplicate is None

        assert (
            observation_engine.registry.count()
            == 1
        )

        print(
            "Test 3 — Exact Duplicate Rejected    : PASS"
        )

        # ==================================================
        # TEST 4 — MESH UNCHANGED
        # ==================================================

        assert (
            context.get_intelligence_mesh().count()
            == 1
        )

        print(
            "Test 4 — Intelligence Mesh Protected : PASS"
        )

        # ==================================================
        # TEST 5 — NEW INFORMATION
        # ==================================================

        new_observation = observation_engine.observe(
            title="New export order received",
            description=(
                "The company received a new export "
                "order from an international customer."
            ),
            source="Synthetic External Source",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=85.0,
        )

        assert new_observation is not None

        assert (
            observation_engine.registry.count()
            == 2
        )

        print(
            "Test 5 — New Observation Accepted    : PASS"
        )

        # ==================================================
        # TEST 6 — NEW INTELLIGENCE
        # ==================================================

        new_intelligence = adapter.publish(
            new_observation
        )

        assert new_intelligence is not None

        assert (
            context.get_intelligence_mesh().count()
            == 2
        )

        print(
            "Test 6 — New Intelligence Published  : PASS"
        )

        # ==================================================
        # TEST 7 — IDENTITY PRESERVATION
        # ==================================================

        intelligence_items = (
            context
            .get_intelligence_mesh()
            .get_all()
        )

        assert (
            intelligence_items[0].title
            == first.title
        )

        assert (
            intelligence_items[1].title
            == new_observation.title
        )

        assert (
            intelligence_items[0].entity
            == "The Anup Engineering Limited"
        )

        assert (
            intelligence_items[1].entity
            == "The Anup Engineering Limited"
        )

        print(
            "Test 7 — Identity Preservation       : PASS"
        )

        # ==================================================
        # TEST 8 — FINAL STATE
        # ==================================================

        assert (
            observation_engine.registry.count()
            == 2
        )

        assert (
            context.get_intelligence_mesh().count()
            == 2
        )

        assert observation_path.exists()

        print(
            "Test 8 — Final State Integrity       : PASS"
        )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print(
        "EIOS EXTERNAL INTELLIGENCE DUPLICATE "
        "BOUNDARY : ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()