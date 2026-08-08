"""
EIOS
Everest Investment Operating System

Expectation Gap Engine

Purpose:
Identifies differences between observable business/economic
developments and what the market appears to expect.

Architecture:

Catalyst
    ↓
Economic Impact
    ↓
Earnings Impact
    ↓
Market Expectation
    ↓
Expectation Gap
    ↓
Potential Mispricing

Design Principles:
- No valuation calculation.
- No investment recommendation.
- No persistence.
- Explicit assumptions.
- Explicit evidence.
- Positive and negative gaps supported.
- Market recognition is treated separately from catalyst strength.
"""

from dataclasses import dataclass, field
from typing import List

from modules.opportunity.catalyst_engine import Catalyst


# ==========================================================
# EXPECTATION GAP
# ==========================================================


@dataclass
class ExpectationGap:
    """
    Institutional representation of an expectation gap.
    """

    gap_id: str = ""

    company: str = ""

    sector: str = ""

    catalyst: Catalyst | None = None

    # ------------------------------------------------------
    # Market Expectation
    # ------------------------------------------------------

    market_expectation: float = 0.0

    eios_expectation: float = 0.0

    expectation_difference: float = 0.0

    # ------------------------------------------------------
    # Earnings
    # ------------------------------------------------------

    market_earnings_expectation: float = 0.0

    eios_earnings_expectation: float = 0.0

    earnings_gap: float = 0.0

    # ------------------------------------------------------
    # Recognition
    # ------------------------------------------------------

    market_recognition: float = 0.0

    unrecognized_potential: float = 0.0

    # ------------------------------------------------------
    # Direction
    # ------------------------------------------------------

    positive_gap: bool = False

    negative_gap: bool = False

    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    gap_score: float = 0.0

    confidence: float = 0.0

    # ------------------------------------------------------
    # Evidence
    # ------------------------------------------------------

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
# EXPECTATION GAP ENGINE
# ==========================================================


class ExpectationGapEngine:
    """
    Determines whether EIOS sees a material difference between
    market expectations and the implications of current evidence.
    """

    MINIMUM_GAP = 15.0

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        *,
        gap_id: str,
        company: str,
        sector: str,
        catalyst: Catalyst,
        market_expectation: float,
        eios_expectation: float,
        market_earnings_expectation: float,
        eios_earnings_expectation: float,
        assumptions: List[str] | None = None,
        invalidation_conditions: List[str] | None = None,
    ) -> ExpectationGap:
        """
        Produce an expectation-gap assessment.

        Values are normalized to a 0-100 analytical scale.
        """

        gap = ExpectationGap()

        gap.gap_id = gap_id
        gap.company = company
        gap.sector = sector
        gap.catalyst = catalyst

        gap.market_expectation = (
            market_expectation
        )

        gap.eios_expectation = (
            eios_expectation
        )

        gap.market_earnings_expectation = (
            market_earnings_expectation
        )

        gap.eios_earnings_expectation = (
            eios_earnings_expectation
        )

        gap.market_recognition = (
            catalyst.market_recognition
        )

        gap.assumptions = list(
            assumptions or []
        )

        gap.invalidation_conditions = list(
            invalidation_conditions or []
        )

        # --------------------------------------------------
        # Calculate Gaps
        # --------------------------------------------------

        gap.expectation_difference = (
            eios_expectation
            - market_expectation
        )

        gap.earnings_gap = (
            eios_earnings_expectation
            - market_earnings_expectation
        )

        gap.unrecognized_potential = max(
            0.0,
            100.0
            - gap.market_recognition,
        )

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        gap.positive_gap = (
            gap.expectation_difference
            >= self.MINIMUM_GAP
        )

        gap.negative_gap = (
            gap.expectation_difference
            <= -self.MINIMUM_GAP
        )

        # --------------------------------------------------
        # Score
        # --------------------------------------------------

        gap.gap_score = self._score(
            gap
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        gap.confidence = self._confidence(
            gap
        )

        # --------------------------------------------------
        # Evidence
        # --------------------------------------------------

        gap.evidence = self._evidence(
            catalyst
        )

        gap.disconfirming_evidence = (
            self._disconfirming_evidence(
                catalyst
            )
        )

        # --------------------------------------------------
        # Reasoning
        # --------------------------------------------------

        self._build_reasoning(
            gap
        )

        return gap

    # ======================================================
    # SCORE
    # ======================================================

    def _score(
        self,
        gap: ExpectationGap,
    ) -> float:
        """
        Score the magnitude of the expectation gap.

        Earnings gap receives greater weight because the
        investment consequence ultimately needs economic
        transmission.
        """

        expectation_component = min(
            100.0,
            abs(
                gap.expectation_difference
            ),
        )

        earnings_component = min(
            100.0,
            abs(
                gap.earnings_gap
            ),
        )

        recognition_component = (
            gap.unrecognized_potential
        )

        catalyst_component = (
            gap.catalyst.catalyst_score
            if gap.catalyst
            else 0.0
        )

        score = (
            expectation_component * 0.30
            + earnings_component * 0.30
            + recognition_component * 0.20
            + catalyst_component * 0.20
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
        gap: ExpectationGap,
    ) -> float:
        """
        Confidence combines catalyst confidence and the
        quality of the identified expectation gap.
        """

        catalyst_confidence = (
            gap.catalyst.confidence
            if gap.catalyst
            else 0.0
        )

        gap_magnitude = min(
            100.0,
            abs(
                gap.expectation_difference
            ) * 2.0,
        )

        earnings_magnitude = min(
            100.0,
            abs(
                gap.earnings_gap
            ) * 2.0,
        )

        confidence = (
            catalyst_confidence * 0.40
            + gap_magnitude * 0.30
            + earnings_magnitude * 0.30
        )

        return max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

    # ======================================================
    # EVIDENCE
    # ======================================================

    def _evidence(
        self,
        catalyst: Catalyst,
    ) -> List[str]:

        evidence = list(
            catalyst.evidence
        )

        for reason in catalyst.reasons:

            if reason not in evidence:
                evidence.append(reason)

        return evidence

    # ======================================================
    # DISCONFIRMING EVIDENCE
    # ======================================================

    def _disconfirming_evidence(
        self,
        catalyst: Catalyst,
    ) -> List[str]:

        evidence = list(
            catalyst.contradictory_evidence
        )

        for warning in catalyst.warnings:

            if warning not in evidence:
                evidence.append(warning)

        return evidence

    # ======================================================
    # REASONING
    # ======================================================

    def _build_reasoning(
        self,
        gap: ExpectationGap,
    ) -> None:

        if gap.positive_gap:

            gap.reasons.append(
                "EIOS expectation is materially above "
                "current market expectation."
            )

        if gap.negative_gap:

            gap.warnings.append(
                "EIOS expectation is materially below "
                "current market expectation."
            )

        if (
            not gap.positive_gap
            and not gap.negative_gap
        ):

            gap.warnings.append(
                "No material expectation gap has been established."
            )

        if gap.earnings_gap > 15:

            gap.reasons.append(
                "Potential earnings surprise is material."
            )

        if gap.unrecognized_potential >= 60:

            gap.reasons.append(
                "Market recognition of the catalyst appears limited."
            )

        if gap.market_recognition >= 70:

            gap.warnings.append(
                "Catalyst appears substantially recognized by the market."
            )

        if gap.disconfirming_evidence:

            gap.warnings.append(
                "Disconfirming evidence exists and requires review."
            )

        if not gap.invalidation_conditions:

            gap.warnings.append(
                "No explicit invalidation conditions supplied."
            )