"""
EIOS
Everest Investment Operating System

Recovery Opportunity Engine

Purpose
-------
Converts completed Recovery Theme + Catalyst Intelligence
into a downstream Recovery Opportunity Signal.

This is a GATE, not an investment decision.

It answers:

    "Is the recovery evidence sufficiently broad,
     confirmed, coherent and catalyst-supported to
     warrant Opportunity Engine attention?"

It does NOT calculate:

- valuation
- intrinsic value
- mispricing
- expected return
- position size
- portfolio weight
- investment recommendation

Design Principles
-----------------
- Deterministic.
- Explicit inputs only.
- No web access.
- No autonomous discovery.
- No mutation of input.
- Transparent reasoning.
- Conservative gating.
"""

from copy import deepcopy
from typing import List

from modules.opportunity.recovery.recovery_theme_assessment import (
    RecoveryThemeAssessment,
)

from modules.opportunity.recovery.recovery_theme_catalyst_link import (
    RecoveryThemeCatalystLink,
    RecoveryCatalystRelationship,
)

from modules.opportunity.recovery.recovery_opportunity_signal import (
    RecoveryOpportunitySignal,
    RecoveryOpportunityStage,
    RecoveryOpportunityDirection,
    RecoveryOpportunityConfidence,
    RecoveryOpportunitySignalType,
)


