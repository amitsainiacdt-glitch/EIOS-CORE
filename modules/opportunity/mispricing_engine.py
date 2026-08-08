"""
EIOS
Everest Investment Operating System

Mispricing Engine

Purpose:
Combines existing EIOS valuation intelligence with
Opportunity Engine catalyst and expectation-gap intelligence.

Important:
This is NOT a valuation engine.

The authoritative valuation remains:
    modules.valuation.valuation_engine.ValuationEngine

This engine evaluates whether the existing valuation,
catalyst and expectation-gap evidence indicate potential
mispricing.

Architecture:

Existing Valuation
        +
Catalyst
        +
Expectation Gap
        ↓
     Mispricing
        ↓
     Asymmetry
"""

from dataclasses import dataclass, field
from typing import List, Optional

from modules.opportunity.catalyst_engine import Catalyst
from modules.opportunity.expectation_gap_engine import (
    ExpectationGap,
)


# ==========================================================
# MISPRICING ASSESSMENT
# ==========================================================


@dataclass
class MispricingAssessment:
    """
    Institutional assessment of potential mispricing.
    """

    company: str = ""

    cmp: float = 0.0

    intrinsic_value: float = 0.0

    fair_value: float = 0.0

    valuation_upside: float = 0.0

    valuation_discount: float = 0.0

    catalyst_score: float = 0.0

    expectation_gap_score: float = 0.0

    expectation_difference: float = 0.0

    earnings_gap: float = 0.0

    market_recognition: float = 0.0

    unrecognized_potential: float = 0.0

    mispricing_score: float = 0.0

    confidence: float = 0.0

    valuation_support: bool = False

    catalyst_support: bool = False

    expectation_support: bool = False

    potential_mispricing: bool = False

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    disconfirming_evidence: List[str] = field(
        default_factory=list
    )

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# MISPRICING ENGINE
# ==========================================================


