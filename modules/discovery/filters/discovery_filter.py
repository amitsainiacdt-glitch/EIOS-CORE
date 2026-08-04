"""
===============================================================================
EIOS
Everest Investment Operating System

Discovery Filter

Purpose:
    Base interface for all Discovery Office filters.

Architecture:
    - Defines the standard contract for discovery filters.
    - All discovery filters inherit from this class.
    - DiscoveryEngine interacts only with this interface.

Author:
    EIOS

Release:
    3.0
===============================================================================
"""

from abc import ABC, abstractmethod

from modules.discovery.discovery_candidate import DiscoveryCandidate


class DiscoveryFilter(ABC):
    """
    Base class for all Discovery Office filters.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable filter name.
        """
        pass

    @abstractmethod
    def evaluate(
        self,
        candidate: DiscoveryCandidate,
    ) -> DiscoveryCandidate:
        """
        Evaluate a DiscoveryCandidate.

        Returns the updated candidate.
        """
        pass