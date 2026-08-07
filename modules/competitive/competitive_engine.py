"""
Competitive Engine

Coordinates peer benchmarking, ranking and
institutional competitive assessment.

Release 3.0

Architecture

CompetitiveEngine
        ↓
CompetitiveSection
        ↓
AnalysisPack
        ↓
AnalysisPackProcessor
        ↓
CompanyResearch
"""

from modules.competitive.peer_registry import PeerRegistry
from modules.competitive.benchmark_engine import BenchmarkEngine
from modules.competitive.ranking_engine import RankingEngine
from modules.competitive.competitive_assessment import (
    CompetitiveAssessmentEngine,
)

from modules.core.scoring.scoring_engine import ScoringEngine
from modules.core.scoring.confidence_engine import ConfidenceEngine

from modules.research.company_research import CompanyResearch
from modules.master_dossier.competitive_section import CompetitiveSection


class CompetitiveEngine:
    """
    Coordinates the Competitive Intelligence subsystem.
    """

    def __init__(self, research: CompanyResearch):

        self.research = research

        self.registry = PeerRegistry()
        self.benchmark = BenchmarkEngine()
        self.ranking = RankingEngine()

        self.assessment = CompetitiveAssessmentEngine()

        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def add_peer(self, peer):
        """
        Register a peer company.
        """

        self.registry.add_peer(peer)

    def analyze(self, metric="Benchmark Score") -> CompetitiveSection:
        """
        Produce typed Competitive Intelligence.

        Release 3.0:
            - No persistence
            - Returns CompetitiveSection only
        """

        # ==========================================================
        # Peer Benchmarking
        # ==========================================================

        peers = self.registry.get_all_peers()

        benchmarked = self.benchmark.evaluate(peers)

        ranked = self.ranking.rank(
            benchmarked,
            metric=metric,
        )

        leader = self.ranking.top_company(ranked)

        laggard = self.ranking.bottom_company(ranked)

        # ==========================================================
        # Competitive Assessment
        # ==========================================================

        assessment = self.assessment.evaluate(ranked)

        # ==========================================================
        # Institutional Scoring
        # ==========================================================

        score_result = self.scoring_engine.calculate(
            score=assessment["Total Score"],
            max_score=assessment["Max Score"],
        )

        # ==========================================================
        # Typed Competitive Section
        # ==========================================================

        competitive = CompetitiveSection()

        competitive.score = score_result.percentage
        competitive.confidence = assessment["Confidence"]
        competitive.rating = score_result.grade

        competitive.peer_count = len(ranked)

        competitive.leader = leader if leader else {}
        competitive.laggard = laggard if laggard else {}

        competitive.ranked_peers = ranked
        competitive.assessment = assessment

        # ==========================================================
        # Supporting Information
        # ==========================================================

        competitive.summary = (
            f"Competitive analysis completed across "
            f"{len(ranked)} peer companies."
        )

        competitive.evidence = [
            "Peer benchmarking completed.",
            "Peer ranking completed.",
            "Competitive assessment completed.",
        ]

        competitive.assumptions = [
            "Peer data accurately represents the competitive landscape."
        ]

        competitive.source = "CompetitiveEngine"

        competitive.metadata = {
            "metric": metric,
            "leader": leader,
            "laggard": laggard,
            "raw_score": score_result.score,
            "maximum_score": score_result.max_score,
        }

        # ==========================================================
        # Release 3.0
        #
        # No persistence here.
        #
        # AnalysisPackProcessor will call:
        #
        #     update_competitive()
        #
        # ==========================================================

        print("Competitive Analysis Completed")

        return competitive

    def summary(self, metric="Benchmark Score"):
        """
        Display Competitive Intelligence Summary.
        """

        competitive = self.analyze(metric)

        print("\n" + "=" * 60)
        print("COMPETITIVE INTELLIGENCE")
        print("=" * 60)

        self.ranking.summary(
            competitive.ranked_peers
        )

        if competitive.leader:

            print(
                f"\nLeader : "
                f"{competitive.leader.get('Company', '')}"
            )

            print(f"Metric : {metric}")

            print(
                f"Competitive Score : "
                f"{competitive.score:.2f}"
            )

            print(
                f"Rating : "
                f"{competitive.rating}"
            )