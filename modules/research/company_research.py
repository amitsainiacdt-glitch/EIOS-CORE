"""
Company Research

Acts as the central coordinator for all research modules.
"""

from modules.master_dossier.master_dossier import MasterDossier


class CompanyResearch:

    def __init__(self, dossier: MasterDossier):
        self.dossier = dossier
        self.master_dossier = dossier

    # ---------------------------------------------------------
    # Business Quality
    # ---------------------------------------------------------

    def update_business_quality(self, data: dict):
        self.dossier.business_quality = data

    # ---------------------------------------------------------
    # Management
    # ---------------------------------------------------------

    def update_management(self, data: dict):
        self.dossier.management = data

    # ---------------------------------------------------------
    # Thesis
    # ---------------------------------------------------------

    def update_thesis(self, data: dict):
        self.dossier.thesis = data

    # ---------------------------------------------------------
    # Investment Committee
    # ---------------------------------------------------------

    def update_committee(self, data: dict):
        self.dossier.committee = data

    # ---------------------------------------------------------
    # Financials
    # ---------------------------------------------------------

    def update_financials(self, data: dict):
        self.dossier.financials = data

    # ---------------------------------------------------------
    # Competitive Intelligence
    # ---------------------------------------------------------

    def update_competitive(self, data: dict):
        self.dossier.competitive = data

    # ---------------------------------------------------------
    # Valuation
    # ---------------------------------------------------------

    def update_valuation(self, data: dict):
        self.dossier.valuation = data

    # ---------------------------------------------------------
    # Risks
    # ---------------------------------------------------------

    def update_risk(self, data: dict):
        self.dossier.risks = data

    # ---------------------------------------------------------
    # Evidence
    # ---------------------------------------------------------

    def add_evidence(self, evidence):
        self.dossier.evidence.add(evidence)

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):
        return self.dossier.to_dict()