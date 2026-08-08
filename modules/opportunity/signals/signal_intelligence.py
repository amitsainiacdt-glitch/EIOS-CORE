"""
EIOS
Everest Investment Operating System

Signal Intelligence Engine

Purpose:
Analyses the evolution of an existing Opportunity Signal.

This engine determines whether a signal is:

- strengthening
- weakening
- accelerating
- decelerating
- persistent
- fading
- contradictory
- stable

Architecture:

Signal
    ↓
Signal Intelligence
    ↓
Signal Evolution
    ↓
Catalyst Engine

Design Principles:
- No persistence.
- No valuation.
- No opportunity scoring.
- No company-specific logic.
- Does not mutate the Signal object.
- Returns a separate typed assessment.
"""

from dataclasses import dataclass, field
from typing import List

from .signal_model import Signal


# ==========================================================
# SIGNAL EVOLUTION
# ==========================================================


@dataclass
class SignalEvolution:
    """
    Institutional assessment of signal evolution.
    """

    strengthening: bool = False

    weakening: bool = False

    accelerating: bool = False

    decelerating: bool = False

    persistent: bool = False

    fading: bool = False

    contradictory: bool = False

    stable: bool = False

    strength_score: float = 0.0

    persistence_score: float = 0.0

    corroboration_score: float = 0.0

    contradiction_score: float = 0.0

    confidence: float = 0.0

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# SIGNAL INTELLIGENCE ENGINE
# ==========================================================


class SignalIntelligenceEngine:
    """
    Analyses the current state and evolution of a Signal.

    Detailed historical time-series analysis can be added later
    without changing the canonical Signal model.
    """

    def analyze(
        self,
        signal: Signal,
    ) -> SignalEvolution:
        """
        Produce a SignalEvolution assessment.

        The Signal object is never mutated.
        """

        result = SignalEvolution()

        # --------------------------------------------------
        # Strength
        # --------------------------------------------------

        result.strength_score = self._strength(
            signal
        )

        # --------------------------------------------------
        # Persistence
        # --------------------------------------------------

        result.persistence_score = self._persistence(
            signal
        )

        # --------------------------------------------------
        # Corroboration
        # --------------------------------------------------

        result.corroboration_score = self._corroboration(
            signal
        )

        # --------------------------------------------------
        # Contradiction
        # --------------------------------------------------

        result.contradiction_score = self._contradiction(
            signal
        )

        # --------------------------------------------------
        # Evolution Classification
        # --------------------------------------------------

        result.strengthening = (
            result.strength_score >= 70
            and result.corroboration_score >= 50
        )

        result.weakening = (
            result.strength_score < 40
        )

        result.accelerating = (
            signal.signal_type.value
            == "Acceleration"
        )

        result.decelerating = (
            signal.signal_type.value
            == "Deceleration"
        )

        result.persistent = (
            result.persistence_score >= 70
        )

        result.fading = (
            result.persistence_score < 30
        )

        result.contradictory = (
            result.contradiction_score >= 30
        )

        result.stable = not any(
            [
                result.strengthening,
                result.weakening,
                result.accelerating,
                result.decelerating,
                result.fading,
            ]
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = self._confidence(
            result
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        self._build_reasons(
            result
        )

        return result

    # ======================================================
    # STRENGTH
    # ======================================================

    def _strength(
        self,
        signal: Signal,
    ) -> float:
        """
        Determine current signal strength.

        The generic layer uses explicit signal magnitude,
        relevance and probability.
        """

        values = [
            signal.magnitude,
            signal.relevance,
            signal.probability,
        ]

        available = [
            value
            for value in values
            if value > 0
        ]

        if not available:
            return 0.0

        return sum(available) / len(
            available
        )

    # ======================================================
    # PERSISTENCE
    # ======================================================

    def _persistence(
        self,
        signal: Signal,
    ) -> float:
        """
        Use the explicit persistence assessment.

        Historical persistence calculations will later be
        supplied by a temporal signal engine.
        """

        return max(
            0.0,
            min(
                100.0,
                signal.persistence,
            ),
        )

    # ======================================================
    # CORROBORATION
    # ======================================================

    def _corroboration(
        self,
        signal: Signal,
    ) -> float:
        """
        Determine independent corroboration strength.
        """

        confirmations = (
            signal.independent_confirmation
        )

        if confirmations >= 3:
            return 100.0

        if confirmations == 2:
            return 80.0

        if confirmations == 1:
            return 55.0

        if signal.supporting_sources:
            return 40.0

        return 0.0

    # ======================================================
    # CONTRADICTION
    # ======================================================

    def _contradiction(
        self,
        signal: Signal,
    ) -> float:
        """
        Measure contradictory evidence.

        Higher score means greater contradiction.
        """

        count = len(
            signal.contradictory_evidence
        )

        if count >= 5:
            return 100.0

        if count >= 3:
            return 70.0

        if count == 2:
            return 50.0

        if count == 1:
            return 30.0

        return 0.0

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        result: SignalEvolution,
    ) -> float:
        """
        Calculate confidence in the evolution assessment.
        """

        confidence = (
            result.strength_score * 0.35
            + result.persistence_score * 0.25
            + result.corroboration_score * 0.25
            + (100.0 - result.contradiction_score)
            * 0.15
        )

        return max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

    # ======================================================
    # REASONS
    # ======================================================

    def _build_reasons(
        self,
        result: SignalEvolution,
    ) -> None:
        """
        Generate transparent reasoning.
        """

        if result.strengthening:
            result.reasons.append(
                "Signal strength and corroboration indicate strengthening."
            )

        if result.weakening:
            result.warnings.append(
                "Signal strength is currently weak."
            )

        if result.accelerating:
            result.reasons.append(
                "Signal is classified as accelerating."
            )

        if result.decelerating:
            result.warnings.append(
                "Signal is classified as decelerating."
            )

        if result.persistent:
            result.reasons.append(
                "Signal shows evidence of persistence."
            )

        if result.fading:
            result.warnings.append(
                "Signal persistence appears weak or fading."
            )

        if result.contradictory:
            result.warnings.append(
                "Contradictory evidence requires investigation."
            )

        if result.stable:
            result.reasons.append(
                "No major directional change detected."
            )