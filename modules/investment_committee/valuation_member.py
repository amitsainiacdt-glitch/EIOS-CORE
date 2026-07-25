from modules.investment_committee.committee_response import CommitteeResponse


class ValuationMember:
    """
    Valuation Committee Member

    Evaluates intrinsic value, margin of safety,
    owner earnings and expected returns.
    """

    def __init__(self):
        self.name = "Valuation"

    def evaluate(self, research):

        dossier = research.master_dossier
        valuation = dossier.valuation_analysis

        if not valuation:
            return CommitteeResponse(
                member="Valuation",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Valuation analysis unavailable"],
                recommendation="Complete valuation analysis first.",
                reason="Valuation analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # ------------------------------------
        # Owner Earnings
        # ------------------------------------

        owner = valuation.get("Owner Earnings", {})

        owner_earnings = owner.get("Owner Earnings", 0)

        if owner_earnings > 0:
            score += 30
            evidence.append(
                f"Positive Owner Earnings ({owner_earnings})"
            )
        else:
            risks.append("Owner earnings unavailable")

        # ------------------------------------
        # Intrinsic Value
        # ------------------------------------

        intrinsic = valuation.get("Intrinsic Value")

        if intrinsic is not None:
            score += 25
            evidence.append("Intrinsic value estimated")
        else:
            risks.append("Intrinsic value not calculated")

        # ------------------------------------
        # Margin of Safety
        # ------------------------------------

        mos = valuation.get("Margin of Safety")

        if mos is not None:

            if mos >= 30:
                score += 25
                evidence.append("Excellent margin of safety")

            elif mos >= 15:
                score += 15
                evidence.append("Acceptable margin of safety")

            else:
                risks.append("Limited margin of safety")

        else:
            risks.append("Margin of safety unavailable")

        # ------------------------------------
        # Expected CAGR
        # ------------------------------------

        expected = valuation.get("Expected CAGR")

        if expected is not None:

            if expected >= 18:
                score += 20
                evidence.append("Excellent expected CAGR")

            elif expected >= 12:
                score += 10
                evidence.append("Reasonable expected CAGR")

            else:
                risks.append("Expected return is modest")

        else:
            risks.append("Expected CAGR unavailable")

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
            member="Valuation",
            vote=vote,
            score=score,
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Valuation Score = {score}",
            reason=f"Valuation Score = {score}",
        )