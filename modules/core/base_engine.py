"""
EIOS
Everest Investment Operating System

Base Engine

Base class for all analytical and calculation engines.
"""

from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    Base class for all EIOS engines.
    """

    METHOD_NAME = ""
    ASSUMPTION_KEY = ""

    @abstractmethod
    def evaluate(self, data):
        """
        Execute the engine.

        Returns a typed result object.
        """
        pass