"""
===============================================================================
EIOS
Everest Investment Operating System

Risk Engine

Purpose:
    Coordinates Risk analysis and produces the typed
    RiskSection.

Architecture:

Specialist Risk Engines
        ↓
RiskScorecard
        ↓
RiskSection
        ↓
AnalysisPack
        ↓
AnalysisPackProcessor
        ↓
CompanyResearch
        ↓
MasterDossier

Rules:
    - Analytical calculations remain inside engines.
    - RiskSection is a passive domain model.
    - Engine never persists data.
    - AnalysisPackProcessor is the only persistence layer.
    - No legacy Risk dictionary is persisted.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from modules.risk.business_risk import BusinessRiskEngine
from modules.risk.financial_risk import FinancialRiskEngine
from modules.risk.governance_risk import GovernanceRiskEngine
from modules.risk.industry_risk import IndustryRiskEngine
from modules.risk.macro_risk import MacroRiskEngine
from modules.risk.scenario_engine import ScenarioEngine
from modules.risk.risk_scorecard import RiskScorecard

from modules.core.scoring.scoring_engine import ScoringEngine
from modules.core.scoring.confidence_engine import ConfidenceEngine

from modules.research.company_research import CompanyResearch
from modules.master_dossier.risk_section import RiskSection

from modules.intelligence.risk_intelligence import RiskIntelligence


class RiskEngine:
    """
    Coordinates Risk analysis and produces typed RiskSection.
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        self.business = BusinessRiskEngine()
        self.financial = FinancialRiskEngine()
        self.governance = GovernanceRiskEngine()
        self.industry = IndustryRiskEngine()
        self.macro = MacroRiskEngine()
        self.scenario = ScenarioEngine()

        self.scorecard = RiskScorecard()

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def analyze(self, risk_data: dict) -> RiskSection:

        print("\nStarting Risk Analysis...")

        # ==========================================================
        # Specialist Risk Analysis
        # ==========================================================

        business = self.business.evaluate(risk_data)
        financial = self.financial.evaluate(risk_data)
        governance = self.governance.evaluate(risk_data)
        industry = self.industry.evaluate(risk_data)
        macro = self.macro.evaluate(risk_data)
        scenario = self.scenario.evaluate(risk_data)

        # ==========================================================
        # Risk Scorecard
        # ==========================================================

        overall = self.scorecard.calculate(
            business,
            financial,
            governance,
            industry,
            macro,
            scenario,
        )

        score_result = self.scoring_engine.calculate(
            score=overall["Raw Score"],
            max_score=overall["Max Score"],
        )

        confidence_result = self.confidence_engine.calculate(
            evidence_items=6,
            expected_items=10,
        )

        # ==========================================================
        # Typed Risk Section
        # ==========================================================

        risk = RiskSection()

        risk.score = score_result.percentage
        risk.confidence = confidence_result.confidence
        risk.rating = score_result.grade

        risk.overall_risk_score = score_result.percentage
        risk.risk_rating = score_result.grade

        risk.summary = (
            "Risk assessment completed across business, financial, "
            "governance, industry, macro and scenario analysis."
        )

        risk.source = "RiskEngine"

        # ==========================================================
        # Risk Categories
        # ==========================================================

        risk.business_risks = [
            business.get("Conclusion", "Business risk evaluated.")
        ]

        risk.financial_risks = [
            financial.get("Conclusion", "Financial risk evaluated.")
        ]

        risk.management_risks = [
            governance.get("Conclusion", "Governance risk evaluated.")
        ]

        risk.industry_risks = [
            industry.get("Conclusion", "Industry risk evaluated.")
        ]

        risk.market_risks = [
            macro.get("Conclusion", "Macro risk evaluated.")
        ]

        risk.watch_items = [
            scenario.get("Conclusion", "Scenario analysis completed.")
        ]

        # ==========================================================
        # Evidence
        # ==========================================================

        risk.evidence = [
            "Business Risk analysis completed.",
            "Financial Risk analysis completed.",
            "Governance Risk analysis completed.",
            "Industry Risk analysis completed.",
            "Macro Risk analysis completed.",
            "Scenario analysis completed.",
        ]

        risk.assumptions = [
            "Risk disclosures remain accurate."
        ]

        risk.metadata = {
            "raw_score": score_result.score,
            "maximum_score": score_result.max_score,
            "business_confidence": business.get("Confidence", 0),
            "financial_confidence": financial.get("Confidence", 0),
            "governance_confidence": governance.get("Confidence", 0),
            "industry_confidence": industry.get("Confidence", 0),
            "macro_confidence": macro.get("Confidence", 0),
            "scenario_confidence": scenario.get("Confidence", 0),
        }

        # ==========================================================
        # Release 3.0
        #
        # No persistence.
        #
        # AnalysisPackProcessor will call:
        #
        #     update_risk()
        #
        # ==========================================================

        risk_intelligence = RiskIntelligence.build(
            self.research,
            confidence_result,
        )

        self.research.context.publish_intelligence(
            risk_intelligence
        )

        print("Risk Analysis Completed")

        return risk