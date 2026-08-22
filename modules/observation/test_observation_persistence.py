"""
EIOS
Everest Investment Operating System

Observation Persistence Test
"""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.observation.observation import (
    Observation,
)

from modules.observation.observation_persistence import (
    ObservationPersistence,
)


def main():

    print("=" * 60)
    print("EIOS OBSERVATION PERSISTENCE TEST")
    print("=" * 60)

    with TemporaryDirectory() as temp_dir:

        path = (
            Path(temp_dir)
            / "observations.json"
        )

        persistence = (
            ObservationPersistence(path)
        )

        # ==================================================
        # TEST 1 — EMPTY STORE
        # ==================================================

        loaded = persistence.load()

        assert loaded == []

        print(
            "Test 1 — Empty Store          : PASS"
        )

        # ==================================================
        # TEST 2 — CREATE OBSERVATIONS
        # ==================================================

        timestamp = datetime.now()

        observations = [

            Observation(
                title="Industrial Capex Accelerates",
                description=(
                    "Industrial investment "
                    "is increasing."
                ),
                source="Industry Data",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=90.0,
                timestamp=timestamp,
            ),

            Observation(
                title="New Capacity Commissioned",
                description=(
                    "Additional capacity "
                    "has been commissioned."
                ),
                source="Company Disclosure",
                category="Company",
                entity="The Anup Engineering Limited",
                confidence=95.0,
                timestamp=timestamp,
            ),
        ]

        # ==================================================
        # TEST 3 — SAVE
        # ==================================================

        persistence.save(
            observations
        )

        assert persistence.exists()

        print(
            "Test 2 — Save                  : PASS"
        )

        # ==================================================
        # TEST 4 — LOAD
        # ==================================================

        loaded = persistence.load()

        assert len(loaded) == 2

        assert (
            loaded[0].title
            == observations[0].title
        )

        assert (
            loaded[1].title
            == observations[1].title
        )

        print(
            "Test 3 — Load                  : PASS"
        )

        # ==================================================
        # TEST 5 — TIMESTAMP PRESERVATION
        # ==================================================

        assert loaded[0].timestamp == timestamp

        assert loaded[1].timestamp == timestamp

        print(
            "Test 4 — Timestamp Preservation: PASS"
        )

        # ==================================================
        # TEST 6 — SOURCE PRESERVATION
        # ==================================================

        assert (
            loaded[0].source
            == "Industry Data"
        )

        assert (
            loaded[1].source
            == "Company Disclosure"
        )

        print(
            "Test 5 — Source Preservation   : PASS"
        )

        # ==================================================
        # TEST 7 — CLEAR
        # ==================================================

        persistence.clear()

        assert not persistence.exists()

        assert (
            persistence.load()
            == []
        )

        print(
            "Test 6 — Clear                  : PASS"
        )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "OBSERVATION PERSISTENCE : ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
