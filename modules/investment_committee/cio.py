class ChiefInvestmentOfficer:
    """
    Chief Investment Officer

    Reviews all committee recommendations and
    makes the final investment decision.
    """

    def __init__(self):
        self.name = "Chief Investment Officer"

    def decide(self, committee_data):

        total_weight = 0
        weighted_score = 0

        evidence = []
        risks = []

        pass_votes = 0
        watch_votes = 0
        reject_votes = 0

        for member in committee_data.values():

            weight = member.get("Weight", 10)
            score = member.get("Score", 0)

            weighted_score += score * weight
            total_weight += weight

            evidence.extend(member.get("Evidence", []))
            risks.extend(member.get("Risks", []))

            vote = member.get("Vote")

            if vote == "Pass":
                pass_votes += 1

            elif vote == "Watch":
                watch_votes += 1

            else:
                reject_votes += 1

        if total_weight == 0:
            final_score = 0
        else:
            final_score = round(weighted_score / total_weight, 2)

        # -----------------------------------
        # Final Decision
        # -----------------------------------

        if final_score >= 85 and reject_votes == 0:

            decision = "STRONG BUY"

        elif final_score >= 75:

            decision = "BUY"

        elif final_score >= 60:

            decision = "WATCH"

        else:

            decision = "REJECT"

        confidence = round(
            (pass_votes / len(committee_data)) * 100,
            2
        )

        return {

            "Decision": decision,

            "Committee Score": final_score,

            "Confidence": confidence,

            "Pass Votes": pass_votes,

            "Watch Votes": watch_votes,

            "Reject Votes": reject_votes,

            "Evidence": evidence,

            "Risks": risks
        }