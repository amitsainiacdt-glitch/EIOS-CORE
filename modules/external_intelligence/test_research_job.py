"""
EIOS
Everest Investment Operating System

Research Job Test
=================

Tests the passive ResearchJob data model.
"""

from modules.external_intelligence.research_job import (
    ResearchJob,
)


def main():

    print("=" * 60)
    print("EIOS RESEARCH JOB TEST")
    print("=" * 60)

    # ======================================================
    # TEST 1 — VALID JOB
    # ======================================================

    job = ResearchJob(
        job_id="JOB-001",
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question=(
            "What new developments have occurred?"
        ),
        intent="GENERAL_RESEARCH",
        frequency_minutes=1440,
        enabled=True,
        priority=80,
        max_sources=5,
        observation_category="External Web",
        observation_confidence=85.0,
    )

    job.validate()

    print(
        "Test 1 — Valid Job             : PASS"
    )

    # ======================================================
    # TEST 2 — IMMUTABILITY
    # ======================================================

    try:

        job.enabled = False

        raise AssertionError(
            "ResearchJob should be immutable"
        )

    except AttributeError:

        pass

    print(
        "Test 2 — Immutability           : PASS"
    )

    # ======================================================
    # TEST 3 — EMPTY COMPANY
    # ======================================================

    try:

        ResearchJob(
            job_id="JOB-002",
            company="",
            ticker="ANUP",
            question="Research company",
            intent="GENERAL_RESEARCH",
            frequency_minutes=1440,
        ).validate()

        raise AssertionError(
            "Empty company should fail"
        )

    except ValueError:

        pass

    print(
        "Test 3 — Company Validation     : PASS"
    )

    # ======================================================
    # TEST 4 — INVALID FREQUENCY
    # ======================================================

    try:

        ResearchJob(
            job_id="JOB-003",
            company="The Anup Engineering Limited",
            ticker="ANUP",
            question="Research company",
            intent="GENERAL_RESEARCH",
            frequency_minutes=0,
        ).validate()

        raise AssertionError(
            "Invalid frequency should fail"
        )

    except ValueError:

        pass

    print(
        "Test 4 — Frequency Validation   : PASS"
    )

    # ======================================================
    # TEST 5 — INVALID CONFIDENCE
    # ======================================================

    try:

        ResearchJob(
            job_id="JOB-004",
            company="The Anup Engineering Limited",
            ticker="ANUP",
            question="Research company",
            intent="GENERAL_RESEARCH",
            frequency_minutes=1440,
            observation_confidence=150.0,
        ).validate()

        raise AssertionError(
            "Invalid confidence should fail"
        )

    except ValueError:

        pass

    print(
        "Test 5 — Confidence Validation  : PASS"
    )

    # ======================================================
    # TEST 6 — CUSTOM PRIORITY
    # ======================================================

    priority_job = ResearchJob(
        job_id="JOB-005",
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check new orders",
        intent="ORDER_MONITORING",
        frequency_minutes=360,
        priority=100,
    )

    priority_job.validate()

    assert priority_job.priority == 100
    assert priority_job.frequency_minutes == 360

    print(
        "Test 6 — Priority / Frequency   : PASS"
    )

    # ======================================================
    # TEST 7 — DEFAULTS
    # ======================================================

    default_job = ResearchJob(
        job_id="JOB-006",
        company="Test Company",
        ticker="TEST",
        question="General research",
        intent="GENERAL_RESEARCH",
        frequency_minutes=60,
    )

    default_job.validate()

    assert default_job.enabled is True
    assert default_job.priority == 50
    assert default_job.max_sources == 5
    assert default_job.observation_category == "External Web"
    assert default_job.observation_confidence == 70.0

    print(
        "Test 7 — Default Configuration  : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "RESEARCH JOB : ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()