class RecoveryOpportunityEngine:
    """
    Deterministic gate between Recovery Intelligence and
    the Opportunity Engine.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        theme: RecoveryThemeAssessment,
        catalyst_links: List[
            RecoveryThemeCatalystLink
        ],
    ) -> RecoveryOpportunitySignal:

        result = RecoveryOpportunitySignal()

        # --------------------------------------------------
        # Empty theme
        # --------------------------------------------------

        if theme is None:

            result.stage = (
                RecoveryOpportunityStage.UNKNOWN
            )

            result.direction = (
                RecoveryOpportunityDirection.UNKNOWN
            )

            result.confidence_level = (
                RecoveryOpportunityConfidence.UNKNOWN
            )

            result.requires_more_evidence = True

            result.warnings.append(
                "No recovery theme supplied."
            )

            return result

        # ==================================================
        # IDENTITY
        # ==================================================

        result.theme_id = theme.theme_id

        result.theme_name = theme.theme_name

        result.signal_id = (
            f"REC-OPP::{theme.theme_id}"
        )

        result.signal_type = (
            RecoveryOpportunitySignalType.RECOVERY
        )

        # ==================================================
        # RECOVERY TRANSFER
        # ==================================================

        result.recovery_breadth = (
            RecoveryOpportunityEngine._bounded(
                theme.recovery_breadth
            )
        )

        result.confirmed_recovery_breadth = (
            RecoveryOpportunityEngine._bounded(
                theme.confirmed_recovery_breadth
            )
        )

        result.recovery_confidence = (
            RecoveryOpportunityEngine._bounded(
                theme.confidence
            )
        )

        result.recovery_coherence = (
            RecoveryOpportunityEngine._bounded(
                theme.coherence_score
            )
        )

        result.temporal_support = (
            RecoveryOpportunityEngine._bounded(
                theme.temporal_support
            )
        )

        result.persistence_score = (
            RecoveryOpportunityEngine._bounded(
                theme.persistence_score
            )
        )

        result.contradiction_score = (
            RecoveryOpportunityEngine._bounded(
                theme.contradiction_score
            )
        )

        # ==================================================
        # CATALYST AGGREGATION
        # ==================================================

        links = list(
            catalyst_links or []
        )

        result.catalyst_count = len(
            links
        )

        result.supporting_catalyst_count = sum(
            1
            for link in links
            if link.relationship
            == RecoveryCatalystRelationship.SUPPORTING
        )

        result.confirming_catalyst_count = sum(
            1
            for link in links
            if link.relationship
            == RecoveryCatalystRelationship.CONFIRMING
        )

        result.accelerating_catalyst_count = sum(
            1
            for link in links
            if link.relationship
            == RecoveryCatalystRelationship.ACCELERATING
        )

        result.catalyst_confidence = (
            RecoveryOpportunityEngine._average(
                [
                    link.catalyst_confidence
                    for link in links
                ]
            )
        )

        result.catalyst_strength = (
            RecoveryOpportunityEngine._average(
                [
                    link.catalyst_strength
                    for link in links
                ]
            )
        )

        result.catalyst_coherence = (
            RecoveryOpportunityEngine._catalyst_coherence(
                links
            )
        )

        # ==================================================
        # CATALYST SUPPORT
        # ==================================================

        result.catalyst_supported = (
            RecoveryOpportunityEngine._catalyst_supported(
                result
            )
        )

        # ==================================================
        # RECOVERY GATES
        # ==================================================

        result.broad_recovery_supported = (
            result.recovery_breadth
            >= 60.0
        )

        result.confirmed_recovery_supported = (
            result.confirmed_recovery_breadth
            >= 40.0
        )

        # ==================================================
        # DIRECTION
        # ==================================================

        result.direction = (
            RecoveryOpportunityEngine._direction(
                result
            )
        )

        # ==================================================
        # STAGE
        # ==================================================

        result.stage = (
            RecoveryOpportunityEngine._stage(
                result
            )
        )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        result.confidence_level = (
            RecoveryOpportunityEngine._confidence_level(
                result
            )
        )

        # ==================================================
        # OPPORTUNITY GATE
        # ==================================================

        result.opportunity_ready = (
            RecoveryOpportunityEngine._opportunity_ready(
                result
            )
        )

        result.requires_more_evidence = (
            not result.opportunity_ready
        )

        # ==================================================
        # CATALYST FAMILY / PATTERN TRANSFER
        # ==================================================

        result.catalyst_families = sorted(
            {
                link.catalyst_family
                for link in links
                if link.catalyst_family
            }
        )

        result.catalyst_patterns = sorted(
            {
                link.catalyst_pattern
                for link in links
                if link.catalyst_pattern
            }
        )

        # ==================================================
        # EVIDENCE TRANSFER
        # ==================================================

        result.evidence_sources = sorted(
            {
                source
                for link in links
                for source in link.evidence_sources
                if source
            }
        )

        result.supporting_evidence = [
            evidence
            for link in links
            for evidence in link.supporting_evidence
        ]

        result.contradictory_evidence = [
            evidence
            for link in links
            for evidence in link.contradictory_evidence
        ]

        # ==================================================
        # REASONING
        # ==================================================

        RecoveryOpportunityEngine._build_reasons(
            result
        )

        return result

    # ======================================================
    # BOUNDED VALUE
    # ======================================================

    @staticmethod
    def _bounded(
        value,
    ) -> float:

        try:
            number = float(value)
        except (
            TypeError,
            ValueError,
        ):
            return 0.0

        return max(
            0.0,
            min(
                100.0,
                number,
            ),
        )

    # ======================================================
    # AVERAGE
    # ======================================================

    @staticmethod
    def _average(
        values,
    ) -> float:

        if not values:
            return 0.0

        return RecoveryOpportunityEngine._bounded(
            sum(values)
            / len(values)
        )

    # ======================================================
    # CATALYST COHERENCE
    # ======================================================

    @staticmethod
    def _catalyst_coherence(
        links,
    ) -> float:

        if not links:
            return 0.0

        scores = []

        for link in links:

            score = 0.0

            if link.catalyst_family:
                score += 25.0

            if link.catalyst_pattern:
                score += 25.0

            if link.transmission.value != "Unknown":
                score += 25.0

            if link.relationship.value != "Unknown":
                score += 25.0

            scores.append(score)

        return RecoveryOpportunityEngine._average(
            scores
        )

    # ======================================================
    # CATALYST SUPPORTED
    # ======================================================

    @staticmethod
    def _catalyst_supported(
        result: RecoveryOpportunitySignal,
    ) -> bool:

        if result.catalyst_count == 0:
            return False

        meaningful_relationships = (
            result.supporting_catalyst_count
            + result.confirming_catalyst_count
            + result.accelerating_catalyst_count
        )

        if meaningful_relationships <= 0:
            return False

        if result.catalyst_confidence < 50.0:
            return False

        if result.catalyst_strength < 50.0:
            return False

        return True

    # ======================================================
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        result: RecoveryOpportunitySignal,
    ) -> RecoveryOpportunityDirection:

        if (
            result.contradiction_score
            >= 60.0
        ):
            return (
                RecoveryOpportunityDirection.NEGATIVE
            )

        if (
            result.recovery_breadth >= 60.0
            and result.confirmed_recovery_breadth >= 40.0
            and result.catalyst_supported
        ):
            return (
                RecoveryOpportunityDirection.POSITIVE
            )

        if (
            result.recovery_breadth > 0.0
            or result.catalyst_count > 0
        ):
            return (
                RecoveryOpportunityDirection.NEUTRAL
            )

        return (
            RecoveryOpportunityDirection.UNKNOWN
        )

    # ======================================================
    # STAGE
    # ======================================================

    @staticmethod
    def _stage(
        result: RecoveryOpportunitySignal,
    ) -> RecoveryOpportunityStage:

        # --------------------------------------------------
        # No evidence
        # --------------------------------------------------

        if (
            result.recovery_breadth <= 0.0
            and result.catalyst_count == 0
        ):
            return (
                RecoveryOpportunityStage.UNKNOWN
            )

        # --------------------------------------------------
        # Actionable
        #
        # Requires:
        # - broad recovery
        # - confirmed recovery
        # - strong recovery coherence
        # - catalyst support
        # - sufficient confidence
        # --------------------------------------------------

        if (
            result.broad_recovery_supported
            and result.confirmed_recovery_supported
            and result.catalyst_supported
            and result.recovery_coherence >= 60.0
            and result.recovery_confidence >= 70.0
            and result.contradiction_score < 40.0
        ):
            return (
                RecoveryOpportunityStage.ACTIONABLE
            )

        # --------------------------------------------------
        # Developing
        # --------------------------------------------------

        if (
            result.recovery_breadth >= 40.0
            or result.catalyst_supported
        ):
            return (
                RecoveryOpportunityStage.DEVELOPING
            )

        # --------------------------------------------------
        # Watch
        # --------------------------------------------------

        if (
            result.recovery_breadth > 0.0
            or result.catalyst_count > 0
        ):
            return (
                RecoveryOpportunityStage.WATCH
            )

        return (
            RecoveryOpportunityStage.UNKNOWN
        )

    # ======================================================
    # CONFIDENCE LEVEL
    # ======================================================

    @staticmethod
    def _confidence_level(
        result: RecoveryOpportunitySignal,
    ) -> RecoveryOpportunityConfidence:

        score = (
            result.recovery_confidence * 0.35
            + result.recovery_breadth * 0.20
            + result.confirmed_recovery_breadth * 0.15
            + result.recovery_coherence * 0.15
            + result.catalyst_confidence * 0.10
            + result.catalyst_strength * 0.05
            - result.contradiction_score * 0.10
        )

        score = max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

        if score >= 85.0:
            return (
                RecoveryOpportunityConfidence.VERY_HIGH
            )

        if score >= 70.0:
            return (
                RecoveryOpportunityConfidence.HIGH
            )

        if score >= 50.0:
            return (
                RecoveryOpportunityConfidence.MODERATE
            )

        if score > 0.0:
            return (
                RecoveryOpportunityConfidence.LOW
            )

        return (
            RecoveryOpportunityConfidence.UNKNOWN
        )

    # ======================================================
    # OPPORTUNITY GATE
    # ======================================================

    @staticmethod
    def _opportunity_ready(
        result: RecoveryOpportunitySignal,
    ) -> bool:

        return (
            result.stage
            == RecoveryOpportunityStage.ACTIONABLE
            and result.direction
            == RecoveryOpportunityDirection.POSITIVE
            and result.catalyst_supported
            and result.broad_recovery_supported
            and result.confirmed_recovery_supported
        )

    # ======================================================
    # REASONING
    # ======================================================

    @staticmethod
    def _build_reasons(
        result: RecoveryOpportunitySignal,
    ) -> None:

        result.reasons.append(
            "Recovery Opportunity Signal was "
            "generated from explicit Recovery Theme "
            "and Catalyst inputs."
        )

        if (
            result.broad_recovery_supported
        ):

            result.reasons.append(
                "Recovery breadth is sufficiently broad."
            )

        if (
            result.confirmed_recovery_supported
        ):

            result.reasons.append(
                "Confirmed recovery breadth provides "
                "meaningful validation."
            )

        if (
            result.catalyst_supported
        ):

            result.reasons.append(
                "Recovery is supported by meaningful "
                "catalyst evidence."
            )

        if (
            result.recovery_coherence
            >= 60.0
        ):

            result.reasons.append(
                "Recovery theme coherence is strong."
            )

        if (
            result.recovery_confidence
            >= 70.0
        ):

            result.reasons.append(
                "Recovery confidence is high."
            )

        if (
            result.opportunity_ready
        ):

            result.reasons.append(
                "Recovery evidence has crossed the "
                "Opportunity Engine readiness gate."
            )

            result.reasons.append(
                "This signal is eligible for downstream "
                "Opportunity Engine evaluation."
            )

        else:

            result.warnings.append(
                "Recovery evidence has not crossed the "
                "Opportunity Engine readiness gate."
            )

        if (
            result.contradiction_score
            >= 40.0
        ):

            result.warnings.append(
                "Material contradictory evidence remains."
            )

        result.warnings.append(
            "Opportunity readiness is not an investment "
            "recommendation and does not imply valuation "
            "or portfolio approval."
        )


__all__ = [
    "RecoveryOpportunityEngine",
]