class ValuationMember:
    """
    Valuation Committee Member

    Reviews the Valuation Analysis section of the Master Dossier
    and determines whether the stock offers an adequate
    margin of safety.
    """

    def __init__(self):
        self.name = "Valuation Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        valuation = dossier.valuation

        if not valuation:
            return {
                "Member": "Valuation",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Weight": 20,
                "Evidence": [],
                "Risks": [],
                "Recommendation": "Valuation unavailable.",
                "Reason": "Valuation analysis unavailable."
            }

        score = 0
        evidence = []
        risks = []

        intrinsic = valuation.get("Intrinsic Value")
        cmp = valuation.get("Current Price")
        mos = valuation.get("Margin of Safety")

        # -----------------------------
        # Margin of Safety
        # -----------------------------

        if mos is not None:

            if mos >= 30:
                score += 40
                evidence.append("Excellent margin of safety")

            elif mos >= 20:
                score += 30
                evidence.append("Good margin of safety")

            elif mos >= 10:
                score += 20
                evidence.append("Limited margin of safety")

            else:
                score += 5
                risks.append("Very small margin of safety")

        # -----------------------------
        # Intrinsic Value
        # -----------------------------

        if intrinsic is not None and cmp is not None:

            if intrinsic > cmp:
                score += 30
                evidence.append("Trading below intrinsic value")

            else:
                score += 10
                risks.append("Trading above intrinsic value")

        # -----------------------------
        # Expected CAGR
        # -----------------------------

        cagr = valuation.get("Expected CAGR")

        if cagr is not None:

            if cagr >= 20:
                score += 30
                evidence.append("High expected CAGR")

            elif cagr >= 15:
                score += 20
                evidence.append("Good expected CAGR")

            elif cagr >= 10:
                score += 10
                evidence.append("Moderate expected CAGR")

            else:
                risks.append("Low expected CAGR")

        # -----------------------------
        # Final Vote
        # -----------------------------

        if score >= 85:
            vote = "Pass"

        elif score >= 65:
            vote = "Watch"

        else:
            vote = "Reject"

        return {

            "Member": "Valuation",

            "Vote": vote,

            "Score": score,

            "Confidence": 90,

            "Weight": 20,

            "Evidence": evidence,

            "Risks": risks,

            "Recommendation":
                f"Valuation Score = {score}",

            "Reason":
                f"Valuation Score = {score}"
        }