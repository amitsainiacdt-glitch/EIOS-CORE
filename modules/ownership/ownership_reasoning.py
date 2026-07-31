"""
===============================================================================
Module: ownership_reasoning.py

Purpose:
    Generate institutional-quality ownership reasoning.

Responsibilities:
    - Interpret ownership scores
    - Explain strengths
    - Highlight risks
    - Generate investment insights
    - Produce Ownership Narrative

Author:
    EIOS
===============================================================================
"""

from .ownership_scorecard import OwnershipScoreCard


class OwnershipReasoningEngine:
    """
    Generates investment reasoning from ownership analysis.
    """

    def generate(
        self,
        scorecard: OwnershipScoreCard,
    ) -> str:

        observations = []

        # --------------------------------------------------------------
        # Overall Ownership Quality
        # --------------------------------------------------------------

        if scorecard.total_score >= 90:
            observations.append(
                "Ownership quality is exceptional."
            )

        elif scorecard.total_score >= 80:
            observations.append(
                "Ownership quality is excellent."
            )

        elif scorecard.total_score >= 70:
            observations.append(
                "Ownership quality is strong."
            )

        elif scorecard.total_score >= 60:
            observations.append(
                "Ownership quality is satisfactory."
            )

        else:
            observations.append(
                "Ownership quality requires caution."
            )

        # --------------------------------------------------------------
        # Promoter
        # --------------------------------------------------------------

        if scorecard.promoter_score >= 85:
            observations.append(
                "Promoter ownership demonstrates strong long-term commitment."
            )

        elif scorecard.promoter_score >= 70:
            observations.append(
                "Promoter ownership appears healthy."
            )

        else:
            observations.append(
                "Promoter ownership should be monitored."
            )

        # --------------------------------------------------------------
        # FII
        # --------------------------------------------------------------

        if scorecard.fii_score >= 80:
            observations.append(
                "Foreign institutional participation is supportive."
            )

        elif scorecard.fii_score < 50:
            observations.append(
                "Limited foreign institutional participation."
            )

        # --------------------------------------------------------------
        # DII
        # --------------------------------------------------------------

        if scorecard.dii_score >= 80:
            observations.append(
                "Domestic institutions show strong conviction."
            )

        elif scorecard.dii_score < 50:
            observations.append(
                "Domestic institutional ownership is relatively weak."
            )

        # --------------------------------------------------------------
        # Insider
        # --------------------------------------------------------------

        if scorecard.insider_score >= 80:
            observations.append(
                "Insider activity aligns with shareholder interests."
            )

        elif scorecard.insider_score < 50:
            observations.append(
                "Insider activity deserves closer review."
            )

        # --------------------------------------------------------------
        # Governance
        # --------------------------------------------------------------

        if scorecard.governance_score >= 80:
            observations.append(
                "Ownership structure supports good governance."
            )

        elif scorecard.governance_score < 50:
            observations.append(
                "Governance signals require further investigation."
            )

        # --------------------------------------------------------------
        # Final Conclusion
        # --------------------------------------------------------------

        if scorecard.total_score >= 85:
            observations.append(
                "Overall ownership profile strengthens the long-term investment case."
            )

        elif scorecard.total_score >= 70:
            observations.append(
                "Ownership profile is supportive but should continue to be monitored."
            )

        else:
            observations.append(
                "Ownership factors introduce additional investment risk."
            )

        return " ".join(observations)