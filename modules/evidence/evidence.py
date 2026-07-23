"""
Evidence Model

Represents verified evidence used by EIOS.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Evidence:
    """
    Represents one verified piece of evidence.
    """

    title: str
    category: str
    description: str
    source: str
    entity: str

    reliability: float
    confidence: float

    timestamp: datetime

    def summary(self):
        """Return a short summary."""

        return (
            f"{self.title} | "
            f"{self.category} | "
            f"{self.entity} | "
            f"Source: {self.source} | "
            f"Reliability: {self.reliability}% | "
            f"Confidence: {self.confidence}%"
        )