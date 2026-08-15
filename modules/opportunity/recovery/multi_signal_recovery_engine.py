"""
EIOS
Everest Investment Operating System

Multi-Signal Recovery Engine

Purpose:
Aggregates independent RecoveryEvidence records and determines
whether recovery evidence is isolated, stabilizing, broad,
or confirmed.

Architecture:

RecoveryEvidence[]
        ↓
Multi-Signal Recovery Engine
        ↓
Multi-Signal Recovery Assessment
        ↓
Catalyst / Opportunity Intelligence

Design Principles:
- No valuation.
- No opportunity scoring.
- No investment recommendation.
- No persistence.
- No company-specific logic.
- No sector-specific logic.
- Duplicate source observations are not independent evidence.
- Contradictory evidence reduces confidence.
- Models remain passive.
- Deterministic output.
"""

from typing import List

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryStage,
    RecoveryDirection,
)

from modules.opportunity.recovery.recovery_evidence import (
    RecoveryEvidence,
)

from modules.opportunity.recovery.multi_signal_recovery_assessment import (
    MultiSignalRecoveryAssessment,
    MultiSignalRecoveryDirection,
    MultiSignalRecoveryStage,
)


# ==========================================================
# MULTI-SIGNAL RECOVERY ENGINE
# ==========================================================


