"""
EIOS
Everest Investment Operating System

Business Committee Member

Consumes the typed BusinessSection from MasterDossier.business.
"""

from core.base_committee_member import BaseCommitteeMember


class BusinessMember(BaseCommitteeMember):
    """
    Evaluates typed Business Quality intelligence from the Master Dossier
    and casts the Business Committee vote.
    """

    MEMBER = "Business"

    BASE_SCORE = 50

    RISK_WEIGHT = 5

    def evaluate(self, research):

        dossier = research.master_dossier
        business = dossier.business

        # ---------------------------------------------------------
        # Availability Check
        # ---------------------------------------------------------

        business_analysis_completed = bool(
            business.summary
            or business.score
            or business.rating
            or business.business_model
        )

        if not business_analysis_completed:

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

        total_checks = 5

        # ---------------------------------------------------------
        # Business Model
        # ---------------------------------------------------------

        if business.business_model:
            score += 10
            evidence.append("Business Model analysed")

        # ---------------------------------------------------------
        # Moat
        # ---------------------------------------------------------

        if business.moat:
            score += 15
            evidence.append("Moat analysed")

        # ---------------------------------------------------------
        # Growth Drivers
        # ---------------------------------------------------------

        if business.growth_drivers:
            score += 10
            evidence.append("Growth Drivers analysed")

        # ---------------------------------------------------------
        # Addressable Market
        # ---------------------------------------------------------

        if business.addressable_market:
            score += 10
            evidence.append("Market Size analysed")

        # ---------------------------------------------------------
        # Risk Evaluation
        # ---------------------------------------------------------

        if len(business.key_risks) <= 2:
            score += self.RISK_WEIGHT
            evidence.append("Key Risks acceptable")

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------

        confidence = int(
            (len(evidence) / total_checks) * 100
        )

        # ---------------------------------------------------------
        # Metrics
        # ---------------------------------------------------------

        metrics = {
            "Criteria Evaluated": total_checks,
            "Criteria Passed": len(evidence),
            "Business Score": score,
        }

        # ---------------------------------------------------------
        # Reason
        # ---------------------------------------------------------

        reason = (
            "Business quality assessment completed. "
            f"{len(evidence)} of {total_checks} criteria satisfied."
        )

        # ---------------------------------------------------------
        # Committee Response
        # ---------------------------------------------------------

        return self.build_response(
            score=score,
            confidence=confidence,
            reason=reason,
            evidence=evidence,
            metrics=metrics,
        )