"""
EIOS
Everest Investment Operating System

Valuation Engine

Coordinates all valuation models and produces the typed
ValuationSection.
"""

from modules.research.company_research import CompanyResearch
from modules.master_dossier.valuation_section import ValuationSection

from modules.valuation.owners_earnings import OwnerEarningsEngine
from modules.valuation.dcf_engine import DCFEngine
from modules.valuation.epv_engine import EPVEngine

from modules.valuation.valuation_registry import (
    ValuationRegistry,
)

from modules.valuation.intrinsic_value_office import (
    IntrinsicValueOffice,
)

from modules.core.scoring.scoring_engine import (
    ScoringEngine,
)

from modules.core.scoring.confidence_engine import (
    ConfidenceEngine,
)


class ValuationEngine:
    """
    Coordinates all institutional valuation models.
    """

    def __init__(
        self,
        research: CompanyResearch,
    ):

        self.research = research

        # ======================================================
        # Valuation Models
        # ======================================================

        self.owner_earnings = OwnerEarningsEngine()

        self.registry = ValuationRegistry()
        self.registry.register(DCFEngine())
        self.registry.register(EPVEngine())

        # ======================================================
        # Institutional Offices
        # ======================================================

        self.intrinsic_value_office = (
            IntrinsicValueOffice()
        )

        # ======================================================
        # Scoring
        # ======================================================

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    # ==========================================================
    # Analysis
    # ==========================================================

    def analyze(
        self,
        financial_data: dict,
    ) -> ValuationSection:

        print("\nStarting Valuation Analysis...")

        valuation = ValuationSection()

        valuation_summary = {}

        # ======================================================
        # Owner Earnings
        # ======================================================

        owner_result = self.owner_earnings.evaluate(
            financial_data
        )

        valuation_summary["Owner Earnings"] = owner_result

        # ======================================================
        # Retrieve typed financial section
        # ======================================================

        financial = self.research.master_dossier.financial

        valuation_assumptions = (
            financial.metadata.get(
                "valuation_assumptions",
                {},
            )
        )

        if not isinstance(
            valuation_assumptions,
            dict,
        ):
            raise TypeError(
                "valuation_assumptions must be a dictionary."
            )
                    # ======================================================
        # Execute Registered Valuation Engines
        # ======================================================

        for engine in self.registry:

            assumptions = valuation_assumptions.get(
                engine.ASSUMPTION_KEY
            )

            if assumptions is None:
                continue

            result = engine.evaluate(
                assumptions
            )

            valuation_summary[
                engine.METHOD_NAME
            ] = result

        # ======================================================
        # Intrinsic Value Office
        # ======================================================

        intrinsic = (
            self.intrinsic_value_office.evaluate(
                valuation_summary
            )
        )

        valuation.intrinsic_value = (
            intrinsic.fair_value
        )

        valuation.fair_value = (
            intrinsic.fair_value
        )

        valuation.valuation_method = (
            intrinsic.primary_method
        )

        valuation.assumptions = [
            "DCF assumptions supplied by FinancialEngine.",
            "EPV assumptions supplied by FinancialEngine.",
            "Owner Earnings included in weighted valuation.",
        ]

        valuation.notes = [
            intrinsic.summary
        ]

        valuation.metadata = {
            "valuation_summary": valuation_summary,
            "intrinsic_value_result": intrinsic,
        }

        # ======================================================
        # Institutional Scoring
        # ======================================================

        score = self.scoring_engine.calculate(
            score=80,
            max_score=100,
        )

        confidence = (
            self.confidence_engine.calculate(
                evidence_items=len(
                    valuation_summary
                ),
                expected_items=3,
            )
        )

        valuation.score = score.percentage
        valuation.rating = score.grade
        valuation.confidence = (
            confidence.confidence
        )

        valuation.summary = (
            "Institutional valuation completed successfully."
        )

        valuation.source = "ValuationEngine"

        valuation.evidence = list(
            valuation_summary.keys()
        )

        print(
            f"Intrinsic Value = {valuation.intrinsic_value}"
        )

        print("Valuation Analysis Completed")

        return valuation