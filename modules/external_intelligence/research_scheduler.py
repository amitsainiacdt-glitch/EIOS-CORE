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
import json
from pathlib import Path

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

    def __init__(self, state_path: str | Path | None = None):

        self._states: dict[
            str,
            ScheduledJobState,
        ] = {}
        self.state_path = Path(state_path) if state_path is not None else None
        self._saved_states = self._load_saved_states()

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

        self._states[job.job_id] = self._saved_states.get(
            job.job_id, ScheduledJobState(job_id=job.job_id)
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
        self._persist()

    def _load_saved_states(self) -> dict[str, ScheduledJobState]:
        if self.state_path is None or not self.state_path.exists():
            return {}
        try:
            payload = json.loads(self.state_path.read_text(encoding="utf-8"))
            if payload.get("schema_version") != 1 or not isinstance(payload.get("jobs"), dict):
                raise ValueError("unsupported scheduler-state schema")
            states = {}
            for job_id, value in payload["jobs"].items():
                if not isinstance(job_id, str) or not job_id or not isinstance(value, dict):
                    raise ValueError("invalid scheduler-state entry")
                last_run = datetime.fromisoformat(value["last_run"]) if value.get("last_run") else None
                next_run = datetime.fromisoformat(value["next_run"]) if value.get("next_run") else None
                if (last_run is None) != (next_run is None):
                    raise ValueError("incomplete scheduler-state entry")
                states[job_id] = ScheduledJobState(job_id, last_run, next_run)
            return states
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid persisted scheduler state: {exc}") from exc

    def _persist(self) -> None:
        if self.state_path is None:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": 1, "jobs": {
            job_id: {
                "last_run": state.last_run.isoformat() if state.last_run else None,
                "next_run": state.next_run.isoformat() if state.next_run else None,
            }
            for job_id, state in sorted(self._states.items())
            if state.last_run is not None
        }}
        temporary = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.state_path)

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
