"""
Ranking Engine

Ranks peer companies based on benchmark scores.
"""

from typing import List


class RankingEngine:
    """
    Responsible for ranking peer companies.
    """

    def rank(self, peers: List[dict], metric: str, reverse: bool = True):
        """
        Rank peers using a single metric.

        Parameters
        ----------
        peers : list[dict]
            List of peer dictionaries.

        metric : str
            Metric to rank by.

        reverse : bool
            True = Highest value ranks first.

        Returns
        -------
        list[dict]
            Ranked peers.
        """

        ranked = sorted(
            peers,
            key=lambda x: x.get(metric, 0),
            reverse=reverse,
        )

        for index, peer in enumerate(ranked, start=1):
            peer["Rank"] = index

        return ranked

    def top_company(self, ranked_peers: List[dict]):

        if not ranked_peers:
            return None

        return ranked_peers[0]

    def bottom_company(self, ranked_peers: List[dict]):

        if not ranked_peers:
            return None

        return ranked_peers[-1]

    def summary(self, ranked_peers: List[dict]):

        print("\nPeer Ranking")

        print("-" * 60)

        for peer in ranked_peers:

            print(
                f"{peer.get('Rank'):>2}. "
                f"{peer.get('Company')} | "
                f"{peer.get('ROCE')} | "
                f"{peer.get('ROIIC')}"
            )