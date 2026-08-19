"""
EIOS
Everest Investment Operating System

Research Runtime Controller
===========================

Coordinates one complete external research runtime cycle.

Responsibilities:
    - Accept the current runtime time.
    - Invoke ScheduledResearchRunner.
    - Return the completed research cycle.
    - Preserve the existing scheduling architecture.

Does NOT:
    - perform scheduling calculations.
    - perform HTTP retrieval.
    - perform searches.
    - create Evidence.
    - create Signals.
    - score Opportunities.
    - perform investment analysis.
    - implement infinite loops.
    - sleep.
    - create background threads.
    - manage operating-system processes.

The controller is intentionally a thin runtime boundary.

A future operating-system scheduler such as Windows
Task Scheduler may invoke this controller periodically.
"""

from __future__ import annotations

from datetime import datetime

from modules.external_intelligence.scheduled_research_runner import (
    ScheduledResearchResult,
    ScheduledResearchRunner,
)


class ResearchRuntimeController:
    """
    Executes one complete EIOS external research cycle.

    The controller delegates all scheduling and research
    responsibilities to existing EIOS components.
    """

    def __init__(
        self,
        runner: ScheduledResearchRunner,
    ) -> None:

        if runner is None:
            raise ValueError(
                "runner must not be None"
            )

        self.runner = runner

    # ======================================================
    # RUN ONCE
    # ======================================================

    def run_once(
        self,
        now: datetime,
    ) -> ScheduledResearchResult:
        """
        Execute one complete research runtime cycle.

        The supplied timestamp is passed unchanged to the
        existing ScheduledResearchRunner.
        """

        if now is None:
            raise ValueError(
                "now must not be None"
            )

        return self.runner.run_once(
            now
        )


__all__ = [
    "ResearchRuntimeController",
]