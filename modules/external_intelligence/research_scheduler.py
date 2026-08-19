"""
EIOS
Everest Investment Operating System

Research Scheduler
==================

Determines which research jobs are due.

The scheduler does NOT:
    - perform HTTP requests
    - perform searches
    - create observations
    - create evidence
    - score opportunities
    - perform investment analysis

It only determines scheduling state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from modules.external_intelligence.research_job import (
    ResearchJob,
)


@dataclass(frozen=True)
class ScheduledJobState:
    """
    Scheduling state for one research job.
    """

    job_id: str

    last_run: datetime | None = None

    next_run: datetime | None = None


class ResearchScheduler:
    """
    Deterministic research scheduler.

    Scheduling decisions are based entirely on:
        - job configuration
        - last execution time
        - current time
    """

    def __init__(self):

        self._states: dict[
            str,
            ScheduledJobState,
        ] = {}

    # ======================================================
    # REGISTER
    # ======================================================

    def register(
        self,
        job: ResearchJob,
    ) -> None:
        """
        Register a research job with the scheduler.
        """

        if job is None:
            raise ValueError(
                "job must not be None"
            )

        job.validate()

        if job.job_id in self._states:
            raise ValueError(
                f"Job already registered: "
                f"{job.job_id}"
            )

        self._states[
            job.job_id
        ] = ScheduledJobState(
            job_id=job.job_id
        )

    # ======================================================
    # STATE
    # ======================================================

    def state(
        self,
        job_id: str,
    ) -> ScheduledJobState | None:
        """
        Return current scheduling state.
        """

        return self._states.get(
            job_id
        )

    # ======================================================
    # DUE
    # ======================================================

    def is_due(
        self,
        job: ResearchJob,
        now: datetime,
    ) -> bool:
        """
        Determine whether a job is due.

        A job is due when:

            enabled == True

        and either:

            it has never run

        or:

            current time >= next_run
        """

        if not job.enabled:
            return False

        state = self._states.get(
            job.job_id
        )

        if state is None:
            raise ValueError(
                f"Job is not registered: "
                f"{job.job_id}"
            )

        if state.next_run is None:
            return True

        return now >= state.next_run

    # ======================================================
    # MARK RUN
    # ======================================================

    def mark_run(
        self,
        job: ResearchJob,
        run_time: datetime,
    ) -> None:
        """
        Record a successful scheduling event.

        This does not execute the research job.
        """

        if job.job_id not in self._states:
            raise ValueError(
                f"Job is not registered: "
                f"{job.job_id}"
            )

        next_run = (
            run_time
            + timedelta(
                minutes=job.frequency_minutes
            )
        )

        self._states[
            job.job_id
        ] = ScheduledJobState(
            job_id=job.job_id,
            last_run=run_time,
            next_run=next_run,
        )

    # ======================================================
    # DUE JOBS
    # ======================================================

    def due_jobs(
        self,
        jobs: list[ResearchJob],
        now: datetime,
    ) -> list[ResearchJob]:
        """
        Return enabled jobs that are due.

        Jobs are ordered by priority descending.
        """

        due = [
            job
            for job in jobs
            if self.is_due(
                job,
                now,
            )
        ]

        return sorted(
            due,
            key=lambda job: (
                -job.priority,
                job.job_id,
            ),
        )


__all__ = [
    "ScheduledJobState",
    "ResearchScheduler",
]