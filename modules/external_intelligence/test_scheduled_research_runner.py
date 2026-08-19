"""
EIOS
Everest Investment Operating System

Scheduled Research Runner Test
"""

from dataclasses import dataclass
from datetime import datetime

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_job_registry import (
    ResearchJobRegistry,
)

from modules.external_intelligence.research_scheduler import (
    ResearchScheduler,
)

from modules.external_intelligence.scheduled_research_runner import (
    ScheduledResearchRunner,
)


# ==========================================================
# FAKE RESULT
# ==========================================================


@dataclass
class FakeResearchResult:

    job_id: str


# ==========================================================
# FAKE EXECUTION SERVICE
# ==========================================================


class FakeExecutionService:

    def __init__(
        self,
        scheduler,
    ):

        self.scheduler = scheduler

        self.executed_jobs = []

        self.run_times = []

    def execute(
        self,
        job,
        *,
        run_time,
    ):

        self.executed_jobs.append(
            job
        )

        self.run_times.append(
            run_time
        )

        # Mirror the real ResearchExecutionService
        # scheduling contract.
        #
        # The production execution service marks the
        # scheduler only after successful execution.
        self.scheduler.mark_run(
            job,
            run_time,
        )

        return FakeResearchResult(
            job_id=job.job_id
        )


# ==========================================================
# JOB FACTORY
# ==========================================================


def make_job(
    job_id,
    frequency_minutes=60,
    enabled=True,
    priority=50,
):

    return ResearchJob(
        job_id=job_id,
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check new developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=frequency_minutes,
        enabled=enabled,
        priority=priority,
    )


# ==========================================================
# MAIN
# ==========================================================


def main():

    print("=" * 60)
    print("EIOS SCHEDULED RESEARCH RUNNER TEST")
    print("=" * 60)

    # ======================================================
    # SETUP
    # ======================================================

    registry = ResearchJobRegistry()

    scheduler = ResearchScheduler()

    execution_service = (
        FakeExecutionService(
            scheduler
        )
    )

    runner = ScheduledResearchRunner(
        registry=registry,
        scheduler=scheduler,
        execution_service=execution_service,
    )

    job_high = make_job(
        "JOB-HIGH",
        priority=100,
    )

    job_low = make_job(
        "JOB-LOW",
        priority=20,
    )

    job_disabled = make_job(
        "JOB-DISABLED",
        enabled=False,
    )

    registry.add(
        job_high
    )

    registry.add(
        job_low
    )

    registry.add(
        job_disabled
    )

    scheduler.register(
        job_high
    )

    scheduler.register(
        job_low
    )

    scheduler.register(
        job_disabled
    )

    now = datetime(
        2026,
        8,
        17,
        10,
        0,
        0,
    )

    # ======================================================
    # TEST 1 — FIRST RUN
    # ======================================================

    result = runner.run_once(
        now
    )

    assert len(
        result.due_jobs
    ) == 2

    assert len(
        result.executed_jobs
    ) == 2

    assert len(
        result.results
    ) == 2

    print(
        "Test 1 — Initial Execution      : PASS"
    )

    # ======================================================
    # TEST 2 — PRIORITY ORDER
    # ======================================================

    assert [
        job.job_id
        for job in result.executed_jobs
    ] == [
        "JOB-HIGH",
        "JOB-LOW",
    ]

    print(
        "Test 2 — Priority Ordering      : PASS"
    )

    # ======================================================
    # TEST 3 — DISABLED JOB
    # ======================================================

    assert (
        "JOB-DISABLED"
        not in [
            job.job_id
            for job in result.executed_jobs
        ]
    )

    print(
        "Test 3 — Disabled Job Excluded  : PASS"
    )

    # ======================================================
    # TEST 4 — EXECUTION COUNT
    # ======================================================

    assert len(
        execution_service.executed_jobs
    ) == 2

    assert len(
        execution_service.run_times
    ) == 2

    print(
        "Test 4 — Execution Delegation   : PASS"
    )

    # ======================================================
    # TEST 5 — SECOND RUN BEFORE DUE
    # ======================================================

    second_run = runner.run_once(
        datetime(
            2026,
            8,
            17,
            10,
            30,
            0,
        )
    )

    assert (
        len(second_run.due_jobs)
        == 0
    )

    assert (
        len(second_run.executed_jobs)
        == 0
    )

    assert (
        len(second_run.results)
        == 0
    )

    print(
        "Test 5 — Interval Protection    : PASS"
    )

    # ======================================================
    # TEST 6 — NEXT RUN
    # ======================================================

    third_run = runner.run_once(
        datetime(
            2026,
            8,
            17,
            11,
            0,
            0,
        )
    )

    assert (
        len(third_run.due_jobs)
        == 2
    )

    assert (
        len(third_run.executed_jobs)
        == 2
    )

    print(
        "Test 6 — Next Scheduled Run     : PASS"
    )

    # ======================================================
    # TEST 7 — RESULT PROVENANCE
    # ======================================================

    assert [
        result.job_id
        for result in third_run.results
    ] == [
        "JOB-HIGH",
        "JOB-LOW",
    ]

    print(
        "Test 7 — Result Preservation    : PASS"
    )

    # ======================================================
    # TEST 8 — RUN TIME PRESERVATION
    # ======================================================

    assert (
        third_run.run_time
        == datetime(
            2026,
            8,
            17,
            11,
            0,
            0,
        )
    )

    print(
        "Test 8 — Run Time Preservation  : PASS"
    )

    # ======================================================
    # TEST 9 — SCHEDULER STATE
    # ======================================================

    high_state = scheduler.state(
        "JOB-HIGH"
    )

    low_state = scheduler.state(
        "JOB-LOW"
    )

    assert high_state is not None
    assert low_state is not None

    assert high_state.last_run == datetime(
        2026,
        8,
        17,
        11,
        0,
        0,
    )

    assert low_state.last_run == datetime(
        2026,
        8,
        17,
        11,
        0,
        0,
    )

    assert high_state.next_run == datetime(
        2026,
        8,
        17,
        12,
        0,
        0,
    )

    assert low_state.next_run == datetime(
        2026,
        8,
        17,
        12,
        0,
        0,
    )

    print(
        "Test 9 — Scheduler State        : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print(
        "SCHEDULED RESEARCH RUNNER : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()