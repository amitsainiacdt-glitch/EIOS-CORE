"""
===============================================================================
EIOS
Everest Investment Operating System

Research Pipeline

Purpose:
    Executes the complete institutional research workflow.

Architecture:

ResearchPipeline
        ↓
ResearchOrchestrator
        ↓
AnalysisPack
        ↓
AnalysisPackProcessor
        ↓
CompanyResearch

Release:
    3.0
===============================================================================
"""

from modules.research.research_orchestrator import (
    ResearchOrchestrator,
)
from modules.research.analysis_pack_processor import (
    AnalysisPackProcessor,
)
from modules.research.company_research import (
    CompanyResearch,
)


class ResearchPipeline:
    """
    Executes the complete EIOS research pipeline.

    Responsibilities
    ----------------
    • Execute all research engines
    • Build AnalysisPack
    • Persist typed sections
    • Return completed AnalysisPack
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        self.orchestrator = ResearchOrchestrator(
            research
        )

        self.processor = AnalysisPackProcessor(
            research
        )

    def run(self, company):

        print()
        print("=" * 70)
        print("EIOS RESEARCH PIPELINE")
        print("=" * 70)

        # ==========================================================
        # Execute Research
        # ==========================================================

        analysis_pack = self.orchestrator.analyze(
            company
        )

        # ==========================================================
        # Persist Typed Sections
        # ==========================================================

        self.processor.process(
            analysis_pack
        )

        print()
        print("=" * 70)
        print("RESEARCH PIPELINE COMPLETED")
        print("=" * 70)

        return analysis_pack