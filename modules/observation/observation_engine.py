"""
EIOS
Everest Investment Operating System

Observation Engine
==================

Creates, validates, registers and persists observations.

The Observation Engine is responsible for ingestion
of observations into the EIOS observation registry.

It does not perform:
    - valuation
    - opportunity scoring
    - signal generation
    - investment analysis

Novelty detection is delegated to ObservationNoveltyEngine.

Persistence is delegated to ObservationPersistence.
"""

from __future__ import annotations

from datetime import datetime, timezone

from .observation import Observation
from .historical_comparison import HistoricalComparison
from .historical_comparison_engine import (
    HistoricalComparisonEngine,
)
from .historical_observation_selector import (
    HistoricalObservationSelection,
    HistoricalObservationSelector,
)
from .observation_novelty_engine import (
    ObservationNoveltyEngine,
)
from .observation_persistence import (
    ObservationPersistence,
)
from .observation_registry import ObservationRegistry


class ObservationEngine:
    """
    Creates and manages observations.

    Existing observations are loaded from persistent state
    when the engine starts.

    New observations are registered and persisted.

    Duplicate observations are rejected deterministically
    by ObservationNoveltyEngine.
    """

    def __init__(
        self,
        registry: ObservationRegistry | None = None,
        novelty_engine: ObservationNoveltyEngine | None = None,
        persistence: ObservationPersistence | None = None,
        historical_comparison_engine: (
            HistoricalComparisonEngine | None
        ) = None,
        historical_observation_selector: (
            HistoricalObservationSelector | None
        ) = None,
    ):

        self.registry = (
            registry
            if registry is not None
            else ObservationRegistry()
        )

        self.novelty_engine = (
            novelty_engine
            if novelty_engine is not None
            else ObservationNoveltyEngine()
        )

        self.persistence = (
            persistence
            if persistence is not None
            else ObservationPersistence()
        )

        self.historical_comparison_engine = (
            historical_comparison_engine
            if historical_comparison_engine is not None
            else HistoricalComparisonEngine()
        )

        self.historical_observation_selector = (
            historical_observation_selector
            if historical_observation_selector is not None
            else HistoricalObservationSelector()
        )

        # --------------------------------------------------
        # LOAD EXISTING STATE
        # --------------------------------------------------

        existing_observations = (
            self.persistence.load()
        )

        for observation in existing_observations:

            self.registry.add(
                observation
            )

    # ======================================================
    # OBSERVE
    # ======================================================

    def observe(
        self,
        title,
        description,
        source,
        category,
        entity,
        confidence,
        provenance=None,
    ):
        """
        Create an observation and register it only when
        the information is new.

        New observations are immediately persisted.

        Returns:
            Observation
                when the observation is new.

            None
                when the observation is a duplicate.
        """

        observation = Observation(
            title=title,
            description=description,
            source=source,
            category=category,
            entity=entity,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc),
            provenance=provenance,
        )

        novelty = self.novelty_engine.assess(
            observation,
            self.registry.all(),
        )

        if not novelty.is_new:

            return None

        self.registry.add(
            observation
        )

        self.persistence.save(
            self.registry.all()
        )

        return observation

    # ======================================================
    # NOVELTY ASSESSMENT
    # ======================================================

    def assess_novelty(
        self,
        observation: Observation,
    ):
        """
        Assess an observation without registering it.
        """

        return self.novelty_engine.assess(
            observation,
            self.registry.all(),
        )

    # ======================================================
    # HISTORICAL COMPARISON
    # ======================================================

    def select_historical(
        self,
        current_observation: Observation,
    ) -> HistoricalObservationSelection:
        """
        Select an unambiguous historical candidate from the
        existing observation registry without mutating state.
        """

        return self.historical_observation_selector.select(
            current_observation=current_observation,
            observations=self.registry.all(),
        )

    def compare_historical(
        self,
        current_observation: Observation,
        historical_observation: Observation,
    ) -> HistoricalComparison:
        """
        Compare two explicitly selected observations.

        Historical candidate selection remains the caller's
        responsibility. The Observation Engine does not infer
        which prior observation is comparable and does not
        register, persist, or publish the comparison result.
        """

        return self.historical_comparison_engine.compare(
            current_observation=current_observation,
            historical_observation=historical_observation,
        )

    # ======================================================
    # RELOAD
    # ======================================================

    def reload(self) -> None:
        """
        Reload persistent observation state.

        Existing in-memory observations are cleared first.
        """

        self.registry.clear()

        existing_observations = (
            self.persistence.load()
        )

        for observation in existing_observations:

            self.registry.add(
                observation
            )

    # ======================================================
    # SAVE
    # ======================================================

    def save(self) -> None:
        """
        Explicitly persist the current observation state.
        """

        self.persistence.save(
            self.registry.all()
        )

    # ======================================================
    # OBSERVATION DISPLAY
    # ======================================================

    def show_observations(self):

        print("=" * 60)
        print("OBSERVATIONS")
        print("=" * 60)

        for observation in self.registry.all():

            print(
                observation.summary()
            )

        print()

        print(
            f"Total Observations : "
            f"{self.registry.count()}"
        )


__all__ = [
    "ObservationEngine",
]
