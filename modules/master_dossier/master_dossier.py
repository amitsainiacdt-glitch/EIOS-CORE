from dataclasses import dataclass, field

from .business_section import BusinessSection
from .committee_section import CommitteeSection
from .competitive_section import CompetitiveSection
from .evidence_library import EvidenceLibrary
from .financial_section import FinancialSection
from .macro_section import MacroSection
from .management_section import ManagementSection
from .ownership_section import OwnershipSection
from .risk_section import RiskSection
from .serializer import MasterDossierSerializer
from .valuation_section import ValuationSection
from .decision_section import DecisionSection

@dataclass
class MasterDossier:
    company_name: str
    ticker: str
    sector: str
    industry: str

    # ==========================================================
    # Core Research Modules
    # ==========================================================

    business: BusinessSection = field(default_factory=BusinessSection)
    financial: FinancialSection = field(default_factory=FinancialSection)
    management: ManagementSection = field(default_factory=ManagementSection)
    ownership: OwnershipSection = field(default_factory=OwnershipSection)
    competitive: CompetitiveSection = field(default_factory=CompetitiveSection)
    risk: RiskSection = field(default_factory=RiskSection)
    valuation: ValuationSection = field(default_factory=ValuationSection)
    decision: DecisionSection = field(default_factory=DecisionSection)
    committee: CommitteeSection = field(default_factory=CommitteeSection)
    macro: MacroSection = field(default_factory=MacroSection)

    evidence: EvidenceLibrary = field(default_factory=EvidenceLibrary)

    # ==========================================================
    # Legacy Compatibility Aliases
    # ==========================================================

    @property
    def financial_analysis(self):
        return self.financial

    @financial_analysis.setter
    def financial_analysis(self, value):
        self.financial = value

    @property
    def management_analysis(self):
        return self.management

    @management_analysis.setter
    def management_analysis(self, value):
        self.management = value

    @property
    def business_analysis(self):
        return self.business

    @business_analysis.setter
    def business_analysis(self, value):
        self.business = value

    @property
    def valuation_analysis(self):
        return self.valuation

    @valuation_analysis.setter
    def valuation_analysis(self, value):
        self.valuation = value

    @property
    def ownership_analysis(self):
        return self.ownership

    @ownership_analysis.setter
    def ownership_analysis(self, value):
        self.ownership = value

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
        return self.risk

    @risk_analysis.setter
    def risk_analysis(self, value):
        self.risk = value

    # ==========================================================
    # Utility Methods
    # ==========================================================

    def add_risk(self, risk: str):
        self.risk.business_risks.append(risk)

    def evidence_count(self):
        return self.evidence.count()

    # ==========================================================
    # Export
    # ==========================================================

    def to_dict(self):
        """
        Export the complete Master Dossier as a JSON-safe dictionary.
        """

        return MasterDossierSerializer.serialize(
            {
                "company_name": self.company_name,
                "ticker": self.ticker,
                "sector": self.sector,
                "industry": self.industry,
                "business": self.business,
                "financial": self.financial,
                "management": self.management,
                "ownership": self.ownership,
                "competitive": self.competitive,
                "risk": self.risk,
                "valuation": self.valuation,
                "decision": self.decision,
                "committee": self.committee,
                "macro": self.macro,
                "evidence": self.evidence.to_dict(),
            }
        )