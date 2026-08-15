"""
EIOS
Everest Investment Operating System

External Evidence Assessment Engine
====================================

Validates explicit evidence-assessment metadata and converts
an Observation plus EvidenceAssessment into the canonical
Opportunity EvidenceItem.

This engine performs validation and translation only.

It does NOT:
- calculate evidence score
- calculate Opportunity score
- calculate valuation
- create Signals
- create Catalysts
- rank opportunities
- make investment decisions
"""

from modules.external_intelligence.evidence_assessment import (
    EvidenceAssessment,
)

from modules.observation.observation import (
    Observation,
)

from modules.opportunity.evidence_engine import (
    EvidenceItem,
)


class EvidenceAssessmentEngine:
    """
    Validates evidence assessment metadata and creates an
    Opportunity EvidenceItem.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    def assess(
        self,
        *,
        observation: Observation,
        assessment: EvidenceAssessment,
        evidence_id: str = "",
    ) -> EvidenceItem:
        """
        Validate explicit assessment metadata and translate
        the Observation into an EvidenceItem.
        """

        if observation is None:
            raise ValueError(
                "observation must not be None"
            )

        if assessment is None:
            raise ValueError(
                "assessment must not be None"
            )

        self._validate_assessment(
            assessment
        )

        return EvidenceItem(
            evidence_id=evidence_id,

            statement=(
                observation.description
            ),

            source=(
                observation.source
            ),

            category=(
                assessment.category
                or observation.category
            ),

            direction=(
                assessment.direction
            ),

            strength=(
                assessment.strength
            ),

            confidence=(
                assessment.confidence
            ),

            independent_confirmation=(
                assessment.independent_confirmation
            ),

            is_primary_source=(
                assessment.is_primary_source
            ),

            is_time_sensitive=(
                assessment.is_time_sensitive
            ),

            notes=(
                assessment.notes
            ),
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def _validate_assessment(
        self,
        assessment: EvidenceAssessment,
    ) -> None:
        """
        Validate explicit assessment values.

        No scoring is performed here.
        """

        if not (
            0.0
            <= assessment.strength
            <= 100.0
        ):
            raise ValueError(
                "strength must be between 0 and 100"
            )

        if not (
            0.0
            <= assessment.confidence
            <= 100.0
        ):
            raise ValueError(
                "confidence must be between 0 and 100"
            )

        if (
            not isinstance(
                assessment.independent_confirmation,
                int,
            )
            or isinstance(
                assessment.independent_confirmation,
                bool,
            )
        ):
            raise ValueError(
                "independent_confirmation must be an integer"
            )

        if (
            assessment.independent_confirmation
            < 0
        ):
            raise ValueError(
                "independent_confirmation "
                "cannot be negative"
            )

        if not assessment.direction:
            raise ValueError(
                "direction must not be empty"
            )


__all__ = [
    "EvidenceAssessmentEngine",
]