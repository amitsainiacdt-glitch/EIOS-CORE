"""
===============================================================================
EIOS
Everest Investment Operating System

Valuation Engine

Purpose:
    Coordinates all valuation models and updates CompanyResearch.

Architecture:
    - Owner Earnings is executed independently.
    - Valuation methods execute through the Valuation Registry.
    - Intrinsic Value Office consolidates intrinsic valuation outputs.
    - Financial inputs are consumed from MasterDossier.financial.
    - New valuation engines require only registration.

Migration Status:
    Financial input:
        Migrated to typed FinancialSection.

    Valuation output:
        Legacy valuation dictionary temporarily preserved until the
        ValuationSection migration sprint.

Author:
    EIOS

Release:
    2.0
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

    Financial intelligence is consumed from the typed
    MasterDossier.financial section.

    Valuation output remains on the legacy valuation interface until
    ValuationSection receives its dedicated migration sprint.
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        # ---------------------------------------------------------------------
        # Owner Earnings
        # ---------------------------------------------------------------------

        self.owner_earnings = OwnerEarningsEngine()

        # ---------------------------------------------------------------------
        # Valuation Registry
        # ---------------------------------------------------------------------

        self.registry = ValuationRegistry()

        self.registry.register(DCFEngine())
        self.registry.register(EPVEngine())

        # ---------------------------------------------------------------------
        # Intrinsic Value Office
        # ---------------------------------------------------------------------

        self.intrinsic_value_office = IntrinsicValueOffice()

        # ---------------------------------------------------------------------
        # Shared Scoring
        # ---------------------------------------------------------------------

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def analyze(self, financial_data: dict):

        print("\nStarting Valuation Analysis...")

        valuation_summary = {}
        valuation = ValuationSection()

        # =====================================================================
        # OWNER EARNINGS
        # =====================================================================

        valuation_summary["Owner Earnings"] = (
            self.owner_earnings.evaluate(financial_data)
        )

        # =====================================================================
        # FETCH TYPED FINANCIAL STATE
        # =====================================================================

        financial = self.research.master_dossier.financial

        # =====================================================================
        # FETCH VALUATION ASSUMPTIONS
        #
        # FinancialEngine V2 currently places valuation assumptions inside
        # FinancialSection.metadata as a controlled migration bridge.
        #
        # This avoids restoring the legacy dossier.financials dictionary.
        # The bridge will be removed when valuation assumptions receive a
        # dedicated typed domain model.
        # =====================================================================

        valuation_assumptions = financial.metadata.get(
            "valuation_assumptions",
            {},
        )

        if not isinstance(valuation_assumptions, dict):
            raise TypeError(
                "FinancialSection.metadata['valuation_assumptions'] "
                "must contain a dictionary during the migration phase."
            )

        # =====================================================================
        # EXECUTE REGISTERED VALUATION ENGINES
        # =====================================================================

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

        # =====================================================================
        # INTRINSIC VALUE OFFICE
        # =====================================================================

        intrinsic_value = (
            self.intrinsic_value_office.evaluate(
                valuation_summary
            )
        )
        print("\n========== INTRINSIC VALUE DEBUG ==========")
        print(intrinsic_value)
        print(type(intrinsic_value))

        if hasattr(intrinsic_value, "__dict__"):
            print(intrinsic_value.__dict__)

        print("===========================================")

        valuation_summary[
            "Intrinsic Value"
        ] = intrinsic_value
        # =====================================================
        # BUILD TYPED VALUATION SECTION
        # =====================================================

        valuation.intrinsic_value = intrinsic_value.fair_value
        valuation.fair_value = intrinsic_value.fair_value
        valuation.valuation_method = "Intrinsic Value Office"

        valuation.score = 80.0
        valuation.confidence = 85.0
        valuation.rating = "A"

        # =====================================================================
        # UPDATE MASTER DOSSIER
        # =====================================================================

        self.research.update_valuation(
            valuation
        )
        print("\n===== DOSSIER AFTER UPDATE =====")
        print("valuation.fair_value =", self.research.dossier.valuation.fair_value)
        print("valuation.intrinsic_value =", self.research.dossier.valuation.intrinsic_value)
        print("===============================")

        # =====================================================================
        # VALUATION OVERALL SCORE
        # =====================================================================

        score_result = self.scoring_engine.calculate(
            score=80,
            max_score=100,
        )

        valuation.score = score_result.percentage
        valuation.confidence = 85.0
        valuation.rating = score_result.grade

        
        print("Valuation Analysis Completed")

        return valuation_summary