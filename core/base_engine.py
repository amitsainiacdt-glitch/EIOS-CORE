"""
EIOS
Everest Investment Operating System

Base Engine

Purpose:
Defines the standard contract for every intelligence engine in EIOS.

Author:
EIOS

Release:
0.8

Sprint:
008.1
"""

from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    Base class for all EIOS intelligence engines.

    Every engine must implement the same lifecycle.

    Responsibilities
    ----------------
    - Validate input
    - Perform analysis
    - Report confidence
    - Produce a human-readable summary

    This class intentionally contains no business logic.
    """

    @abstractmethod
    def validate(self, context):
        """
        Validate the supplied PipelineContext.

        Parameters
        ----------
        context
            Shared pipeline context.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @abstractmethod
    def analyze(self, context):
        """
        Execute the engine's analysis.

        Parameters
        ----------
        context
            Shared pipeline context.

        Returns
        -------
        AnalysisPack
        """
        raise NotImplementedError

    @abstractmethod
    def confidence(self):
        """
        Return the confidence score of the analysis.

        Returns
        -------
        float
        """
        raise NotImplementedError

    @abstractmethod
    def summary(self):
        """
        Return a concise summary of the analysis.

        Returns
        -------
        str
        """
        raise NotImplementedError