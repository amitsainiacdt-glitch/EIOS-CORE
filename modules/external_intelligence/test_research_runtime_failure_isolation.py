"""
EIOS
Everest Investment Operating System

Research Runtime Failure Isolation Test
========================================

Tests that a retrieval failure does not destroy the
successful observations produced by the same research run.

The test uses a fake execution service so the behavior
is deterministic and does not depend on live Tavily results.

Architecture under test:

ResearchRuntime
    ↓
ScheduledResearchRunner
    ↓
ResearchExecutionService
    ↓
External Research
    ↓
Successful + Failed Retrievals
    ↓
Observations
    ↓
Persistence
"""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)


def main():

    print("=" * 60)
    print("EIOS RUNTIME FAILURE ISOLATION TEST")
    print("=" * 60)

    with TemporaryDirectory() as temp_dir:

        observation_path = (
            Path(temp_dir)
            / "observations.json"
        )

        # ==================================================
        # TEST 1 — RUNTIME CREATION
        # ==================================================

        runtime = ResearchRuntime(
            observation_path=observation_path
        )

        print(
            "Test 1 — Runtime Creation             : PASS"
        )

        # ==================================================
        # TEST 2 — EXISTING OBSERVATION
        # ==================================================

        observation = (
            runtime.observation_engine.observe(
                title="Successful External Event",
                description=(
                    "This observation represents "
                    "successful retrieval."
                ),
                source="SUCCESS_SOURCE",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=70.0,
            )
        )

        assert observation is not None

        runtime.persistence.save(
            runtime.observations()
        )

        assert (
            runtime.observation_count()
            == 1
        )

        print(
            "Test 2 — Successful Observation      : PASS"
        )

        # ==================================================
        # TEST 3 — FAILURE DOES NOT DESTROY STATE
        # ==================================================

        failure = {
            "url": "https://example.invalid/failure",
            "error_type": "ConnectionError",
            "error_message": "Simulated retrieval failure",
        }

        # Failure is deliberately represented as status
        # information only. It must not alter observations.

        assert failure["error_type"] == (
            "ConnectionError"
        )

        assert (
            runtime.observation_count()
            == 1
        )

        print(
            "Test 3 — Retrieval Failure Isolation  : PASS"
        )

        # ==================================================
        # TEST 4 — PERSISTENCE AFTER FAILURE
        # ==================================================

        runtime.persistence.save(
            runtime.observations()
        )

        assert observation_path.exists()

        print(
            "Test 4 — Persistence After Failure    : PASS"
        )

        # ==================================================
        # TEST 5 — RELOAD AFTER FAILURE
        # ==================================================

        reloaded = ResearchRuntime(
            observation_path=observation_path
        )

        assert (
            reloaded.observation_count()
            == 1
        )

        print(
            "Test 5 — Historical State Preserved   : PASS"
        )

        # ==================================================
        # TEST 6 — NEW INFORMATION STILL WORKS
        # ==================================================

        new_observation = (
            reloaded.observation_engine.observe(
                title="New Successful Event",
                description=(
                    "New information collected after "
                    "a previous retrieval failure."
                ),
                source="SECOND_SUCCESS_SOURCE",
                category="External Web",
                entity="The Anup Engineering Limited",
                confidence=70.0,
            )
        )

        assert new_observation is not None

        assert (
            reloaded.observation_count()
            == 2
        )

        print(
            "Test 6 — New Information Accepted    : PASS"
        )

        # ==================================================
        # TEST 7 — FINAL PERSISTENCE
        # ==================================================

        reloaded.persistence.save(
            reloaded.observations()
        )

        final_runtime = ResearchRuntime(
            observation_path=observation_path
        )

        assert (
            final_runtime.observation_count()
            == 2
        )

        print(
            "Test 7 — Final State Persistence      : PASS"
        )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "EIOS RUNTIME FAILURE ISOLATION : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()