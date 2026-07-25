from modules.investment_committee.committee_response import CommitteeResponse


class ManagementMember:
    """
    Management Committee Member

    Evaluates management quality, governance and capital allocation.
    """

    def __init__(self):
        self.name = "Management"

    def evaluate(self, research):

        dossier = research.master_dossier
        management = dossier.management_analysis

        if not management:
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

        # -------------------------------
        # Governance
        # -------------------------------

        governance = management.get("Governance", {})
        if governance.get("Score", 0) >= 85:
            score += 25
            evidence.append("Strong corporate governance")
        else:
            risks.append("Governance requires monitoring")

        # -------------------------------
        # Capital Allocation
        # -------------------------------

        capital = management.get("Capital Allocation", {})
        if capital.get("Score", 0) >= 80:
            score += 25
            evidence.append("Disciplined capital allocation")
        else:
            risks.append("Capital allocation needs improvement")

        # -------------------------------
        # Behaviour
        # -------------------------------

        behaviour = management.get("Behaviour", {})
        if behaviour.get("Score", 0) >= 80:
            score += 25
            evidence.append("Management execution is consistent")
        else:
            risks.append("Execution risk")

        # -------------------------------
        # Communication
        # -------------------------------

        communication = management.get("Communication", {})
        if communication.get("Score", 0) >= 80:
            score += 25
            evidence.append("Transparent communication")
        else:
            risks.append("Communication quality below expectation")

        # -------------------------------
        # Final Vote
        # -------------------------------

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
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Management Score = {score}",
            reason=f"Management Score = {score}",
        )