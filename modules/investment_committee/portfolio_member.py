class PortfolioMember:
    """
    Portfolio Committee Member

    Evaluates whether the investment fits within the current
    portfolio considering diversification, concentration,
    liquidity and risk.
    """

    def __init__(self):
        self.name = "Portfolio Committee"

    def evaluate(self, research):

        dossier = research.master_dossier
        portfolio = dossier.portfolio_analysis

        if not portfolio:
            return {
                "Member": "Portfolio",
                "Vote": "Watch",
                "Score": 0,
                "Confidence": 0,
                "Weight": 15,
                "Evidence": [],
                "Risks": [],
                "Recommendation": "Portfolio analysis unavailable.",
                "Reason": "Portfolio analysis unavailable."
            }

        score = 0
        evidence = []
        risks = []

        # -----------------------------------
        # Diversification
        # -----------------------------------

        if portfolio.get("Diversification"):
            score += 20
            evidence.append("Improves portfolio diversification")
        else:
            risks.append("Limited diversification benefit")

        # -----------------------------------
        # Sector Exposure
        # -----------------------------------

        if portfolio.get("Sector Exposure"):
            score += 20
            evidence.append("Sector allocation acceptable")
        else:
            risks.append("Sector concentration high")

        # -----------------------------------
        # Position Size
        # -----------------------------------

        if portfolio.get("Position Size"):
            score += 20
            evidence.append("Position sizing appropriate")
        else:
            risks.append("Position size needs review")

        # -----------------------------------
        # Liquidity
        # -----------------------------------

        if portfolio.get("Liquidity"):
            score += 20
            evidence.append("Adequate trading liquidity")
        else:
            risks.append("Liquidity concerns")

        # -----------------------------------
        # Portfolio Correlation
        # -----------------------------------

        if portfolio.get("Correlation"):
            score += 20
            evidence.append("Low correlation with existing holdings")
        else:
            risks.append("High portfolio correlation")

        # -----------------------------------
        # Final Vote
        # -----------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return {

            "Member": "Portfolio",

            "Vote": vote,

            "Score": score,

            "Confidence": 90,

            "Weight": 15,

            "Evidence": evidence,

            "Risks": risks,

            "Recommendation":
                f"Portfolio Fit Score = {score}",

            "Reason":
                f"Portfolio Fit Score = {score}"
        }