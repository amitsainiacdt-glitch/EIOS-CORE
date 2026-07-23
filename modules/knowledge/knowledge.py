from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Knowledge:
    """
    Represents structured knowledge created from validated evidence.
    """

    title: str
    category: str
    description: str

    confidence: float = 0.0

    source_evidence: list = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.now)

    tags: list = field(default_factory=list)

    def add_evidence(self, evidence):
        """
        Link supporting evidence.
        """
        self.source_evidence.append(evidence)

    def add_tag(self, tag: str):
        """
        Add a knowledge tag.
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def update_confidence(self, confidence: float):
        """
        Update confidence score.
        """
        self.confidence = confidence

    def summary(self):
        """
        Short summary.
        """
        return (
            f"{self.title} | "
            f"Category: {self.category} | "
            f"Confidence: {self.confidence:.0f}%"
        )

    def to_dict(self):
        """
        Convert object to dictionary.
        """
        return {
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "confidence": self.confidence,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "evidence_count": len(self.source_evidence),
        }