"""
EIOS
Everest Investment Operating System

Opportunity Ranking Engine
==========================

Competitive selection layer for the Opportunity Engine.

Purpose
-------
Ranks synthesized opportunities against one another for scarce
EIOS research capacity.

Important distinction
---------------------
Opportunity Synthesis asks:

    "Is this individual opportunity attractive?"

Opportunity Ranking asks:

    "Which of these opportunities deserve research priority
     relative to the alternatives?"

Design principles
-----------------
- Reuse existing synthesis outputs.
- Do not recalculate Catalyst, Mispricing, Asymmetry,
  Expectation Gap, or Evidence scores.
- Keep confidence separate from attractiveness.
- Apply hard evidence and risk gates.
- Reward research efficiency.
- Ranking is comparative.
- No valuation calculations.
- No portfolio allocation.
- No investment recommendation.
"""

from typing import List, Sequence, Tuple

from modules.opportunity.ranking.ranking_models import (
    OpportunityRanking,
    OpportunityRankingSet,
)

from modules.opportunity.opportunity_synthesis_engine import (
    OpportunitySynthesis,
)


# ==========================================================
# RANKING ENGINE
# ==========================================================


class OpportunityRankingEngine:
    """
    Competitive ranking engine for synthesized opportunities.
    """

    # ------------------------------------------------------
    # Institutional thresholds
    # ------------------------------------------------------

    MIN_OPPORTUNITY_SCORE = 60.0

    MIN_CONFIDENCE = 60.0

    MIN_EVIDENCE_SCORE = 50.0

    MIN_EVIDENCE_CONFIDENCE = 60.0

    MAX_PERMANENT_LOSS_PROBABILITY = 25.0

    MAX_EXPECTED_TIME_MONTHS = 120.0

    # ------------------------------------------------------
    # Ranking weights
    #
    # These weights operate on already-produced synthesis
    # outputs. They do not duplicate underlying engines.
    # ------------------------------------------------------

    OPPORTUNITY_WEIGHT = 0.40

    CONFIDENCE_WEIGHT = 0.20

    RISK_ADJUSTED_WEIGHT = 0.20

    RESEARCH_EFFICIENCY_WEIGHT = 0.20

    # ======================================================
    # PUBLIC API
    # ======================================================

    def rank(
        self,
        opportunities: Sequence[
            OpportunitySynthesis
        ],
    ) -> OpportunityRankingSet:
        """
        Rank multiple synthesized opportunities.

        Ranking is comparative and deterministic.
        """

        opportunity_list = list(
            opportunities
        )

        if not opportunity_list:

            return OpportunityRankingSet(
                warnings=[
                    "No opportunities supplied for ranking."
                ]
            )

        preliminary: List[
            OpportunityRanking
        ] = []

        # --------------------------------------------------
        # Evaluate each opportunity independently
        # --------------------------------------------------

        for opportunity in opportunity_list:

            ranking = self._evaluate(
                opportunity
            )

            preliminary.append(
                ranking
            )

        # --------------------------------------------------
        # Sort eligible opportunities first
        # --------------------------------------------------

        preliminary.sort(
            key=lambda item: (
                item.eligible,
                item.research_priority_score,
                item.opportunity_score,
                item.confidence_score,
            ),
            reverse=True,
        )

        # --------------------------------------------------
        # Assign ranks
        # --------------------------------------------------

        eligible_rank = 0

        for item in preliminary:

            if item.eligible:

                eligible_rank += 1

                item.rank = eligible_rank

                self._assign_tier(
                    item
                )

            else:

                item.rank = 0

                item.tier = "EXCLUDED"

                item.priority = "DO NOT PROMOTE"

        eligible = [
            item
            for item in preliminary
            if item.eligible
        ]

        excluded = [
            item
            for item in preliminary
            if not item.eligible
        ]

        top_company = ""

        top_score = 0.0

        if eligible:

            top_company = (
                eligible[0].company
            )

            top_score = (
                eligible[0]
                .research_priority_score
            )

        return OpportunityRankingSet(
            rankings=preliminary,
            eligible_count=len(
                eligible
            ),
            excluded_count=len(
                excluded
            ),
            top_company=top_company,
            top_priority_score=top_score,
        )

    # ======================================================
    # INDIVIDUAL EVALUATION
    # ======================================================

    def _evaluate(
        self,
        opportunity: OpportunitySynthesis,
    ) -> OpportunityRanking:
        """
        Convert an individual synthesis into a ranking
        candidate.

        No underlying analytical score is recalculated.
        """

        result = OpportunityRanking()

        result.company = (
            opportunity.company
        )

        # --------------------------------------------------
        # Source metrics
        # --------------------------------------------------

        result.opportunity_score = (
            opportunity.opportunity_score
        )

        result.confidence_score = (
            opportunity.confidence
        )

        result.evidence_score = (
            opportunity.evidence_score
        )

        result.evidence_confidence = (
            opportunity.evidence_confidence
        )

        result.asymmetry_score = (
            opportunity.asymmetry_score
        )

        # --------------------------------------------------
        # Gates
        # --------------------------------------------------

        (
            result.evidence_gate_passed,
            evidence_reasons,
        ) = self._evidence_gate(
            opportunity
        )

        (
            result.permanent_loss_gate_passed,
            loss_reasons,
        ) = self._permanent_loss_gate(
            opportunity
        )

        (
            result.confidence_gate_passed,
            confidence_reasons,
        ) = self._confidence_gate(
            opportunity
        )

        (
            result.kill_switch_gate_passed,
            kill_switch_reasons,
        ) = self._kill_switch_gate(
            opportunity
        )

        # --------------------------------------------------
        # Exclusions
        # --------------------------------------------------

        gate_reasons = (
            evidence_reasons
            + loss_reasons
            + confidence_reasons
            + kill_switch_reasons
        )

        result.exclusion_reasons.extend(
            gate_reasons
        )

        result.eligible = (
            len(
                result.exclusion_reasons
            )
            == 0
        )

        # --------------------------------------------------
        # Risk-adjusted score
        # --------------------------------------------------

        result.risk_adjusted_score = (
            self._risk_adjusted_score(
                opportunity
            )
        )

        # --------------------------------------------------
        # Research efficiency
        # --------------------------------------------------

        result.research_efficiency_score = (
            self._research_efficiency(
                opportunity
            )
        )

        # --------------------------------------------------
        # Competitive priority
        # --------------------------------------------------

        result.research_priority_score = (
            self._research_priority(
                result
            )
        )

        # --------------------------------------------------
        # Reasoning
        # --------------------------------------------------

        self._build_reasons(
            result,
            opportunity,
        )

        return result

    # ======================================================
    # EVIDENCE GATE
    # ======================================================

    def _evidence_gate(
        self,
        opportunity: OpportunitySynthesis,
    ) -> Tuple[bool, List[str]]:
        """
        Evidence is a hard qualification gate.
        """

        reasons = []

        if not opportunity.evidence_sufficient:

            reasons.append(
                "Evidence gate failed: evidence "
                "is insufficient."
            )

        if (
            opportunity.evidence_score
            < self.MIN_EVIDENCE_SCORE
        ):

            reasons.append(
                "Evidence gate failed: evidence score "
                "is below the minimum threshold."
            )

        if (
            opportunity.evidence_confidence
            < self.MIN_EVIDENCE_CONFIDENCE
        ):

            reasons.append(
                "Evidence gate failed: evidence confidence "
                "is below the minimum threshold."
            )

        return (
            len(reasons) == 0,
            reasons,
        )

    # ======================================================
    # PERMANENT LOSS GATE
    # ======================================================

    def _permanent_loss_gate(
        self,
        opportunity: OpportunitySynthesis,
    ) -> Tuple[bool, List[str]]:
        """
        Prevent excessive permanent-capital-loss risk
        from being hidden by a high opportunity score.
        """

        reasons = []

        if (
            opportunity.permanent_loss_probability
            > self.MAX_PERMANENT_LOSS_PROBABILITY
        ):

            reasons.append(
                "Permanent-loss gate failed: permanent "
                "loss probability exceeds the institutional "
                "threshold."
            )

        return (
            len(reasons) == 0,
            reasons,
        )

    # ======================================================
    # CONFIDENCE GATE
    # ======================================================

    def _confidence_gate(
        self,
        opportunity: OpportunitySynthesis,
    ) -> Tuple[bool, List[str]]:
        """
        Require sufficient analytical confidence.
        """

        reasons = []

        if (
            opportunity.confidence
            < self.MIN_CONFIDENCE
        ):

            reasons.append(
                "Confidence gate failed: synthesis "
                "confidence is below the minimum threshold."
            )

        return (
            len(reasons) == 0,
            reasons,
        )

    # ======================================================
    # KILL SWITCH GATE
    # ======================================================

    @staticmethod
    def _kill_switch_gate(
        opportunity: OpportunitySynthesis,
    ) -> Tuple[bool, List[str]]:
        """
        A researchable opportunity should have explicit
        invalidation logic.

        The Synthesis Engine already carries kill-switch
        information; ranking merely qualifies it.
        """

        reasons = []

        if not opportunity.kill_switches:

            reasons.append(
                "Kill-switch gate failed: no explicit "
                "kill switch is recorded."
            )

        return (
            len(reasons) == 0,
            reasons,
        )

    # ======================================================
    # RISK-ADJUSTED SCORE
    # ======================================================

    @staticmethod
    def _risk_adjusted_score(
        opportunity: OpportunitySynthesis,
    ) -> float:
        """
        Adjust the existing Opportunity Score for
        permanent-loss and downside risk.

        This does not recalculate the Opportunity Score.
        """

        score = (
            opportunity.opportunity_score
        )

        permanent_loss_penalty = min(
            40.0,
            opportunity.permanent_loss_probability
            * 0.80,
        )

        downside_penalty = min(
            20.0,
            opportunity.downside_probability
            * 0.20,
        )

        adjusted = (
            score
            - permanent_loss_penalty
            - downside_penalty
        )

        return round(
            max(
                0.0,
                min(
                    100.0,
                    adjusted,
                ),
            ),
            2,
        )

    # ======================================================
    # RESEARCH EFFICIENCY
    # ======================================================

    def _research_efficiency(
        self,
        opportunity: OpportunitySynthesis,
    ) -> float:
        """
        Measure expected return relative to time required
        for the thesis.

        The result is normalized to 0-100.
        """

        months = (
            opportunity.expected_time_months
        )

        expected_return = max(
            0.0,
            opportunity.expected_return,
        )

        if months <= 0:

            return 0.0

        if months > self.MAX_EXPECTED_TIME_MONTHS:

            months = (
                self.MAX_EXPECTED_TIME_MONTHS
            )

        annualized_proxy = (
            expected_return
            * 12.0
            / months
        )

        # Conservative normalization.
        score = min(
            100.0,
            annualized_proxy
            * 2.0,
        )

        return round(
            max(
                0.0,
                score,
            ),
            2,
        )

    # ======================================================
    # RESEARCH PRIORITY
    # ======================================================

    def _research_priority(
        self,
        ranking: OpportunityRanking,
    ) -> float:
        """
        Calculate comparative research priority from
        already-produced synthesis metrics.
        """

        score = (
            ranking.opportunity_score
            * self.OPPORTUNITY_WEIGHT
            + ranking.confidence_score
            * self.CONFIDENCE_WEIGHT
            + ranking.risk_adjusted_score
            * self.RISK_ADJUSTED_WEIGHT
            + ranking.research_efficiency_score
            * self.RESEARCH_EFFICIENCY_WEIGHT
        )

        # Ineligible opportunities can still retain their
        # analytical score for transparency, but they cannot
        # receive research priority.
        if not ranking.eligible:

            return 0.0

        return round(
            max(
                0.0,
                min(
                    100.0,
                    score,
                ),
            ),
            2,
        )

    # ======================================================
    # TIER
    # ======================================================

    @staticmethod
    def _assign_tier(
        ranking: OpportunityRanking,
    ) -> None:
        """
        Assign research-priority tier.
        """

        score = (
            ranking.research_priority_score
        )

        if score >= 85.0:

            ranking.tier = (
                "TIER 1 — PRIORITY RESEARCH"
            )

            ranking.priority = "VERY HIGH"

        elif score >= 75.0:

            ranking.tier = (
                "TIER 2 — DEEP RESEARCH"
            )

            ranking.priority = "HIGH"

        elif score >= 65.0:

            ranking.tier = (
                "TIER 3 — STANDARD RESEARCH"
            )

            ranking.priority = "MEDIUM"

        else:

            ranking.tier = (
                "TIER 4 — WATCH"
            )

            ranking.priority = "LOW"

    # ======================================================
    # REASONING
    # ======================================================

    @staticmethod
    def _build_reasons(
        ranking: OpportunityRanking,
        opportunity: OpportunitySynthesis,
    ) -> None:
        """
        Build transparent ranking reasoning.
        """

        reasons = []

        if ranking.eligible:

            reasons.append(
                "Opportunity passed all institutional "
                "ranking gates."
            )

        if (
            ranking.opportunity_score
            >= 80.0
        ):

            reasons.append(
                "High individual Opportunity Score."
            )

        if (
            ranking.confidence_score
            >= 80.0
        ):

            reasons.append(
                "High analytical confidence."
            )

        if (
            ranking.evidence_confidence
            >= 80.0
        ):

            reasons.append(
                "Strong evidence confidence."
            )

        if (
            ranking.risk_adjusted_score
            >= ranking.opportunity_score
        ):

            reasons.append(
                "Risk profile is relatively benign."
            )

        if (
            ranking.research_efficiency_score
            >= 70.0
        ):

            reasons.append(
                "Attractive expected-return-to-time "
                "relationship."
            )

        if opportunity.permanent_loss_probability > 0:

            reasons.append(
                "Permanent-loss probability has been "
                "incorporated into risk adjustment."
            )

        ranking.reasons.extend(
            reasons
        )


__all__ = [
    "OpportunityRankingEngine",
]