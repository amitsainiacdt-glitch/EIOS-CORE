"""
EIOS
Everest Investment Operating System

Research Execution Service Test
"""

from dataclasses import dataclass
from datetime import datetime

from modules.external_intelligence.research_execution_service import (
    ResearchExecutionService,
)

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_scheduler import (
    ResearchScheduler,
)

from modules.research.question_engine import (
    Question,
)


# ==========================================================
# FAKE ORCHESTRATOR
# ==========================================================


class FakeResult:
    pass


class FakeOrchestrator:

    def __init__(self):

        self.last_query = None

        self.last_arguments = None

        self.result = FakeResult()

    def execute(
        self,
        query,
        *,
        max_sources,
        observation_category,
        observation_confidence,
        cycle_id=None,
        job_id=None,
        retrieved_at=None,
    ):

        self.last_query = query

        self.last_arguments = {
            "max_sources": max_sources,
            "observation_category": (
                observation_category
            ),
            "observation_confidence": (
                observation_confidence
            ),
            "cycle_id": cycle_id,
            "job_id": job_id,
            "retrieved_at": retrieved_at,
        }

        return self.result


# ==========================================================
# FAKE QUERY BUILDER
# ==========================================================


class FakeQueryBuilder:

    def __init__(self):

        self.last_question = None

        self.last_arguments = None

    def build(
        self,
        *,
        company,
        ticker,
        question,
        intent,
    ):

        self.last_question = question

        self.last_arguments = {
            "company": company,
            "ticker": ticker,
            "question": question,
            "intent": intent,
        }

        return FakeQuery(
            company=company,
            ticker=ticker,
            question=question.question,
            intent=intent,
        )


# ==========================================================
# FAKE QUERY
# ==========================================================


@dataclass(frozen=True)
class FakeQuery:

    company: str
    ticker: str
    question: str
    intent: str


# ==========================================================
# JOB FACTORY
# ==========================================================


def make_job():

    return ResearchJob(
        job_id="JOB-001",
        company="The Anup Engineering Limited",
        ticker="ANUP",
        question="Check new developments",
        intent="GENERAL_RESEARCH",
        frequency_minutes=60,
        enabled=True,
        priority=80,
        max_sources=7,
        observation_category="External Web",
        observation_confidence=85.0,
    )


# ==========================================================
# MAIN
# ==========================================================


def main():

    print("=" * 60)
    print("EIOS RESEARCH EXECUTION SERVICE TEST")
    print("=" * 60)

    # ======================================================
    # SETUP
    # ======================================================

    scheduler = ResearchScheduler()

    job = make_job()

    scheduler.register(
        job
    )

    query_builder = FakeQueryBuilder()

    orchestrator = FakeOrchestrator()

    service = ResearchExecutionService(
        orchestrator=orchestrator,
        scheduler=scheduler,
        query_builder=query_builder,
    )

    run_time = datetime(
        2026,
        8,
        17,
        10,
        0,
        0,
    )

    # ======================================================
    # TEST 1 — EXECUTION
    # ======================================================

    result = service.execute(
        job,
        run_time=run_time,
    )

    assert result is orchestrator.result

    print(
        "Test 1 — Execution              : PASS"
    )

    # ======================================================
    # TEST 2 — QUESTION ADAPTER
    # ======================================================

    assert isinstance(
        query_builder.last_question,
        Question,
    )

    assert (
        query_builder.last_question.question
        == "Check new developments"
    )

    assert (
        query_builder.last_question.weight
        == 1
    )

    print(
        "Test 2 — Question Adapter       : PASS"
    )

    # ======================================================
    # TEST 3 — QUERY CONSTRUCTION
    # ======================================================

    assert query_builder.last_arguments == {
        "company": (
            "The Anup Engineering Limited"
        ),
        "ticker": "ANUP",
        "question": (
            query_builder.last_question
        ),
        "intent": "GENERAL_RESEARCH",
    }

    assert (
        orchestrator.last_query.company
        == "The Anup Engineering Limited"
    )

    assert (
        orchestrator.last_query.ticker
        == "ANUP"
    )

    assert (
        orchestrator.last_query.question
        == "Check new developments"
    )

    assert (
        orchestrator.last_query.intent
        == "GENERAL_RESEARCH"
    )

    print(
        "Test 3 — Query Construction     : PASS"
    )

    # ======================================================
    # TEST 4 — JOB CONFIGURATION
    # ======================================================

    assert orchestrator.last_arguments == {
        "max_sources": 7,
        "observation_category": "External Web",
        "observation_confidence": 85.0,
        "cycle_id": None,
        "job_id": "JOB-001",
        "retrieved_at": run_time,
    }

    print(
        "Test 4 — Job Configuration      : PASS"
    )

    # ======================================================
    # TEST 5 — SCHEDULER STATE
    # ======================================================

    state = scheduler.state(
        "JOB-001"
    )

    assert state is not None

    assert state.last_run == run_time

    assert state.next_run == datetime(
        2026,
        8,
        17,
        11,
        0,
        0,
    )

    print(
        "Test 5 — Scheduler Update       : PASS"
    )

    # ======================================================
    # TEST 6 — NOT DUE AFTER RUN
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
        "Test 6 — Interval Protection    : PASS"
    )

    # ======================================================
    # TEST 7 — DUE AFTER INTERVAL
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
        "Test 7 — Next Run Calculation   : PASS"
    )

    # ======================================================
    # TEST 8 — JOB IMMUTABILITY
    # ======================================================

    assert job.job_id == "JOB-001"

    assert job.company == (
        "The Anup Engineering Limited"
    )

    assert job.ticker == "ANUP"

    assert job.frequency_minutes == 60

    assert job.max_sources == 7

    print(
        "Test 8 — Job Immutability        : PASS"
    )

    # ======================================================
    # FINAL
    # ======================================================

    print()
    print(
        "RESEARCH EXECUTION SERVICE : "
        "ALL TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
