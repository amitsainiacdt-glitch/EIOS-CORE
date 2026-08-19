"""
EIOS
Everest Investment Operating System

Research Execution Logger Test
"""

from datetime import datetime

from modules.external_intelligence.research_execution_log import (
    ResearchExecutionLog,
)

from modules.external_intelligence.research_execution_logger import (
    ResearchExecutionLogger,
)


def main():

    print("=" * 60)
    print("EIOS RESEARCH EXECUTION LOGGER TEST")
    print("=" * 60)

    logger = ResearchExecutionLogger()

    # ======================================================
    # TEST 1 — EMPTY LOGGER
    # ======================================================

    assert logger.count() == 0
    assert logger.latest() is None

    print(
        "Test 1 — Empty Logger             : PASS"
    )

    # ======================================================
    # TEST 2 — RECORD
    # ======================================================

    run_time = datetime(
        2026,
        8,
        18,
        12,
        30,
        0,
    )

    log = ResearchExecutionLog(
        run_time=run_time,
        status="SUCCESS",
        jobs_due=2,
        jobs_executed=2,
        observations_before=5,
        observations_after=7,
        observations_created=2,
        failures=0,
        duration_seconds=8.5,
    )

    logger.record(log)

    assert logger.count() == 1

    print(
        "Test 2 — Record                  : PASS"
    )

    # ======================================================
    # TEST 3 — PRESERVATION
    # ======================================================

    assert logger.latest() == log

    assert logger.latest().run_time == run_time
    assert logger.latest().status == "SUCCESS"
    assert logger.latest().jobs_due == 2
    assert logger.latest().jobs_executed == 2
    assert logger.latest().observations_created == 2
    assert logger.latest().failures == 0

    print(
        "Test 3 — Record Preservation      : PASS"
    )

    # ======================================================
    # TEST 4 — ALL
    # ======================================================

    logs = logger.all()

    assert len(logs) == 1
    assert logs[0] == log

    print(
        "Test 4 — All Logs                 : PASS"
    )

    # ======================================================
    # TEST 5 — COPY PROTECTION
    # ======================================================

    logs.append(
        log
    )

    assert logger.count() == 1

    print(
        "Test 5 — Collection Protection    : PASS"
    )

    # ======================================================
    # TEST 6 — MULTIPLE RECORDS
    # ======================================================

    second_log = ResearchExecutionLog(
        run_time=datetime(
            2026,
            8,
            18,
            13,
            30,
            0,
        ),
        status="PARTIAL_FAILURE",
        jobs_due=3,
        jobs_executed=3,
        observations_before=7,
        observations_after=8,
        observations_created=1,
        failures=2,
        duration_seconds=12.0,
    )

    logger.record(
        second_log
    )

    assert logger.count() == 2
    assert logger.latest() == second_log

    print(
        "Test 6 — Multiple Records        : PASS"
    )

    # ======================================================
    # TEST 7 — CLEAR
    # ======================================================

    logger.clear()

    assert logger.count() == 0
    assert logger.latest() is None

    print(
        "Test 7 — Clear                    : PASS"
    )

    print()
    print(
        "RESEARCH EXECUTION LOGGER : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()