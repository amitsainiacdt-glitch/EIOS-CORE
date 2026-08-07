"""
===============================================================================
EIOS
Everest Investment Operating System

Valuation Engine

Purpose:
    Coordinates all valuation models and produces the typed
    ValuationSection.

Architecture:

FinancialSection
        ↓
Owner Earnings
        ↓
Valuation Registry
        ↓
Intrinsic Value Office
        ↓
ValuationSection
        ↓
AnalysisPack
        ↓
AnalysisPackProcessor
        ↓
CompanyResearch

Rules:
    - All calculations remain inside valuation engines.
    - ValuationSection is a passive data model.
    - No persistence occurs inside this engine.
    - AnalysisPackProcessor is the only persistence layer.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.research.company_research import CompanyResearch
from modules.master_dossier.valuation_section import ValuationSection

from modules.valuation.owners_earnings import OwnerEarningsEngine
from modules.valuation.dcf_engine import DCFEngine
from modules.valuation.epv_engine import EPVEngine

from modules.valuation.valuation_registry import ValuationRegistry
from modules.valuation.intrinsic_value_office import IntrinsicValueOffice

from modules.core.scoring.scoring_engine import ScoringEngine
from modules.core.scoring.confidence_engine import ConfidenceEngine


class ValuationEngine:
    """
    Coordinates all valuation models.
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        self.owner_earnings = OwnerEarningsEngine()

        self.registry = ValuationRegistry()

        self.registry.register(DCFEngine())
        self.registry.register(EPVEngine())

        self.intrinsic_value_office = IntrinsicValueOffice()

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def analyze(self, financial_data: dict) -> ValuationSection:

        print("\nStarting Valuation Analysis...")

        valuation_summary = {}
        valuation = ValuationSection()

        # ==========================================================
        # OWNER EARNINGS
        # ==========================================================

        valuation_summary["Owner Earnings"] = (
            self.owner_earnings.evaluate(financial_data)
        )

        # ==========================================================
        # FETCH TYPED FINANCIAL STATE
        # ==========================================================

        financial = self.research.master_dossier.financial

        # ==========================================================
        # FETCH VALUATION ASSUMPTIONS
        # ==========================================================

        valuation_assumptions = financial.metadata.get(
            "valuation_assumptions",
            {},
        )

        if not isinstance(valuation_assumptions, dict):
            raise TypeError(
                "FinancialSection.metadata['valuation_assumptions'] "
                "must contain a dictionary during migration."
            )

        # ==========================================================
        # EXECUTE REGISTERED ENGINES
        # ==========================================================

        for engine in self.registry:

            assumptions = valuation_assumptions.get(
                engine.ASSUMPTION_KEY
            )

            if assumptions:

                valuation_summary[
                    engine.METHOD_NAME
                ] = engine.evaluate(
                    assumptions
                )

        # ==========================================================
        # INTRINSIC VALUE OFFICE
        # ==========================================================

        intrinsic_value = (
            self.intrinsic_value_office.evaluate(
                valuation_summary
            )
        )

        valuation_summary[
            "Intrinsic Value"
        ] = intrinsic_value

        # ==========================================================
        # BUILD TYPED VALUATION SECTION
        # ==========================================================

        valuation.intrinsic_value = intrinsic_value.fair_value
        valuation.fair_value = intrinsic_value.fair_value

        valuation.valuation_method = (
            "Intrinsic Value Office"
        )

        # ==========================================================
        # Institutional Score
        # ==========================================================

        score_result = self.scoring_engine.calculate(
            score=80,
            max_score=100,
        )

        confidence_result = (
            self.confidence_engine.calculate(
                evidence_items=3,
                expected_items=5,
            )
        )

        valuation.score = score_result.percentage
        valuation.confidence = confidence_result.confidence
        valuation.rating = score_result.grade

        valuation.summary = (
            "Intrinsic valuation completed successfully."
        )

        valuation.evidence = [
            "Owner Earnings",
            "DCF",
            "EPV",
            "Intrinsic Value Office",
        ]

        valuation.assumptions = [
            "Financial assumptions remain valid."
        ]

        valuation.source = "ValuationEngine"

        valuation.metadata = {
            "valuation_summary": valuation_summary,
        }

        # ==========================================================
        # Release 3.0
        #
        # No persistence.
        #
        # AnalysisPackProcessor will call:
        #
        #     update_valuation()
        #
        # ==========================================================

        print("Valuation Analysis Completed")

        return valuationpython -m py_compile modules\valuation\valuation_engine.py
    