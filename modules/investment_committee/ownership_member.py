from modules.investment_committee.committee_response import CommitteeResponse


class OwnershipMember:
    """
    Ownership Committee Member

    Reviews promoter ownership, institutional ownership,
    governance and shareholding quality.
    """

    def __init__(self):
        self.name = "Ownership"

    def evaluate(self, research):

        dossier = research.master_dossier
        ownership = dossier.ownership

        if ownership is None:
            return CommitteeResponse(
                member="Ownership",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Ownership analysis unavailable"],
                recommendation="Complete ownership analysis first.",
                reason="Ownership analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # ---------------------------------------------------------
        # Read OwnershipSection
        # ---------------------------------------------------------

        promoter_holding = ownership.promoter_holding
        promoter_pledge = ownership.promoter_pledge
        fii_holding = ownership.fii_holding
        dii_holding = ownership.dii_holding

        # ---------------------------------------------------------
        # Promoter Holding
        # ---------------------------------------------------------

        if promoter_holding >= 50:
            score += 30
            evidence.append(
                f"High promoter holding ({promoter_holding:.2f}%)"
            )
        elif promoter_holding >= 40:
            score += 20
            evidence.append(
                f"Healthy promoter holding ({promoter_holding:.2f}%)"
            )
        else:
            risks.append(
                f"Low promoter holding ({promoter_holding:.2f}%)"
            )

        # ---------------------------------------------------------
        # Promoter Pledge
        # ---------------------------------------------------------

        if promoter_pledge == 0:
            score += 25
            evidence.append("No promoter pledge")
        elif promoter_pledge <= 5:
            score += 15
            evidence.append(
                f"Low promoter pledge ({promoter_pledge:.2f}%)"
            )
        else:
            risks.append(
                f"High promoter pledge ({promoter_pledge:.2f}%)"
            )

        # ---------------------------------------------------------
        # FII Participation
        # ---------------------------------------------------------

        if fii_holding >= 15:
            score += 20
            evidence.append(
                f"Strong FII ownership ({fii_holding:.2f}%)"
            )
        else:
            risks.append(
                f"Low FII ownership ({fii_holding:.2f}%)"
            )

        # ---------------------------------------------------------
        # DII Participation
        # ---------------------------------------------------------

        if dii_holding >= 10:
            score += 15
            evidence.append(
                f"Healthy DII ownership ({dii_holding:.2f}%)"
            )
        else:
            risks.append(
                f"Low DII ownership ({dii_holding:.2f}%)"
            )

        # ---------------------------------------------------------
        # Governance Score
        # ---------------------------------------------------------

        if ownership.governance_score >= 80:
            score += 10
            evidence.append(
                f"Strong governance ({ownership.governance_score:.1f})"
            )
        else:
            risks.append(
                f"Governance score below target ({ownership.governance_score:.1f})"
            )

        # ---------------------------------------------------------
        # Vote
        # ---------------------------------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        confidence = min(100, score + 10)

        return CommitteeResponse(
            member="Ownership",
            vote=vote,
            score=score,
            confidence=confidence,
            evidence=evidence,
            risks=risks,
            recommendation=f"Ownership Score = {score}",
            reason=(
                f"Promoter={promoter_holding:.2f}%, "
                f"Pledge={promoter_pledge:.2f}%, "
                f"FII={fii_holding:.2f}%, "
                f"DII={dii_holding:.2f}%"
            ),
        )