"""
EIOS
Everest Investment Operating System

Research Execution Logger
=========================

Stores execution-log records produced by ResearchRuntime.

This logger does not:
    - schedule jobs
    - perform retrieval
    - create observations
    - perform investment analysis
"""

from __future__ import annotations

from modules.external_intelligence.research_execution_log import (
    ResearchExecutionLog,
)


class ResearchExecutionLogger:
    """
    In-memory execution log.

    Persistence of execution logs can be added later behind
    this boundary without changing ResearchRuntime.
    """

    def __init__(self):

        self._logs: list[
            ResearchExecutionLog
        ] = []

    def record(
        self,
        log: ResearchExecutionLog,
    ) -> None:

        if log is None:
            raise ValueError(
                "log must not be None"
            )

        self._logs.append(
            log
        )

    def all(
        self,
    ) -> list[ResearchExecutionLog]:

        return list(
            self._logs
        )

    def latest(
        self,
    ) -> ResearchExecutionLog | None:

        if not self._logs:
            return None

        return self._logs[-1]

    def count(
        self,
    ) -> int:

        return len(
            self._logs
        )

    def clear(
        self,
    ) -> None:

        self._logs.clear()


__all__ = [
    "ResearchExecutionLogger",
]