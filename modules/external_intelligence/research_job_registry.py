"""
EIOS
Everest Investment Operating System

Research Job Registry
=====================

Stores and manages scheduled research jobs.

Design Principles
-----------------
- Stores ResearchJob objects only.
- Does not execute research.
- Does not perform scheduling.
- Does not retrieve external data.
- Deterministic job lookup.
- Duplicate job IDs are rejected.
"""

from __future__ import annotations

from modules.external_intelligence.research_job import (
    ResearchJob,
)


class ResearchJobRegistry:
    """
    Registry for EIOS external research jobs.
    """

    def __init__(self):

        self._jobs: dict[
            str,
            ResearchJob,
        ] = {}

    # ======================================================
    # ADD
    # ======================================================

    def add(
        self,
        job: ResearchJob,
    ) -> None:
        """
        Add a research job.

        Duplicate job IDs are rejected.
        """

        if job is None:
            raise ValueError(
                "job must not be None"
            )

        job.validate()

        if job.job_id in self._jobs:
            raise ValueError(
                f"Research job already exists: "
                f"{job.job_id}"
            )

        self._jobs[job.job_id] = job

    # ======================================================
    # GET
    # ======================================================

    def get(
        self,
        job_id: str,
    ) -> ResearchJob | None:
        """
        Return a job by ID.
        """

        return self._jobs.get(job_id)

    # ======================================================
    # ALL
    # ======================================================

    def all(
        self,
    ) -> list[ResearchJob]:
        """
        Return all registered jobs.
        """

        return list(
            self._jobs.values()
        )

    # ======================================================
    # ENABLED
    # ======================================================

    def enabled(
        self,
    ) -> list[ResearchJob]:
        """
        Return enabled research jobs.
        """

        return [
            job
            for job in self._jobs.values()
            if job.enabled
        ]

    # ======================================================
    # COUNT
    # ======================================================

    def count(self) -> int:
        """
        Return total number of registered jobs.
        """

        return len(
            self._jobs
        )

    # ======================================================
    # REMOVE
    # ======================================================

    def remove(
        self,
        job_id: str,
    ) -> ResearchJob | None:
        """
        Remove and return a job.

        Returns None when the job does not exist.
        """

        return self._jobs.pop(
            job_id,
            None,
        )

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(self) -> None:
        """
        Remove all jobs.
        """

        self._jobs.clear()


__all__ = [
    "ResearchJobRegistry",
]