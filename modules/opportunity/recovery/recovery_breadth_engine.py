"""
EIOS
Everest Investment Operating System

Recovery Breadth Engine

Purpose:
Aggregates RecoveryClusterAssessment records and determines
whether recovery is isolated, broadening, broadly established,
or contracting across an explicitly defined recovery universe.

Architecture:

Recovery Signals
        ↓
Recovery Detection
        ↓
Recovery Cluster
        ↓
Recovery Breadth
        ↓
Sector / Theme Recovery Intelligence
        ↓
Opportunity Intelligence

Design Principles:
- Explicit cluster assessments only.
- No automatic sector guessing.
- No valuation.
- No opportunity scoring.
- No investment recommendation.
- No company-specific investment decision.
- Input objects are never mutated.
- Deterministic.
- Transparent reasoning.
- Missing information is not treated as negative evidence.

Important Institutional Rule:
- Recovery strength within one cluster is NOT equivalent to
  broad recovery across the universe.
- A single assessed cluster is always classified as ISOLATED.
- Broadening may occur before recovery is confirmed.
"""


from typing import List

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
)

from modules.opportunity.recovery.recovery_breadth_assessment import (
    RecoveryBreadthAssessment,
    RecoveryBreadthDirection,
    RecoveryBreadthStage,
    RecoveryBreadthType,
    RecoveryLeadershipState,
)


