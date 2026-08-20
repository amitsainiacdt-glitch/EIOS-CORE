"""
Observation Model

Represents a single observation collected from the outside world.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ObservationProvenance:
    """Optional runtime lineage for an externally created observation."""

    cycle_id: Optional[str] = None
    job_id: Optional[str] = None
    research_intent: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    source_url: Optional[str] = None
    source_domain: Optional[str] = None
    source_type: Optional[str] = None
    content_fingerprint: Optional[str] = None


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
    provenance: Optional[ObservationProvenance] = None

    def summary(self):
        """Return a short summary."""

        return (
            f"[{self.category}] "
            f"{self.title} "
            f"({self.entity}) "
            f"Confidence: {self.confidence}%"
        )