class MispricingEngine:
    """
    Evaluates potential mispricing using existing EIOS
    valuation output and Opportunity Intelligence.

    It does not calculate intrinsic value.
    """

    MINIMUM_VALUATION_UPSIDE = 15.0
    MINIMUM_EXPECTATION_GAP = 15.0
    MINIMUM_MISPRICING_SCORE = 60.0

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        *,
        company: str,
        cmp: float,
        valuation,
        catalyst: Optional[Catalyst] = None,
        expectation_gap: Optional[
            ExpectationGap
        ] = None,
        assumptions: Optional[
            List[str]
        ] = None,
        invalidation_conditions: Optional[
            List[str]
        ] = None,
    ) -> MispricingAssessment:
        """
        Evaluate potential mispricing.

        `valuation` must be the output of the existing
        EIOS ValuationEngine / ValuationSection.
        """

        result = MispricingAssessment()

        result.company = company
        result.cmp = cmp

        result.assumptions = list(
            assumptions or []
        )

        result.invalidation_conditions = list(
            invalidation_conditions or []
        )

        # ==================================================
        # EXISTING VALUATION
        # ==================================================

        result.intrinsic_value = float(
            getattr(
                valuation,
                "intrinsic_value",
                0.0,
            )
            or 0.0
        )

        result.fair_value = float(
            getattr(
                valuation,
                "fair_value",
                result.intrinsic_value,
            )
            or 0.0
        )

        # ==================================================
        # VALUATION UPSIDE
        # ==================================================

        reference_value = (
            result.fair_value
            or result.intrinsic_value
        )

        if cmp > 0 and reference_value > 0:

            result.valuation_upside = (
                (
                    reference_value
                    / cmp
                )
                - 1.0
            ) * 100.0

            result.valuation_discount = (
                100.0
                - (
                    cmp
                    / reference_value
                ) * 100.0
            )

        # ==================================================
        # CATALYST
        # ==================================================

        if catalyst:

            result.catalyst_score = (
                catalyst.catalyst_score
            )

            result.market_recognition = (
                catalyst.market_recognition
            )

            result.unrecognized_potential = (
                catalyst.market_recognition
                if catalyst.market_recognition < 0
                else 100.0
                - catalyst.market_recognition
            )

            result.catalyst_support = (
                catalyst.catalyst_score >= 60.0
                and catalyst.confidence >= 60.0
            )

            result.evidence.extend(
                catalyst.evidence
            )

            result.disconfirming_evidence.extend(
                catalyst.contradictory_evidence
            )

        # ==================================================
        # EXPECTATION GAP
        # ==================================================

        if expectation_gap:

            result.expectation_gap_score = (
                expectation_gap.gap_score
            )

            result.expectation_difference = (
                expectation_gap.expectation_difference
            )

            result.earnings_gap = (
                expectation_gap.earnings_gap
            )

            result.expectation_support = (
                expectation_gap.positive_gap
                or expectation_gap.negative_gap
            )

            result.evidence.extend(
                expectation_gap.evidence
            )

            result.disconfirming_evidence.extend(
                expectation_gap.disconfirming_evidence
            )

        # ==================================================
        # VALUATION SUPPORT
        # ==================================================

        result.valuation_support = (
            result.valuation_upside
            >= self.MINIMUM_VALUATION_UPSIDE
        )

        # ==================================================
        # MISPRICING SCORE
        # ==================================================

        result.mispricing_score = (
            self._score(result)
        )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        result.confidence = (
            self._confidence(
                result,
                valuation,
            )
        )

        # ==================================================
        # POTENTIAL MISPRICING
        # ==================================================

        result.potential_mispricing = (
            result.valuation_support
            and result.catalyst_support
            and result.expectation_support
            and result.mispricing_score
            >= self.MINIMUM_MISPRICING_SCORE
        )

        # ==================================================
        # REASONING
        # ==================================================

        self._build_reasoning(
            result
        )

        return result

    # ======================================================
    # SCORE
    # ======================================================

    def _score(
        self,
        result: MispricingAssessment,
    ) -> float:
        """
        Combine valuation, catalyst and expectation-gap
        evidence.

        Valuation remains important, but Opportunity
        Intelligence determines whether the discount has
        a credible reason to close.
        """

        valuation_component = min(
            100.0,
            max(
                0.0,
                result.valuation_upside
                * 2.0,
            ),
        )

        catalyst_component = (
            result.catalyst_score
        )

        expectation_component = (
            result.expectation_gap_score
        )

        unrecognized_component = (
            result.unrecognized_potential
        )

        score = (
            valuation_component * 0.30
            + catalyst_component * 0.25
            + expectation_component * 0.25
            + unrecognized_component * 0.20
        )

        return max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        result: MispricingAssessment,
        valuation,
    ) -> float:
        """
        Confidence is based on the quality of the
        underlying valuation and opportunity evidence.
        """

        valuation_confidence = float(
            getattr(
                valuation,
                "confidence",
                0.0,
            )
            or 0.0
        )

        opportunity_confidence = (
            result.catalyst_score
            if result.catalyst_score > 0
            else 0.0
        )

        expectation_confidence = (
            result.expectation_gap_score
            if result.expectation_gap_score > 0
            else 0.0
        )

        confidence = (
            valuation_confidence * 0.30
            + opportunity_confidence * 0.30
            + expectation_confidence * 0.40
        )

        contradiction_penalty = min(
            30.0,
            len(
                result.disconfirming_evidence
            ) * 2.0,
        )

        return max(
            0.0,
            min(
                100.0,
                confidence
                - contradiction_penalty,
            ),
        )

    # ======================================================
    # REASONING
    # ======================================================

    def _build_reasoning(
        self,
        result: MispricingAssessment,
    ) -> None:

        if result.valuation_support:

            result.reasons.append(
                "Existing EIOS valuation indicates material upside "
                "relative to the current market price."
            )

        else:

            result.warnings.append(
                "Existing valuation does not establish the required "
                "minimum valuation support."
            )

        if result.catalyst_support:

            result.reasons.append(
                "Catalyst evidence is sufficiently strong."
            )

        else:

            result.warnings.append(
                "Catalyst evidence is insufficient."
            )

        if result.expectation_support:

            result.reasons.append(
                "A material expectation gap has been identified."
            )

        else:

            result.warnings.append(
                "No material expectation gap has been established."
            )

        if result.potential_mispricing:

            result.reasons.append(
                "Valuation, catalyst and expectation-gap evidence "
                "combine to indicate potential mispricing."
            )

        else:

            result.warnings.append(
                "Evidence is not yet sufficient to classify the "
                "opportunity as potential mispricing."
            )

        if result.disconfirming_evidence:

            result.warnings.append(
                "Disconfirming evidence exists and must be reviewed."
            )