"""
===============================================================================
EIOS
Everest Investment Operating System

Management Engine

Purpose:
    Coordinates Management analysis and produces the typed
    ManagementSection stored in the Master Dossier.

Architecture:
    Specialist Management Engines
        -> ManagementScorecard
        -> ManagementSection
        -> CompanyResearch
        -> MasterDossier.management

Rules:
    - Analytical calculations remain inside engines.
    - ManagementSection is a passive domain model.
    - CompanyResearch only persists completed intelligence.
    - No legacy Management dictionary is persisted.

Author:
    EIOS

Release:
    2.0
===============================================================================
"""

from modules.management.capital_allocation import CapitalAllocationEngine
from modules.management.governance import GovernanceEngine
from modules.management.behaviour import BehaviourEngine
from modules.management.communication import CommunicationEngine
from modules.management.management_scorecard import ManagementScorecard

from modules.research.company_research import CompanyResearch
from modules.master_dossier.management_section import ManagementSection

from modules.core.scoring.scoring_engine import ScoringEngine
from modules.core.scoring.confidence_engine import ConfidenceEngine

from modules.intelligence.management_intelligence import ManagementIntelligence


class ManagementEngine:
    """
    Coordinates Management analysis and publishes typed
    ManagementSection intelligence.
    """

    def __init__(self, research: CompanyResearch):
        self.research = research

        self.capital_allocation = CapitalAllocationEngine()
        self.governance = GovernanceEngine()
        self.behaviour = BehaviourEngine()
        self.communication = CommunicationEngine()
        self.scorecard = ManagementScorecard()

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def analyze(self, management_data: dict) -> ManagementSection:

        print("\nStarting Management Analysis...")

        # =====================================================================
        # Specialist Management Analysis
        # =====================================================================

        capital = self.capital_allocation.evaluate(
            management_data
        )

        governance = self.governance.evaluate(
            management_data
        )

        behaviour = self.behaviour.evaluate(
            management_data
        )

        communication = self.communication.evaluate(
            management_data
        )

        # =====================================================================
        # Management Scorecard
        # =====================================================================

        overall = self.scorecard.calculate(
            capital,
            governance,
            behaviour,
            communication,
        )

        score_result = self.scoring_engine.calculate(
            score=overall["Raw Score"],
            max_score=overall["Max Score"],
        )

        confidence_result = self.confidence_engine.calculate(
            evidence_items=4,
            expected_items=10,
        )

        # =====================================================================
        # Typed Management Section
        # =====================================================================

        management = ManagementSection()

        # ---------------------------------------------------------------------
        # Overall Assessment
        # ---------------------------------------------------------------------

        management.score = score_result.percentage
        management.confidence = confidence_result.confidence
        management.rating = score_result.grade

        management.summary = (
            "Management quality assessment completed across "
            "capital allocation, governance, behaviour, and communication."
        )

        management.source = "ManagementEngine"

        # ---------------------------------------------------------------------
        # Specialist Scores
        # ---------------------------------------------------------------------

        management.capital_allocation_score = float(
            capital.get("Score", 0)
        )

        management.governance_score = float(
            governance.get("Score", 0)
        )

        management.behaviour_score = float(
            behaviour.get("Score", 0)
        )

        management.communication_score = float(
            communication.get("Score", 0)
        )

        # Execution is one component of Behaviour.
        # Until a dedicated execution scoring engine exists, preserve the
        # Behaviour score separately and do not manufacture an execution score.

        # ---------------------------------------------------------------------
        # Capital Allocation
        # ---------------------------------------------------------------------

        management.roiic_assessment = capital.get(
            "ROIIC",
            "",
        )

        management.capital_allocation_assessment = capital.get(
            "Capital Allocation",
            "",
        )

        management.reinvestment_quality = capital.get(
            "Reinvestment",
            "",
        )

        management.acquisition_quality = capital.get(
            "Acquisitions",
            "",
        )

        management.buyback_policy = capital.get(
            "Buybacks",
            "",
        )

        management.dividend_policy = capital.get(
            "Dividend Policy",
            "",
        )

        # ---------------------------------------------------------------------
        # Governance
        # ---------------------------------------------------------------------

        management.promoter_holding_assessment = governance.get(
            "Promoter Holding",
            "",
        )

        management.promoter_pledge_assessment = governance.get(
            "Promoter Pledge",
            "",
        )

        management.related_party_transactions = governance.get(
            "Related Party Transactions",
            "",
        )

        management.auditor_quality = governance.get(
            "Auditor Quality",
            "",
        )

        management.regulatory_issues = governance.get(
            "Regulatory Issues",
            "",
        )

        management.board_independence = governance.get(
            "Board Independence",
            "",
        )

        # ---------------------------------------------------------------------
        # Behaviour
        # ---------------------------------------------------------------------

        management.execution_assessment = behaviour.get(
            "Execution",
            "",
        )

        management.guidance_reliability = behaviour.get(
            "Guidance Reliability",
            "",
        )

        management.capital_discipline = behaviour.get(
            "Capital Discipline",
            "",
        )

        management.transparency = behaviour.get(
            "Transparency",
            "",
        )

        management.long_term_focus = behaviour.get(
            "Long-term Focus",
            "",
        )

        management.shareholder_orientation = behaviour.get(
            "Shareholder Orientation",
            "",
        )

        # ---------------------------------------------------------------------
        # Communication
        # ---------------------------------------------------------------------

        management.conference_call_quality = communication.get(
            "Conference Calls",
            "",
        )

        management.annual_report_quality = communication.get(
            "Annual Report Quality",
            "",
        )

        management.guidance_clarity = communication.get(
            "Guidance Clarity",
            "",
        )

        management.risk_disclosure = communication.get(
            "Risk Disclosure",
            "",
        )

        management.shareholder_communication = communication.get(
            "Shareholder Communication",
            "",
        )

        management.management_accessibility = communication.get(
            "Management Accessibility",
            "",
        )

        # ---------------------------------------------------------------------
        # Evidence / Assumptions
        # ---------------------------------------------------------------------

        management.evidence = [
            "Capital Allocation assessment completed.",
            "Governance assessment completed.",
            "Management Behaviour assessment completed.",
            "Management Communication assessment completed.",
        ]

        management.assumptions = [
            "Management disclosures are accurate.",
        ]

        # Preserve specialist confidence information without introducing
        # additional calculated state into the passive section model.

        management.metadata = {
            "capital_allocation_confidence": capital.get(
                "Confidence",
                0,
            ),
            "governance_confidence": governance.get(
                "Confidence",
                0,
            ),
            "behaviour_confidence": behaviour.get(
                "Confidence",
                0,
            ),
            "communication_confidence": communication.get(
                "Confidence",
                0,
            ),
            "raw_score": score_result.score,
            "maximum_score": score_result.max_score,
        }

        # =====================================================================
        # Persist Typed Management Intelligence
        # =====================================================================

        self.research.update_management(management)

        # =====================================================================
        # Publish Management Intelligence
        # =====================================================================

        management_intelligence = ManagementIntelligence.build(
            self.research,
            confidence_result,
        )

        self.research.context.publish_intelligence(
            management_intelligence
        )

        print("Management Analysis Completed")

        return management