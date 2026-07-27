"""
EIOS
Everest Investment Operating System

Valuation Engine

Coordinates all valuation models and updates CompanyResearch.

Architecture:
- Owner Earnings is executed independently.
- Valuation methods are executed through the Valuation Registry.
- Intrinsic Value Office consolidates intrinsic valuation outputs.
- New valuation engines require only registration.
"""

from modules.research.company_research import CompanyResearch

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

    Owner Earnings is treated as an operating cash-flow analysis.

    Intrinsic valuation methods execute through the
    Valuation Registry.

    The Intrinsic Value Office combines completed valuation
    outputs into a single institutional intrinsic value estimate.
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        # -----------------------------------------------------
        # Owner Earnings (not an intrinsic valuation method)
        # -----------------------------------------------------

        self.owner_earnings = OwnerEarningsEngine()

        # -----------------------------------------------------
        # Valuation Registry
        # -----------------------------------------------------

        self.registry = ValuationRegistry()

        self.registry.register(DCFEngine())
        self.registry.register(EPVEngine())

        # -----------------------------------------------------
        # Intrinsic Value Office
        # -----------------------------------------------------

        self.intrinsic_value_office = IntrinsicValueOffice()

        # -----------------------------------------------------
        # Shared Scoring
        # -----------------------------------------------------

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def analyze(self, financial_data: dict):

        print("\nStarting Valuation Analysis...")

        valuation_summary = {}

        # =====================================================
        # OWNER EARNINGS
        # =====================================================

        valuation_summary["Owner Earnings"] = (
            self.owner_earnings.evaluate(financial_data)
        )

        # =====================================================
        # FETCH VALUATION ASSUMPTIONS
        # =====================================================

        financial_summary = (
            self.research.master_dossier.financials
        )

        valuation_assumptions = financial_summary.get(
            "Valuation Assumptions",
            {}
        )

        # =====================================================
        # EXECUTE REGISTERED VALUATION ENGINES
        # =====================================================

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

        # =====================================================
        # INTRINSIC VALUE OFFICE
        # =====================================================

        intrinsic_value = (
            self.intrinsic_value_office.evaluate(
                valuation_summary
            )
        )

        valuation_summary[
            "Intrinsic Value"
        ] = intrinsic_value

        # =====================================================
        # UPDATE MASTER DOSSIER
        # =====================================================

        self.research.update_valuation(
            valuation_summary
        )

        # =====================================================
        # VALUATION OVERALL SCORE
        # =====================================================

        # Temporary institutional score.
        # Sprint 18 will replace this with an evidence-driven
        # valuation assessment engine.

        score_result = self.scoring_engine.calculate(
            score=80,
            max_score=100,
        )

        self.research.dossier.valuation["Overall Score"] = {
            "Overall Score": score_result.percentage,
            "Raw Score": score_result.score,
            "Maximum Score": score_result.max_score,
            "Confidence": 85.0,
            "Rating": score_result.grade,
        }

        print("Valuation Analysis Completed")

        return valuation_summary