"""
Company Research

Acts as the central coordinator for all research modules.
"""

from modules.research_context.research_context import ResearchContext


class CompanyResearch:

    def __init__(self, context: ResearchContext):
        self.context = context

    # ---------------------------------------------------------
    # Backward Compatibility
    # ---------------------------------------------------------

    @property
    def dossier(self):
        return self.context.get_master_dossier()

    @property
    def master_dossier(self):
        return self.context.get_master_dossier()

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
    # Decision Office
    # ---------------------------------------------------------

    def update_decision(self, data: dict):
        self.dossier.decision = data

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