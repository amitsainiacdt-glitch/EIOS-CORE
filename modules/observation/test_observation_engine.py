"""
EIOS
Everest Investment Operating System

Observation Engine Integration Test
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from modules.observation.observation_engine import (
    ObservationEngine,
)

from modules.observation.observation_persistence import (
    ObservationPersistence,
)


def main():

    print("=" * 60)
    print("EIOS OBSERVATION ENGINE TEST")
    print("=" * 60)

    # ======================================================
    # TEST ISOLATED PERSISTENCE
    # ======================================================

    temp_dir = TemporaryDirectory()
    test_path = Path(temp_dir.name) / "observations.json"

    test_persistence = ObservationPersistence(
        path=test_path
    )

    # Ensure the test always starts from a clean state.
    test_persistence.clear()

    engine = ObservationEngine(
        persistence=test_persistence
    )

    try:

        # ==================================================
        # TEST 1 — FIRST OBSERVATION
        # ==================================================

        first = engine.observe(
            title="Industrial Capex Accelerates",
            description=(
                "Industrial investment is increasing."
            ),
            source="https://example.com/article",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=90.0,
        )

        assert first is not None

        assert (
            engine.registry.count()
            == 1
        )

        print(
            "Test 1 — First Ingestion      : PASS"
        )

        # ==================================================
        # TEST 2 — DUPLICATE
        # ==================================================

        duplicate = engine.observe(
            title="Industrial Capex Accelerates",
            description=(
                "Industrial investment is increasing."
            ),
            source="https://example.com/article",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=90.0,
        )

        assert duplicate is None

        assert (
            engine.registry.count()
            == 1
        )

        print(
            "Test 2 — Duplicate Rejected   : PASS"
        )

        # ==================================================
        # TEST 3 — DIFFERENT INFORMATION
        # ==================================================

        second = engine.observe(
            title="New Capacity Commissioned",
            description=(
                "The company commissioned "
                "additional manufacturing capacity."
            ),
            source="https://example.com/article",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=92.0,
        )

        assert second is not None

        assert (
            engine.registry.count()
            == 2
        )

        print(
            "Test 3 — New Information      : PASS"
        )

        # ==================================================
        # TEST 4 — DIFFERENT SOURCE
        # ==================================================

        third = engine.observe(
            title="Industrial Capex Accelerates",
            description=(
                "Industrial investment is increasing."
            ),
            source="https://another.example/article",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=88.0,
        )

        assert third is not None

        assert (
            engine.registry.count()
            == 3
        )

        print(
            "Test 4 — Independent Source   : PASS"
        )

        # ==================================================
        # TEST 5 — CASE / WHITESPACE NORMALIZATION
        # ==================================================

        normalized_duplicate = engine.observe(
            title=(
                "  INDUSTRIAL   CAPEX "
                "ACCELERATES "
            ),
            description=(
                " Industrial investment "
                "is increasing. "
            ),
            source=(
                " HTTPS://EXAMPLE.COM/ARTICLE "
            ),
            category=" external web ",
            entity=(
                " THE ANUP ENGINEERING LIMITED "
            ),
            confidence=95.0,
        )

        assert normalized_duplicate is None

        assert (
            engine.registry.count()
            == 3
        )

        print(
            "Test 5 — Normalized Duplicate : PASS"
        )

        # ==================================================
        # TEST 6 — REGISTRY INTEGRITY
        # ==================================================

        assert (
            engine.registry.latest()
            is third
        )

        assert (
            engine.registry.count()
            == 3
        )

        print(
            "Test 6 — Registry Integrity   : PASS"
        )

        # ==================================================
        # TEST 7 — NOVELTY ASSESSMENT
        # ==================================================

        novelty = engine.assess_novelty(
            third
        )

        assert not novelty.is_new

        assert (
            novelty.matched_observation
            is third
        )

        print(
            "Test 7 — Novelty Assessment   : PASS"
        )

        # ==================================================
        # FINAL
        # ==================================================

        print()

        print(
            "OBSERVATION ENGINE : ALL TESTS PASSED"
        )

        print("=" * 60)

    finally:

        # ==================================================
        # TEST CLEANUP
        # ==================================================

        test_persistence.clear()
        temp_dir.cleanup()


if __name__ == "__main__":
    main()
