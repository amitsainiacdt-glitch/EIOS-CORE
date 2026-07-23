"""
Observation Pipeline Stage

Creates observations and stores them in the pipeline context.
"""

from .pipeline_stage import PipelineStage


class ObservationStage(PipelineStage):

    def __init__(self, observation_engine):

        self.observation_engine = observation_engine

    def execute(self, context):

        observation = self.observation_engine.observe(
            title="RBI cuts Repo Rate",
            description="Repo rate reduced by 25 basis points.",
            source="Reserve Bank of India",
            category="Macro",
            entity="Indian Economy",
            confidence=98
        )

        context.observation = observation

        return context