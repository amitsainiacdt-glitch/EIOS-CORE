"""
EIOS
Everest Investment Operating System

Temporal Signal Intelligence Engine

Purpose:
Analyses the evolution of a chronological sequence of
Opportunity Signals.

Architecture:

Signal
    ↓
Signal Intelligence
    ↓
Temporal Signal Intelligence
    ↓
Signal Aggregation
    ↓
Catalyst Detection

Design Principles:
- Does not mutate Signal objects.
- Does not persist data.
- Does not access the internet.
- Does not perform valuation.
- Does not score investment opportunities.
- Does not make investment decisions.
- Uses the canonical Signal model.
- Returns a separate typed temporal assessment.
- Missing or invalid dates are reported rather than guessed.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .signal_model import (
    Signal,
    SignalDirection,
)


# ==========================================================
# TEMPORAL SIGNAL EVOLUTION
# ==========================================================


@dataclass
class TemporalSignalEvolution:
    """
    Institutional assessment of Signal evolution through time.

    This is a passive result object.

    The engine determines the values.
    """

    direction: SignalDirection = (
        SignalDirection.UNKNOWN
    )

    trend: bool = False

    accelerating: bool = False

    decelerating: bool = False

    stabilizing: bool = False

    inflection: bool = False

    bottoming: bool = False

    reversal: bool = False

    persistent: bool = False

    strength_score: float = 0.0

    confidence: float = 0.0

    observations: int = 0

    valid_observations: int = 0

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# TEMPORAL SIGNAL ENGINE
# ==========================================================


class TemporalSignalEngine:
    """
    Analyses chronological Signal sequences.

    The engine performs generic temporal analysis only.

    It does not determine whether a company or sector is
    investable.

    Recovery interpretation belongs to higher-level engines.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    def analyze(
        self,
        signals: List[Signal],
    ) -> TemporalSignalEvolution:
        """
        Analyse a chronological Signal sequence.

        Signals are ordered internally using detected_date.

        Invalid or missing dates are not guessed.

        A minimum of two valid observations is required for
        directional temporal analysis.
        """

        result = TemporalSignalEvolution()

        result.observations = len(
            signals
        )

        if not signals:
            result.warnings.append(
                "No signals supplied."
            )

            return result

        dated_signals = []

        for signal in signals:

            detected_date = self._parse_date(
                signal.detected_date
            )

            if detected_date is None:

                result.warnings.append(
                    "Signal missing a valid detected date."
                )

                continue

            dated_signals.append(
                (
                    detected_date,
                    signal,
                )
            )

        result.valid_observations = len(
            dated_signals
        )

        if result.valid_observations < 2:

            result.warnings.append(
                "At least two valid dated observations "
                "are required for temporal analysis."
            )

            if result.valid_observations == 1:

                signal = dated_signals[0][1]

                result.direction = (
                    signal.direction
                )

                result.strength_score = (
                    self._signal_strength(
                        signal
                    )
                )

                result.confidence = (
                    self._confidence(
                        result
                    )
                )

            return result

        # --------------------------------------------------
        # Chronological ordering
        # --------------------------------------------------

        dated_signals.sort(
            key=lambda item: item[0]
        )

        ordered_signals = [
            item[1]
            for item in dated_signals
        ]

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        result.direction = (
            self._direction(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Strength
        # --------------------------------------------------

        result.strength_score = (
            self._strength(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Trend
        # --------------------------------------------------

        result.trend = (
            self._is_trend(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Acceleration / deceleration
        # --------------------------------------------------

        result.accelerating = (
            self._is_accelerating(
                ordered_signals
            )
        )

        result.decelerating = (
            self._is_decelerating(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Stabilisation
        # --------------------------------------------------

        result.stabilizing = (
            self._is_stabilizing(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Inflection
        # --------------------------------------------------

        result.inflection = (
            self._is_inflection(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Bottoming
        # --------------------------------------------------

        result.bottoming = (
            self._is_bottoming(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Reversal
        # --------------------------------------------------

        result.reversal = (
            self._is_reversal(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Persistence
        # --------------------------------------------------

        result.persistent = (
            self._is_persistent(
                ordered_signals
            )
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = (
            self._confidence(
                result
            )
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        self._build_reasons(
            result
        )

        return result

    # ======================================================
    # DATE PARSING
    # ======================================================

    def _parse_date(
        self,
        value: str,
    ) -> Optional[datetime]:
        """
        Parse supported ISO-style date formats.

        Invalid values return None.

        The engine never invents a date.
        """

        if not value:
            return None

        value = value.strip()

        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
        ]

        for date_format in formats:

            try:

                return datetime.strptime(
                    value,
                    date_format,
                )

            except ValueError:
                continue

        return None

    # ======================================================
    # SIGNAL STRENGTH
    # ======================================================

    def _signal_strength(
        self,
        signal: Signal,
    ) -> float:
        """
        Calculate generic signal strength from explicit
        canonical Signal fields.
        """

        values = [
            signal.magnitude,
            signal.relevance,
            signal.probability,
            signal.confidence,
        ]

        available = [
            value
            for value in values
            if value > 0
        ]

        if not available:
            return 0.0

        return (
            sum(available)
            / len(available)
        )

    # ======================================================
    # STRENGTH
    # ======================================================

    def _strength(
        self,
        signals: List[Signal],
    ) -> float:
        """
        Calculate average temporal signal strength.
        """

        values = [
            self._signal_strength(
                signal
            )
            for signal in signals
        ]

        values = [
            value
            for value in values
            if value > 0
        ]

        if not values:
            return 0.0

        return (
            sum(values)
            / len(values)
        )

    # ======================================================
    # DIRECTION
    # ======================================================

    def _direction(
        self,
        signals: List[Signal],
    ) -> SignalDirection:
        """
        Determine dominant direction from the sequence.
        """

        positive = 0
        negative = 0
        neutral = 0

        for signal in signals:

            if signal.direction == (
                SignalDirection.POSITIVE
            ):
                positive += 1

            elif signal.direction == (
                SignalDirection.NEGATIVE
            ):
                negative += 1

            elif signal.direction == (
                SignalDirection.NEUTRAL
            ):
                neutral += 1

        if positive > negative:
            return SignalDirection.POSITIVE

        if negative > positive:
            return SignalDirection.NEGATIVE

        if (
            positive == negative
            and positive > 0
        ):
            return SignalDirection.MIXED

        if neutral > 0:
            return SignalDirection.NEUTRAL

        return SignalDirection.UNKNOWN

    # ======================================================
    # TREND
    # ======================================================

    def _is_trend(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect persistent directional consistency.
        """

        if len(signals) < 3:
            return False

        directions = [
            signal.direction
            for signal in signals
        ]

        positive = directions.count(
            SignalDirection.POSITIVE
        )

        negative = directions.count(
            SignalDirection.NEGATIVE
        )

        required = (
            len(signals) * 2
            + 2
        ) // 3

        return (
            positive >= required
            or negative >= required
        )

    # ======================================================
    # ACCELERATION
    # ======================================================

    def _is_accelerating(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect increasing positive signal strength.

        Requires at least three observations.
        """

        if len(signals) < 3:
            return False

        strengths = [
            self._signal_strength(
                signal
            )
            for signal in signals
        ]

        first = strengths[0]

        middle = strengths[
            len(strengths) // 2
        ]

        last = strengths[-1]

        return (
            last > middle
            and middle >= first
        )

    # ======================================================
    # DECELERATION
    # ======================================================

    def _is_decelerating(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect declining signal strength.
        """

        if len(signals) < 3:
            return False

        strengths = [
            self._signal_strength(
                signal
            )
            for signal in signals
        ]

        first = strengths[0]

        middle = strengths[
            len(strengths) // 2
        ]

        last = strengths[-1]

        return (
            last < middle
            and middle <= first
        )

    # ======================================================
    # STABILISATION
    # ======================================================

    def _is_stabilizing(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect a recent reduction in directional deterioration.

        Stabilisation is deliberately weaker than recovery.
        """

        if len(signals) < 3:
            return False

        directions = [
            signal.direction
            for signal in signals
        ]

        negative_count = directions.count(
            SignalDirection.NEGATIVE
        )

        recent = directions[-2:]

        return (
            negative_count >= 2
            and not all(
                direction
                == SignalDirection.NEGATIVE
                for direction in recent
            )
        )

    # ======================================================
    # INFLECTION
    # ======================================================

    def _is_inflection(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect a directional transition in the sequence.

        Example:

            Negative
            Negative
            Neutral
            Positive
        """

        if len(signals) < 3:
            return False

        directions = [
            signal.direction
            for signal in signals
        ]

        negative_before = any(
            direction
            == SignalDirection.NEGATIVE
            for direction in directions[
                :-2
            ]
        )

        positive_after = any(
            direction
            == SignalDirection.POSITIVE
            for direction in directions[
                -2:
            ]
        )

        return (
            negative_before
            and positive_after
        )

    # ======================================================
    # BOTTOMING
    # ======================================================

    def _is_bottoming(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect deterioration followed by stabilisation.

        Bottoming is not interpreted as recovery.
        """

        if len(signals) < 3:
            return False

        strengths = [
            self._signal_strength(
                signal
            )
            for signal in signals
        ]

        if not strengths:
            return False

        minimum_index = (
            strengths.index(
                min(strengths)
            )
        )

        return (
            minimum_index > 0
            and minimum_index
            < len(strengths) - 1
            and strengths[-1]
            >= strengths[
                minimum_index
            ]
        )

    # ======================================================
    # REVERSAL
    # ======================================================

    def _is_reversal(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect a negative-to-positive directional reversal.
        """

        if len(signals) < 3:
            return False

        previous = [
            signal.direction
            for signal in signals[
                :-2
            ]
        ]

        recent = [
            signal.direction
            for signal in signals[
                -2:
            ]
        ]

        had_negative = (
            SignalDirection.NEGATIVE
            in previous
        )

        has_positive = (
            SignalDirection.POSITIVE
            in recent
        )

        return (
            had_negative
            and has_positive
        )

    # ======================================================
    # PERSISTENCE
    # ======================================================

    def _is_persistent(
        self,
        signals: List[Signal],
    ) -> bool:
        """
        Detect persistence across the sequence.
        """

        if len(signals) < 3:
            return False

        active = [
            signal
            for signal in signals
            if (
                signal.persistence >= 50
                or signal.confidence >= 50
            )
        ]

        return (
            len(active)
            >= (
                len(signals) * 2
                + 2
            ) // 3
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        result: TemporalSignalEvolution,
    ) -> float:
        """
        Calculate confidence in the temporal assessment.

        Confidence is based on:
        - observation breadth
        - signal strength
        - persistence
        - temporal structure
        """

        breadth = min(
            100.0,
            result.valid_observations
            * 20.0,
        )

        temporal_structure = 0.0

        if result.trend:
            temporal_structure += 20.0

        if result.inflection:
            temporal_structure += 20.0

        if result.bottoming:
            temporal_structure += 15.0

        if result.reversal:
            temporal_structure += 20.0

        if result.stabilizing:
            temporal_structure += 10.0

        if result.persistent:
            temporal_structure += 15.0

        confidence = (
            result.strength_score
            * 0.40
            + breadth
            * 0.25
            + min(
                100.0,
                temporal_structure,
            )
            * 0.35
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
        result: TemporalSignalEvolution,
    ) -> None:
        """
        Build transparent temporal reasoning.
        """

        if result.trend:
            result.reasons.append(
                "A persistent directional trend "
                "is present across the signal sequence."
            )

        if result.accelerating:
            result.reasons.append(
                "Signal strength is increasing "
                "through the observed sequence."
            )

        if result.decelerating:
            result.warnings.append(
                "Signal strength is declining "
                "through the observed sequence."
            )

        if result.stabilizing:
            result.reasons.append(
                "Recent observations indicate "
                "stabilisation after deterioration."
            )

        if result.inflection:
            result.reasons.append(
                "The sequence shows a directional inflection."
            )

        if result.bottoming:
            result.reasons.append(
                "Signal strength appears to have "
                "bottomed and subsequently stabilized."
            )

        if result.reversal:
            result.reasons.append(
                "The sequence shows a negative-to-positive reversal."
            )

        if result.persistent:
            result.reasons.append(
                "Temporal persistence is supported "
                "across multiple observations."
            )

        if result.direction == (
            SignalDirection.POSITIVE
        ):
            result.reasons.append(
                "The dominant temporal direction is positive."
            )

        elif result.direction == (
            SignalDirection.NEGATIVE
        ):
            result.warnings.append(
                "The dominant temporal direction is negative."
            )

        if result.valid_observations < (
            result.observations
        ):
            result.warnings.append(
                "Some observations were excluded because "
                "their dates were missing or invalid."
            )


__all__ = [
    "TemporalSignalEvolution",
    "TemporalSignalEngine",
]