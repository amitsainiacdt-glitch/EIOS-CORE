"""
Evidence Engine

Creates and manages evidence.
"""

from datetime import datetime

from .evidence import Evidence
from .evidence_registry import EvidenceRegistry


class EvidenceEngine:

    def __init__(self):

        self.registry = EvidenceRegistry()

    def add_evidence(
        self,
        title,
        category,
        description,
        source,
        entity,
        reliability,
        confidence
    ):

        evidence = Evidence(
            title=title,
            category=category,
            description=description,
            source=source,
            entity=entity,
            reliability=reliability,
            confidence=confidence,
            timestamp=datetime.now()
        )

        self.registry.add(evidence)

        return evidence

    def create_from_observation(self, observation):
        """
        Convert an Observation into Evidence.
        """

        return self.add_evidence(
            title=observation.title,
            category=observation.category,
            description=observation.description,
            source=observation.source,
            entity=observation.entity,
            reliability=100,
            confidence=observation.confidence
        )

    def show_evidence(self):

        print("=" * 60)
        print("EVIDENCE")
        print("=" * 60)

        for evidence in self.registry.all():
            print(evidence.summary())

        print()
        print(f"Total Evidence : {self.registry.count()}")