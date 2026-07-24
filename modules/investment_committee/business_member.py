"""
EIOS
Everest Investment Operating System

Business Committee Member
"""

from core.base_committee_member import BaseCommitteeMember

class BusinessMember(BaseCommitteeMember):
    """
    Evaluates Business Quality from the Master Dossier
    and casts the Business Committee vote.
    """

    MEMBER = "Business"

    BASE_SCORE = 50

    CRITERIA = {
        "Business Model": 10,
        "Moat": 15,
        "Growth Drivers": 10,
        "Market Size": 10,
    }

    RISK_WEIGHT = 5

    def evaluate(self, research):

        dossier = research.master_dossier
        business = dossier.business_quality

        if not business:

            return self.build_response(
                score=0,
                confidence=0,
                reason="Business Quality analysis unavailable.",
                warnings=[
                    "Business Quality section missing from Master Dossier."
                ],
            )

        score = self.BASE_SCORE

        evidence = []

        total_checks = len(self.CRITERIA) + 1

        # -----------------------------
        # Evaluate Core Business Fields
        # -----------------------------

        for field, weight in self.CRITERIA.items():

            if business.get(field):

                score += weight
                evidence.append(f"{field} analysed")

        # -----------------------------
        # Risk Evaluation
        # -----------------------------

        risks = business.get("Key Risks", [])

        if isinstance(risks, list) and len(risks) <= 2:

            score += self.RISK_WEIGHT
            evidence.append("Key Risks acceptable")

        # -----------------------------
        # Confidence
        # -----------------------------

        confidence = int((len(evidence) / total_checks) * 100)

        # -----------------------------
        # Metrics
        # -----------------------------

        metrics = {
            "Criteria Evaluated": total_checks,
            "Criteria Passed": len(evidence),
            "Business Score": score,
        }

        # -----------------------------
        # Reason
        # -----------------------------

        reason = (
            f"Business quality assessment completed. "
            f"{len(evidence)} of {total_checks} criteria satisfied."
        )

        # -----------------------------
        # Response
        # -----------------------------

        return self.build_response(
            score=score,
            confidence=confidence,
            reason=reason,
            evidence=evidence,
            metrics=metrics,
        )