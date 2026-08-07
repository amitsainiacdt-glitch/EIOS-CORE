"""
===============================================================================
EIOS
Everest Investment Operating System

Company Research

Purpose:
    Acts as the central coordinator between EIOS research engines
    and the Master Dossier.

Architecture:
    - CompanyResearch performs no domain calculations.
    - Research engines produce domain intelligence.
    - CompanyResearch stores that intelligence in the Master Dossier.
    - MasterDossier remains the single source of truth.
    - Typed section migration is performed subsystem by subsystem.

Migration Status:
    Business domain:
        Migrated to typed BusinessSection.

    Financial domain:
        Migrated to typed FinancialSection.

    Management domain:
        Migrated to typed ManagementSection.

    Risk domain:
        Migrated to typed RiskSection.

    Competitive domain:
        Migrated to typed CompetitiveSection.

    Other domains:
        Legacy interfaces temporarily preserved until their respective
        migration sprints are completed.

Author:
    EIOS

Release:
    2.4
===============================================================================
"""

from modules.master_dossier.business_section import BusinessSection
from modules.master_dossier.financial_section import FinancialSection
from modules.master_dossier.management_section import ManagementSection
from modules.master_dossier.risk_section import RiskSection
from modules.master_dossier.competitive_section import CompetitiveSection
from modules.master_dossier.valuation_section import ValuationSection

from modules.research_context.research_context import ResearchContext
from modules.master_dossier.decision_section import DecisionSection
from modules.master_dossier.committee_section import CommitteeSection
from modules.master_dossier.ownership_section import OwnershipSection
class CompanyResearch:
    """
    Coordinates research updates into the Master Dossier.

    This class is an application-layer bridge between research engines
    and the domain model.

    It must not perform business, financial, valuation, management,
    risk, competitive, or other analytical calculations.
    """

    def __init__(self, context: ResearchContext):
        self.context = context

    # =========================================================================
    # Master Dossier Access
    # =========================================================================

    @property
    def dossier(self):
        """
        Return the Master Dossier owned by the ResearchContext.
        """
        return self.context.get_master_dossier()

    @property
    def master_dossier(self):
        """
        Explicit Master Dossier accessor.
        """
        return self.context.get_master_dossier()

    # =========================================================================
    # Business Quality
    # =========================================================================

    def update_business_quality(
        self,
        business: BusinessSection,
    ) -> None:

        if not isinstance(business, BusinessSection):
            raise TypeError(
                "CompanyResearch.update_business_quality() requires "
                "BusinessSection; received "
                f"{type(business).__name__}."
            )

        self.dossier.business = business

    # =========================================================================
    # Management
    # =========================================================================

    def update_management(
        self,
        management: ManagementSection,
    ) -> None:

        if not isinstance(management, ManagementSection):
            raise TypeError(
                "CompanyResearch.update_management() requires "
                "ManagementSection; received "
                f"{type(management).__name__}."
            )

        self.dossier.management = management

    # =========================================================================
    # Financial
    # =========================================================================

    def update_financials(
        self,
        financial: FinancialSection,
    ) -> None:

        if not isinstance(financial, FinancialSection):
            raise TypeError(
                "CompanyResearch.update_financials() requires "
                "FinancialSection; received "
                f"{type(financial).__name__}."
            )

        self.dossier.financial = financial
        # =========================================================================
    # Ownership
    # =========================================================================

    def update_ownership(
        self,
        ownership: OwnershipSection,
    ) -> None:

        if not isinstance(ownership, OwnershipSection):
            raise TypeError(
                "CompanyResearch.update_ownership() requires "
                "OwnershipSection; received "
                f"{type(ownership).__name__}."
            )

        self.dossier.ownership = ownership

    # =========================================================================
    # Risk
    # =========================================================================

    def update_risk(
        self,
        risk: RiskSection,
    ) -> None:

        if not isinstance(risk, RiskSection):
            raise TypeError(
                "CompanyResearch.update_risk() requires "
                "RiskSection; received "
                f"{type(risk).__name__}."
            )

        self.dossier.risk = risk

    # =========================================================================
    # Competitive Intelligence
    # =========================================================================

    def update_competitive(
        self,
        competitive: CompetitiveSection,
    ) -> None:

        if not isinstance(competitive, CompetitiveSection):
            raise TypeError(
                "CompanyResearch.update_competitive() requires "
                "CompetitiveSection; received "
                f"{type(competitive).__name__}."
            )

        self.dossier.competitive = competitive

    # =========================================================================
    # Thesis
    # =========================================================================

    def update_thesis(self, data: dict):
        """
        Legacy thesis update interface.
        """
        self.dossier.thesis = data

    # =========================================================================
    # Investment Committee
    # =========================================================================

        # =========================================================================
    # Investment Committee
    # =========================================================================

    def update_committee(
        self,
        committee: CommitteeSection,
    ) -> None:

        if not isinstance(committee, CommitteeSection):
            raise TypeError(
                "CompanyResearch.update_committee() requires "
                "CommitteeSection; received "
                f"{type(committee).__name__}."
            )

        self.dossier.committee = committee

    # =========================================================================
    # Valuation
    # =========================================================================

    def update_valuation(
        self,
        valuation: ValuationSection,
    ) -> None:

        if not isinstance(valuation, ValuationSection):
            raise TypeError(
                "CompanyResearch.update_valuation() requires "
                "ValuationSection; received "
                f"{type(valuation).__name__}."
            )

        self.dossier.valuation = valuation
    # =========================================================================
    # Decision Office
    # =========================================================================

    def update_decision(
        self,
        decision: DecisionSection,
    ) -> None:

        if not isinstance(decision, DecisionSection):
            raise TypeError(
                "CompanyResearch.update_decision() requires "
                "DecisionSection; received "
                f"{type(decision).__name__}."
            )

        self.dossier.decision = decision
    # =========================================================================
    # Evidence
    # =========================================================================

    def add_evidence(self, evidence):
        """
        Add evidence to the Master Dossier.
        """
        self.dossier.evidence.add(evidence)

    # =========================================================================
    # Summary
    # =========================================================================

    def summary(self):
        """
        Return the serialized Master Dossier.
        """
        return self.dossier.to_dict()