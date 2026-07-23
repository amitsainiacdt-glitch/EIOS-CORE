from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Evidence:
    title: str
    source: str
    category: str
    confidence: str
    notes: str
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


class EvidenceLibrary:

    def __init__(self):
        self.evidence: List[Evidence] = []

    def add(self, evidence: Evidence):
        self.evidence.append(evidence)

    def count(self):
        return len(self.evidence)

    def to_dict(self):
        return [e.__dict__ for e in self.evidence]