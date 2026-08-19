"""
EIOS
Everest Investment Operating System

Research Scheduler Test
"""

from datetime import datetime

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_scheduler import (
    ResearchScheduler,
)


def make_job(
    job_id,
    frequency_minutes,
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


def main():

    print("=" * 60)
    print("EIOS RESEARCH SCHEDULER TEST")
    print("=" * 60)

    scheduler = ResearchScheduler()

    job = make_job(
        "JOB-001",
        frequency_minutes=60,
    )

    scheduler.register(job)

    now = datetime(
        2026,
        8,
        17,
        10,
        0,
        0,
    )

    # ======================================================
    # TEST 1 — NEVER RUN
    # ======================================================

    assert scheduler.is_due(
        job,
        now,
    )

    print(
        "Test 1 — Initial Due            : PASS"
    )

    # ======================================================
    # TEST 2 — MARK RUN
    # ======================================================

    scheduler.mark_run(
        job,
        now,
    )

    state = scheduler.state(
        "JOB-001"
    )

    assert state is not None
    assert state.last_run == now

    assert state.next_run == datetime(
        2026,
        8,
        17,
        11,
        0,
        0,
    )

    print(
        "Test 2 — Run State              : PASS"
    )

    # ======================================================
    # TEST 3 — NOT YET DUE
    # ======================================================

    assert not scheduler.is_due(
        job,
        datetime(
            2026,
            8,
            17,
            10,
            30,
        ),
    )

    print(
        "Test 3 — Not Yet Due            : PASS"
    )

    # ======================================================
    # TEST 4 — DUE
    # ======================================================

    assert scheduler.is_due(
        job,
        datetime(
            2026,
            8,
            17,
            11,
            0,
        ),
    )

    print(
        "Test 4 — Due After Interval     : PASS"
    )

    # ======================================================
    # TEST 5 — DISABLED
    # ======================================================

    disabled_job = make_job(
        "JOB-002",
        frequency_minutes=60,
        enabled=False,
    )

    scheduler.register(
        disabled_job
    )

    assert not scheduler.is_due(
        disabled_job,
        now,
    )

    print(
        "Test 5 — Disabled Job           : PASS"
    )

    # ======================================================
    # TEST 6 — PRIORITY ORDER
    # ======================================================

    high = make_job(
        "JOB-HIGH",
        frequency_minutes=60,
        priority=100,
    )

    low = make_job(
        "JOB-LOW",
        frequency_minutes=60,
        priority=10,
    )

    scheduler.register(high)
    scheduler.register(low)

    due = scheduler.due_jobs(
        [
            low,
            high,
        ],
        now,
    )

    assert [
        job.job_id
        for job in due
    ] == [
        "JOB-HIGH",
        "JOB-LOW",
    ]

    print(
        "Test 6 — Priority Ordering      : PASS"
    )

    # ======================================================
    # TEST 7 — UNREGISTERED JOB
    # ======================================================

    unknown = make_job(
        "UNKNOWN",
        frequency_minutes=60,
    )

    try:

        scheduler.is_due(
            unknown,
            now,
        )

        raise AssertionError(
            "Unregistered job should fail"
        )

    except ValueError:

        pass

    print(
        "Test 7 — Registration Guard      : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "RESEARCH SCHEDULER : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()