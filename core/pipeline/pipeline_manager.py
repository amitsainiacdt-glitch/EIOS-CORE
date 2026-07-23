"""
Pipeline Manager

Controls the execution of the EIOS processing pipeline.
"""

from .pipeline_context import PipelineContext


class PipelineManager:
    """
    Executes the EIOS processing pipeline.
    """

    def __init__(self):

        self._stages = []

    def add_stage(self, stage):
        """
        Register a pipeline stage.
        """

        self._stages.append(stage)

    def run(self, context=None):
        """
        Execute all registered stages.
        """

        if context is None:
            context = PipelineContext()

        for stage in self._stages:
            context = stage.execute(context)

        return context

    def clear(self):
        """
        Remove all registered stages.
        """

        self._stages.clear()

    def count(self):
        """
        Return the number of registered stages.
        """

        return len(self._stages)

    def stages(self):
        """
        Return all registered stages.
        """

        return self._stages.copy()