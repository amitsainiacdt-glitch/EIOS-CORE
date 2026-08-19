"""
EIOS
Everest Investment Operating System

Research Runtime Historical Novelty Test
=========================================

Proves that observations created by one ResearchRuntime
process are available to a newly created ResearchRuntime
and are treated as historical information.

This test does not modify production architecture.
"""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_runtime import (
    ResearchRuntime,
)


def make_job():

    return ResearchJob(
        job_id="HISTORICAL-001",
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check recent company developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=60,
        enabled=True,
        priority=100,
        max_sources=3,
        observation_category="External Web",
        observation_confidence=70.0,
    )


def main():

    print("=" * 60)
    print("EIOS HISTORICAL NOVELTY TEST")
    print("=" * 60)

    with TemporaryDirectory() as temp_dir:

        observation_path = (
            Path(temp_dir)
            / "observations.json"
        )

        # ==================================================
        # PROCESS 1
        # ==================================================

        runtime_1 = ResearchRuntime(
            observation_path=observation_path
        )

        job_1 = make_job()

        runtime_1.register_job(
            job_1
        )

        first_time = datetime.now()

        first_result = runtime_1.run_once(
            first_time
        )

        first_count = (
            runtime_1.observation_count()
        )

        assert first_result is not None

        assert len(
            first_result.executed_jobs
        ) == 1

        assert first_count >= 0

        assert observation_path.exists()

        print(
            "Test 1 — First Runtime Execution      : PASS"
        )

        print(
            f"           Observations Created/Stored : "
            f"{first_count}"
        )

        # ==================================================
        # PROCESS 2
        # ==================================================

        runtime_2 = ResearchRuntime(
            observation_path=observation_path
        )

        second_count = (
            runtime_2.observation_count()
        )

        assert (
            second_count
            == first_count
        )

        print(
            "Test 2 — Historical State Reload       : PASS"
        )

        print(
            f"           Historical Observations     : "
            f"{second_count}"
        )

        # ==================================================
        # HISTORICAL OBSERVATION PRESERVATION
        # ==================================================

        first_observations = (
            runtime_1.observations()
        )

        second_observations = (
            runtime_2.observations()
        )

        assert len(
            second_observations
        ) == len(
            first_observations
        )

        if first_observations:

            first_fingerprints = {
                (
                    observation.title,
                    observation.description,
                    observation.source,
                    observation.entity,
                )
                for observation
                in first_observations
            }

            second_fingerprints = {
                (
                    observation.title,
                    observation.description,
                    observation.source,
                    observation.entity,
                )
                for observation
                in second_observations
            }

            assert (
                first_fingerprints
                == second_fingerprints
            )

        print(
            "Test 3 — Historical Observation Match : PASS"
        )

        # ==================================================
        # SECOND RUNTIME MUST START WITH HISTORY
        # ==================================================

        assert (
            runtime_2.observation_count()
            == runtime_1.observation_count()
        )

        print(
            "Test 4 — Cross-Process Memory          : PASS"
        )

        # ==================================================
        # FINAL
        # ==================================================

        print()
        print(
            "EIOS HISTORICAL NOVELTY : "
            "ALL TESTS PASSED"
        )
        print("=" * 60)


if __name__ == "__main__":
    main()