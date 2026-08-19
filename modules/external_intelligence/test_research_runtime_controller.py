"""
EIOS
Everest Investment Operating System

Research Runtime Controller Test
"""

from dataclasses import dataclass
from datetime import datetime

from modules.external_intelligence.research_runtime_controller import (
    ResearchRuntimeController,
)


# ==========================================================
# FAKE RESULT
# ==========================================================


@dataclass
class FakeScheduledResearchResult:

    run_time: datetime

    due_jobs: list

    executed_jobs: list

    results: list


# ==========================================================
# FAKE RUNNER
# ==========================================================


class FakeRunner:

    def __init__(self):

        self.calls = []

    def run_once(
        self,
        now,
    ):

        self.calls.append(
            now
        )

        return FakeScheduledResearchResult(
            run_time=now,
            due_jobs=[],
            executed_jobs=[],
            results=[],
        )


# ==========================================================
# MAIN
# ==========================================================


def main():

    print("=" * 60)
    print("EIOS RESEARCH RUNTIME CONTROLLER TEST")
    print("=" * 60)

    # ======================================================
    # SETUP
    # ======================================================

    runner = FakeRunner()

    controller = ResearchRuntimeController(
        runner
    )

    run_time = datetime(
        2026,
        8,
        17,
        12,
        0,
        0,
    )

    # ======================================================
    # TEST 1 — CONTROLLER CREATION
    # ======================================================

    assert controller.runner is runner

    print(
        "Test 1 — Controller Creation    : PASS"
    )

    # ======================================================
    # TEST 2 — EXECUTION DELEGATION
    # ======================================================

    result = controller.run_once(
        run_time
    )

    assert len(
        runner.calls
    ) == 1

    assert runner.calls[0] == run_time

    print(
        "Test 2 — Execution Delegation   : PASS"
    )

    # ======================================================
    # TEST 3 — RESULT PRESERVATION
    # ======================================================

    assert isinstance(
        result,
        FakeScheduledResearchResult,
    )

    assert result.run_time == run_time

    print(
        "Test 3 — Result Preservation    : PASS"
    )

    # ======================================================
    # TEST 4 — TIME PRESERVATION
    # ======================================================

    second_time = datetime(
        2026,
        8,
        17,
        13,
        30,
        0,
    )

    second_result = controller.run_once(
        second_time
    )

    assert runner.calls[-1] == second_time

    assert (
        second_result.run_time
        == second_time
    )

    print(
        "Test 4 — Time Preservation      : PASS"
    )

    # ======================================================
    # TEST 5 — NONE TIME PROTECTION
    # ======================================================

    try:

        controller.run_once(
            None
        )

        raise AssertionError(
            "None runtime should fail"
        )

    except ValueError:

        pass

    print(
        "Test 5 — Invalid Time Protection: PASS"
    )

    # ======================================================
    # TEST 6 — NONE RUNNER PROTECTION
    # ======================================================

    try:

        ResearchRuntimeController(
            None
        )

        raise AssertionError(
            "None runner should fail"
        )

    except ValueError:

        pass

    print(
        "Test 6 — Runner Validation       : PASS"
    )

    # ======================================================
    # TEST 7 — SINGLE DELEGATION
    # ======================================================

    assert len(
        runner.calls
    ) == 2

    print(
        "Test 7 — Single-Cycle Boundary  : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()

    print(
        "RESEARCH RUNTIME CONTROLLER : "
        "ALL TESTS PASSED"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()