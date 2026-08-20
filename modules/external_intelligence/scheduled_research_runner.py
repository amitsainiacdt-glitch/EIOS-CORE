"""
EIOS
Everest Investment Operating System

Scheduled Research Runner
==========================

Coordinates scheduled external research execution.

Responsibilities:
    - Read registered ResearchJob objects.
    - Ask ResearchScheduler which jobs are due.
    - Execute due jobs through ResearchExecutionService.
    - Return execution results.

Does NOT:
    - perform scheduling calculations.
    - perform HTTP retrieval directly.
    - create Evidence.
    - create Signals.
    - score Opportunities.
    - perform investment analysis.

The runner executes one scheduling cycle at a time.

It does NOT contain:
    - infinite loops
    - background threads
    - timers
    - automatic process management

Those concerns belong to the future runtime layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from modules.external_intelligence.research_execution_service import (
    ResearchExecutionService,
)

from modules.external_intelligence.research_job import (
    ResearchJob,
)

from modules.external_intelligence.research_job_registry import (
    ResearchJobRegistry,
)

from modules.external_intelligence.research_scheduler import (
    ResearchScheduler,
)


@dataclass
class ScheduledResearchResult:
    """
    Result of one scheduled research cycle.
    """

    run_time: datetime

    due_jobs: list[ResearchJob]

    executed_jobs: list[ResearchJob]

    results: list[object]


class ScheduledResearchRunner:
    """
    Executes one scheduled research cycle.

    The runner itself does not decide when it should run.
    The caller provides the current time.
    """

    def __init__(
        self,
        registry: ResearchJobRegistry,
        scheduler: ResearchScheduler,
        execution_service: ResearchExecutionService,
    ) -> None:

        if registry is None:
            raise ValueError(
                "registry must not be None"
            )

        if scheduler is None:
            raise ValueError(
                "scheduler must not be None"
            )

        if execution_service is None:
            raise ValueError(
                "execution_service must not be None"
            )

        self.registry = registry

        self.scheduler = scheduler

        self.execution_service = (
            execution_service
        )

    # ======================================================
    # RUN ONCE
    # ======================================================

    def run_once(
        self,
        now: datetime,
    ) -> ScheduledResearchResult:
        """
        Execute all currently due research jobs once.

        Jobs are obtained from the registry and filtered
        by the scheduler.
        """

        jobs = self.registry.enabled()

        due_jobs = self.scheduler.due_jobs(
            jobs,
            now,
        )

        executed_jobs = []

        results = []

        cycle_id = now.isoformat()

        for job in due_jobs:

            result = self.execution_service.execute(
                job,
                run_time=now,
                cycle_id=cycle_id,
            )

            executed_jobs.append(
                job
            )

            results.append(
                result
            )

        return ScheduledResearchResult(
            run_time=now,
            due_jobs=due_jobs,
            executed_jobs=executed_jobs,
            results=results,
        )


__all__ = [
    "ScheduledResearchResult",
    "ScheduledResearchRunner",
]
