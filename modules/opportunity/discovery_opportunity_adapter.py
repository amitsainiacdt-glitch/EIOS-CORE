"""
EIOS
Everest Investment Operating System

Discovery → Opportunity Research Adapter

Purpose:
Converts a DiscoveryCandidate into an
OpportunityResearchIntake.

This adapter does NOT perform Opportunity analysis.
"""

from modules.discovery.discovery_candidate import (
    DiscoveryCandidate,
)

from modules.opportunity.discovery_opportunity_intake import (
    OpportunityResearchIntake,
)


class DiscoveryOpportunityAdapter:
    """
    Creates an Opportunity research intake from
    a Discovery Candidate.

    No analytical values are invented.
    """

    def create_intake(
        self,
        candidate: DiscoveryCandidate,
    ) -> OpportunityResearchIntake:

        return OpportunityResearchIntake(
            company=candidate.company_name,
            ticker=candidate.ticker,
            sector=candidate.sector,
            industry=candidate.industry,

            discovery_score=candidate.overall_score,
            discovery_confidence=candidate.confidence,
            discovery_status=candidate.status,
            discovery_source=candidate.source,

            strengths=list(
                candidate.strengths
            ),

            concerns=list(
                candidate.concerns
            ),

            catalysts=list(
                candidate.catalysts
            ),

            risks=list(
                candidate.risks
            ),

            discovery_notes=list(
                candidate.discovery_notes
            ),
        )


__all__ = [
    "DiscoveryOpportunityAdapter",
]