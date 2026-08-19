"""
EIOS
Everest Investment Operating System

Evidence Intelligence Adapter
==============================

Converts verified EIOS Evidence into the standard
Intelligence contract.

Architecture:

Evidence
    ↓
EvidenceIntelligenceAdapter
    ↓
Intelligence
    ↓
ResearchContext
    ↓
IntelligenceMesh

Design Principles
-----------------
- Does not perform investment analysis.
- Does not calculate valuation.
- Does not calculate opportunity scores.
- Does not generate catalysts.
- Does not modify Evidence.
- Does not create new Evidence.
- Does not reinterpret the Evidence.
- Preserves Evidence identity and provenance.
- Uses the existing Intelligence contract.
- Uses the existing ResearchContext publication boundary.
"""

from __future__ import annotations

from modules.evidence.evidence import Evidence
from modules.intelligence.intelligence import Intelligence
from modules.research_context.research_context import ResearchContext


class EvidenceIntelligenceAdapter:
    """
    Controlled boundary between verified Evidence and
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
    # PUBLISH ONE
    # ======================================================

    def publish(
        self,
        evidence: Evidence,
    ) -> Intelligence:
        """
        Convert one Evidence object into Intelligence
        and publish it through ResearchContext.

        No analytical transformation is performed.
        """

        if evidence is None:
            raise ValueError(
                "evidence must not be None"
            )

        if not isinstance(evidence, Evidence):
            raise TypeError(
                "evidence must be an Evidence instance"
            )

        intelligence = Intelligence(
            title=evidence.title,
            category=evidence.category,
            source_engine="EvidenceEngine",
            conclusion=evidence.description,
            entity=evidence.entity,
            confidence=evidence.confidence,
            evidence=[
                evidence.source
            ],
            assumptions=[],
            reasoning=[
                (
                    "Intelligence derived directly from "
                    "verified EIOS Evidence."
                )
            ],
            tags=[
                "evidence",
                "verified",
            ],
            timestamp=evidence.timestamp,
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
        evidences: list[Evidence],
    ) -> list[Intelligence]:
        """
        Publish multiple Evidence objects independently.
        """

        if evidences is None:
            raise ValueError(
                "evidences must not be None"
            )

        intelligences = []

        for evidence in evidences:

            intelligences.append(
                self.publish(
                    evidence
                )
            )

        return intelligences


__all__ = [
    "EvidenceIntelligenceAdapter",
]