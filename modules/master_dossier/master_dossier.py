from dataclasses import dataclass, field
from typing import Dict, List
from .evidence_library import EvidenceLibrary


@dataclass
class MasterDossier:
    company_name: str
    ticker: str
    sector: str
    industry: str

    business_quality: Dict = field(default_factory=dict)
    management: Dict = field(default_factory=dict)
    thesis: Dict = field(default_factory=dict)
    committee: Dict = field(default_factory=dict)
    financials: Dict = field(default_factory=dict)
    competitive: Dict = field(default_factory=dict)
    valuation: Dict = field(default_factory=dict)

    risks: List[str] = field(default_factory=list)
    evidence: EvidenceLibrary = field(default_factory=EvidenceLibrary)

    def add_risk(self, risk: str):
        self.risks.append(risk)

    def evidence_count(self):
        return self.evidence.count()

    def to_dict(self):
        return {
            "company_name": self.company_name,
            "ticker": self.ticker,
            "sector": self.sector,
            "industry": self.industry,
            "business_quality": self.business_quality,
            "management": self.management,
            "thesis": self.thesis,
            "committee": self.committee,
            "financials": self.financials,
            "competitive": self.competitive,
            "valuation": self.valuation,
            "risks": self.risks,
            "evidence": self.evidence.to_dict(),
        }