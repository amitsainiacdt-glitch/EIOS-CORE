"""
Pipeline Stage

Base class for all EIOS pipeline stages.
"""

from abc import ABC, abstractmethod


class PipelineStage(ABC):
    """
    Base class for every pipeline stage.
    """

    @abstractmethod
    def execute(self, context):
        """
        Execute one pipeline stage.

        Parameters
        ----------
        context : PipelineContext
            Shared pipeline context.

        Returns
        -------
        PipelineContext
        """

        pass