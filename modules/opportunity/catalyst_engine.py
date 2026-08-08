"""
EIOS
Everest Investment Operating System

Catalyst Engine
===============

Converts validated Opportunity signals and causal chains
into an institutional Catalyst assessment.

Responsibilities
----------------
- Classify the catalyst.
- Determine direction.
- Determine time horizon.
- Estimate magnitude.
- Estimate probability.
- Estimate persistence.
- Estimate market recognition.
- Evaluate supporting evidence.
- Evaluate contradictions.
- Calculate catalyst score.
- Calculate catalyst confidence.
- Record assumptions and invalidation conditions.

Non-responsibilities
--------------------
- Valuation.
- Portfolio allocation.
- Trade execution.
- Opportunity ranking.
- Mutation of source Signal objects.

Architecture
------------

Signals
    ↓
Catalyst Classifier
    ↓
Catalyst Classification
    ↓
Catalyst Engine
    ↓
Catalyst Assessment
    ↓
Expectation Gap
"""

from dataclasses import dataclass, field
from typing import List

from modules.opportunity.catalyst.catalyst_classifier import (
    CatalystClassifier,
    CatalystClassification,
)

from modules.opportunity.signals.signal_model import (
    Signal,
    SignalDirection,
    SignalStage,
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

    # ------------------------------------------------------
    # Identity
    # ------------------------------------------------------

    catalyst_id: str = ""

    title: str = ""

    description: str = ""

    trigger: str = ""

    mechanism: str = ""

    # ------------------------------------------------------
    # Classification
    # ------------------------------------------------------

    primary_catalyst_id: str = ""

    primary_catalyst_family: str = ""

    secondary_catalyst_ids: List[str] = field(
        default_factory=list
    )

    secondary_catalyst_families: List[str] = field(
        default_factory=list
    )

    classification_confidence: float = 0.0

    classification_reasoning: List[str] = field(
        default_factory=list
    )

    unclassified_signals: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Direction / Horizon
    # ------------------------------------------------------

    direction: SignalDirection = (
        SignalDirection.UNKNOWN
    )

    horizon: TimeHorizon = (
        TimeHorizon.MEDIUM_TERM
    )

    # ------------------------------------------------------
    # Source Intelligence
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Economic Impact
    # ------------------------------------------------------

    economic_impact: str = ""

    earnings_impact: str = ""

    valuation_impact: str = ""

    # ------------------------------------------------------
    # Quantitative Assessment
    # ------------------------------------------------------

    magnitude: float = 0.0

    probability: float = 0.0

    persistence: float = 0.0

    market_recognition: float = 0.0

    catalyst_score: float = 0.0

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

    contradictory_evidence: List[str] = field(
        default_factory=list
    )

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Reasoning
    # ------------------------------------------------------

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
    institutional Catalyst assessments.
    """

    # ------------------------------------------------------
    # SCORE THRESHOLDS
    # ------------------------------------------------------

    MINIMUM_CATALYST_SCORE = 50.0

    # ======================================================
    # INITIALIZATION
    # ======================================================

    def __init__(self) -> None:

        self.classifier = CatalystClassifier()

    # ======================================================
    # PUBLIC ANALYSIS
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

        # ==================================================
        # BASIC DATA
        # ==================================================

        catalyst.catalyst_id = catalyst_id

        catalyst.title = title

        catalyst.description = description

        catalyst.trigger = trigger

        catalyst.signals = list(
            signals
        )

        catalyst.causal_chain = causal_chain

        catalyst.economic_impact = (
            economic_impact
        )

        catalyst.earnings_impact = (
            earnings_impact
        )

        catalyst.valuation_impact = (
            valuation_impact
        )

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

        # ==================================================
        # 1. CATALYST CLASSIFICATION
        # ==================================================

        classification = (
            self.classifier.classify(
                signals=signals,
                causal_chain=causal_chain,
            )
        )

        self._apply_classification(
            catalyst,
            classification,
        )

        # ==================================================
        # 2. CAUSAL MECHANISM
        # ==================================================

        if causal_chain:

            catalyst.mechanism = (
                self._mechanism(
                    causal_chain
                )
            )

        # ==================================================
        # 3. DIRECTION
        # ==================================================

        catalyst.direction = (
            self._direction(
                signals
            )
        )

        # ==================================================
        # 4. TIME HORIZON
        # ==================================================

        catalyst.horizon = (
            self._horizon(
                signals
            )
        )

        # ==================================================
        # 5. MAGNITUDE
        # ==================================================

        catalyst.magnitude = (
            self._magnitude(
                signals
            )
        )

        # ==================================================
        # 6. PROBABILITY
        # ==================================================

        catalyst.probability = (
            self._probability(
                signals
            )
        )

        # ==================================================
        # 7. PERSISTENCE
        # ==================================================

        catalyst.persistence = (
            self._persistence(
                signals
            )
        )

        # ==================================================
        # 8. MARKET RECOGNITION
        # ==================================================

        catalyst.market_recognition = (
            self._market_recognition(
                signals
            )
        )

        # ==================================================
        # 9. EVIDENCE
        # ==================================================

        self._collect_evidence(
            catalyst
        )

        # ==================================================
        # 10. CONTRADICTIONS
        # ==================================================

        self._collect_contradictions(
            catalyst
        )

        # ==================================================
        # 11. CATALYST SCORE
        # ==================================================

        catalyst.catalyst_score = (
            self._calculate_score(
                catalyst
            )
        )

        # ==================================================
        # 12. CONFIDENCE
        # ==================================================

        catalyst.confidence = (
            self._calculate_confidence(
                catalyst
            )
        )

        # ==================================================
        # 13. REASONING
        # ==================================================

        self._build_reasoning(
            catalyst
        )

        # ==================================================
        # 14. WARNINGS
        # ==================================================

        self._build_warnings(
            catalyst
        )

        return catalyst

    # ======================================================
    # CLASSIFICATION HAND-OFF
    # ======================================================

    @staticmethod
    def _apply_classification(
        catalyst: Catalyst,
        classification: CatalystClassification,
    ) -> None:
        """
        Transfer classifier output into the Catalyst object.

        Classification does not alter catalyst scoring.
        """

        if classification.primary is not None:

            catalyst.primary_catalyst_id = (
                classification.primary.catalyst_id
            )

            catalyst.primary_catalyst_family = (
                classification.primary.family.value
            )

        catalyst.secondary_catalyst_ids = [
            item.catalyst_id
            for item in classification.secondary
        ]

        catalyst.secondary_catalyst_families = [
            item.family.value
            for item in classification.secondary
        ]

        catalyst.classification_confidence = (
            classification.confidence
        )

        catalyst.classification_reasoning = list(
            classification.reasoning
        )

        catalyst.unclassified_signals = list(
            classification.unclassified_signals
        )

        catalyst.warnings.extend(
            classification.warnings
        )

    # ======================================================
    # MECHANISM
    # ======================================================

    @staticmethod
    def _mechanism(
        causal_chain: CausalChain,
    ) -> str:
        """
        Convert causal-chain information into a concise
        mechanism description.
        """

        return str(
            causal_chain
        )

    # ======================================================
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        signals: List[Signal],
    ) -> SignalDirection:
        """
        Determine aggregate catalyst direction.
        """

        if not signals:

            return SignalDirection.UNKNOWN

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

        mixed = sum(
            1
            for signal in signals
            if signal.direction
            == SignalDirection.MIXED
        )

        if mixed > 0:

            return SignalDirection.MIXED

        if positive > negative:

            return SignalDirection.POSITIVE

        if negative > positive:

            return SignalDirection.NEGATIVE

        return SignalDirection.NEUTRAL

    # ======================================================
    # HORIZON
    # ======================================================

    @staticmethod
    def _horizon(
        signals: List[Signal],
    ) -> TimeHorizon:
        """
        Determine aggregate catalyst horizon.
        """

        if not signals:

            return TimeHorizon.MEDIUM_TERM

        horizons = [
            signal.horizon
            for signal in signals
        ]

        counts = {}

        for horizon in horizons:

            counts[horizon] = (
                counts.get(
                    horizon,
                    0,
                )
                + 1
            )

        return max(
            counts,
            key=counts.get,
        )

    # ======================================================
    # MAGNITUDE
    # ======================================================

    @staticmethod
    def _magnitude(
        signals: List[Signal],
    ) -> float:
        """
        Estimate catalyst magnitude from signal maturity
        and direction.

        This remains deliberately conservative.
        """

        if not signals:

            return 0.0

        values = []

        stage_weights = {
            SignalStage.NOISE: 20.0,
            SignalStage.WEAK: 35.0,
            SignalStage.EMERGING: 55.0,
            SignalStage.VALIDATED: 75.0,
            SignalStage.CATALYST: 90.0,
            SignalStage.EARNINGS_IMPACT: 95.0,
            SignalStage.MARKET_RECOGNIZED: 70.0,
        }

        for signal in signals:

            values.append(
                stage_weights.get(
                    signal.stage,
                    40.0,
                )
            )

        return round(
            sum(values)
            / len(values),
            2,
        )

    # ======================================================
    # PROBABILITY
    # ======================================================

    @staticmethod
    def _probability(
        signals: List[Signal],
    ) -> float:
        """
        Estimate catalyst probability from signal maturity.
        """

        if not signals:

            return 0.0

        stage_weights = {
            SignalStage.NOISE: 15.0,
            SignalStage.WEAK: 30.0,
            SignalStage.EMERGING: 50.0,
            SignalStage.VALIDATED: 75.0,
            SignalStage.CATALYST: 90.0,
            SignalStage.EARNINGS_IMPACT: 95.0,
            SignalStage.MARKET_RECOGNIZED: 85.0,
        }

        values = [
            stage_weights.get(
                signal.stage,
                40.0,
            )
            for signal in signals
        ]

        return round(
            sum(values)
            / len(values),
            2,
        )

    # ======================================================
    # PERSISTENCE
    # ======================================================

    @staticmethod
    def _persistence(
        signals: List[Signal],
    ) -> float:
        """
        Estimate persistence from signal horizon.
        """

        if not signals:

            return 0.0

        horizon_weights = {
            TimeHorizon.IMMEDIATE: 30.0,
            TimeHorizon.MEDIUM_TERM: 55.0,
            TimeHorizon.STRUCTURAL: 80.0,
            TimeHorizon.LONG_TERM: 90.0,
        }

        values = [
            horizon_weights.get(
                signal.horizon,
                50.0,
            )
            for signal in signals
        ]

        return round(
            sum(values)
            / len(values),
            2,
        )

    # ======================================================
    # MARKET RECOGNITION
    # ======================================================

    @staticmethod
    def _market_recognition(
        signals: List[Signal],
    ) -> float:
        """
        Estimate market recognition.

        Lower recognition is generally more interesting
        for Opportunity discovery because the catalyst
        may not yet be fully priced in.
        """

        if not signals:

            return 0.0

        values = []

        for signal in signals:

            if (
                signal.stage
                == SignalStage.MARKET_RECOGNIZED
            ):

                values.append(90.0)

            elif (
                signal.stage
                == SignalStage.EARNINGS_IMPACT
            ):

                values.append(75.0)

            elif (
                signal.stage
                == SignalStage.CATALYST
            ):

                values.append(55.0)

            elif (
                signal.stage
                == SignalStage.VALIDATED
            ):

                values.append(40.0)

            elif (
                signal.stage
                == SignalStage.EMERGING
            ):

                values.append(25.0)

            elif (
                signal.stage
                == SignalStage.WEAK
            ):

                values.append(15.0)

            else:

                values.append(10.0)

        return round(
            sum(values)
            / len(values),
            2,
        )

    # ======================================================
    # EVIDENCE
    # ======================================================

    @staticmethod
    def _collect_evidence(
        catalyst: Catalyst,
    ) -> None:
        """
        Collect evidence already embedded in signals.
        """

        evidence = []

        for signal in catalyst.signals:

            if signal.source:

                evidence.append(
                    signal.source
                )

            if signal.description:

                evidence.append(
                    signal.description
                )

        catalyst.evidence = evidence

    # ======================================================
    # CONTRADICTIONS
    # ======================================================

    @staticmethod
    def _collect_contradictions(
        catalyst: Catalyst,
    ) -> None:
        """
        Identify obvious contradictory signal directions.
        """

        contradictory = []

        for signal in catalyst.signals:

            if (
                signal.direction
                == SignalDirection.NEGATIVE
            ):

                if signal.description:

                    contradictory.append(
                        signal.description
                    )

                elif signal.title:

                    contradictory.append(
                        signal.title
                    )

        catalyst.contradictory_evidence = (
            contradictory
        )

    # ======================================================
    # SCORE
    # ======================================================

    @staticmethod
    def _calculate_score(
        catalyst: Catalyst,
    ) -> float:
        """
        Calculate Catalyst Score.

        The score rewards:
        - magnitude
        - probability
        - persistence
        - evidence confidence

        It penalizes:
        - market recognition
        - contradictory evidence
        """

        base = (
            catalyst.magnitude * 0.25
            + catalyst.probability * 0.25
            + catalyst.persistence * 0.20
            + catalyst.confidence * 0.20
        )

        recognition_adjustment = (
            100.0
            - catalyst.market_recognition
        ) * 0.10

        contradiction_penalty = min(
            20.0,
            len(
                catalyst.contradictory_evidence
            ) * 5.0,
        )

        score = (
            base
            + recognition_adjustment
            - contradiction_penalty
        )

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
    # CONFIDENCE
    # ======================================================

    @staticmethod
    def _calculate_confidence(
        catalyst: Catalyst,
    ) -> float:
        """
        Calculate Catalyst confidence.

        Classification confidence contributes to the
        analytical confidence but does not replace
        evidence quality.
        """

        signal_confidence = (
            catalyst.classification_confidence
        )

        if not catalyst.signals:

            return 0.0

        source_quality = sum(
            100.0
            if signal.source
            else 40.0
            for signal in catalyst.signals
        ) / len(
            catalyst.signals
        )

        contradiction_penalty = min(
            30.0,
            len(
                catalyst.contradictory_evidence
            ) * 10.0,
        )

        confidence = (
            signal_confidence * 0.35
            + source_quality * 0.45
            + (
                catalyst.probability
                * 0.20
            )
            - contradiction_penalty
        )

        return round(
            max(
                0.0,
                min(
                    100.0,
                    confidence,
                ),
            ),
            2,
        )

    # ======================================================
    # REASONING
    # ======================================================

    @staticmethod
    def _build_reasoning(
        catalyst: Catalyst,
    ) -> None:
        """
        Build concise institutional reasoning.
        """

        reasons = []

        if catalyst.primary_catalyst_family:

            reasons.append(
                (
                    "Primary catalyst family: "
                    f"{catalyst.primary_catalyst_family}."
                )
            )

        if catalyst.direction == (
            SignalDirection.POSITIVE
        ):

            reasons.append(
                "Signal direction is predominantly positive."
            )

        elif catalyst.direction == (
            SignalDirection.NEGATIVE
        ):

            reasons.append(
                "Signal direction is predominantly negative."
            )

        if catalyst.persistence >= 75.0:

            reasons.append(
                "Catalyst has a potentially durable time horizon."
            )

        if catalyst.market_recognition < 40.0:

            reasons.append(
                "Market recognition appears relatively low."
            )

        if catalyst.affected_companies:

            reasons.append(
                "Company-level exposure has been identified."
            )

        catalyst.reasons.extend(
            reasons
        )

        catalyst.reasons.extend(
            catalyst.classification_reasoning
        )

    # ======================================================
    # WARNINGS
    # ======================================================

    @staticmethod
    def _build_warnings(
        catalyst: Catalyst,
    ) -> None:
        """
        Build institutional warnings.
        """

        warnings = []

        if not catalyst.signals:

            warnings.append(
                "No signals supplied."
            )

        if not catalyst.primary_catalyst_id:

            warnings.append(
                "Catalyst could not be classified."
            )

        if catalyst.classification_confidence < 60.0:

            warnings.append(
                "Catalyst classification confidence "
                "is below the preferred threshold."
            )

        if not catalyst.evidence:

            warnings.append(
                "No explicit evidence source identified."
            )

        if not catalyst.affected_companies:

            warnings.append(
                "Company-level exposure has not been explicitly established."
            )

        if catalyst.contradictory_evidence:

            warnings.append(
                "Contradictory evidence is present."
            )

        if (
            catalyst.catalyst_score
            < CatalystEngine.MINIMUM_CATALYST_SCORE
        ):

            warnings.append(
                "Catalyst score is below the preferred "
                "Opportunity threshold."
            )

        catalyst.warnings.extend(
            warnings
        )


# ==========================================================
# PUBLIC API
# ==========================================================


__all__ = [
    "Catalyst",
    "CatalystEngine",
]