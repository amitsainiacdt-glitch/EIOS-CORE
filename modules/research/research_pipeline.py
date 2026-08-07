"""
EIOS
Everest Investment Operating System

Research Pipeline

Purpose
-------
Coordinates the complete institutional research workflow.

Architecture

Research Pipeline
        │
        ▼
Kill Switch
        │
        ▼
Question Engine
        │
        ▼
Research Orchestrator
        │
        ▼
Analysis Pack
        │
        ▼
Analysis Pack Processor
        │
        ▼
Company Research
        │
        ▼
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

    def __init__(self, research):

        self.research = research

        self.kill_switch = KillSwitchEngine()

        self.question_engine = QuestionEngine()

        self.orchestrator = ResearchOrchestrator(
            research
        )

        self.processor = AnalysisPackProcessor(
            research
        )

    # ==========================================================
    # Execute
    # ==========================================================

    def execute(self, company):

        print()
        print("=" * 60)
        print("RESEARCH PIPELINE")
        print("=" * 60)

        # ======================================================
        # Stage 1
        # Kill Switch
        # ======================================================

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

        # ======================================================
        # Stage 2
        # Research Questions
        # ======================================================

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

        # ======================================================
        # Stage 3
        # Institutional Research
        # ======================================================

        print()
        print("=" * 60)
        print("INSTITUTIONAL RESEARCH")
        print("=" * 60)

        analysis_pack = self.orchestrator.analyze(
            company
        )

        # ======================================================
        # Stage 4
        # Persist Research
        # ======================================================

        self.processor.process(
            analysis_pack
        )

        print()

        print("Analysis Pack Successfully Processed.")

        return self.research