class MultiSignalRecoveryEngine:
    """
    Aggregates RecoveryEvidence into a higher-order
    multi-signal recovery assessment.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        evidence: List[RecoveryEvidence],
    ) -> MultiSignalRecoveryAssessment:
        """
        Aggregate recovery evidence.

        The input evidence objects are never mutated.
        """

        result = (
            MultiSignalRecoveryAssessment()
        )

        if not evidence:
            result.warnings.append(
                "No recovery evidence supplied."
            )

            return result

        # --------------------------------------------------
        # Basic Counts
        # --------------------------------------------------

        result.total_signals = len(
            evidence
        )

        # --------------------------------------------------
        # Direction Counts
        # --------------------------------------------------

        (
            result.improving_signals,
            result.stabilizing_signals,
            result.deteriorating_signals,
            result.neutral_signals,
        ) = (
            MultiSignalRecoveryEngine
            ._direction_counts(evidence)
        )

        # --------------------------------------------------
        # Supporting / Contradictory IDs
        # --------------------------------------------------

        (
            result.supporting_signal_ids,
            result.contradictory_signal_ids,
        ) = (
            MultiSignalRecoveryEngine
            ._signal_ids(evidence)
        )

        # --------------------------------------------------
        # Breadth
        # --------------------------------------------------

        result.breadth_score = (
            MultiSignalRecoveryEngine
            ._breadth_score(evidence)
        )

        # --------------------------------------------------
        # Corroboration
        # --------------------------------------------------

        result.corroboration_score = (
            MultiSignalRecoveryEngine
            ._corroboration_score(evidence)
        )

        # --------------------------------------------------
        # Temporal Support
        # --------------------------------------------------

        result.temporal_score = (
            MultiSignalRecoveryEngine
            ._temporal_score(evidence)
        )

        # --------------------------------------------------
        # Consistency
        # --------------------------------------------------

        result.consistency_score = (
            MultiSignalRecoveryEngine
            ._consistency_score(evidence)
        )

        # --------------------------------------------------
        # Contradiction
        # --------------------------------------------------

        result.contradiction_score = (
            MultiSignalRecoveryEngine
            ._contradiction_score(evidence)
        )

        # --------------------------------------------------
        # Characteristics
        # --------------------------------------------------

        result.isolated_improvement = (
            MultiSignalRecoveryEngine
            ._isolated_improvement(evidence)
        )

        result.broad_stabilization = (
            MultiSignalRecoveryEngine
            ._broad_stabilization(evidence)
        )

        result.broad_inflection = (
            MultiSignalRecoveryEngine
            ._broad_inflection(evidence)
        )

        result.broad_reversal = (
            MultiSignalRecoveryEngine
            ._broad_reversal(evidence)
        )

        result.persistent_recovery = (
            MultiSignalRecoveryEngine
            ._persistent_recovery(evidence)
        )

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        result.direction = (
            MultiSignalRecoveryEngine
            ._direction(result)
        )

        # --------------------------------------------------
        # Stage
        # --------------------------------------------------

        result.stage = (
            MultiSignalRecoveryEngine
            ._stage(result)
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = (
            MultiSignalRecoveryEngine
            ._confidence(result)
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        MultiSignalRecoveryEngine._build_reasons(
            result
        )

        return result

    # ======================================================
    # DIRECTION COUNTS
    # ======================================================

    @staticmethod
    def _direction_counts(
        evidence: List[RecoveryEvidence],
    ):
        improving = 0
        stabilizing = 0
        deteriorating = 0
        neutral = 0

        for item in evidence:

            assessment = (
                item.recovery_assessment
            )

            if assessment is None:
                neutral += 1
                continue

            if (
                assessment.direction
                == RecoveryDirection.POSITIVE
            ):
                improving += 1

            elif (
                assessment.direction
                == RecoveryDirection.STABILIZING
            ):
                stabilizing += 1

            elif (
                assessment.direction
                == RecoveryDirection.NEGATIVE
            ):
                deteriorating += 1

            else:
                neutral += 1

        return (
            improving,
            stabilizing,
            deteriorating,
            neutral,
        )

    # ======================================================
    # SIGNAL IDS
    # ======================================================

    @staticmethod
    def _signal_ids(
        evidence: List[RecoveryEvidence],
    ):
        supporting = []
        contradictory = []

        for item in evidence:

            assessment = (
                item.recovery_assessment
            )

            if assessment is None:
                continue

            if (
                assessment.direction
                in (
                    RecoveryDirection.POSITIVE,
                    RecoveryDirection.STABILIZING,
                )
            ):
                if (
                    item.signal_id
                    and item.signal_id
                    not in supporting
                ):
                    supporting.append(
                        item.signal_id
                    )

            if (
                assessment.direction
                == RecoveryDirection.NEGATIVE
            ):
                if (
                    item.signal_id
                    and item.signal_id
                    not in contradictory
                ):
                    contradictory.append(
                        item.signal_id
                    )

        return (
            supporting,
            contradictory,
        )

    # ======================================================
    # BREADTH
    # ======================================================

    @staticmethod
    def _breadth_score(
        evidence: List[RecoveryEvidence],
    ) -> float:
        """
        Measure the proportion of evidence showing
        stabilization or improvement.

        Duplicate source records do not increase breadth.
        """

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        if not valid:
            return 0.0

        unique_source_groups = {}

        for item in valid:

            key = (
                item.source_key
                or item.signal_id
            )

            if key not in unique_source_groups:
                unique_source_groups[key] = item

        independent = list(
            unique_source_groups.values()
        )

        if not independent:
            return 0.0

        positive = sum(
            1
            for item in independent
            if item.recovery_assessment.direction
            in (
                RecoveryDirection.POSITIVE,
                RecoveryDirection.STABILIZING,
            )
        )

        return min(
            100.0,
            positive
            / len(independent)
            * 100.0,
        )

    # ======================================================
    # CORROBORATION
    # ======================================================

    @staticmethod
    def _corroboration_score(
        evidence: List[RecoveryEvidence],
    ) -> float:
        """
        Measure independent source corroboration.
        """

        sources = {
            item.source_key
            for item in evidence
            if item.source_key
        }

        if not sources:
            return 0.0

        return min(
            100.0,
            len(sources) * 20.0,
        )

    # ======================================================
    # TEMPORAL SCORE
    # ======================================================

    @staticmethod
    def _temporal_score(
        evidence: List[RecoveryEvidence],
    ) -> float:

        values = []

        for item in evidence:

            assessment = (
                item.recovery_assessment
            )

            if assessment is None:
                continue

            values.append(
                assessment.temporal_support
            )

        if not values:
            return 0.0

        return (
            sum(values)
            / len(values)
        )

    # ======================================================
    # CONSISTENCY
    # ======================================================

    @staticmethod
    def _consistency_score(
        evidence: List[RecoveryEvidence],
    ) -> float:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        if not valid:
            return 0.0

        positive = sum(
            1
            for item in valid
            if item.recovery_assessment.direction
            == RecoveryDirection.POSITIVE
        )

        stabilizing = sum(
            1
            for item in valid
            if item.recovery_assessment.direction
            == RecoveryDirection.STABILIZING
        )

        negative = sum(
            1
            for item in valid
            if item.recovery_assessment.direction
            == RecoveryDirection.NEGATIVE
        )

        supportive = (
            positive
            + stabilizing
        )

        dominant = max(
            supportive,
            negative,
        )

        if dominant == 0:
            return 0.0

        return min(
            100.0,
            dominant
            / len(valid)
            * 100.0,
        )

    # ======================================================
    # CONTRADICTION
    # ======================================================

    @staticmethod
    def _contradiction_score(
        evidence: List[RecoveryEvidence],
    ) -> float:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        if not valid:
            return 0.0

        negative = sum(
            1
            for item in valid
            if item.recovery_assessment.direction
            == RecoveryDirection.NEGATIVE
        )

        return min(
            100.0,
            negative
            / len(valid)
            * 100.0,
        )

    # ======================================================
    # ISOLATED IMPROVEMENT
    # ======================================================

    @staticmethod
    def _isolated_improvement(
        evidence: List[RecoveryEvidence],
    ) -> bool:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        improving = [
            item
            for item in valid
            if item.recovery_assessment.direction
            == RecoveryDirection.POSITIVE
        ]

        return (
            len(improving) == 1
            and len(valid) >= 2
        )

    # ======================================================
    # BROAD STABILIZATION
    # ======================================================

    @staticmethod
    def _broad_stabilization(
        evidence: List[RecoveryEvidence],
    ) -> bool:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        if len(valid) < 3:
            return False

        supportive = sum(
            1
            for item in valid
            if item.recovery_assessment.stage
            in (
                RecoveryStage.STABILIZING,
                RecoveryStage.EARLY_INFLECTION,
                RecoveryStage.EARLY_RECOVERY,
                RecoveryStage.CONFIRMED_RECOVERY,
            )
        )

        return (
            supportive >= 3
            and supportive
            / len(valid)
            >= 0.60
        )

    # ======================================================
    # BROAD INFLECTION
    # ======================================================

    @staticmethod
    def _broad_inflection(
        evidence: List[RecoveryEvidence],
    ) -> bool:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        inflections = sum(
            1
            for item in valid
            if item.recovery_assessment.inflection_detected
            or item.recovery_assessment.reversal_detected
        )

        return (
            len(valid) >= 3
            and inflections >= 2
        )

    # ======================================================
    # BROAD REVERSAL
    # ======================================================

    @staticmethod
    def _broad_reversal(
        evidence: List[RecoveryEvidence],
    ) -> bool:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        reversals = sum(
            1
            for item in valid
            if item.recovery_assessment.reversal_detected
        )

        return (
            len(valid) >= 3
            and reversals >= 2
        )

    # ======================================================
    # PERSISTENT RECOVERY
    # ======================================================

    @staticmethod
    def _persistent_recovery(
        evidence: List[RecoveryEvidence],
    ) -> bool:

        valid = [
            item
            for item in evidence
            if item.recovery_assessment is not None
        ]

        persistent = sum(
            1
            for item in valid
            if item.recovery_assessment.persistence_detected
        )

        return (
            len(valid) >= 3
            and persistent >= 2
        )

    # ======================================================
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        result: MultiSignalRecoveryAssessment,
    ) -> MultiSignalRecoveryDirection:

        supportive = (
            result.improving_signals
            + result.stabilizing_signals
        )

        negative = (
            result.deteriorating_signals
        )

        if supportive == 0 and negative == 0:
            return (
                MultiSignalRecoveryDirection.UNKNOWN
            )

        if (
            supportive > 0
            and negative > 0
        ):
            if (
                supportive
                > negative
            ):
                return (
                    MultiSignalRecoveryDirection.POSITIVE
                )

            if (
                negative
                > supportive
            ):
                return (
                    MultiSignalRecoveryDirection.NEGATIVE
                )

            return (
                MultiSignalRecoveryDirection.MIXED
            )

        if supportive > 0:

            if (
                result.improving_signals
                > result.stabilizing_signals
            ):
                return (
                    MultiSignalRecoveryDirection.POSITIVE
                )

            return (
                MultiSignalRecoveryDirection.STABILIZING
            )

        return (
            MultiSignalRecoveryDirection.NEGATIVE
        )

    # ======================================================
    # STAGE
    # ======================================================

    @staticmethod
    def _stage(
        result: MultiSignalRecoveryAssessment,
    ) -> MultiSignalRecoveryStage:

        # --------------------------------------------------
        # No evidence
        # --------------------------------------------------

        if result.total_signals == 0:
            return (
                MultiSignalRecoveryStage
                .INSUFFICIENT_EVIDENCE
            )

        # --------------------------------------------------
        # Confirmed Broad Recovery
        # --------------------------------------------------

        if (
            result.total_signals >= 4
            and result.improving_signals >= 3
            and result.breadth_score >= 70.0
            and result.corroboration_score >= 60.0
            and result.consistency_score >= 70.0
            and result.temporal_score >= 60.0
            and result.broad_reversal
            and result.persistent_recovery
            and result.contradiction_score < 30.0
        ):
            return (
                MultiSignalRecoveryStage
                .CONFIRMED_BROAD_RECOVERY
            )

        # --------------------------------------------------
        # Early Broad Recovery
        # --------------------------------------------------

        if (
            result.total_signals >= 3
            and result.improving_signals >= 2
            and result.breadth_score >= 60.0
            and result.corroboration_score >= 40.0
            and (
                result.broad_inflection
                or result.broad_reversal
            )
        ):
            return (
                MultiSignalRecoveryStage
                .EARLY_BROAD_RECOVERY
            )

        # --------------------------------------------------
        # Broad Stabilization
        # --------------------------------------------------

        if result.broad_stabilization:
            return (
                MultiSignalRecoveryStage
                .BROAD_STABILIZATION
            )

        # --------------------------------------------------
        # Isolated Improvement
        # --------------------------------------------------

        if result.isolated_improvement:
            return (
                MultiSignalRecoveryStage
                .ISOLATED_IMPROVEMENT
            )

        # --------------------------------------------------
        # Insufficient Evidence
        # --------------------------------------------------

        return (
            MultiSignalRecoveryStage
            .INSUFFICIENT_EVIDENCE
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    @staticmethod
    def _confidence(
        result: MultiSignalRecoveryAssessment,
    ) -> float:

        confidence = (
            result.breadth_score * 0.25
            + result.corroboration_score * 0.20
            + result.temporal_score * 0.20
            + result.consistency_score * 0.20
            + (
                100.0
                - result.contradiction_score
            ) * 0.15
        )

        return max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

    # ======================================================
    # REASONS
    # ======================================================

    @staticmethod
    def _build_reasons(
        result: MultiSignalRecoveryAssessment,
    ) -> None:

        if result.total_signals > 0:
            result.reasons.append(
                f"{result.total_signals} recovery evidence "
                "records were evaluated."
            )

        if result.improving_signals > 0:
            result.reasons.append(
                f"{result.improving_signals} signals show "
                "positive recovery direction."
            )

        if result.stabilizing_signals > 0:
            result.reasons.append(
                f"{result.stabilizing_signals} signals show "
                "stabilization."
            )

        if result.breadth_score >= 60.0:
            result.reasons.append(
                "Recovery evidence has meaningful breadth."
            )

        if result.corroboration_score >= 40.0:
            result.reasons.append(
                "Multiple independent sources provide "
                "corroborating evidence."
            )

        if result.broad_inflection:
            result.reasons.append(
                "Multiple signals indicate directional "
                "inflection."
            )

        if result.broad_reversal:
            result.reasons.append(
                "Multiple signals indicate directional reversal."
            )

        if result.persistent_recovery:
            result.reasons.append(
                "Recovery characteristics show persistence "
                "across multiple signals."
            )

        if result.isolated_improvement:
            result.warnings.append(
                "Only one signal is improving; this is not "
                "sufficient evidence of broad recovery."
            )

        if result.contradiction_score > 0:
            result.warnings.append(
                "Deteriorating signals create contradictory "
                "evidence."
            )

        if result.contradiction_score >= 30.0:
            result.warnings.append(
                "Contradictory evidence is material and "
                "reduces recovery confidence."
            )

        if (
            result.stage
            == MultiSignalRecoveryStage.BROAD_STABILIZATION
        ):
            result.warnings.append(
                "Broad stabilization is not yet confirmed "
                "broad recovery."
            )

        if (
            result.stage
            == MultiSignalRecoveryStage.INSUFFICIENT_EVIDENCE
        ):
            result.warnings.append(
                "Evidence is insufficient to establish a "
                "broad recovery."
            )


__all__ = [
    "MultiSignalRecoveryEngine",
]