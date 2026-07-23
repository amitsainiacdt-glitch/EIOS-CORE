"""
Benchmark Engine

Calculates benchmark scores for peer companies.
"""


class BenchmarkEngine:
    """
    Evaluates peer companies based on key business quality metrics.
    """

    def evaluate(self, peers):
        """
        Evaluate each peer and calculate a benchmark score.

        Parameters
        ----------
        peers : list[dict]

        Returns
        -------
        list[dict]
        """

        evaluated = []

        for peer in peers:

            score = self.calculate_score(peer)

            peer["Benchmark Score"] = score

            evaluated.append(peer)

        return evaluated

    def calculate_score(self, peer):
        """
        Weighted benchmark score.

        Weightage:
        ROIIC              30%
        ROCE               25%
        ROE                15%
        Revenue Growth     15%
        EPS Growth         10%
        Operating Margin    5%
        """

        score = (
            peer.get("ROIIC", 0) * 0.30 +
            peer.get("ROCE", 0) * 0.25 +
            peer.get("ROE", 0) * 0.15 +
            peer.get("Revenue Growth", 0) * 0.15 +
            peer.get("EPS Growth", 0) * 0.10 +
            peer.get("Operating Margin", 0) * 0.05
        )

        return round(score, 2)