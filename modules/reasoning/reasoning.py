from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class Reasoning:

    title: str
    conclusion: str

    evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    confidence: str = "UNKNOWN"

    metadata: Dict = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def add_evidence(self, item: str):
        self.evidence.append(item)

    def add_assumption(self, item: str):
        self.assumptions.append(item)

    def set_confidence(self, confidence: str):
        self.confidence = confidence

    def to_dict(self):
        return {
            "title": self.title,
            "conclusion": self.conclusion,
            "evidence": self.evidence,
            "assumptions": self.assumptions,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)