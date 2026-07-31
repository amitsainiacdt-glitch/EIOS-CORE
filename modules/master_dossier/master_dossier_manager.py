"""
===============================================================================
EIOS
Master Dossier Manager

Purpose:
    Central write gateway for updating the Master Dossier.

    All Research Engines update the dossier through this manager.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from .master_dossier import MasterDossier
from .section_updater import SectionUpdater


class MasterDossierManager:
    """
    Central manager responsible for updating the Master Dossier.
    """

    def __init__(self, dossier: MasterDossier):
        self.dossier = dossier

    # ==========================================================
    # Business
    # ==========================================================

    def update_business(self, analysis):
        SectionUpdater.update(self.dossier.business, analysis)

    # ==========================================================
    # Financial
    # ==========================================================

    def update_financial(self, analysis):
        SectionUpdater.update(self.dossier.financial, analysis)

    # ==========================================================
    # Management
    # ==========================================================

    def update_management(self, analysis):
        SectionUpdater.update(self.dossier.management, analysis)

    # ==========================================================
    # Ownership
    # ==========================================================

    def update_ownership(self, analysis):
        SectionUpdater.update(self.dossier.ownership, analysis)

    # ==========================================================
    # Competitive
    # ==========================================================

    def update_competitive(self, analysis):
        SectionUpdater.update(self.dossier.competitive, analysis)

    # ==========================================================
    # Risk
    # ==========================================================

    def update_risk(self, analysis):
        SectionUpdater.update(self.dossier.risk, analysis)

    # ==========================================================
    # Valuation
    # ==========================================================

    def update_valuation(self, analysis):
        SectionUpdater.update(self.dossier.valuation, analysis)

    # ==========================================================
    # Macro
    # ==========================================================

    def update_macro(self, analysis):
        SectionUpdater.update(self.dossier.macro, analysis)

    # ==========================================================
    # Committee
    # ==========================================================

    def update_committee(self, analysis):
        SectionUpdater.update(self.dossier.committee, analysis)

    # ==========================================================
    # Utility
    # ==========================================================

    def get_dossier(self) -> MasterDossier:
        """
        Return the current Master Dossier.
        """
        return self.dossier