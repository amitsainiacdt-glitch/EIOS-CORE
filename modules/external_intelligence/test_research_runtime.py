"""
EIOS
Everest Investment Operating System

Research Runtime Integration Test
"""

from datetime import datetime, timedelta
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
        job_id="RUNTIME-001",
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
    print("EIOS RESEARCH RUNTIME INTEGRATION TEST")
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

        assert runtime.provider.configured

        print(
            "Test 1 — Tavily Configuration       : PASS"
        )

        # ==================================================
        # TEST 2 — JOB REGISTRATION
        # ==================================================

        job = make_job()

        runtime.register_job(
            job
        )

        assert (
            runtime.registry.get(
                "RUNTIME-001"
            )
            is job
        )

        assert (
            runtime.scheduler.state(
                "RUNTIME-001"
            )
            is not None
        )

        print(
            "Test 2 — Job Registration            : PASS"
        )

        # ==================================================
        # TEST 3 — FIRST RUNTIME EXECUTION
        # ==================================================

        run_time = datetime.now()

        result = runtime.run_once(
            run_time
        )

        assert result is not None

        assert len(
            result.due_jobs
        ) == 1

        assert len(
            result.executed_jobs
        ) == 1

        print(
            "Test 3 — Scheduled Execution         : PASS"
        )

        # ==================================================
        # TEST 4 — OBSERVATION HANDOFF
        # ==================================================

        observation_count = (
            runtime.observation_count()
        )

        print(
            f"Runtime observation count : "
            f"{observation_count}"
        )

        assert observation_count > 0

        print(
            "Test 4 — Observation Handoff          : PASS"
        )

        # ==================================================
        # TEST 5 — PERSISTENCE
        # ==================================================

        assert observation_path.exists()

        print(
            "Test 5 — Observation Persistence     : PASS"
        )

        # ==================================================
        # TEST 6 — RELOAD
        # ==================================================

        reloaded = ResearchRuntime(
            observation_path=observation_path
        )

        runtime_count = (
            runtime.observation_count()
        )

        reloaded_count = (
            reloaded.observation_count()
        )

        print()
        print(
            "----- PERSISTENCE DIAGNOSTIC -----"
        )

        print(
            f"Runtime observation count : "
            f"{runtime_count}"
        )

        print(
            f"Reloaded observation count: "
            f"{reloaded_count}"
        )

        print(
            f"Persistent file exists    : "
            f"{observation_path.exists()}"
        )

        print()
        print(
            "Persistent file contents:"
        )

        print(
            observation_path.read_text(
                encoding="utf-8"
            )
        )

        print(
            "----- END DIAGNOSTIC -----"
        )
        print()

        assert (
            reloaded_count
            == runtime_count
        )

        print(
            "Test 6 — Historical State Reload      : PASS"
        )

        # ==================================================
        # TEST 7 — SCHEDULER INTERVAL
        # ==================================================

        second_time = (
            run_time.replace(
                second=0,
                microsecond=0,
            )
        )

        before_next_run = (
            second_time
            + timedelta(
                minutes=30
            )
        )

        second_result = runtime.run_once(
            before_next_run
        )

        assert (
            len(
                second_result.due_jobs
            )
            == 0
        )

        assert (
            len(
                second_result.executed_jobs
            )
            == 0
        )

        print(
            "Test 7 — Scheduler Interval          : PASS"
        )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print(
        "EIOS RESEARCH RUNTIME : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()