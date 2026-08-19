"""
EIOS
Everest Investment Operating System

Research Runtime Execution Logging Test
========================================

Validates that ResearchRuntime:

- initializes execution logging
- executes scheduled research
- records execution logs
- exposes execution log collection
- exposes latest execution log
- exposes execution log count
- preserves runtime result contract
- records observations before/after
- records execution duration
- supports multiple execution cycles
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
        job_id="LOG-001",
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check recent company developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=60,
        enabled=True,
        priority=100,
        max_sources=2,
        observation_category="External Web",
        observation_confidence=70.0,
    )


def main():

    print("=" * 60)
    print(
        "EIOS RESEARCH RUNTIME EXECUTION LOGGING TEST"
    )
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

        assert (
            runtime.execution_log_count()
            == 0
        )

        assert (
            runtime.execution_logs()
            == []
        )

        assert (
            runtime.latest_execution_log()
            is None
        )

        print(
            "Test 1 — Logger Initialization       : PASS"
        )

        # ==================================================
        # TEST 2 — REGISTER JOB
        # ==================================================

        job = make_job()

        runtime.register_job(
            job
        )

        print(
            "Test 2 — Job Registration            : PASS"
        )

        # ==================================================
        # TEST 3 — EXECUTE
        # ==================================================

        run_time = datetime.now()

        result = runtime.run_once(
            run_time
        )

        assert result is not None

        print(
            "Test 3 — Runtime Execution            : PASS"
        )

        # ==================================================
        # TEST 4 — LOG CREATED
        # ==================================================

        assert (
            runtime.execution_log_count()
            == 1
        )

        print(
            "Test 4 — Execution Log Created        : PASS"
        )

        # ==================================================
        # TEST 5 — LOG CONTENT
        # ==================================================

        log = (
            runtime.latest_execution_log()
        )

        assert log is not None

        assert (
            log.run_time
            == run_time
        )

        assert (
            log.status
            in (
                "SUCCESS",
                "PARTIAL_FAILURE",
            )
        )

        assert (
            log.jobs_due
            == 1
        )

        assert (
            log.jobs_executed
            == 1
        )

        assert (
            log.observations_after
            >= log.observations_before
        )

        assert (
            log.observations_created
            >= 0
        )

        assert (
            log.failures
            >= 0
        )

        assert (
            log.duration_seconds
            >= 0
        )

        print(
            "Test 5 — Log Content                 : PASS"
        )

        # ==================================================
        # TEST 6 — COLLECTION
        # ==================================================

        logs = (
            runtime.execution_logs()
        )

        assert (
            len(logs)
            == 1
        )

        assert (
            logs[0]
            == log
        )

        print(
            "Test 6 — Log Collection               : PASS"
        )

        # ==================================================
        # TEST 7 — MULTIPLE EXECUTION CYCLES
        # ==================================================

        second_time = (
            run_time.replace(
                second=0,
                microsecond=0,
            )
        )

        next_run = (
            second_time
            + timedelta(
                minutes=60
            )
        )

        second_result = runtime.run_once(
            next_run
        )

        assert second_result is not None

        assert (
            runtime.execution_log_count()
            == 2
        )

        logs_after_second_run = (
            runtime.execution_logs()
        )

        assert (
            len(logs_after_second_run)
            == 2
        )

        latest = (
            runtime.latest_execution_log()
        )

        assert latest is not None

        assert (
            latest.run_time
            == next_run
        )

        print(
            "Test 7 — Multiple Runtime Logs        : PASS"
        )

    print()
    print("---")
    print()

    print(
        "RESEARCH RUNTIME EXECUTION LOGGING : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()