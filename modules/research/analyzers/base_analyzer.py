"""
===============================================================================
EIOS
Base Analyzer

Purpose:
    Base interface for all analyzers.

Every analyzer in EIOS must inherit from this class.

Author:
    EIOS

Release:
    1.0
===============================================================================
"""

from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    """
    Base class for every analyzer.
    """

    @abstractmethod
    def analyze(self, company):
        """
        Analyze a company.

        Parameters
        ----------
        company
            Company object.

        Returns
        -------
        Analysis Result
        """
        raise NotImplementedError

