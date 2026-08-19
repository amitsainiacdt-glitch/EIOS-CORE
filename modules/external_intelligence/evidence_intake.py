"""
EIOS
Everest Investment Operating System

External Evidence Intake
========================

Controlled boundary between external Observations and the
existing EvidenceAssessmentEngine.

Architecture:

External Observation
        ↓
ExternalEvidenceIntake
        ↓
EvidenceAssessmentEngine
        ↓
EvidenceItem

Design Principles
-----------------

- Does not perform HTTP requests.
- Does not perform searches.
- Does not create Observations.
- Does not calculate evidence strength.
- Does not calculate confidence.
- Does not score Opportunities.
- Does not perform valuation.
- Does not create Signals.
- Does not make investment decisions.
- Does not fabricate EvidenceAssessment values.

An Observation becomes an EvidenceItem only when an
explicit EvidenceAssessment is supplied.
"""

from __future__ import annotations

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.external_intelligence.evidence_assessment_engine import (
    EvidenceAssessmentEngine,
)

from modules.observation.observation import (
    Observation,
)

from modules.opportunity.evidence_engine import (
    EvidenceItem,
)


class ExternalEvidenceIntake:
    """
    Controlled boundary for converting externally obtained
    observations into canonical EvidenceItems.

    EvidenceAssessment values must be explicitly supplied
    by the caller.
    """

    def __init__(
        self,
        engine: EvidenceAssessmentEngine | None = None,
    ) -> None:

        self.engine = (
            engine
            if engine is not None
            else EvidenceAssessmentEngine()
        )

    # ======================================================
    # ASSESS
    # ======================================================

    def assess(
        self,
        *,
        observation: Observation,
        assessment: EvidenceAssessment,
        evidence_id: str = "",
    ) -> EvidenceItem:
        """
        Convert one Observation plus explicit assessment
        metadata into the canonical EvidenceItem.
        """

        if observation is None:
            raise ValueError(
                "observation must not be None"
            )

        if assessment is None:
            raise ValueError(
                "assessment must not be None"
            )

        return self.engine.assess(
            observation=observation,
            assessment=assessment,
            evidence_id=evidence_id,
        )

    # ======================================================
    # ASSESS MANY
    # ======================================================

    def assess_many(
        self,
        *,
        observations: list[Observation],
        assessments: list[EvidenceAssessment],
    ) -> list[EvidenceItem]:
        """
        Convert multiple observations into EvidenceItems.

        Every observation must have a corresponding
        explicit EvidenceAssessment.

        No assessment is fabricated.
        """

        if observations is None:
            raise ValueError(
                "observations must not be None"
            )

        if assessments is None:
            raise ValueError(
                "assessments must not be None"
            )

        if len(observations) != len(assessments):
            raise ValueError(
                "observations and assessments "
                "must have the same length"
            )

        evidence_items = []

        for index, (
            observation,
            assessment,
        ) in enumerate(
            zip(
                observations,
                assessments,
            )
        ):

            evidence_items.append(
                self.assess(
                    observation=observation,
                    assessment=assessment,
                    evidence_id=(
                        f"EXT-{index + 1:04d}"
                    ),
                )
            )

        return evidence_items


__all__ = [
    "ExternalEvidenceIntake",
]