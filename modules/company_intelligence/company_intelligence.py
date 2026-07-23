from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CompanyIntelligenceProfile:

    company_name: str
    ticker: str

    identity: Dict = field(default_factory=dict)

    master_dossier: Dict = field(default_factory=dict)

    evidence: List = field(default_factory=list)

    macro_intelligence: Dict = field(default_factory=dict)

    industry_intelligence: Dict = field(default_factory=dict)

    business_intelligence: Dict = field(default_factory=dict)

    management_intelligence: Dict = field(default_factory=dict)

    financial_intelligence: Dict = field(default_factory=dict)

    competitive_intelligence: Dict = field(default_factory=dict)

    risk_intelligence: Dict = field(default_factory=dict)

    valuation_intelligence: Dict = field(default_factory=dict)

    signal_intelligence: Dict = field(default_factory=dict)

    portfolio_intelligence: Dict = field(default_factory=dict)

    decision_history: List = field(default_factory=list)

    learning_history: List = field(default_factory=list)

    knowledge_confidence: Dict = field(default_factory=dict)

    def summary(self):
        return {
            "Company": self.company_name,
            "Ticker": self.ticker,
            "Evidence": len(self.evidence),
            "Decisions": len(self.decision_history),
            "Learning": len(self.learning_history)
        }