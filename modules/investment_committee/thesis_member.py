from modules.investment_committee.committee_response import CommitteeResponse


class ThesisMember:
    """
    Investment Thesis Committee Member

    Evaluates whether the overall investment thesis
    remains strong and evidence-backed.
    """

    def __init__(self):
        self.name = "Thesis"

    def evaluate(self, research):

        dossier = research.master_dossier
        thesis = dossier.investment_thesis

        if not thesis:
            return CommitteeResponse(
                member="Thesis",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Investment thesis unavailable"],
                recommendation="Complete investment thesis.",
                reason="Investment thesis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # ------------------------------------
        # Thesis Strength
        # ------------------------------------

        strength = thesis.get("Strength", 0)

        if strength >= 85:
            score += 35
            evidence.append("Strong investment thesis")
        elif strength >= 70:
            score += 25
            evidence.append("Reasonable investment thesis")
        else:
            risks.append("Weak investment thesis")

        # ------------------------------------
        # Key Drivers
        # ------------------------------------

        drivers = thesis.get("Key Drivers", [])

        if drivers:
            score += 20
            evidence.append(f"{len(drivers)} key value drivers identified")
        else:
            risks.append("No key value drivers identified")

        # ------------------------------------
        # Risks
        # ------------------------------------

        thesis_risks = thesis.get("Key Risks", [])

        if len(thesis_risks) <= 3:
            score += 20
            evidence.append("Risk profile is manageable")
        else:
            risks.append("Numerous thesis risks identified")

        # ------------------------------------
        # Kill Switch
        # ------------------------------------

        kill_switch = thesis.get("Kill Switch")

        if kill_switch:
            score += 25
            evidence.append("Clear kill switch defined")
        else:
            risks.append("Kill switch not defined")

        # ------------------------------------
        # Final Vote
        # ------------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return CommitteeResponse(
            member="Thesis",
            vote=vote,
            score=score,
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Thesis Score = {score}",
            reason=f"Thesis Score = {score}",
        )