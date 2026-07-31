"""
===============================================================================
Module: ownership_pipeline_stage.py

Purpose:
    Execute Ownership Intelligence inside the EIOS pipeline.

Author:
    EIOS
===============================================================================
"""

from core.pipeline_context import PipelineContext

from .ownership_engine import OwnershipEngine


class OwnershipPipelineStage:
    """
    Pipeline stage responsible for ownership analysis.
    """

    STAGE_NAME = "Ownership"

    def __init__(self):

        self.engine = OwnershipEngine()

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        if not self.engine.validate(context):
            raise ValueError(
                "OwnershipPipelineStage received invalid PipelineContext."
            )

        analysis = self.engine.analyze(context)

        context.ownership_analysis = analysis

        return context