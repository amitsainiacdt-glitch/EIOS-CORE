"""
===============================================================================
EIOS
Everest Investment Operating System

Management Committee Member

Purpose:
    Evaluates typed Management Intelligence from the Master Dossier
    and casts the Management Committee vote.

Architecture:
    - Consumes MasterDossier.management as ManagementSection.
    - Performs committee evaluation only.
    - Does not mutate ManagementSection.
    - Does not depend on legacy management dictionaries.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from modules.investment_committee.committee_response import CommitteeResponse


class ManagementMember:
    """
    Evaluates management quality, governance, behaviour,
    communication, and capital allocation.
    """

    def __init__(self):
        self.name = "Management"

    def evaluate(self, research):

        dossier = research.master_dossier
        management = dossier.management

        # ==========================================================
        # Availability Check
        # ==========================================================

        management_available = bool(
            management.summary
            or management.evidence
            or management.score
            or management.rating
        )

        if not management_available:
            return CommitteeResponse(
                member="Management",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Management analysis unavailable"],
                recommendation="Complete management analysis first.",
                reason="Management analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # ==========================================================
        # Governance
        # ==========================================================

        if management.governance_score >= 85:
            score += 25
            evidence.append("Strong corporate governance")
        else:
            risks.append("Governance requires monitoring")

        # ==========================================================
        # Capital Allocation
        # ==========================================================

        if management.capital_allocation_score >= 80:
            score += 25
            evidence.append("Disciplined capital allocation")
        else:
            risks.append("Capital allocation needs improvement")

        # ==========================================================
        # Behaviour
        # ==========================================================

        if management.behaviour_score >= 80:
            score += 25
            evidence.append("Management execution is consistent")
        else:
            risks.append("Execution risk")

        # ==========================================================
        # Communication
        # ==========================================================

        if management.communication_score >= 80:
            score += 25
            evidence.append("Transparent communication")
        else:
            risks.append("Communication quality below expectation")

        # ==========================================================
        # Final Vote
        # ==========================================================

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return CommitteeResponse(
            member="Management",
            vote=vote,
            score=score,
            confidence=management.confidence,
            evidence=evidence,
            risks=risks,
            recommendation=f"Management Score = {score}",
            reason=f"Management Score = {score}",
        )