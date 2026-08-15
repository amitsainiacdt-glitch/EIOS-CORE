"""
EIOS
Everest Investment Operating System

Recovery Theme Engine

Purpose:
Aggregates RecoveryClusterAssessment records into an
economically coherent RecoveryThemeAssessment.

Design Principles:
- Explicit cluster inputs only.
- No automatic company selection.
- No valuation.
- No opportunity scoring.
- No portfolio decision.
- No mutation of input objects.
- Deterministic.
- Transparent reasoning.
"""


from typing import List

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
)

from modules.opportunity.recovery.recovery_theme_assessment import (
    RecoveryThemeAssessment,
    RecoveryThemeType,
    RecoveryThemeStage,
    RecoveryThemeDirection,
    RecoveryThemeConfidence,
)


class RecoveryThemeEngine:
    """
    Institutional engine for identifying coherent recovery
    themes across explicitly supplied recovery clusters.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        assessments: List[RecoveryClusterAssessment],
        theme_id: str = "",
        theme_name: str = "",
        theme_type: RecoveryThemeType = (
            RecoveryThemeType.UNKNOWN
        ),
    ) -> RecoveryThemeAssessment:

        result = RecoveryThemeAssessment()

        result.theme_id = theme_id
        result.theme_name = theme_name
        result.theme_type = theme_type

        # --------------------------------------------------
        # Empty input
        # --------------------------------------------------

        if not assessments:

            result.stage = (
                RecoveryThemeStage.UNKNOWN
            )

            result.direction = (
                RecoveryThemeDirection.UNKNOWN
            )

            result.confidence_level = (
                RecoveryThemeConfidence.UNKNOWN
            )

            result.warnings.append(
                "No recovery cluster assessments supplied."
            )

            return result

        # ==================================================
        # CLUSTER POPULATION
        # ==================================================

        result.cluster_count = len(
            assessments
        )

        result.independent_clusters = len(
            {
                assessment.cluster_id
                for assessment in assessments
                if assessment.cluster_id
            }
        )

        result.cluster_ids = sorted(
            {
                assessment.cluster_id
                for assessment in assessments
                if assessment.cluster_id
            }
        )

        result.cluster_names = sorted(
            {
                assessment.cluster_name
                for assessment in assessments
                if assessment.cluster_name
            }
        )

        # ==================================================
        # RECOVERY COUNTS
        # ==================================================

        for assessment in assessments:

            if (
                assessment.supporting_assessments
                > 0
            ):
                result.recovering_cluster_count += 1

            if (
                assessment.confirmed_recovery_cluster
            ):
                result.confirmed_cluster_count += 1

            if (
                assessment.stabilizing_assessments
                > 0
            ):
                result.stabilizing_cluster_count += 1

            if (
                assessment.deteriorating_assessments
                > 0
            ):
                result.deteriorating_cluster_count += 1

        # ==================================================
        # BREADTH
        # ==================================================

        result.recovery_breadth = (
            RecoveryThemeEngine._percentage(
                result.recovering_cluster_count,
                result.cluster_count,
            )
        )

        result.confirmed_recovery_breadth = (
            RecoveryThemeEngine._percentage(
                result.confirmed_cluster_count,
                result.cluster_count,
            )
        )

        # ==================================================
        # EVIDENCE
        # ==================================================

        result.independent_sources = sum(
            assessment.independent_sources
            for assessment in assessments
        )

        result.independent_signals = sum(
            assessment.independent_signals
            for assessment in assessments
        )

        # ==================================================
        # TEMPORAL SUPPORT
        # ==================================================

        result.temporal_support = (
            RecoveryThemeEngine._average(
                [
                    assessment.temporal_score
                    for assessment in assessments
                ]
            )
        )

        result.persistence_score = (
            RecoveryThemeEngine._average(
                [
                    assessment.persistence_breadth
                    for assessment in assessments
                ]
            )
        )

        result.inflection_score = (
            RecoveryThemeEngine._average(
                [
                    assessment.inflection_breadth
                    for assessment in assessments
                ]
            )
        )

        result.reversal_score = (
            RecoveryThemeEngine._average(
                [
                    assessment.reversal_breadth
                    for assessment in assessments
                ]
            )
        )

        # ==================================================
        # CONTRADICTION
        # ==================================================

        result.contradiction_score = (
            RecoveryThemeEngine._average(
                [
                    assessment.contradiction_score
                    for assessment in assessments
                ]
            )
        )

        # ==================================================
        # COHERENCE
        # ==================================================

        result.coherence_score = (
            RecoveryThemeEngine._coherence(
                assessments
            )
        )

        result.cross_cluster_consistency = (
            result.coherence_score
        )

        result.mechanism_consistency = (
            result.coherence_score
        )

        # ==================================================
        # STAGE
        # ==================================================

        result.stage = (
            RecoveryThemeEngine._stage(
                result
            )
        )

        # ==================================================
        # DIRECTION
        # ==================================================

        result.direction = (
            RecoveryThemeEngine._direction(
                result
            )
        )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        result.confidence = (
            RecoveryThemeEngine._confidence(
                result
            )
        )

        result.confidence_level = (
            RecoveryThemeEngine._confidence_level(
                result.confidence
            )
        )

        # ==================================================
        # REASONING
        # ==================================================

        RecoveryThemeEngine._build_reasons(
            result
        )

        return result

    # ======================================================
    # PERCENTAGE
    # ======================================================

    @staticmethod
    def _percentage(
        numerator: int,
        denominator: int,
    ) -> float:

        if denominator <= 0:
            return 0.0

        return max(
            0.0,
            min(
                100.0,
                numerator
                / denominator
                * 100.0,
            ),
        )

    # ======================================================
    # AVERAGE
    # ======================================================

    @staticmethod
    def _average(
        values: List[float],
    ) -> float:

        if not values:
            return 0.0

        return max(
            0.0,
            min(
                100.0,
                sum(values)
                / len(values),
            ),
        )

    # ======================================================
    # COHERENCE
    # ======================================================

    @staticmethod
    def _coherence(
        assessments: List[
            RecoveryClusterAssessment
        ],
    ) -> float:

        if not assessments:
            return 0.0

        scores = []

        for assessment in assessments:

            if hasattr(
                assessment,
                "coherence_score",
            ):
                scores.append(
                    assessment.coherence_score
                )

            elif hasattr(
                assessment,
                "coherence",
            ):
                scores.append(
                    assessment.coherence
                )

        return RecoveryThemeEngine._average(
            scores
        )

    # ======================================================
    # STAGE
    # ======================================================

    @staticmethod
    def _stage(
        result: RecoveryThemeAssessment,
    ) -> RecoveryThemeStage:

        # --------------------------------------------------
        # No population
        # --------------------------------------------------

        if result.cluster_count == 0:
            return RecoveryThemeStage.UNKNOWN

        # --------------------------------------------------
        # Reversal
        # --------------------------------------------------

        if (
            result.deteriorating_cluster_count
            > result.recovering_cluster_count
            and result.deteriorating_cluster_count
            > 0
        ):
            return RecoveryThemeStage.REVERSING

        # --------------------------------------------------
        # STRUCTURAL
        #
        # Five clusters can establish a validated theme.
        # Six or more are required before calling it
        # structural.
        # --------------------------------------------------

        if (
            result.cluster_count >= 6
            and result.recovery_breadth >= 80.0
            and result.confirmed_recovery_breadth >= 60.0
            and result.coherence_score >= 70.0
            and result.temporal_support >= 60.0
        ):
            return RecoveryThemeStage.STRUCTURAL

        # --------------------------------------------------
        # VALIDATED
        # --------------------------------------------------

        if (
            result.cluster_count >= 4
            and result.recovery_breadth >= 70.0
            and result.confirmed_recovery_breadth >= 40.0
            and result.coherence_score >= 60.0
        ):
            return RecoveryThemeStage.VALIDATED

        # --------------------------------------------------
        # BROAD
        # --------------------------------------------------

        if (
            result.cluster_count >= 3
            and result.recovery_breadth >= 60.0
            and result.coherence_score >= 50.0
        ):
            return RecoveryThemeStage.BROAD

        # --------------------------------------------------
        # DEVELOPING
        # --------------------------------------------------

        if (
            result.cluster_count >= 2
            and result.recovery_breadth >= 40.0
        ):
            return RecoveryThemeStage.DEVELOPING

        # --------------------------------------------------
        # EMERGING
        # --------------------------------------------------

        if result.recovery_breadth > 0.0:
            return RecoveryThemeStage.EMERGING

        return RecoveryThemeStage.UNKNOWN

    # ======================================================
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        result: RecoveryThemeAssessment,
    ) -> RecoveryThemeDirection:

        if result.cluster_count == 0:
            return RecoveryThemeDirection.UNKNOWN

        if (
            result.deteriorating_cluster_count
            > result.recovering_cluster_count
        ):
            return RecoveryThemeDirection.NEGATIVE

        if (
            result.recovery_breadth >= 60.0
            and result.confirmed_recovery_breadth >= 30.0
        ):
            return RecoveryThemeDirection.POSITIVE

        if (
            result.recovery_breadth >= 40.0
        ):
            return RecoveryThemeDirection.MIXED

        if (
            result.recovery_breadth > 0.0
        ):
            return RecoveryThemeDirection.STABLE

        return RecoveryThemeDirection.UNKNOWN

    # ======================================================
    # CONFIDENCE
    # ======================================================

    @staticmethod
    def _confidence(
        result: RecoveryThemeAssessment,
    ) -> float:

        confidence = (
            result.recovery_breadth * 0.30
            + result.confirmed_recovery_breadth * 0.20
            + result.coherence_score * 0.25
            + result.temporal_support * 0.15
            + (
                100.0
                - result.contradiction_score
            ) * 0.10
        )

        return max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

    # ======================================================
    # CONFIDENCE LEVEL
    # ======================================================

    @staticmethod
    def _confidence_level(
        confidence: float,
    ) -> RecoveryThemeConfidence:

        if confidence >= 85.0:
            return RecoveryThemeConfidence.VERY_HIGH

        if confidence >= 70.0:
            return RecoveryThemeConfidence.HIGH

        if confidence >= 50.0:
            return RecoveryThemeConfidence.MODERATE

        if confidence > 0.0:
            return RecoveryThemeConfidence.LOW

        return RecoveryThemeConfidence.UNKNOWN

    # ======================================================
    # REASONING
    # ======================================================

    @staticmethod
    def _build_reasons(
        result: RecoveryThemeAssessment,
    ) -> None:

        result.reasons.append(
            f"{result.cluster_count} recovery clusters "
            "were evaluated."
        )

        if (
            result.recovering_cluster_count
            > 0
        ):

            result.reasons.append(
                f"{result.recovering_cluster_count} "
                "clusters show recovery."
            )

        if (
            result.confirmed_cluster_count
            > 0
        ):

            result.reasons.append(
                f"{result.confirmed_cluster_count} "
                "clusters show confirmed recovery."
            )

        if (
            result.recovery_breadth
            >= 60.0
        ):

            result.reasons.append(
                "Recovery is broad across the "
                "defined cluster universe."
            )

        if (
            result.coherence_score
            >= 60.0
        ):

            result.reasons.append(
                "Recovery clusters exhibit meaningful "
                "economic coherence."
            )

        if (
            result.temporal_support
            >= 60.0
        ):

            result.reasons.append(
                "Temporal evidence supports the "
                "recovery theme."
            )

        if (
            result.contradiction_score
            >= 30.0
        ):

            result.warnings.append(
                "Contradictory evidence is material."
            )

        if (
            result.stage
            == RecoveryThemeStage.REVERSING
        ):

            result.warnings.append(
                "The recovery theme is showing "
                "signs of reversal."
            )

        if (
            result.stage
            == RecoveryThemeStage.EMERGING
        ):

            result.reasons.append(
                "An emerging recovery theme is visible."
            )

        if (
            result.stage
            == RecoveryThemeStage.DEVELOPING
        ):

            result.reasons.append(
                "The recovery theme is developing "
                "across multiple clusters."
            )

        if (
            result.stage
            == RecoveryThemeStage.BROAD
        ):

            result.reasons.append(
                "The recovery theme is broad-based."
            )

        if (
            result.stage
            == RecoveryThemeStage.VALIDATED
        ):

            result.reasons.append(
                "The recovery theme has meaningful "
                "cross-cluster validation."
            )

        if (
            result.stage
            == RecoveryThemeStage.STRUCTURAL
        ):

            result.reasons.append(
                "The recovery theme shows broad, "
                "persistent and coherent characteristics."
            )


__all__ = [
    "RecoveryThemeEngine",
]