"""
EIOS
Application Factory

Creates all application level objects.

Author:
EIOS
"""

from modules.master_dossier.master_dossier import MasterDossier
from modules.research_context.research_context import ResearchContext
from modules.research.company_research import CompanyResearch


class ApplicationFactory:

    @staticmethod
    def create_research(company):

        dossier = MasterDossier(
            company_name=company.name,
            ticker=company.ticker,
            sector=company.sector,
            industry=company.industry,
        )

        context = ResearchContext()

        context.set_master_dossier(dossier)

        research = CompanyResearch(context)

        return research

