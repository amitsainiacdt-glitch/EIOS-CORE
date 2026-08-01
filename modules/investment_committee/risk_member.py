from modules.investment_committee.committee_response import CommitteeResponse


class RiskMember:
    """
    Risk Committee Member

    Evaluates overall business risk using RiskSection.
    """

    def __init__(self):
        self.name = "Risk"

    def evaluate(self, research):

        dossier = research.master_dossier
        risk = dossier.risk

        if risk is None:
            return CommitteeResponse(
                member="Risk",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Risk analysis unavailable"],
                recommendation="Complete risk analysis first.",
                reason="Risk analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # -------------------------------------------------
        # Overall Risk Score
        # -------------------------------------------------

        overall_score = risk.overall_risk_score

        if overall_score >= 85:
            score += 40
            evidence.append(
                f"Excellent overall risk profile ({overall_score:.2f})"
            )
        elif overall_score >= 75:
            score += 30
            evidence.append(
                f"Acceptable overall risk profile ({overall_score:.2f})"
            )
        else:
            risks.append(
                f"Overall risk score is low ({overall_score:.2f})"
            )

        # -------------------------------------------------
        # Financial Risks
        # -------------------------------------------------

        if len(risk.financial_risks) == 0:
            score += 20
            evidence.append("No major financial risks")
        else:
            risks.extend(risk.financial_risks)

        # -------------------------------------------------
        # Management Risks
        # -------------------------------------------------

        if len(risk.management_risks) == 0:
            score += 15
            evidence.append("No management concerns")
        else:
            risks.extend(risk.management_risks)

        # -------------------------------------------------
        # Industry Risks
        # -------------------------------------------------

        if len(risk.industry_risks) == 0:
            score += 15
            evidence.append("Industry risks acceptable")
        else:
            risks.extend(risk.industry_risks)

        # -------------------------------------------------
        # Red Flags
        # -------------------------------------------------

        if len(risk.red_flags) == 0:
            score += 10
            evidence.append("No red flags detected")
        else:
            risks.extend(risk.red_flags)

        # -------------------------------------------------
        # Final Vote
        # -------------------------------------------------

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        confidence = min(100, score + 10)

        return CommitteeResponse(
            member="Risk",
            vote=vote,
            score=score,
            confidence=confidence,
            evidence=evidence,
            risks=risks,
            recommendation=f"Risk Score = {score}",
            reason=f"Overall Risk = {overall_score:.2f}",
        )