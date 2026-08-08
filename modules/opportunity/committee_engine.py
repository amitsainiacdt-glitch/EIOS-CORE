"""
EIOS
Everest Investment Operating System

Opportunity Committee Engine

Purpose:
Converts competitive Opportunity Ranking results into
Committee-level research decisions.

Design Principles:
- No scoring.
- No valuation.
- No duplicate ranking.
- No portfolio allocation.
- Ranking remains authoritative.
- Committee converts ranking output into lifecycle decisions.
- Approval is never automatic.
"""

from dataclasses import dataclass, field
from typing import List

from modules.opportunity.ranking.ranking_models import (
    OpportunityRanking,
    OpportunityRankingSet,
)


# ==========================================================
# COMMITTEE DECISION
# ==========================================================

@dataclass
class OpportunityCommitteeDecision:
    """
    Committee decision for one ranked opportunity.
    """

    company: str = ""

    rank: int = 0

    research_priority_score: float = 0.0

    tier: str = ""

    decision: str = ""

    eligible: bool = False

    rationale: List[str] = field(
        default_factory=list
    )

    conditions: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# COMMITTEE RESULT
# ==========================================================

@dataclass
class OpportunityCommitteeResult:
    """
    Complete Committee review output.
    """

    decisions: List[
        OpportunityCommitteeDecision
    ] = field(default_factory=list)

    committee_review_count: int = 0

    watchlist_count: int = 0

    rejected_count: int = 0

    approved_count: int = 0

    top_candidate: str = ""

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# COMMITTEE ENGINE
# ==========================================================

class OpportunityCommitteeEngine:
    """
    Converts Ranking results into Committee decisions.

    This engine deliberately does not calculate
    investment attractiveness.
    """

    COMMITTEE_TIERS = {
        "TIER 1 — PRIORITY RESEARCH",
        "TIER 2 — DEEP RESEARCH",
    }

    WATCHLIST_TIERS = {
        "TIER 3 — STANDARD RESEARCH",
        "TIER 4 — WATCH",
    }

    # ======================================================
    # REVIEW
    # ======================================================

    def review(
        self,
        ranking_set: OpportunityRankingSet,
    ) -> OpportunityCommitteeResult:
        """
        Convert a competitive Ranking Set into
        Committee-level decisions.
        """

        result = OpportunityCommitteeResult()

        for ranking in ranking_set.rankings:

            decision = self._decide(ranking)

            result.decisions.append(decision)

        result.committee_review_count = sum(
            1
            for item in result.decisions
            if item.decision == "COMMITTEE_REVIEW"
        )

        result.watchlist_count = sum(
            1
            for item in result.decisions
            if item.decision == "WATCHLIST"
        )

        result.rejected_count = sum(
            1
            for item in result.decisions
            if item.decision == "REJECT"
        )

        result.approved_count = sum(
            1
            for item in result.decisions
            if item.decision == "APPROVED"
        )

        review_candidates = [
            item
            for item in result.decisions
            if item.decision == "COMMITTEE_REVIEW"
        ]

        if review_candidates:
            result.top_candidate = (
                review_candidates[0].company
            )

        return result

    # ======================================================
    # DECISION
    # ======================================================

    def _decide(
        self,
        ranking: OpportunityRanking,
    ) -> OpportunityCommitteeDecision:
        """
        Convert one Ranking result into a Committee decision.
        """

        result = OpportunityCommitteeDecision()

        result.company = ranking.company
        result.rank = ranking.rank
        result.research_priority_score = (
            ranking.research_priority_score
        )
        result.tier = ranking.tier
        result.eligible = ranking.eligible

        # --------------------------------------------------
        # Hard rejection
        # --------------------------------------------------

        if not ranking.eligible:

            result.decision = "REJECT"

            result.rationale.extend(
                ranking.exclusion_reasons
            )

            result.warnings.extend(
                ranking.warnings
            )

            return result

        # --------------------------------------------------
        # Priority research
        # --------------------------------------------------

        if ranking.tier in self.COMMITTEE_TIERS:

            result.decision = "COMMITTEE_REVIEW"

            result.rationale.append(
                "Opportunity passed all Ranking gates "
                "and meets the Committee research-priority tier."
            )

            result.conditions.append(
                "Committee must independently review "
                "the investment thesis before approval."
            )

            result.warnings.extend(
                ranking.warnings
            )

            return result

        # --------------------------------------------------
        # Watchlist
        # --------------------------------------------------

        if ranking.tier in self.WATCHLIST_TIERS:

            result.decision = "WATCHLIST"

            result.rationale.append(
                "Opportunity is eligible but does not "
                "currently meet the highest research-priority tier."
            )

            result.conditions.append(
                "Reassess if evidence, catalyst strength, "
                "valuation or confidence improves."
            )

            result.warnings.extend(
                ranking.warnings
            )

            return result

        # --------------------------------------------------
        # Defensive fallback
        # --------------------------------------------------

        result.decision = "WATCHLIST"

        result.rationale.append(
            "Opportunity is eligible but has no recognized "
            "Committee classification."
        )

        result.warnings.append(
            "Unrecognized ranking tier."
        )

        return result


__all__ = [
    "OpportunityCommitteeDecision",
    "OpportunityCommitteeResult",
    "OpportunityCommitteeEngine",
]