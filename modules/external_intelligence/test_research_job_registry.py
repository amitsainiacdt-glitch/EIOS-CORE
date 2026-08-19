"""
EIOS
Everest Investment Operating System

Research Job Registry Test
"""

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_job_registry import (
    ResearchJobRegistry,
)


def make_job(
    job_id: str,
    enabled: bool = True,
    priority: int = 50,
) -> ResearchJob:

    return ResearchJob(
        job_id=job_id,
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check new developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=1440,
        enabled=enabled,
        priority=priority,
    )


def main():

    print("=" * 60)
    print("EIOS RESEARCH JOB REGISTRY TEST")
    print("=" * 60)

    registry = ResearchJobRegistry()

    # ======================================================
    # TEST 1 — EMPTY REGISTRY
    # ======================================================

    assert registry.count() == 0

    print(
        "Test 1 — Empty Registry        : PASS"
    )

    # ======================================================
    # TEST 2 — ADD
    # ======================================================

    job_1 = make_job(
        "JOB-001",
        enabled=True,
        priority=80,
    )

    registry.add(job_1)

    assert registry.count() == 1

    print(
        "Test 2 — Add Job               : PASS"
    )

    # ======================================================
    # TEST 3 — GET
    # ======================================================

    retrieved = registry.get(
        "JOB-001"
    )

    assert retrieved is job_1
    assert retrieved.job_id == "JOB-001"

    print(
        "Test 3 — Get Job               : PASS"
    )

    # ======================================================
    # TEST 4 — MULTIPLE JOBS
    # ======================================================

    job_2 = make_job(
        "JOB-002",
        enabled=True,
        priority=60,
    )

    job_3 = make_job(
        "JOB-003",
        enabled=False,
        priority=40,
    )

    registry.add(job_2)
    registry.add(job_3)

    assert registry.count() == 3

    print(
        "Test 4 — Multiple Jobs         : PASS"
    )

    # ======================================================
    # TEST 5 — ALL
    # ======================================================

    jobs = registry.all()

    assert len(jobs) == 3

    assert {
        job.job_id
        for job in jobs
    } == {
        "JOB-001",
        "JOB-002",
        "JOB-003",
    }

    print(
        "Test 5 — All Jobs              : PASS"
    )

    # ======================================================
    # TEST 6 — ENABLED
    # ======================================================

    enabled_jobs = registry.enabled()

    assert len(enabled_jobs) == 2

    assert {
        job.job_id
        for job in enabled_jobs
    } == {
        "JOB-001",
        "JOB-002",
    }

    print(
        "Test 6 — Enabled Jobs          : PASS"
    )

    # ======================================================
    # TEST 7 — DUPLICATE PROTECTION
    # ======================================================

    try:

        registry.add(
            make_job("JOB-001")
        )

        raise AssertionError(
            "Duplicate job ID should fail"
        )

    except ValueError:

        pass

    print(
        "Test 7 — Duplicate Protection  : PASS"
    )

    # ======================================================
    # TEST 8 — REMOVE
    # ======================================================

    removed = registry.remove(
        "JOB-003"
    )

    assert removed is job_3
    assert registry.count() == 2
    assert registry.get("JOB-003") is None

    print(
        "Test 8 — Remove Job             : PASS"
    )

    # ======================================================
    # TEST 9 — CLEAR
    # ======================================================

    registry.clear()

    assert registry.count() == 0
    assert registry.all() == []

    print(
        "Test 9 — Clear Registry        : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "RESEARCH JOB REGISTRY : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()