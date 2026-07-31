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

    Other domains:
        Legacy interfaces temporarily preserved until their respective
        migration sprints are completed.

Author:
    EIOS

Release:
    2.2
===============================================================================
"""

from modules.master_dossier.business_section import BusinessSection
from modules.master_dossier.financial_section import FinancialSection
from modules.master_dossier.management_section import ManagementSection
from modules.research_context.research_context import ResearchContext


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

        Retained as an access alias while downstream modules are migrated
        to the typed Master Dossier architecture.
        """
        return self.context.get_master_dossier()

    @property
    def master_dossier(self):
        """
        Explicit Master Dossier accessor.

        Existing EIOS modules may currently use either this property
        or ``dossier``.
        """
        return self.context.get_master_dossier()

    # =========================================================================
    # Business Quality
    # =========================================================================

    def update_business_quality(
        self,
        business: BusinessSection,
    ) -> None:
        """
        Store typed business-quality intelligence in the Master Dossier.

        BusinessSection is the authoritative persistent state for the
        Business domain. No legacy business-quality dictionary is created
        or persisted here.

        Args:
            business:
                Fully populated BusinessSection produced by the
                BusinessQualityEngine.

        Raises:
            TypeError:
                If a legacy dictionary or any object other than
                BusinessSection is submitted.
        """

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
        """
        Store typed management intelligence in the Master Dossier.

        ManagementSection is the authoritative persistent state for the
        Management domain. No legacy management dictionary is created
        or persisted here.

        Args:
            management:
                Fully populated ManagementSection produced by the
                ManagementEngine.

        Raises:
            TypeError:
                If a legacy dictionary or any object other than
                ManagementSection is submitted.
        """

        if not isinstance(management, ManagementSection):
            raise TypeError(
                "CompanyResearch.update_management() requires "
                "ManagementSection; received "
                f"{type(management).__name__}."
            )

        self.dossier.management = management

    # =========================================================================
    # Thesis
    # =========================================================================

    def update_thesis(self, data: dict):
        """
        Legacy thesis update interface.

        Preserved until the thesis domain is migrated.
        """
        self.dossier.thesis = data

    # =========================================================================
    # Investment Committee
    # =========================================================================

    def update_committee(self, data: dict):
        """
        Legacy Investment Committee update interface.

        Preserved until CommitteeSection becomes the authoritative
        committee domain model.
        """
        self.dossier.committee = data

    # =========================================================================
    # Financial
    # =========================================================================

    def update_financials(
        self,
        financial: FinancialSection,
    ) -> None:
        """
        Store typed financial intelligence in the Master Dossier.

        FinancialSection is the authoritative financial domain state.
        No legacy financial dictionary is created or persisted here.

        Args:
            financial:
                Fully populated FinancialSection produced by the
                FinancialEngine.

        Raises:
            TypeError:
                If a legacy dictionary or any object other than
                FinancialSection is submitted.
        """

        if not isinstance(financial, FinancialSection):
            raise TypeError(
                "CompanyResearch.update_financials() requires "
                "FinancialSection; received "
                f"{type(financial).__name__}."
            )

        self.dossier.financial = financial

    # =========================================================================
    # Competitive Intelligence
    # =========================================================================

    def update_competitive(self, data: dict):
        """
        Legacy competitive-intelligence update interface.

        Preserved until CompetitiveSection migration.
        """
        self.dossier.competitive = data

    # =========================================================================
    # Valuation
    # =========================================================================

    def update_valuation(self, data: dict):
        """
        Legacy valuation update interface.

        Preserved until ValuationSection migration.
        """
        self.dossier.valuation = data

    # =========================================================================
    # Decision Office
    # =========================================================================

    def update_decision(self, data: dict):
        """
        Legacy Decision Office update interface.

        Preserved until Decision Intelligence migration.
        """
        self.dossier.decision = data

    # =========================================================================
    # Risk
    # =========================================================================

    def update_risk(self, data: dict):
        """
        Legacy risk update interface.

        Preserved until RiskSection migration.
        """
        self.dossier.risks = data

    # =========================================================================
    # Evidence
    # =========================================================================

    def add_evidence(self, evidence):
        """
        Add an evidence object to the Master Dossier evidence library.
        """
        self.dossier.evidence.add(evidence)

    # =========================================================================
    # Summary
    # =========================================================================

    def summary(self):
        """
        Return the complete serialized Master Dossier.
        """
        return self.dossier.to_dict()