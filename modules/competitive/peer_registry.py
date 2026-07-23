"""
Peer Registry

Stores and manages peer companies for competitive analysis.
"""

from typing import List
from modules.competitive.peer import Peer


class PeerRegistry:
    """
    Stores peer companies used for benchmarking.
    """

    def __init__(self):
        self._peers: List[Peer] = []

    def add_peer(self, peer: Peer):
        """
        Add a peer company.
        """
        self._peers.append(peer)

    def remove_peer(self, company: str):
        """
        Remove a peer by company name.
        """
        self._peers = [
            peer for peer in self._peers
            if peer.company != company
        ]

    def get_all_peers(self):
        """
        Return all peers as dictionaries.
        """
        return [peer.to_dict() for peer in self._peers]

    def count(self):
        """
        Return the number of peers.
        """
        return len(self._peers)

    def clear(self):
        """
        Remove all peers.
        """
        self._peers.clear()