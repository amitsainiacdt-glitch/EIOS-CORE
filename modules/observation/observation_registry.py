"""
Observation Registry

Stores all observations collected by EIOS.
"""

from .observation import Observation


class ObservationRegistry:

    def __init__(self):

        self._observations = []

    def add(self, observation: Observation):

        self._observations.append(observation)

    def all(self):

        return self._observations

    def count(self):

        return len(self._observations)

    def latest(self):

        if self._observations:
            return self._observations[-1]
        return None

    def clear(self):

        self._observations.clear()