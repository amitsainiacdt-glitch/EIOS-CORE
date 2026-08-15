"""
EIOS
Everest Investment Operating System

Recovery Detection Engine

Purpose:
Interprets TemporalSignalEvolution and determines the current
generic stage of an economic or business recovery.

Architecture:

Signal
    ↓
Signal Intelligence
    ↓
Temporal Signal Intelligence
    ↓
Recovery Detection Engine
    ↓
Recovery Assessment

Design Principles:
- Uses the existing Temporal Signal Engine.
- Produces the existing RecoveryAssessment model.
- No company-specific logic.
- No sector-specific logic.
- No internet access.
- No persistence.
- No valuation.
- No opportunity scoring.
- No investment decision.
- Does not mutate input objects.
- Transparent deterministic classification.
"""

from .recovery_assessment import (
    RecoveryAssessment,
    RecoveryDirection,
    RecoveryStage,
)

from modules.opportunity.signals.temporal_signal_engine import (
    TemporalSignalEvolution,
)


# ==========================================================
# RECOVERY DETECTION ENGINE
# ==========================================================


class RecoveryDetectionEngine:
    """
    Determines the generic recovery stage represented by
    temporal signal evolution.

    The engine deliberately distinguishes:

        bottoming
            from
        recovery

    A signal sequence can bottom without establishing a
    genuine recovery.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        temporal: TemporalSignalEvolution,
    ) -> RecoveryAssessment:
        """
        Convert temporal signal evolution into a typed
        RecoveryAssessment.
        """

        result = RecoveryAssessment()

        # --------------------------------------------------
        # Evidence transfer
        # --------------------------------------------------

        result.temporal_support = (
            RecoveryDetectionEngine._temporal_support(
                temporal
            )
        )

        result.persistence = (
            100.0
            if temporal.persistent
            else 0.0
        )

        result.bottoming_detected = (
            temporal.bottoming
        )

        result.stabilization_detected = (
            temporal.stabilizing
        )

        result.inflection_detected = (
            temporal.inflection
        )

        result.reversal_detected = (
            temporal.reversal
        )

        result.persistence_detected = (
            temporal.persistent
        )

        result.corroboration = (
            RecoveryDetectionEngine._corroboration(
                temporal
            )
        )

        result.contradiction = 0.0

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        result.direction = (
            RecoveryDetectionEngine._direction(
                temporal
            )
        )

        # --------------------------------------------------
        # Stage
        # --------------------------------------------------

        result.stage = (
            RecoveryDetectionEngine._stage(
                temporal
            )
        )

        # --------------------------------------------------
        # Signal breadth
        # --------------------------------------------------

        result.signal_breadth = (
            RecoveryDetectionEngine._signal_breadth(
                temporal
            )
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = (
            RecoveryDetectionEngine._confidence(
                temporal,
                result,
            )
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        RecoveryDetectionEngine._build_reasons(
            temporal,
            result,
        )

        return result

    # ======================================================
    # TEMPORAL SUPPORT
    # ======================================================

    @staticmethod
    def _temporal_support(
        temporal: TemporalSignalEvolution,
    ) -> float:
        """
        Estimate the strength of temporal structure.

        This does not perform investment scoring.
        """

        score = 0.0

        if temporal.trend:
            score += 15.0

        if temporal.accelerating:
            score += 15.0

        if temporal.stabilizing:
            score += 20.0

        if temporal.inflection:
            score += 20.0

        if temporal.bottoming:
            score += 15.0

        if temporal.reversal:
            score += 20.0

        if temporal.persistent:
            score += 15.0

        return min(
            100.0,
            score,
        )

    # ======================================================
    # CORROBORATION
    # ======================================================

    @staticmethod
    def _corroboration(
        temporal: TemporalSignalEvolution,
    ) -> float:
        """
        Estimate corroboration from the temporal structure.

        This remains deliberately conservative because a single
        temporal sequence does not establish independent
        evidence sources.
        """

        score = 0.0

        if temporal.persistent:
            score += 35.0

        if temporal.trend:
            score += 20.0

        if temporal.inflection:
            score += 20.0

        if temporal.reversal:
            score += 25.0

        return min(
            100.0,
            score,
        )

    # ======================================================
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        temporal: TemporalSignalEvolution,
    ) -> RecoveryDirection:
        """
        Translate generic SignalDirection into recovery
        direction.
        """

        value = (
            temporal.direction.value
        )

        if value == "Positive":
            return RecoveryDirection.POSITIVE

        if value == "Negative":
            return RecoveryDirection.NEGATIVE

        if value == "Neutral":
            return RecoveryDirection.STABILIZING

        return RecoveryDirection.UNKNOWN

    # ======================================================
    # STAGE
    # ======================================================

    @staticmethod
    def _stage(
        temporal: TemporalSignalEvolution,
    ) -> RecoveryStage:
        """
        Determine recovery stage.

        Ordering is deliberate:

        confirmed recovery
            requires sustained positive evidence

        early recovery
            requires positive inflection/reversal with
            supporting temporal structure

        early inflection
            identifies directional change without enough
            evidence for recovery

        stabilizing
            identifies slowing deterioration/stabilization

        slowing deterioration
            identifies weakening negative momentum

        deteriorating
            remains the conservative default
        """

        # --------------------------------------------------
        # Confirmed Recovery
        # --------------------------------------------------

        if (
            temporal.reversal
            and temporal.persistent
            and temporal.trend
            and temporal.accelerating
            and temporal.direction.value
            == "Positive"
        ):
            return RecoveryStage.CONFIRMED_RECOVERY

        # --------------------------------------------------
        # Early Recovery
        # --------------------------------------------------

        if (
            temporal.direction.value
            == "Positive"
            and (
                temporal.reversal
                or temporal.inflection
            )
            and (
                temporal.persistent
                or temporal.accelerating
                or temporal.trend
            )
        ):
            return RecoveryStage.EARLY_RECOVERY

        # --------------------------------------------------
        # Early Inflection
        # --------------------------------------------------

        if (
            temporal.inflection
            or temporal.reversal
        ):
            return RecoveryStage.EARLY_INFLECTION

        # --------------------------------------------------
        # Stabilizing
        # --------------------------------------------------

        if (
            temporal.stabilizing
            or temporal.bottoming
        ):
            return RecoveryStage.STABILIZING

        # --------------------------------------------------
        # Slowing Deterioration
        # --------------------------------------------------

        if temporal.decelerating:
            return (
                RecoveryStage.SLOWING_DETERIORATION
            )

        # --------------------------------------------------
        # Deteriorating
        # --------------------------------------------------

        return RecoveryStage.DETERIORATING

    # ======================================================
    # SIGNAL BREADTH
    # ======================================================

    @staticmethod
    def _signal_breadth(
        temporal: TemporalSignalEvolution,
    ) -> float:
        """
        Estimate structural breadth represented by the
        temporal assessment.

        This is intentionally generic.

        Multi-signal breadth across independent indicators
        will be supplied by the aggregation layer later.
        """

        components = 0

        if temporal.trend:
            components += 1

        if temporal.accelerating:
            components += 1

        if temporal.stabilizing:
            components += 1

        if temporal.inflection:
            components += 1

        if temporal.bottoming:
            components += 1

        if temporal.reversal:
            components += 1

        if temporal.persistent:
            components += 1

        return min(
            100.0,
            components
            * 100.0
            / 7.0,
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    @staticmethod
    def _confidence(
        temporal: TemporalSignalEvolution,
        result: RecoveryAssessment,
    ) -> float:
        """
        Calculate deterministic confidence.

        Temporal confidence remains the dominant input.
        Recovery classification does not override the
        evidence quality of the underlying temporal engine.
        """

        confidence = (
            temporal.confidence * 0.50
            + result.temporal_support * 0.20
            + result.signal_breadth * 0.15
            + result.corroboration * 0.15
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

    @staticmethod
    def _build_reasons(
        temporal: TemporalSignalEvolution,
        result: RecoveryAssessment,
    ) -> None:
        """
        Generate transparent recovery reasoning.
        """

        if temporal.bottoming:
            result.reasons.append(
                "Temporal evidence indicates that signal "
                "strength has bottomed."
            )

        if temporal.stabilizing:
            result.reasons.append(
                "Recent observations indicate stabilization."
            )

        if temporal.inflection:
            result.reasons.append(
                "A directional inflection is present."
            )

        if temporal.reversal:
            result.reasons.append(
                "The sequence contains a negative-to-positive "
                "directional reversal."
            )

        if temporal.persistent:
            result.reasons.append(
                "The observed direction shows temporal persistence."
            )

        if temporal.accelerating:
            result.reasons.append(
                "Positive signal strength is accelerating."
            )

        if temporal.decelerating:
            result.warnings.append(
                "Signal momentum is decelerating."
            )

        if result.stage == (
            RecoveryStage.EARLY_RECOVERY
        ):
            result.reasons.append(
                "Evidence is consistent with an early recovery "
                "rather than merely stabilization."
            )

        if result.stage == (
            RecoveryStage.CONFIRMED_RECOVERY
        ):
            result.reasons.append(
                "Persistent positive trend, reversal and "
                "acceleration support confirmed recovery."
            )

        if result.stage == (
            RecoveryStage.STABILIZING
        ):
            result.warnings.append(
                "Stabilization alone does not establish recovery."
            )

        if result.stage == (
            RecoveryStage.EARLY_INFLECTION
        ):
            result.warnings.append(
                "Directional inflection detected, but evidence "
                "is insufficient for confirmed recovery."
            )

        if result.stage == (
            RecoveryStage.SLOWING_DETERIORATION
        ):
            result.warnings.append(
                "Deterioration is slowing, but direction "
                "has not yet established recovery."
            )

        if result.stage == (
            RecoveryStage.DETERIORATING
        ):
            result.warnings.append(
                "Temporal evidence does not currently establish "
                "a recovery process."
            )


__all__ = [
    "RecoveryDetectionEngine",
]