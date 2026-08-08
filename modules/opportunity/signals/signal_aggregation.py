"""
EIOS
Everest Investment Operating System

Signal Aggregation Engine

Purpose:
Combines related individual signals into higher-order
intelligence themes.

Architecture:

Individual Signals
        ↓
Signal Aggregation
        ↓
Signal Cluster
        ↓
Emerging Theme
        ↓
Catalyst Engine
        ↓
Opportunity Engine

Design Principles:
- No persistence.
- No valuation.
- No investment recommendation.
- No mutation of Signal objects.
- Independent signals should strengthen a theme.
- Contradictory signals should reduce confidence.
- Duplicate observations must not be treated as independent evidence.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from .signal_model import (
    Signal,
    SignalDomain,
    SignalDirection,
)


# ==========================================================
# SIGNAL CLUSTER
# ==========================================================


@dataclass
class SignalCluster:
    """
    Higher-order intelligence created from related signals.
    """

    cluster_id: str = ""

    theme: str = ""

    signals: List[Signal] = field(
        default_factory=list
    )

    domains: List[SignalDomain] = field(
        default_factory=list
    )

    sectors: List[str] = field(
        default_factory=list
    )

    companies: List[str] = field(
        default_factory=list
    )

    direction: SignalDirection = (
        SignalDirection.UNKNOWN
    )

    signal_count: int = 0

    independent_sources: int = 0

    average_strength: float = 0.0

    average_confidence: float = 0.0

    contradiction_count: int = 0

    cluster_score: float = 0.0

    confidence: float = 0.0

    emerging: bool = False

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# SIGNAL AGGREGATION ENGINE
# ==========================================================


class SignalAggregationEngine:
    """
    Combines related signals into higher-order themes.
    """

    # ======================================================
    # AGGREGATE
    # ======================================================

    def aggregate(
        self,
        signals: List[Signal],
        *,
        theme: str,
        cluster_id: str = "",
    ) -> SignalCluster:
        """
        Aggregate signals belonging to one logical theme.

        The engine does not decide whether a theme is
        investable. It only determines whether the combined
        evidence represents a meaningful intelligence cluster.
        """

        cluster = SignalCluster()

        cluster.cluster_id = cluster_id
        cluster.theme = theme
        cluster.signals = list(signals)

        if not signals:
            cluster.warnings.append(
                "No signals supplied."
            )

            return cluster

        # --------------------------------------------------
        # Basic Counts
        # --------------------------------------------------

        cluster.signal_count = len(
            signals
        )

        # --------------------------------------------------
        # Domains
        # --------------------------------------------------

        cluster.domains = self._unique_domains(
            signals
        )

        # --------------------------------------------------
        # Sectors
        # --------------------------------------------------

        cluster.sectors = self._unique_values(
            signals,
            "sectors",
        )

        # --------------------------------------------------
        # Companies
        # --------------------------------------------------

        cluster.companies = self._unique_values(
            signals,
            "companies",
        )

        # --------------------------------------------------
        # Sources
        # --------------------------------------------------

        cluster.independent_sources = (
            self._independent_sources(
                signals
            )
        )

        # --------------------------------------------------
        # Strength
        # --------------------------------------------------

        cluster.average_strength = (
            self._average_strength(
                signals
            )
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        cluster.average_confidence = (
            self._average_confidence(
                signals
            )
        )

        # --------------------------------------------------
        # Contradictions
        # --------------------------------------------------

        cluster.contradiction_count = (
            self._contradictions(
                signals
            )
        )

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        cluster.direction = (
            self._direction(
                signals
            )
        )

        # --------------------------------------------------
        # Cluster Score
        # --------------------------------------------------

        cluster.cluster_score = (
            self._cluster_score(
                cluster
            )
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        cluster.confidence = (
            self._cluster_confidence(
                cluster
            )
        )

        # --------------------------------------------------
        # Emerging Theme
        # --------------------------------------------------

        cluster.emerging = (
            self._is_emerging(
                cluster
            )
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        self._build_reasons(
            cluster
        )

        return cluster

    # ======================================================
    # UNIQUE DOMAINS
    # ======================================================

    def _unique_domains(
        self,
        signals: List[Signal],
    ) -> List[SignalDomain]:

        domains = []

        for signal in signals:

            if signal.domain not in domains:
                domains.append(
                    signal.domain
                )

        return domains

    # ======================================================
    # UNIQUE VALUES
    # ======================================================

    def _unique_values(
        self,
        signals: List[Signal],
        attribute: str,
    ) -> List[str]:

        values = []

        for signal in signals:

            for value in getattr(
                signal,
                attribute,
                [],
            ):

                if value and value not in values:
                    values.append(value)

        return values

    # ======================================================
    # INDEPENDENT SOURCES
    # ======================================================

    def _independent_sources(
        self,
        signals: List[Signal],
    ) -> int:

        sources = set()

        for signal in signals:

            if signal.source:
                sources.add(
                    signal.source
                )

            for source in signal.supporting_sources:
                if source:
                    sources.add(source)

        return len(sources)

    # ======================================================
    # AVERAGE STRENGTH
    # ======================================================

    def _average_strength(
        self,
        signals: List[Signal],
    ) -> float:

        values = []

        for signal in signals:

            components = [
                signal.magnitude,
                signal.relevance,
                signal.probability,
            ]

            available = [
                value
                for value in components
                if value > 0
            ]

            if available:
                values.append(
                    sum(available)
                    / len(available)
                )

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ======================================================
    # AVERAGE CONFIDENCE
    # ======================================================

    def _average_confidence(
        self,
        signals: List[Signal],
    ) -> float:

        values = [
            signal.confidence
            for signal in signals
            if signal.confidence > 0
        ]

        if not values:
            return 0.0

        return sum(values) / len(values)

    # ======================================================
    # CONTRADICTIONS
    # ======================================================

    def _contradictions(
        self,
        signals: List[Signal],
    ) -> int:

        return sum(
            len(
                signal.contradictory_evidence
            )
            for signal in signals
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

        if positive == negative and positive > 0:
            return SignalDirection.MIXED

        return SignalDirection.UNKNOWN

    # ======================================================
    # CLUSTER SCORE
    # ======================================================

    def _cluster_score(
        self,
        cluster: SignalCluster,
    ) -> float:

        breadth = min(
            100.0,
            cluster.signal_count * 15.0,
        )

        source_score = min(
            100.0,
            cluster.independent_sources * 20.0,
        )

        contradiction_penalty = min(
            40.0,
            cluster.contradiction_count * 5.0,
        )

        score = (
            cluster.average_strength * 0.40
            + cluster.average_confidence * 0.25
            + breadth * 0.20
            + source_score * 0.15
            - contradiction_penalty
        )

        return max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

    # ======================================================
    # CLUSTER CONFIDENCE
    # ======================================================

    def _cluster_confidence(
        self,
        cluster: SignalCluster,
    ) -> float:

        confidence = (
            cluster.average_confidence * 0.40
            + min(
                100.0,
                cluster.independent_sources * 25.0,
            ) * 0.25
            + cluster.average_strength * 0.25
            + min(
                100.0,
                cluster.signal_count * 20.0,
            ) * 0.10
        )

        contradiction_penalty = min(
            30.0,
            cluster.contradiction_count * 5.0,
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
    # EMERGING
    # ======================================================

    def _is_emerging(
        self,
        cluster: SignalCluster,
    ) -> bool:

        return (
            cluster.signal_count >= 3
            and cluster.independent_sources >= 2
            and cluster.cluster_score >= 60.0
            and cluster.confidence >= 60.0
        )

    # ======================================================
    # REASONS
    # ======================================================

    def _build_reasons(
        self,
        cluster: SignalCluster,
    ) -> None:

        if cluster.signal_count >= 3:
            cluster.reasons.append(
                "Multiple related signals detected."
            )

        if cluster.independent_sources >= 2:
            cluster.reasons.append(
                "Evidence originates from multiple sources."
            )

        if len(cluster.domains) >= 2:
            cluster.reasons.append(
                "Signal cluster spans multiple intelligence domains."
            )

        if cluster.average_strength >= 70:
            cluster.reasons.append(
                "Average signal strength is elevated."
            )

        if cluster.contradiction_count > 0:
            cluster.warnings.append(
                "Contradictory evidence exists within the cluster."
            )

        if cluster.emerging:
            cluster.reasons.append(
                "Cluster meets the threshold for an emerging theme."
            )