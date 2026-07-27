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


class RiskEngine:

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

    def analyze(self, risk_data: dict):

        print("\nStarting Risk Analysis...")

        business = self.business.evaluate(risk_data)
        financial = self.financial.evaluate(risk_data)
        governance = self.governance.evaluate(risk_data)
        industry = self.industry.evaluate(risk_data)
        macro = self.macro.evaluate(risk_data)
        scenario = self.scenario.evaluate(risk_data)

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

        risk_summary = {
            "Business Risk": business,
            "Financial Risk": financial,
            "Governance Risk": governance,
            "Industry Risk": industry,
            "Macro Risk": macro,
            "Scenario Analysis": scenario,
            "Overall Risk": {
                "Overall Score": score_result.percentage,
                "Raw Score": score_result.score,
                "Maximum Score": score_result.max_score,
                "Confidence": overall["Confidence"],
                "Rating": score_result.grade,
            },
        }

        self.research.update_risk(risk_summary)

        # =====================================================
        # OVERALL RISK SCORE
        # =====================================================

        self.research.dossier.risks["Overall Risk"] = {
            "Overall Score": score_result.percentage,
            "Raw Score": score_result.score,
            "Maximum Score": score_result.max_score,
            "Confidence": overall["Confidence"],
            "Rating": score_result.grade,
        }

        print("Risk Analysis Completed")