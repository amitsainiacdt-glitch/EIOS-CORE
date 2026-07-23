from modules.master_dossier.master_dossier import MasterDossier
from modules.company.company import Company
from modules.company.company_registry import CompanyRegistry

from modules.research.company_research import CompanyResearch
from modules.research.stage_engine import StageEngine
from modules.research.business_quality import BusinessQualityEngine
from modules.research.kill_switch import KillSwitchEngine

from modules.financial.financial_engine import FinancialEngine

from modules.observation import ObservationEngine
from modules.evidence import EvidenceEngine
from modules.knowledge.knowledge_engine import KnowledgeEngine
from modules.reasoning import ReasoningEngine
from modules.competitive.competitive_engine import CompetitiveEngine
from modules.competitive.peer import Peer
from modules.valuation.valuation_engine import ValuationEngine
from modules.management.management_engine import ManagementEngine
from modules.risk.risk_engine import RiskEngine
from modules.thesis.thesis_engine import ThesisEngine
from modules.investment_committee.committee_engine import CommitteeEngine

class EIOSApplication:

    def __init__(self):
        self.registry = CompanyRegistry()
        self.kill_switch = KillSwitchEngine()
        self.observation_engine = ObservationEngine()
        self.evidence_engine = EvidenceEngine()
        self.knowledge_engine = KnowledgeEngine()
        self.reasoning_engine = ReasoningEngine()

    def run(self):

        # ==========================================================
        # COMPANY REGISTRY
        # ==========================================================

        self.registry.add_company(
                Company(
                    name="The Anup Engineering Limited",
                    ticker="ANUP",
                    sector="Capital Goods",
                    industry="Process Equipment",
                )
            )

        print("=" * 60)
        print("EVEREST INVESTMENT OPERATING SYSTEM (EIOS)")
        print("=" * 60)
        print(f"Companies Registered : {self.registry.count()}")

        # ==========================================================
        # KILL SWITCH
        # ==========================================================

        result = self.kill_switch.evaluate(
            tam=True,
            moat=True,
            management=True,
            financial_quality=True,
            customer_concentration=True,
        )

        print("\nKILL SWITCH")

        if result.passed:
            print("Status : PASS")
            print("Research Approved\n")
        else:
            print("Status : FAIL")
            print(result.failed_checks)
            print("\nResearch Terminated")
            return

        # ==========================================================
        # MASTER DOSSIER
        # ==========================================================

        dossier = MasterDossier(
            company_name="The Anup Engineering Limited",
            ticker="ANUP",
            sector="Capital Goods",
            industry="Process Equipment",
        )

        research = CompanyResearch(dossier)

        # ==========================================================
        # FINANCIAL ENGINE
        # ==========================================================

        financial_engine = FinancialEngine(research)

        financial_data = {
            "current_revenue": 1200,
            "previous_revenue": 1000,
            "current_eps": 45,
            "previous_eps": 36,
            "current_profit": 180,
            "previous_profit": 150,
            "operating_cash_flow": 240,
            "capital_expenditure": 60,
            "ebit": 250,
            "capital_employed": 1000,
            "net_profit": 180,
            "shareholder_equity": 900,
            "total_debt": 150,
            "interest_expense": 20,
            "revenue": 1200,
            "total_assets": 1600,
            "current_nopat": 175,
            "previous_nopat": 145,
            "current_invested_capital": 980,
            "previous_invested_capital": 850,
        }

        financial_engine.analyze(financial_data)

        # ==========================================================
        # VALUATION
        # ==========================================================

        valuation_engine = ValuationEngine(research)
        valuation_engine.analyze(financial_data)

        # ==========================================================
        # MANAGEMENT
        # ==========================================================

        management_engine = ManagementEngine(research)

        management_engine.analyze(
            {
                "company": dossier.company_name,
            }
        )

        # ==========================================================
        # RISK
        # ==========================================================

        risk_engine = RiskEngine(research)

        risk_engine.analyze(
            {
                "company": dossier.company_name,
            }
        )

        # ==========================================================
        # THESIS ENGINE
        # ==========================================================

        thesis_engine = ThesisEngine(research)

        # ==========================================================
        # INVESTMENT COMMITTEE
        # ==========================================================

        committee_engine = CommitteeEngine(research)
        # ==========================================================
        # COMPETITIVE INTELLIGENCE
        # ==========================================================

        competitive_engine = CompetitiveEngine()

        competitive_engine.add_peer(
            Peer(
                company="The Anup Engineering Limited",
                revenue_growth=20,
                eps_growth=25,
                roce=25,
                roe=22,
                roiic=24,
                operating_margin=18,
                debt_to_equity=0.20,
            )
        )

        competitive_engine.add_peer(
            Peer(
                company="Thermax",
                revenue_growth=15,
                eps_growth=18,
                roce=20,
                roe=18,
                roiic=17,
                operating_margin=14,
                debt_to_equity=0.15,
            )
        )

        competitive_engine.add_peer(
            Peer(
                company="ISGEC Heavy Engineering",
                revenue_growth=12,
                eps_growth=14,
                roce=17,
                roe=15,
                roiic=14,
                operating_margin=10,
                debt_to_equity=0.35,
            )
        )

        competitive_result = competitive_engine.analyze()
        research.update_competitive(competitive_result)

        # ==========================================================
        # OBSERVATION
        # ==========================================================

        observation = self.observation_engine.observe(
            title="RBI cuts Repo Rate",
            description="Repo rate reduced by 25 basis points.",
            source="Reserve Bank of India",
            category="Macro",
            entity="Indian Economy",
            confidence=98,
        )

        # ==========================================================
        # EVIDENCE
        # ==========================================================

        evidence = self.evidence_engine.create_from_observation(
            observation
        )

        research.add_evidence(evidence)

        # ==========================================================
        # KNOWLEDGE
        # ==========================================================

        knowledge = self.knowledge_engine.create_from_evidence(
            evidence
        )

        # ==========================================================
        # REASONING
        # ==========================================================

        reasoning = self.reasoning_engine.create_from_knowledge(
            knowledge
        )

        # ==========================================================
        # BUSINESS QUALITY
        # ==========================================================

        print()
        print("=" * 60)
        print("BUSINESS QUALITY ANALYSIS")
        print("=" * 60)
        print()

        business_engine = BusinessQualityEngine(research)

        business_engine.analyze(
            business_model="Engineering-to-order manufacturing",
            moat="High engineering expertise and long customer relationships",
            industry="Process Equipment",
            market_size="Large global process equipment market",
            growth_drivers=[
                "Capex revival",
                "Export growth",
                "Energy transition",
            ],
            risks=[
                "Project execution delays",
                "Commodity price volatility",
            ],
        )

        # ==========================================================
        # THESIS
        # ==========================================================

        thesis_engine.analyze()

        # ==========================================================
        # INVESTMENT COMMITTEE
        # ==========================================================

        committee_data = {
            "business_quality": "Pass",
            "financial_quality": "Pass",
            "management_quality": "Pass",
            "risk": "Low",
            "valuation": "Fair",
            "portfolio_fit": "Watch",
            "position_size": "5%",
            "portfolio_priority": "Medium",
            "diversification_impact": "Neutral",
            "capital_allocation": "Wait",
        }

        committee_engine.analyze(committee_data)

       
        # ==========================================================
        # DISPLAY
        # ==========================================================

        print()
        self.observation_engine.show_observations()

        print()
        self.evidence_engine.show_evidence()

        print()
        self.knowledge_engine.show_knowledge()

        print()
        self.reasoning_engine.show_reasoning()

        print()
        competitive_engine.summary()

        # ==========================================================
        # MASTER DOSSIER
        # ==========================================================

        print()
        print("=" * 60)
        print("MASTER DOSSIER")
        print("=" * 60)

        print(dossier.to_dict())