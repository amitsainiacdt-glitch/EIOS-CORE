"""
EIOS
Everest Investment Operating System

External Observation Adapter
============================

Purpose
-------
Provides the controlled boundary between externally obtained
information and the existing EIOS Observation layer.

Architecture
------------

External Information
        ↓
ExternalObservationAdapter
        ↓
ObservationEngine
        ↓
ObservationRegistry

Design Principles
-----------------
- Does not perform investment analysis.
- Does not create Signals.
- Does not create Evidence.
- Does not calculate valuation.
- Does not calculate opportunity scores.
- Does not modify existing Observation objects.
- Does not fetch from the internet.
- Accepts externally obtained information only.
- Uses the existing ObservationEngine.
- Keeps external ingestion isolated from downstream engines.
"""

from __future__ import annotations

from modules.observation.observation import Observation
from modules.observation.observation_engine import ObservationEngine


class ExternalObservationAdapter:
    """
    Controlled boundary for converting externally obtained
    information into an EIOS Observation.

    The adapter deliberately does not perform:
        - web retrieval
        - HTTP requests
        - API authentication
        - signal generation
        - evidence verification
        - catalyst analysis
        - valuation
        - opportunity scoring
    """

    def __init__(
        self,
        observation_engine: ObservationEngine | None = None,
    ) -> None:

        self.observation_engine = (
            observation_engine
            if observation_engine is not None
            else ObservationEngine()
        )

    # ======================================================
    # PUBLIC INGESTION
    # ======================================================

    def ingest(
        self,
        *,
        title: str,
        description: str,
        source: str,
        category: str,
        entity: str,
        confidence: float,
    ) -> Observation:
        """
        Convert externally obtained information into an
        EIOS Observation.

        No analytical transformation is performed.
        """

        return self.observation_engine.observe(
            title=title,
            description=description,
            source=source,
            category=category,
            entity=entity,
            confidence=self._clamp_confidence(
                confidence
            ),
        )

    # ======================================================
    # CONFIDENCE PROTECTION
    # ======================================================

    @staticmethod
    def _clamp_confidence(
        confidence: float,
    ) -> float:
        """
        Protect the Observation boundary from invalid
        confidence values.

        Confidence is constrained to 0–100.
        """

        try:
            value = float(confidence)
        except (
            TypeError,
            ValueError,
        ):
            return 0.0

        return max(
            0.0,
            min(
                100.0,
                value,
            ),
        )


__all__ = [
    "ExternalObservationAdapter",
]