from modules.investment_committee.committee_response import CommitteeResponse


class PortfolioMember:
    """
    Portfolio Committee Member

    Evaluates whether the investment fits within the current
    portfolio considering diversification, concentration,
    liquidity and risk.
    """

    def __init__(self):
        self.name = "Portfolio"

    def evaluate(self, research):

        dossier = research.master_dossier

        portfolio = getattr(dossier, "portfolio_analysis", {})

        if portfolio is None:
            portfolio = {}

        if not portfolio:
            return CommitteeResponse(
                member="Portfolio",
                vote="Watch",
                score=0,
                confidence=0,
                reason="Portfolio analysis unavailable.",
                evidence=[],
                warnings=[],
                metrics={},
                risks=["Portfolio analysis unavailable."],
                recommendation="Portfolio analysis unavailable.",
                weight=15,
            )

        score = 0
        evidence = []
        risks = []

        # Diversification
        if portfolio.get("Diversification"):
            score += 20
            evidence.append("Improves portfolio diversification")
        else:
            risks.append("Limited diversification benefit")

        # Sector Exposure
        if portfolio.get("Sector Exposure"):
            score += 20
            evidence.append("Sector allocation acceptable")
        else:
            risks.append("Sector concentration high")

        # Position Size
        if portfolio.get("Position Size"):
            score += 20
            evidence.append("Position sizing appropriate")
        else:
            risks.append("Position size needs review")

        # Liquidity
        if portfolio.get("Liquidity"):
            score += 20
            evidence.append("Adequate trading liquidity")
        else:
            risks.append("Liquidity concerns")

        # Correlation
        if portfolio.get("Correlation"):
            score += 20
            evidence.append("Low correlation with existing holdings")
        else:
            risks.append("High portfolio correlation")

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return CommitteeResponse(
            member="Portfolio",
            vote=vote,
            score=score,
            confidence=90,
            reason=f"Portfolio Fit Score = {score}",
            evidence=evidence,
            warnings=[],
            metrics={},
            risks=risks,
            recommendation=f"Portfolio Fit Score = {score}",
            weight=15,
        )