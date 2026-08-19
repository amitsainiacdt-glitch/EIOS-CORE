"""
EIOS
Everest Investment Operating System

External Intelligence Adapter
==============================

Converts externally collected EIOS Observations into the
existing Intelligence contract used by ResearchContext
and IntelligenceMesh.

Architecture:

External Observation
        ↓
ExternalIntelligenceAdapter
        ↓
Intelligence
        ↓
ResearchContext
        ↓
IntelligenceMesh

Design Principles
-----------------
- Does not perform HTTP requests.
- Does not perform searches.
- Does not perform investment analysis.
- Does not calculate valuation.
- Does not calculate opportunity scores.
- Does not modify the Observation.
- Does not create Evidence.
- Uses the existing Intelligence model.
- Uses the existing ResearchContext publication boundary.
- Keeps external intelligence integration isolated.
"""

from __future__ import annotations

from modules.intelligence.intelligence import (
    Intelligence,
)

from modules.observation.observation import (
    Observation,
)

from modules.research_context.research_context import (
    ResearchContext,
)


class ExternalIntelligenceAdapter:
    """
    Controlled boundary between external Observations and
    the EIOS Intelligence Mesh.
    """

    def __init__(
        self,
        context: ResearchContext,
    ) -> None:

        if context is None:
            raise ValueError(
                "context must not be None"
            )

        self.context = context

    # ======================================================
    # PUBLISH
    # ======================================================

    def publish(
        self,
        observation: Observation,
    ) -> Intelligence:
        """
        Convert one external Observation into Intelligence
        and publish it through ResearchContext.
        """

        if observation is None:
            raise ValueError(
                "observation must not be None"
            )

        intelligence = Intelligence(
            title=observation.title,
            category=observation.category,
            source_engine="ExternalResearch",
            conclusion=observation.description,
            entity=observation.entity,
            confidence=observation.confidence,
            evidence=[
                observation.source
            ],
            assumptions=[],
            reasoning=[
                (
                    "Information obtained from an "
                    "external research source."
                )
            ],
            tags=[
                "external",
                "web",
            ],
            timestamp=observation.timestamp,
        )

        self.context.publish_intelligence(
            intelligence
        )

        return intelligence

    # ======================================================
    # PUBLISH MANY
    # ======================================================

    def publish_many(
        self,
        observations: list[Observation],
    ) -> list[Intelligence]:
        """
        Publish multiple external observations.

        Each observation is converted independently.
        """

        if observations is None:
            raise ValueError(
                "observations must not be None"
            )

        intelligence = []

        for observation in observations:

            intelligence.append(
                self.publish(
                    observation
                )
            )

        return intelligence


__all__ = [
    "ExternalIntelligenceAdapter",
]