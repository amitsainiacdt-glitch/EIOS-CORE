"""
Observation Model

Represents a single observation collected from the outside world.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Observation:
    """
    Represents one real-world observation.
    """

    title: str
    description: str
    source: str
    category: str
    entity: str
    confidence: float
    timestamp: datetime

    def summary(self):
        """Return a short summary."""

        return (
            f"[{self.category}] "
            f"{self.title} "
            f"({self.entity}) "
            f"Confidence: {self.confidence}%"
        )