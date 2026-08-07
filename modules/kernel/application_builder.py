"""
EIOS
Application Builder

Constructs all objects required to execute
institutional research.

Author:
EIOS
"""

from modules.kernel.application_factory import ApplicationFactory
from modules.research.research_pipeline import ResearchPipeline


class ApplicationBuilder:

    def __init__(self):
        pass

    def build(self, company):

        research = ApplicationFactory.create_research(
            company
        )

        pipeline = ResearchPipeline(
            research
        )

        return {
            "research": research,
            "pipeline": pipeline,
            "dossier": research.dossier,
        }

