"""
EIOS
Everest Investment Operating System

Research Job Configuration
===========================

Provides deterministic production research-job definitions.

Design Principles
-----------------
- Creates ResearchJob objects only.
- No retrieval.
- No HTTP calls.
- No scheduling calculations.
- No runtime execution.
- No observation creation.
- No evidence creation.
- No investment analysis.
- Configuration remains separate from ResearchRuntime.
"""

from __future__ import annotations

from modules.external_intelligence.research_job import (
    ResearchJob,
)


class ResearchJobConfiguration:
    """
    Factory for production external research jobs.

    The configuration layer describes WHAT EIOS should
    monitor. The scheduler determines WHEN it runs.
    """

    # ======================================================
    # ANUP
    # ======================================================

    @staticmethod
    def anup_jobs() -> list[ResearchJob]:
        """
        Return the standard external research jobs for ANUP.
        """

        return [
            ResearchJob(
                job_id="ANUP-COMPANY-DEVELOPMENTS",
                company="The Anup Engineering Limited",
                ticker="ANUP",
                question=(
                    "Check recent company developments, "
                    "announcements and material business updates"
                ),
                intent="COMPANY_DEVELOPMENTS",
                frequency_minutes=1440,
                enabled=True,
                priority=100,
                max_sources=5,
                observation_category="External Web",
                observation_confidence=70.0,
            ),
            ResearchJob(
                job_id="ANUP-ORDERS-CAPACITY",
                company="The Anup Engineering Limited",
                ticker="ANUP",
                question=(
                    "Check for new orders, contracts, "
                    "capacity expansion and major project developments"
                ),
                intent="ORDER_AND_CAPACITY",
                frequency_minutes=1440,
                enabled=True,
                priority=95,
                max_sources=5,
                observation_category="External Web",
                observation_confidence=70.0,
            ),
            ResearchJob(
                job_id="ANUP-REGULATORY",
                company="The Anup Engineering Limited",
                ticker="ANUP",
                question=(
                    "Check for regulatory, government, "
                    "policy and compliance developments affecting the company"
                ),
                intent="REGULATORY_DEVELOPMENTS",
                frequency_minutes=1440,
                enabled=True,
                priority=90,
                max_sources=5,
                observation_category="External Web",
                observation_confidence=70.0,
            ),
            ResearchJob(
                job_id="ANUP-FINANCIAL-RESULTS",
                company="The Anup Engineering Limited",
                ticker="ANUP",
                question=(
                    "Check for recent financial results, "
                    "earnings updates, guidance and material financial developments"
                ),
                intent="FINANCIAL_DEVELOPMENTS",
                frequency_minutes=1440,
                enabled=True,
                priority=95,
                max_sources=5,
                observation_category="External Web",
                observation_confidence=70.0,
            ),
            ResearchJob(
                job_id="ANUP-MANAGEMENT-CORPORATE",
                company="The Anup Engineering Limited",
                ticker="ANUP",
                question=(
                    "Check for management changes, corporate actions, "
                    "promoter developments and major shareholder events"
                ),
                intent="MANAGEMENT_AND_CORPORATE",
                frequency_minutes=1440,
                enabled=True,
                priority=85,
                max_sources=5,
                observation_category="External Web",
                observation_confidence=70.0,
            ),
            ResearchJob(
                job_id="ANUP-INDUSTRY-COMPETITIVE",
                company="The Anup Engineering Limited",
                ticker="ANUP",
                question=(
                    "Check for industry developments, competitor activity, "
                    "technology changes and market developments relevant to the company"
                ),
                intent="INDUSTRY_AND_COMPETITIVE",
                frequency_minutes=1440,
                enabled=True,
                priority=80,
                max_sources=5,
                observation_category="External Web",
                observation_confidence=70.0,
            ),
        ]

    # ======================================================
    # ALL PRODUCTION JOBS
    # ======================================================

    @classmethod
    def all_jobs(
        cls,
    ) -> list[ResearchJob]:
        """
        Return all currently configured production jobs.
        """

        return cls.anup_jobs()


__all__ = [
    "ResearchJobConfiguration",
]