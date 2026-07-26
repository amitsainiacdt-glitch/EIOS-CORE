from dataclasses import dataclass, field
from typing import Dict, List

from .evidence_library import EvidenceLibrary


@dataclass
class MasterDossier:
    company_name: str
    ticker: str
    sector: str
    industry: str

    # ==========================================================
    # Core Research Modules
    # ==========================================================

    business_quality: Dict = field(default_factory=dict)
    management: Dict = field(default_factory=dict)
    thesis: Dict = field(default_factory=dict)
    committee: Dict = field(default_factory=dict)

    financials: Dict = field(default_factory=dict)
    competitive: Dict = field(default_factory=dict)
    valuation: Dict = field(default_factory=dict)

    # NEW
    decision: Dict = field(default_factory=dict)

    risks: List[str] = field(default_factory=list)
    evidence: EvidenceLibrary = field(default_factory=EvidenceLibrary)

    # ==========================================================
    # Legacy compatibility aliases
    # ==========================================================

    @property
    def financial_analysis(self):
        return self.financials

    @financial_analysis.setter
    def financial_analysis(self, value):
        self.financials = value

    @property
    def management_analysis(self):
        return self.management

    @management_analysis.setter
    def management_analysis(self, value):
        self.management = value

    @property
    def business_analysis(self):
        return self.business_quality

    @business_analysis.setter
    def business_analysis(self, value):
        self.business_quality = value

    @property
    def valuation_analysis(self):
        return self.valuation

    @valuation_analysis.setter
    def valuation_analysis(self, value):
        self.valuation = value

    @property
    def competitive_analysis(self):
        return self.competitive

    @competitive_analysis.setter
    def competitive_analysis(self, value):
        self.competitive = value

    @property
    def competitive_intelligence(self):
        return self.competitive

    @competitive_intelligence.setter
    def competitive_intelligence(self, value):
        self.competitive = value

    @property
    def risk_analysis(self):
        return self.risks

    @risk_analysis.setter
    def risk_analysis(self, value):
        self.risks = value

    @property
    def thesis_analysis(self):
        return self.thesis

    @thesis_analysis.setter
    def thesis_analysis(self, value):
        self.thesis = value

    @property
    def investment_thesis(self):
        return self.thesis

    @investment_thesis.setter
    def investment_thesis(self, value):
        self.thesis = value

    # ==========================================================
    # Utility Methods
    # ==========================================================

    def add_risk(self, risk: str):
        self.risks.append(risk)

    def evidence_count(self):
        return self.evidence.count()

    # ==========================================================
    # Export
    # ==========================================================

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
            "decision": self.decision,
            "risks": self.risks,
            "evidence": self.evidence.to_dict(),
        }