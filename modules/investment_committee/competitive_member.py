from modules import competitive
from modules.investment_committee.committee_response import CommitteeResponse


class CompetitiveMember:
    """
    Competitive Intelligence Committee Member

    Evaluates competitive positioning, peer ranking,
    industry leadership and moat.
    """

    def __init__(self):
        self.name = "Competitive"

    def evaluate(self, research):

        dossier = research.master_dossier
        competitive = dossier.competitive_intelligence

        if not competitive:
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

        leader = competitive.leader
        peer_count = competitive.peer_count
        ranked = competitive.ranked_peers
        # ------------------------------------
        # Industry Leader
        # ------------------------------------

        if leader:
            score += 30
            evidence.append(
                f"Industry leader: {leader.get('Company','Unknown')}"
            )
        else:
            risks.append("Industry leader not identified")

        # ------------------------------------
        # Peer Ranking
        # ------------------------------------

        if ranked:
            top = ranked[0]

            if top.get("Rank") == 1:
                score += 30
                evidence.append("Ranked #1 among peers")
            elif top.get("Rank") <= 3:
                score += 20
                evidence.append("Top-three peer ranking")
            else:
                risks.append("Peer ranking is weak")
        else:
            risks.append("Peer ranking unavailable")

        # ------------------------------------
        # Peer Coverage
        # ------------------------------------

        if peer_count >= 3:
            score += 20
            evidence.append("Adequate peer comparison")
        else:
            risks.append("Limited peer coverage")

        # ------------------------------------
        # Benchmark Score
        # ------------------------------------

        if leader:
            benchmark = leader.get("Benchmark Score", 0) if leader else 0

            if benchmark >= 20:
                score += 20
                evidence.append("Strong benchmark score")
            else:
                risks.append("Benchmark score below target")

        # ------------------------------------
        # Final Vote
        # ------------------------------------

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
            confidence=90,
            evidence=evidence,
            risks=risks,
            recommendation=f"Competitive Score = {score}",
            reason=f"Competitive Score = {score}",
        )