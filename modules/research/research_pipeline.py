"""
EIOS
Everest Investment Operating System

Research Pipeline

Purpose:
Coordinates the complete institutional research workflow.

Architecture:

Research Pipeline
        ↓
Kill Switch
        ↓
Question Engine
        ↓
Research Orchestrator
        ↓
Analysis Pack
        ↓
Analysis Pack Processor
        ↓
Company Research
        ↓
Master Dossier

The pipeline performs workflow orchestration only.

It performs NO business calculations.

Author:
EIOS
"""

from modules.research.kill_switch import KillSwitchEngine
from modules.research.question_engine import QuestionEngine
from modules.research.research_orchestrator import ResearchOrchestrator
from modules.research.analysis_pack_processor import AnalysisPackProcessor


class ResearchPipeline:
    """
    Coordinates the complete institutional research workflow.

    Responsibilities:

    - Execute Kill Switch
    - Generate Research Questions
    - Run ResearchOrchestrator
    - Receive immutable AnalysisPack
    - Pass AnalysisPack to AnalysisPackProcessor

    No domain calculations or persistence are performed here.
    """

    def __init__(self, research):

        self.research = research

        # ==========================================================
        # Core Pipeline Services
        # ==========================================================

        self.kill_switch = KillSwitchEngine()

        self.question_engine = QuestionEngine()

        self.orchestrator = ResearchOrchestrator(
            research
        )

        self.processor = AnalysisPackProcessor(
            research
        )

    # ==============================================================
    # EXECUTE
    # ==============================================================

    def execute(
        self,
        company,
        financial_data,
        ownership_data,
        management_data,
        risk_data,
        business_data,
        peers=None,
    ):
        """
        Execute the complete institutional research pipeline.

        Parameters
        ----------
        company:
            Company object being researched.

        financial_data:
            Financial inputs required by FinancialEngine
            and ValuationEngine.

        ownership_data:
            Ownership inputs required by TypedOwnershipEngine.

        management_data:
            Management inputs required by ManagementEngine.

        risk_data:
            Risk inputs required by RiskEngine.

        peers:
            Optional list of Peer objects used by
            CompetitiveEngine.

        Returns
        -------
        CompanyResearch
            Updated research object after AnalysisPack
            processing.
        """

        print()
        print("=" * 60)
        print("RESEARCH PIPELINE")
        print("=" * 60)

        # ==========================================================
        # STAGE 1
        # KILL SWITCH
        # ==========================================================

        result = self.kill_switch.evaluate(
            tam=True,
            moat=True,
            management=True,
            financial_quality=True,
            customer_concentration=True,
        )

        if not result.passed:

            print()
            print("Research Terminated")

            for failure in result.failed_checks:
                print(f" - {failure}")

            return None

        print("Kill Switch : PASS")

        # ==========================================================
        # STAGE 2
        # RESEARCH QUESTIONS
        # ==========================================================

        self.question_engine.add(
            "Is the business easy to understand?",
            10,
        )

        self.question_engine.add(
            "Does it have pricing power?",
            15,
        )

        self.question_engine.add(
            "Does it have a durable moat?",
            20,
        )

        self.question_engine.show()

        print()

        print(
            f"Business Quality Weight : "
            f"{self.question_engine.total_weight()}"
        )

        # ==========================================================
        # STAGE 3
        # INSTITUTIONAL RESEARCH
        # ==========================================================

        print()
        print("=" * 60)
        print("INSTITUTIONAL RESEARCH")
        print("=" * 60)

        analysis_pack = self.orchestrator.analyze(
            company=company,
            financial_data=financial_data,
            ownership_data=ownership_data,
            management_data=management_data,
            risk_data=risk_data,
            business_data=business_data,
            peers=peers,
        )

        # ==========================================================
        # STAGE 4
        # PERSIST RESEARCH
        # ==========================================================

        self.processor.process(
            analysis_pack
        )

        print()
        print("Analysis Pack Successfully Processed.")

        return self.research