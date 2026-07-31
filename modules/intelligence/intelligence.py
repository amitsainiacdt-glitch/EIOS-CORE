from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Intelligence:
    """
    Standard intelligence object exchanged between EIOS engines.
    """

    title: str
    category: str
    source_engine: str

    conclusion: str = ""
    entity: str = ""

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "source_engine": self.source_engine,
            "conclusion": self.conclusion,
            "entity": self.entity,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "assumptions": self.assumptions,
            "reasoning": self.reasoning,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
        }