"""
EIOS
Everest Investment Operating System

Research Runtime Duplicate Protection Test
===========================================

Proves that an observation already stored by one runtime
is rejected as a duplicate by a newly created runtime.

This test deliberately uses deterministic observations
rather than live Tavily results.

It validates:

    Runtime 1
        ↓
    Observation created
        ↓
    Persistence
        ↓
    Runtime 2
        ↓
    Same observation submitted
        ↓
    ObservationNoveltyEngine
        ↓
    Duplicate rejected
"""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)


class FakeSearchProvider:
    """Configured provider fake; this test never executes research."""

    configured = True

    def __init__(self, api_key=None):
        self.api_key = api_key

    def search(self, query):
        raise AssertionError("Search is outside this test's scope")


def make_runtime(observation_path):
    with patch(
        "modules.external_intelligence.research_runtime.TavilySearchProvider",
        FakeSearchProvider,
    ):
        return ResearchRuntime(observation_path=observation_path)


def main():

    print("=" * 60)
    print("EIOS RUNTIME DUPLICATE PROTECTION TEST")
    print("=" * 60)

    with TemporaryDirectory() as temp_dir:

        observation_path = (
            Path(temp_dir)
            / "observations.json"
        )

        # ==================================================
        # RUNTIME 1
        # ==================================================

        runtime_1 = make_runtime(observation_path)

        observation_1 = (
            runtime_1.observation_engine.observe(
                title="Anup Engineering Test Event",
                description=(
                    "Deterministic test observation "
                    "for duplicate protection."
                ),
                source="EIOS_TEST_SOURCE",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=70.0,
            )
        )

        assert observation_1 is not None

        first_count = (
            runtime_1.observation_count()
        )

        assert first_count == 1

        # Persist the observation.

        runtime_1.persistence.save(
            runtime_1.observations()
        )

        assert observation_path.exists()

        print(
            "Test 1 — First Observation          : PASS"
        )

        # ==================================================
        # RUNTIME 2 — RESTART
        # ==================================================

        runtime_2 = make_runtime(observation_path)

        assert (
            runtime_2.observation_count()
            == 1
        )

        print(
            "Test 2 — Historical Observation      : PASS"
        )

        # ==================================================
        # SUBMIT EXACT DUPLICATE
        # ==================================================

        duplicate = (
            runtime_2.observation_engine.observe(
                title="Anup Engineering Test Event",
                description=(
                    "Deterministic test observation "
                    "for duplicate protection."
                ),
                source="EIOS_TEST_SOURCE",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=70.0,
            )
        )

        assert duplicate is None

        assert (
            runtime_2.observation_count()
            == 1
        )

        print(
            "Test 3 — Exact Duplicate Rejected    : PASS"
        )

        # ==================================================
        # SUBMIT NORMALIZED DUPLICATE
        # ==================================================

        normalized_duplicate = (
            runtime_2.observation_engine.observe(
                title="  Anup Engineering Test Event  ",
                description=(
                    "DETERMINISTIC TEST OBSERVATION "
                    "FOR DUPLICATE PROTECTION."
                ),
                source="EIOS_TEST_SOURCE",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=70.0,
            )
        )

        assert normalized_duplicate is None

        assert (
            runtime_2.observation_count()
            == 1
        )

        print(
            "Test 4 — Normalized Duplicate        : PASS"
        )

        # ==================================================
        # SUBMIT GENUINELY NEW INFORMATION
        # ==================================================

        new_observation = (
            runtime_2.observation_engine.observe(
                title="Anup Engineering New Test Event",
                description=(
                    "This is genuinely new deterministic "
                    "test information."
                ),
                source="EIOS_TEST_SOURCE",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=70.0,
            )
        )

        assert new_observation is not None

        assert (
            runtime_2.observation_count()
            == 2
        )

        print(
            "Test 5 — New Information Accepted    : PASS"
        )

        # ==================================================
        # PERSIST SECOND STATE
        # ==================================================

        runtime_2.persistence.save(
            runtime_2.observations()
        )

        # ==================================================
        # RUNTIME 3 — FINAL RELOAD
        # ==================================================

        runtime_3 = make_runtime(observation_path)

        assert (
            runtime_3.observation_count()
            == 2
        )

        print(
            "Test 6 — Final State Persistence      : PASS"
        )

        # ==================================================
        # FINAL
        # ==================================================

        print()
        print(
            "EIOS RUNTIME DUPLICATE PROTECTION : "
            "ALL TESTS PASSED"
        )
        print("=" * 60)


if __name__ == "__main__":
    with patch(
        "socket.create_connection",
        side_effect=AssertionError("Network access is forbidden in this test"),
    ):
        main()
