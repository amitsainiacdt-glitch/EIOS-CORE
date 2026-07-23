"""
Observation Engine

Creates and manages observations.
"""

from datetime import datetime

from .observation import Observation
from .observation_registry import ObservationRegistry


class ObservationEngine:

    def __init__(self):

        self.registry = ObservationRegistry()

    def observe(
        self,
        title,
        description,
        source,
        category,
        entity,
        confidence
    ):

        observation = Observation(
            title=title,
            description=description,
            source=source,
            category=category,
            entity=entity,
            confidence=confidence,
            timestamp=datetime.now()
        )

        self.registry.add(observation)

        return observation

    def show_observations(self):

        print("=" * 60)
        print("OBSERVATIONS")
        print("=" * 60)

        for observation in self.registry.all():
            print(observation.summary())

        print()
        print(f"Total Observations : {self.registry.count()}")
