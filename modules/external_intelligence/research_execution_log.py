"""
EIOS
Everest Investment Operating System

Research Execution Log
======================

Passive record of one ResearchRuntime execution cycle.

This module performs no scheduling, retrieval, analysis,
or persistence of observations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ResearchExecutionLog:
    """
    Immutable record of one runtime execution cycle.
    """

    run_time: datetime

    status: str

    jobs_due: int

    jobs_executed: int

    observations_before: int

    observations_after: int

    observations_created: int

    failures: int

    duration_seconds: float


__all__ = [
    "ResearchExecutionLog",
]