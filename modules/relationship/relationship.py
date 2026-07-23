"""
Relationship Model

Represents a relationship between two pieces of knowledge.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Relationship:
    """
    Represents an intelligence relationship.
    """

    source: str
    relationship_type: str
    target: str

    confidence: float

    description: str = ""

    evidence: List = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)

    def add_evidence(self, evidence):
        self.evidence.append(evidence)

    def summary(self):

        return (
            f"{self.source} "
            f"--[{self.relationship_type}]--> "
            f"{self.target} "
            f"(Confidence: {self.confidence}%)"
        )