"""
EIOS
Everest Investment Operating System

Observation Persistence Integration Test
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
    print("EIOS OBSERVATION PERSISTENCE INTEGRATION TEST")
    print("=" * 60)

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "observations.json"
        )

        # ==================================================
        # ENGINE A — FIRST RUN
        # ==================================================

        persistence_a = (
            ObservationPersistence(path)
        )

        engine_a = ObservationEngine(
            persistence=persistence_a
        )

        first = engine_a.observe(
            title="Industrial Capex Accelerates",
            description=(
                "Industrial investment is increasing."
            ),
            source="Industry Data",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=90.0,
        )

        assert first is not None

        assert (
            engine_a.registry.count()
            == 1
        )

        assert persistence_a.exists()

        print(
            "Test 1 — First Run Save       : PASS"
        )

        # ==================================================
        # ENGINE B — SECOND RUN
        # ==================================================

        persistence_b = (
            ObservationPersistence(path)
        )

        engine_b = ObservationEngine(
            persistence=persistence_b
        )

        assert (
            engine_b.registry.count()
            == 1
        )

        print(
            "Test 2 — State Reload         : PASS"
        )

        # ==================================================
        # DUPLICATE AFTER RESTART
        # ==================================================

        duplicate = engine_b.observe(
            title="Industrial Capex Accelerates",
            description=(
                "Industrial investment is increasing."
            ),
            source="Industry Data",
            category="External Web",
            entity="The Anup Engineering Limited",
            confidence=90.0,
        )

        assert duplicate is None

        assert (
            engine_b.registry.count()
            == 1
        )

        print(
            "Test 3 — Cross-Run Duplicate  : PASS"
        )

        # ==================================================
        # NEW INFORMATION AFTER RESTART
        # ==================================================

        second = engine_b.observe(
            title="New Capacity Commissioned",
            description=(
                "Additional manufacturing capacity "
                "has been commissioned."
            ),
            source="Company Disclosure",
            category="Company",
            entity="The Anup Engineering Limited",
            confidence=95.0,
        )

        assert second is not None

        assert (
            engine_b.registry.count()
            == 2
        )

        print(
            "Test 4 — New Data After Restart: PASS"
        )

        # ==================================================
        # ENGINE C — THIRD RUN
        # ==================================================

        persistence_c = (
            ObservationPersistence(path)
        )

        engine_c = ObservationEngine(
            persistence=persistence_c
        )

        assert (
            engine_c.registry.count()
            == 2
        )

        print(
            "Test 5 — Second State Reload  : PASS"
        )

        # ==================================================
        # BOTH OBSERVATIONS REMAIN
        # ==================================================

        titles = [
            observation.title
            for observation
            in engine_c.registry.all()
        ]

        assert (
            "Industrial Capex Accelerates"
            in titles
        )

        assert (
            "New Capacity Commissioned"
            in titles
        )

        print(
            "Test 6 — Historical State     : PASS"
        )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "OBSERVATION PERSISTENCE INTEGRATION : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()