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
    # Additive metadata.  Older persisted observations remain loadable.
    content_type: Optional[str] = None
    source_quality_tier: Optional[str] = None
    canonical_url: Optional[str] = None
    observation_fingerprint: Optional[str] = None
    # Source-neutral document timing and identity. These remain optional so
    # observations persisted before primary-source ingestion still load.
    published_at: Optional[datetime] = None
    filing_at: Optional[datetime] = None
    source_document_id: Optional[str] = None
    document_hash: Optional[str] = None
    extraction_method: Optional[str] = None
    public_fact_candidate_id: Optional[str] = None
    public_fact_event_type: Optional[str] = None
    public_fact_statement_posture: Optional[str] = None
    public_fact_proposal_id: Optional[str] = None
    public_fact_review_id: Optional[str] = None
    contributing_job_ids: tuple[str, ...] = ()
    contributing_research_intents: tuple[str, ...] = ()


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