class RecoveryBreadthEngine:
    """
    Institutional engine for assessing recovery breadth.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        assessments: List[RecoveryClusterAssessment],
        breadth_id: str = "",
        breadth_name: str = "",
        breadth_type: RecoveryBreadthType = (
            RecoveryBreadthType.UNKNOWN
        ),
        total_entities: int = 0,
        previous_breadth: float = 0.0,
    ) -> RecoveryBreadthAssessment:
        """
        Assess recovery breadth across explicitly supplied
        recovery cluster assessments.

        No input assessment is mutated.
        """

        result = RecoveryBreadthAssessment()

        # --------------------------------------------------
        # Identity
        # --------------------------------------------------

        result.breadth_id = breadth_id
        result.breadth_name = breadth_name
        result.breadth_type = breadth_type

        result.total_entities = max(
            0,
            total_entities,
        )

        result.previous_breadth = max(
            0.0,
            min(
                100.0,
                previous_breadth,
            ),
        )

        # --------------------------------------------------
        # Empty State
        # --------------------------------------------------

        if not assessments:

            result.stage = (
                RecoveryBreadthStage.INSUFFICIENT
            )

            result.direction = (
                RecoveryBreadthDirection.UNKNOWN
            )

            result.leadership_state = (
                RecoveryLeadershipState.UNKNOWN
            )

            result.warnings.append(
                "No recovery cluster assessments supplied."
            )

            return result

        # --------------------------------------------------
        # Population
        # --------------------------------------------------

        result.assessed_entities = len(
            assessments
        )

        # --------------------------------------------------
        # Aggregate Assessment Counts
        # --------------------------------------------------

        for assessment in assessments:

            if (
                assessment.supporting_assessments
                > 0
            ):
                result.improving_entities += 1

            elif (
                assessment.stabilizing_assessments
                > 0
            ):
                result.stabilizing_entities += 1

            elif (
                assessment.deteriorating_assessments
                > 0
            ):
                result.deteriorating_entities += 1

            else:
                result.insufficient_entities += 1

            # ----------------------------------------------
            # Early Inflection
            # ----------------------------------------------

            if hasattr(
                assessment,
                "early_inflection_breadth",
            ):

                if (
                    assessment.early_inflection_breadth
                    > 0
                ):
                    result.early_inflection_entities += 1

            elif (
                assessment.inflection_breadth
                > 0
            ):

                result.early_inflection_entities += 1

            # ----------------------------------------------
            # Early Recovery
            # ----------------------------------------------

            if (
                assessment.early_recovery_cluster
            ):
                result.early_recovery_entities += 1

            # ----------------------------------------------
            # Confirmed Recovery
            # ----------------------------------------------

            if (
                assessment.confirmed_recovery_cluster
            ):
                result.confirmed_recovery_entities += 1

        # --------------------------------------------------
        # Unchanged
        # --------------------------------------------------

        result.unchanged_entities = max(
            0,
            result.assessed_entities
            - result.improving_entities
            - result.stabilizing_entities
            - result.deteriorating_entities
            - result.insufficient_entities,
        )

        # ==================================================
        # BREADTH CALCULATIONS
        # ==================================================

        result.improvement_breadth = (
            RecoveryBreadthEngine._percentage(
                result.improving_entities,
                result.assessed_entities,
            )
        )

        result.stabilization_breadth = (
            RecoveryBreadthEngine._percentage(
                result.stabilizing_entities,
                result.assessed_entities,
            )
        )

        result.recovery_breadth = (
            RecoveryBreadthEngine._percentage(
                (
                    result.improving_entities
                    + result.stabilizing_entities
                ),
                result.assessed_entities,
            )
        )

        result.confirmed_recovery_breadth = (
            RecoveryBreadthEngine._percentage(
                result.confirmed_recovery_entities,
                result.assessed_entities,
            )
        )

        result.deterioration_breadth = (
            RecoveryBreadthEngine._percentage(
                result.deteriorating_entities,
                result.assessed_entities,
            )
        )

        result.contradiction_breadth = (
            RecoveryBreadthEngine._average(
                [
                    assessment.contradiction_score
                    for assessment in assessments
                ]
            )
        )

        # ==================================================
        # CURRENT BREADTH
        # ==================================================

        result.current_breadth = (
            result.recovery_breadth
        )

        result.breadth_change = (
            result.current_breadth
            - result.previous_breadth
        )

        # ==================================================
        # BREADTH DIRECTION
        # ==================================================

        result.direction = (
            RecoveryBreadthEngine._direction(
                result
            )
        )

        # ==================================================
        # BREADTH STATE
        # ==================================================

        result.breadth_expanding = (
            result.direction
            == RecoveryBreadthDirection.EXPANDING
        )

        result.breadth_stable = (
            result.direction
            == RecoveryBreadthDirection.STABLE
        )

        result.breadth_contracting = (
            result.direction
            == RecoveryBreadthDirection.CONTRACTING
        )

        # ==================================================
        # LEADERSHIP
        # ==================================================

        RecoveryBreadthEngine._leadership(
            result,
            assessments,
        )

        # ==================================================
        # EVIDENCE
        #
        # Evidence must be calculated BEFORE stage
        # classification because stage thresholds depend
        # on corroboration_score.
        # ==================================================

        result.independent_sources = sum(
            assessment.independent_sources
            for assessment in assessments
        )

        result.independent_signals = sum(
            assessment.independent_signals
            for assessment in assessments
        )

        result.independent_domains = sum(
            assessment.independent_domains
            for assessment in assessments
        )

        result.temporal_support = (
            RecoveryBreadthEngine._average(
                [
                    assessment.temporal_score
                    for assessment in assessments
                ]
            )
        )

        result.corroboration_score = (
            RecoveryBreadthEngine._average(
                [
                    assessment.corroboration_score
                    for assessment in assessments
                ]
            )
        )

        result.contradiction_score = (
            RecoveryBreadthEngine._average(
                [
                    assessment.contradiction_score
                    for assessment in assessments
                ]
            )
        )

        # ==================================================
        # BREADTH CLASSIFICATION
        # ==================================================

        result.stage = (
            RecoveryBreadthEngine._stage(
                result
            )
        )

        # ==================================================
        # SIGNALS
        # ==================================================

        result.early_breadth_signal = (
            result.stage
            == RecoveryBreadthStage.EARLY_BREADTH
        )

        result.recovery_breadth_signal = (
            result.stage
            in (
                RecoveryBreadthStage.BROADENING,
                RecoveryBreadthStage.BROAD_RECOVERY,
                RecoveryBreadthStage.SATURATED,
            )
        )

        result.confirmed_breadth_signal = (
            result.stage
            in (
                RecoveryBreadthStage.BROAD_RECOVERY,
                RecoveryBreadthStage.SATURATED,
            )
        )

        result.broad_based = (
            result.recovery_breadth >= 60.0
            and result.assessed_entities >= 3
        )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        result.confidence = (
            RecoveryBreadthEngine._confidence(
                result
            )
        )

        # ==================================================
        # REASONING
        # ==================================================

        RecoveryBreadthEngine._build_reasons(
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
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        result: RecoveryBreadthAssessment,
    ) -> RecoveryBreadthDirection:

        change = result.breadth_change

        # --------------------------------------------------
        # Strong expansion
        # --------------------------------------------------

        if change >= 10.0:
            return RecoveryBreadthDirection.EXPANDING

        # --------------------------------------------------
        # Meaningful contraction
        # --------------------------------------------------

        if change <= -10.0:
            return RecoveryBreadthDirection.CONTRACTING

        # --------------------------------------------------
        # New recovery from zero baseline
        # --------------------------------------------------

        if (
            result.previous_breadth == 0.0
            and result.current_breadth > 0.0
        ):
            return RecoveryBreadthDirection.EXPANDING

        # --------------------------------------------------
        # Stable meaningful breadth
        # --------------------------------------------------

        if (
            abs(change) < 10.0
            and result.current_breadth >= 20.0
        ):
            return RecoveryBreadthDirection.STABLE

        return RecoveryBreadthDirection.MIXED

    # ======================================================
    # LEADERSHIP
    # ======================================================

    @staticmethod
    def _leadership(
        result: RecoveryBreadthAssessment,
        assessments: List[
            RecoveryClusterAssessment
        ],
    ) -> None:

        leaders = []

        for assessment in assessments:

            if (
                assessment.early_recovery_cluster
                or assessment.confirmed_recovery_cluster
            ):

                if assessment.cluster_id:

                    leaders.append(
                        assessment.cluster_id
                    )

        result.leading_entities = sorted(
            set(leaders)
        )

        result.leader_count = len(
            result.leading_entities
        )

        result.leader_breadth = (
            RecoveryBreadthEngine._percentage(
                result.leader_count,
                result.assessed_entities,
            )
        )

        if result.leader_count == 0:

            result.leadership_state = (
                RecoveryLeadershipState.NO_LEADERSHIP
            )

        elif result.leader_breadth < 25.0:

            result.leadership_state = (
                RecoveryLeadershipState.EARLY_LEADERS
            )

        elif result.leader_breadth < 60.0:

            result.leadership_state = (
                RecoveryLeadershipState.CLEAR_LEADERS
            )

        else:

            result.leadership_state = (
                RecoveryLeadershipState.BROAD_LEADERSHIP
            )

    # ======================================================
    # STAGE
    # ======================================================

    @staticmethod
    def _stage(
        result: RecoveryBreadthAssessment,
    ) -> RecoveryBreadthStage:

        # --------------------------------------------------
        # No population
        # --------------------------------------------------

        if result.assessed_entities == 0:
            return RecoveryBreadthStage.INSUFFICIENT

        # --------------------------------------------------
        # Single cluster
        #
        # A single cluster can never establish broad
        # recovery.
        # --------------------------------------------------

        if result.assessed_entities == 1:

            if result.current_breadth > 0.0:
                return RecoveryBreadthStage.ISOLATED

            return RecoveryBreadthStage.INSUFFICIENT

        # --------------------------------------------------
        # Contracting
        # --------------------------------------------------

        if (
            result.breadth_contracting
            and result.current_breadth >= 20.0
        ):
            return RecoveryBreadthStage.CONTRACTING

        # --------------------------------------------------
        # SATURATED
        #
        # Very broad recovery with substantial confirmation.
        # --------------------------------------------------

        if (
            result.assessed_entities >= 9
            and result.current_breadth >= 85.0
            and result.confirmed_recovery_breadth >= 60.0
            and result.corroboration_score >= 60.0
        ):
            return RecoveryBreadthStage.SATURATED

        # --------------------------------------------------
        # BROAD RECOVERY
        #
        # Broad recovery requires meaningful confirmation.
        # --------------------------------------------------

        if (
            result.assessed_entities >= 5
            and result.current_breadth >= 70.0
            and result.confirmed_recovery_breadth >= 40.0
        ):
            return RecoveryBreadthStage.BROAD_RECOVERY

        # --------------------------------------------------
        # BROADENING
        #
        # Institutional rule:
        #
        # Broadening requires a sufficiently meaningful
        # assessed population. Four or fewer clusters are
        # not enough to establish broadening across the
        # universe.
        #
        # Confirmation is NOT required.
        # --------------------------------------------------

        if (
            result.assessed_entities >= 5
            and result.current_breadth >= 50.0
            and result.breadth_expanding
            and result.corroboration_score >= 40.0
        ):
            return RecoveryBreadthStage.BROADENING

        # --------------------------------------------------
        # EARLY BREADTH
        #
        # Multiple clusters are beginning to improve, but
        # the evidence base is still too small to establish
        # broadening.
        #
        # This stage intentionally covers smaller populations
        # and emerging breadth before the universe is large
        # enough to call the recovery BROADENING.
        # --------------------------------------------------

        if (
            result.assessed_entities >= 3
            and result.current_breadth >= 25.0
            and (
                result.breadth_expanding
                or result.early_recovery_entities >= 1
                or result.early_inflection_entities >= 1
            )
        ):
            return RecoveryBreadthStage.EARLY_BREADTH

        # --------------------------------------------------
        # ISOLATED
        # --------------------------------------------------

        if result.current_breadth > 0.0:
            return RecoveryBreadthStage.ISOLATED

        return RecoveryBreadthStage.INSUFFICIENT

    # ======================================================
    # CONFIDENCE
    # ======================================================

    @staticmethod
    def _confidence(
        result: RecoveryBreadthAssessment,
    ) -> float:

        confidence = (
            result.current_breadth * 0.30
            + result.corroboration_score * 0.25
            + result.temporal_support * 0.20
            + result.leader_breadth * 0.10
            + (
                100.0
                - result.contradiction_score
            ) * 0.15
        )

        # --------------------------------------------------
        # Small population confidence penalty
        # --------------------------------------------------

        if result.assessed_entities == 1:

            confidence *= 0.50

        elif result.assessed_entities == 2:

            confidence *= 0.75

        return max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

    # ======================================================
    # REASONING
    # ======================================================

    @staticmethod
    def _build_reasons(
        result: RecoveryBreadthAssessment,
    ) -> None:

        result.reasons.append(
            f"{result.assessed_entities} recovery "
            "cluster assessments were evaluated."
        )

        if result.improving_entities > 0:

            result.reasons.append(
                f"{result.improving_entities} clusters "
                "show improvement."
            )

        if result.stabilizing_entities > 0:

            result.reasons.append(
                f"{result.stabilizing_entities} clusters "
                "show stabilization."
            )

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        if result.breadth_expanding:

            result.reasons.append(
                "Recovery breadth is expanding."
            )

        elif result.breadth_stable:

            result.reasons.append(
                "Recovery breadth is currently stable."
            )

        elif result.breadth_contracting:

            result.warnings.append(
                "Recovery breadth is contracting."
            )

        # --------------------------------------------------
        # Recovery stages
        # --------------------------------------------------

        if result.early_recovery_entities > 0:

            result.reasons.append(
                f"{result.early_recovery_entities} clusters "
                "have reached early recovery."
            )

        if result.confirmed_recovery_entities > 0:

            result.reasons.append(
                f"{result.confirmed_recovery_entities} clusters "
                "have confirmed recovery."
            )

        # --------------------------------------------------
        # Broad based
        # --------------------------------------------------

        if result.broad_based:

            result.reasons.append(
                "Recovery has become broad-based."
            )

        # --------------------------------------------------
        # Leadership
        # --------------------------------------------------

        if (
            result.leadership_state
            == RecoveryLeadershipState.EARLY_LEADERS
        ):

            result.reasons.append(
                "A small group of early recovery leaders "
                "is emerging."
            )

        if (
            result.leadership_state
            == RecoveryLeadershipState.CLEAR_LEADERS
        ):

            result.reasons.append(
                "Clear recovery leaders are visible."
            )

        if (
            result.leadership_state
            == RecoveryLeadershipState.BROAD_LEADERSHIP
        ):

            result.reasons.append(
                "Recovery leadership is broad-based."
            )

        # --------------------------------------------------
        # Contradiction
        # --------------------------------------------------

        if (
            result.contradiction_score
            >= 30.0
        ):

            result.warnings.append(
                "Contradictory recovery evidence "
                "is material."
            )

        # --------------------------------------------------
        # Stage explanation
        # --------------------------------------------------

        if (
            result.stage
            == RecoveryBreadthStage.ISOLATED
        ):

            result.warnings.append(
                "Improvement remains isolated and does "
                "not yet represent broad recovery."
            )

        if (
            result.stage
            == RecoveryBreadthStage.EARLY_BREADTH
        ):

            result.reasons.append(
                "Early breadth expansion is visible, "
                "but recovery is not yet broad."
            )

        if (
            result.stage
            == RecoveryBreadthStage.BROADENING
        ):

            result.reasons.append(
                "Recovery is spreading across a meaningful "
                "portion of the assessed universe."
            )

        if (
            result.stage
            == RecoveryBreadthStage.BROAD_RECOVERY
        ):

            result.reasons.append(
                "Recovery breadth is broad and supported "
                "by meaningful confirmation."
            )

        if (
            result.stage
            == RecoveryBreadthStage.SATURATED
        ):

            result.reasons.append(
                "Recovery is widespread across the "
                "assessed universe."
            )

        if (
            result.stage
            == RecoveryBreadthStage.CONTRACTING
        ):

            result.warnings.append(
                "Previously established recovery breadth "
                "is narrowing."
            )


__all__ = [
    "RecoveryBreadthEngine",
]