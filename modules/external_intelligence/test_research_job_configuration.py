"""
EIOS
Everest Investment Operating System

Research Job Configuration Test
"""

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_job_configuration import (
    ResearchJobConfiguration,
)


def main():

    print("=" * 60)
    print("EIOS RESEARCH JOB CONFIGURATION TEST")
    print("=" * 60)

    # ======================================================
    # TEST 1 — ANUP JOB CREATION
    # ======================================================

    jobs = (
        ResearchJobConfiguration.anup_jobs()
    )

    assert len(jobs) == 6

    print(
        "Test 1 — ANUP Jobs Created          : PASS"
    )

    # ======================================================
    # TEST 2 — TYPE PROTECTION
    # ======================================================

    assert all(
        isinstance(
            job,
            ResearchJob,
        )
        for job in jobs
    )

    print(
        "Test 2 — ResearchJob Types           : PASS"
    )

    # ======================================================
    # TEST 3 — UNIQUE JOB IDS
    # ======================================================

    job_ids = [
        job.job_id
        for job in jobs
    ]

    assert len(job_ids) == len(set(job_ids))

    print(
        "Test 3 — Unique Job IDs              : PASS"
    )

    # ======================================================
    # TEST 4 — VALIDATION
    # ======================================================

    for job in jobs:
        job.validate()

    print(
        "Test 4 — Job Validation               : PASS"
    )

    # ======================================================
    # TEST 5 — ENABLED JOBS
    # ======================================================

    assert all(
        job.enabled
        for job in jobs
    )

    print(
        "Test 5 — Enabled Configuration        : PASS"
    )

    # ======================================================
    # TEST 6 — PRIORITY
    # ======================================================

    priorities = [
        job.priority
        for job in jobs
    ]

    assert max(priorities) == 100

    assert min(priorities) == 80

    print(
        "Test 6 — Priority Configuration       : PASS"
    )

    # ======================================================
    # TEST 7 — ALL JOBS
    # ======================================================

    all_jobs = (
        ResearchJobConfiguration.all_jobs()
    )

    assert len(all_jobs) == 6

    assert [
        job.job_id
        for job in all_jobs
    ] == job_ids

    print(
        "Test 7 — All Jobs Configuration       : PASS"
    )

    # ======================================================
    # TEST 8 — IMMUTABILITY
    # ======================================================

    try:

        jobs[0].priority = 1

        raise AssertionError(
            "ResearchJob should be immutable"
        )

    except (
        AttributeError,
        TypeError,
    ):

        pass

    print(
        "Test 8 — Job Immutability             : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print(
        "RESEARCH JOB CONFIGURATION : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()