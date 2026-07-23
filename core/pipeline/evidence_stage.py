"""
Evidence Pipeline Stage

Converts observations into evidence.
"""

from .pipeline_stage import PipelineStage


class EvidenceStage(PipelineStage):

    def __init__(self, evidence_engine):

        self.evidence_engine = evidence_engine

    def execute(self, context):

        if context.observation is None:
            return context

        evidence = self.evidence_engine.create_from_observation(
            context.observation
        )

        context.evidence = evidence

        return context