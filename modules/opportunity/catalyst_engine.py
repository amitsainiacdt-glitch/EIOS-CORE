"""
EIOS
Everest Investment Operating System

Catalyst Intelligence Engine

Purpose:
Converts validated signals and causal chains into
institutional Catalyst assessments.

A catalyst is not simply a news event.

A catalyst requires:
    1. A meaningful trigger
    2. A causal transmission mechanism
    3. A potentially material economic consequence
    4. A defined time horizon
    5. Evidence supporting the mechanism

Architecture:

Signals
    ↓
Validation
    ↓
Aggregation
    ↓
Causal Chain
    ↓
Catalyst Engine
    ↓
Earnings Impact
    ↓
Expectation Gap
    ↓
Mispricing

Design Principles:
- No persistence.
- No valuation.
- No investment recommendation.
- No mutation of source objects.
- Explicit evidence and assumptions.
- Contradictory evidence reduces confidence.
"""

from dataclasses import dataclass, field
from typing import List

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDirection,
    TimeHorizon,
)

from modules.opportunity.signals.causal_chain_engine import (
    CausalChain,
)


# ==========================================================
# CATALYST
# ==========================================================


@dataclass
class Catalyst:
    """
    Institutional Catalyst representation.
    """

    catalyst_id: str = ""

    title: str = ""

    description: str = ""

    trigger: str = ""

    mechanism: str = ""

    direction: SignalDirection = (
        SignalDirection.UNKNOWN
    )

    horizon: TimeHorizon = (
        TimeHorizon.MEDIUM_TERM
    )

    signals: List[Signal] = field(
        default_factory=list
    )

    causal_chain: CausalChain | None = None

    affected_sectors: List[str] = field(
        default_factory=list
    )

    affected_companies: List[str] = field(
        default_factory=list
    )

    economic_impact: str = ""

    earnings_impact: str = ""

    valuation_impact: str = ""

    magnitude: float = 0.0

    probability: float = 0.0

    persistence: float = 0.0

    market_recognition: float = 0.0

    catalyst_score: float = 0.0

    confidence: float = 0.0

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    contradictory_evidence: List[str] = field(
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
# CATALYST ENGINE
# ==========================================================


class CatalystEngine:
    """
    Converts validated signals and causal chains into
    Catalyst objects.
    """

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        *,
        catalyst_id: str,
        title: str,
        trigger: str,
        signals: List[Signal],
        causal_chain: CausalChain | None = None,
        description: str = "",
        economic_impact: str = "",
        earnings_impact: str = "",
        valuation_impact: str = "",
        affected_sectors: List[str] | None = None,
        affected_companies: List[str] | None = None,
        assumptions: List[str] | None = None,
        invalidation_conditions: List[str] | None = None,
    ) -> Catalyst:
        """
        Produce an institutional Catalyst assessment.
        """

        catalyst = Catalyst()

        catalyst.catalyst_id = catalyst_id
        catalyst.title = title
        catalyst.description = description
        catalyst.trigger = trigger
        catalyst.signals = list(signals)

        catalyst.causal_chain = causal_chain

        catalyst.economic_impact = economic_impact
        catalyst.earnings_impact = earnings_impact
        catalyst.valuation_impact = valuation_impact

        catalyst.affected_sectors = list(
            affected_sectors or []
        )

        catalyst.affected_companies = list(
            affected_companies or []
        )

        catalyst.assumptions = list(
            assumptions or []
        )

        catalyst.invalidation_conditions = list(
            invalidation_conditions or []
        )

        # --------------------------------------------------
        # Mechanism
        # --------------------------------------------------

        if causal_chain:
            catalyst.mechanism = self._mechanism(
                causal_chain
            )

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        catalyst.direction = self._direction(
            signals
        )

        # --------------------------------------------------
        # Horizon
        # --------------------------------------------------

        catalyst.horizon = self._horizon(
            signals
        )

        # --------------------------------------------------
        # Quantitative Attributes
        # --------------------------------------------------

        catalyst.magnitude = self._magnitude(
            signals
        )

        catalyst.probability = self._probability(
            signals
        )

        catalyst.persistence = self._persistence(
            signals
        )

        catalyst.market_recognition = (
            self._market_recognition(
                signals
            )
        )

        # --------------------------------------------------
        # Evidence
        # --------------------------------------------------

        catalyst.evidence = self._evidence(
            signals
        )

        catalyst.contradictory_evidence = (
            self._contradictions(
                signals
            )
        )

        # --------------------------------------------------
        # Score
        # --------------------------------------------------

        catalyst.catalyst_score = (
            self._score(catalyst)
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        catalyst.confidence = (
            self._confidence(catalyst)
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        self._build_reasoning(
            catalyst
        )

        return catalyst

    # ======================================================
    # MECHANISM
    # ======================================================

    def _mechanism(
        self,
        chain: CausalChain,
    ) -> str:

        if not chain.links:
            return ""

        return " → ".join(
            [
                link.effect
                for link in chain.links
            ]
        )

    # ======================================================
    # DIRECTION
    # ======================================================

    def _direction(
        self,
        signals: List[Signal],
    ) -> SignalDirection:

        positive = sum(
            1
            for signal in signals
            if signal.direction
            == SignalDirection.POSITIVE
        )

        negative = sum(
            1
            for signal in signals
            if signal.direction
            == SignalDirection.NEGATIVE
        )

        if positive > negative:
            return SignalDirection.POSITIVE

        if negative > positive:
            return SignalDirection.NEGATIVE

        if positive and negative:
            return SignalDirection.MIXED

        return SignalDirection.UNKNOWN

    # ======================================================
    # HORIZON
    # ======================================================

    def _horizon(
        self,
        signals: List[Signal],
    ) -> TimeHorizon:

        if not signals:
            return TimeHorizon.MEDIUM_TERM

        priority = {
            TimeHorizon.IMMEDIATE: 1,
            TimeHorizon.MEDIUM_TERM: 2,
            TimeHorizon.STRUCTURAL: 3,
            TimeHorizon.LONG_TERM: 4,
        }

        return max(
            signals,
            key=lambda signal:
                priority[signal.horizon],
        ).horizon

    # ======================================================
    # MAGNITUDE
    # ======================================================

    def _magnitude(
        self,
        signals: List[Signal],
    ) -> float:

        values = [
            signal.magnitude
            for signal in signals
            if signal.magnitude > 0
        ]

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ======================================================
    # PROBABILITY
    # ======================================================

    def _probability(
        self,
        signals: List[Signal],
    ) -> float:

        values = [
            signal.probability
            for signal in signals
            if signal.probability > 0
        ]

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ======================================================
    # PERSISTENCE
    # ======================================================

    def _persistence(
        self,
        signals: List[Signal],
    ) -> float:

        values = [
            signal.persistence
            for signal in signals
            if signal.persistence > 0
        ]

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ======================================================
    # MARKET RECOGNITION
    # ======================================================

    def _market_recognition(
        self,
        signals: List[Signal],
    ) -> float:

        values = [
            signal.market_recognition
            for signal in signals
            if signal.market_recognition > 0
        ]

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ======================================================
    # EVIDENCE
    # ======================================================

    def _evidence(
        self,
        signals: List[Signal],
    ) -> List[str]:

        evidence = []

        for signal in signals:

            for item in signal.evidence:

                if item not in evidence:
                    evidence.append(item)

            for source in signal.supporting_sources:

                if source not in evidence:
                    evidence.append(source)

        return evidence

    # ======================================================
    # CONTRADICTIONS
    # ======================================================

    def _contradictions(
        self,
        signals: List[Signal],
    ) -> List[str]:

        contradictions = []

        for signal in signals:

            for item in (
                signal.contradictory_evidence
            ):

                if item not in contradictions:
                    contradictions.append(item)

        return contradictions

    # ======================================================
    # SCORE
    # ======================================================

    def _score(
        self,
        catalyst: Catalyst,
    ) -> float:

        score = (
            catalyst.magnitude * 0.25
            + catalyst.probability * 0.20
            + catalyst.persistence * 0.15
            + catalyst.confidence * 0.25
            + (
                100.0
                - catalyst.market_recognition
            ) * 0.15
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
        catalyst: Catalyst,
    ) -> float:

        signal_confidences = [
            signal.confidence
            for signal in catalyst.signals
            if signal.confidence > 0
        ]

        if signal_confidences:
            base = (
                sum(signal_confidences)
                / len(signal_confidences)
            )
        else:
            base = 0.0

        if catalyst.causal_chain:

            base = (
                base * 0.70
                + catalyst.causal_chain.confidence
                * 0.30
            )

        contradiction_penalty = min(
            30.0,
            len(
                catalyst.contradictory_evidence
            ) * 5.0,
        )

        return max(
            0.0,
            min(
                100.0,
                base
                - contradiction_penalty,
            ),
        )

    # ======================================================
    # REASONING
    # ======================================================

    def _build_reasoning(
        self,
        catalyst: Catalyst,
    ) -> None:

        if catalyst.trigger:
            catalyst.reasons.append(
                "A defined trigger has been identified."
            )

        if catalyst.mechanism:
            catalyst.reasons.append(
                "A causal transmission mechanism has been identified."
            )

        if catalyst.magnitude >= 70:
            catalyst.reasons.append(
                "Potential economic magnitude is material."
            )

        if catalyst.persistence >= 70:
            catalyst.reasons.append(
                "Catalyst appears capable of persisting."
            )

        if catalyst.market_recognition < 40:
            catalyst.reasons.append(
                "Market recognition appears relatively limited."
            )

        if catalyst.market_recognition >= 70:
            catalyst.warnings.append(
                "Catalyst appears substantially recognized by the market."
            )

        if catalyst.contradictory_evidence:
            catalyst.warnings.append(
                "Contradictory evidence requires investigation."
            )

        if not catalyst.affected_companies:
            catalyst.warnings.append(
                "Company-level exposure has not yet been established."
            )

        if not catalyst.earnings_impact:
            catalyst.warnings.append(
                "Earnings transmission has not yet been explicitly established."
            )