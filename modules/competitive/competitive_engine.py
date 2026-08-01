"""
Competitive Engine

Coordinates peer benchmarking, ranking and
institutional competitive assessment.
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

        # Institutional Competitive Assessment
        self.assessment = CompetitiveAssessmentEngine()

        # Shared Institutional Scoring
        self.scoring_engine = ScoringEngine()
        self.confidence_engine = ConfidenceEngine()

    def add_peer(self, peer):
        """
        Add a peer company.
        """

        self.registry.add_peer(peer)

    def analyze(self, metric="Benchmark Score"):
        """
        Analyze peer companies and generate
        institutional competitive assessment.
        """

        peers = self.registry.get_all_peers()

        benchmarked = self.benchmark.evaluate(peers)

        ranked = self.ranking.rank(
            benchmarked,
            metric=metric,
        )

        leader = self.ranking.top_company(ranked)

        laggard = self.ranking.bottom_company(ranked)

        # =====================================================
        # COMPETITIVE ASSESSMENT
        # =====================================================

        assessment = self.assessment.evaluate(ranked)

        # =====================================================
        # SHARED SCORING ENGINE
        # =====================================================

        score_result = self.scoring_engine.calculate(
            score=assessment["Total Score"],
            max_score=assessment["Max Score"],
        )
        competitive = CompetitiveSection()

        competitive.score = score_result.percentage
        competitive.confidence = assessment["Confidence"]
        competitive.rating = score_result.grade

        competitive.peer_count = len(ranked)
        competitive.leader = leader if leader else {}
        competitive.laggard = laggard if laggard else {}
        competitive.ranked_peers = ranked
        competitive.assessment = assessment
        self.research.update_competitive(competitive)
        return {

            "metric": metric,

            "peer_count": len(ranked),

            "leader": leader,

            "laggard": laggard,

            "ranked_peers": ranked,

            "Assessment": assessment,

            "Overall Score": {

                "Overall Score": score_result.percentage,

                "Raw Score": score_result.score,

                "Maximum Score": score_result.max_score,

                "Confidence": assessment["Confidence"],

                "Rating": score_result.grade,
            },
        }

    def summary(self, metric="Benchmark Score"):
        """
        Display Competitive Intelligence Summary.
        """

        result = self.analyze(metric)

        print("\n" + "=" * 60)
        print("COMPETITIVE INTELLIGENCE")
        print("=" * 60)

        self.ranking.summary(result["ranked_peers"])

        if result["leader"] is not None:

            print(f"\nLeader : {result['leader']['Company']}")
            print(f"Metric : {metric}")

            print(
                f"Competitive Score : "
                f"{result['Overall Score']['Overall Score']}"
            )

            print(
                f"Rating : "
                f"{result['Overall Score']['Rating']}"
            )