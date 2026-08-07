from modules.investment_committee.committee_response import CommitteeResponse


class CompetitiveMember:
    """
    Competitive Intelligence Committee Member.

    Evaluates competitive positioning,
    peer ranking and benchmark strength.
    """

    def __init__(self):
        self.name = "Competitive"

    def evaluate(self, research):

        dossier = research.master_dossier
        competitive = dossier.competitive

        if competitive is None:
            return CommitteeResponse(
                member="Competitive",
                vote="Watch",
                score=0,
                confidence=0,
                evidence=[],
                risks=["Competitive intelligence unavailable"],
                recommendation="Complete competitive analysis first.",
                reason="Competitive analysis unavailable.",
            )

        score = 0
        evidence = []
        risks = []

        # =====================================================
        # Read values produced by CompetitiveEngine
        # =====================================================

        leader = competitive.metadata.get("leader", {})
        laggard = competitive.metadata.get("laggard", {})

        benchmark = leader.get("Benchmark Score", 0)
        rank = leader.get("Rank", 999)

        peer_count = (
            len(competitive.ranked_peers)
            if hasattr(competitive, "ranked_peers")
            else 0
        )

        # =====================================================
        # Leader
        # =====================================================

        if leader:
            score += 30
            evidence.append(
                f"Industry leader: {leader.get('Company', 'Unknown')}"
            )
        else:
            risks.append("Industry leader not identified")

        # =====================================================
        # Peer Ranking
        # =====================================================

        if rank == 1:
            score += 30
            evidence.append("Ranked #1 among peers")
        elif rank <= 3:
            score += 20
            evidence.append("Top-three peer ranking")
        else:
            risks.append("Weak peer ranking")

        # =====================================================
        # Peer Coverage
        # =====================================================

        if peer_count >= 3:
            score += 20
            evidence.append("Adequate peer coverage")
        else:
            risks.append("Limited peer coverage")

        # =====================================================
        # Benchmark Score
        # =====================================================

        if benchmark >= 20:
            score += 20
            evidence.append("Strong benchmark score")
        else:
            risks.append("Benchmark score below target")

        # =====================================================
        # Final Vote
        # =====================================================

        if score >= 85:
            vote = "Pass"
        elif score >= 65:
            vote = "Watch"
        else:
            vote = "Reject"

        return CommitteeResponse(
            member="Competitive",
            vote=vote,
            score=score,
            confidence=competitive.confidence,
            evidence=evidence,
            risks=risks,
            recommendation=f"Competitive Score = {score}",
            reason=f"Competitive Score = {score}",
        )