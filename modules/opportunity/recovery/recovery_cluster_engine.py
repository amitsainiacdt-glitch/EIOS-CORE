"""
EIOS
Everest Investment Operating System

Recovery Cluster Engine

Purpose:
Aggregates explicitly assigned RecoveryClusterEvidence records
and determines whether a coherent economic recovery cluster exists.

Architecture:

Recovery Evidence
        ↓
Recovery Cluster Evidence
        ↓
Recovery Cluster Engine
        ↓
Recovery Cluster Assessment
        ↓
Catalyst / Opportunity Intelligence

Design Principles:
- Cluster membership must already be explicit.
- No automatic sector guessing.
- No valuation.
- No opportunity scoring.
- No investment recommendation.
- No persistence.
- No company-specific investment logic.
- Duplicate source observations do not count as independent
  corroboration.
- Contradictory evidence reduces confidence.
- Input evidence is never mutated.
- Output is deterministic.
- Missing metadata is not treated as negative evidence.
"""

from typing import List

from modules.opportunity.recovery.recovery_assessment import (
    RecoveryDirection,
    RecoveryStage,
)

from modules.opportunity.recovery.recovery_cluster_evidence import (
    RecoveryClusterEvidence,
)

from modules.opportunity.recovery.recovery_cluster_assessment import (
    RecoveryClusterAssessment,
    RecoveryClusterDirection,
    RecoveryClusterStage,
)


class RecoveryClusterEngine:
    """
    Institutional engine for evaluating recovery clusters.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    @staticmethod
    def assess(
        evidence: List[RecoveryClusterEvidence],
    ) -> RecoveryClusterAssessment:
        """
        Assess a group of explicitly assigned recovery evidence.

        All records must belong to the same cluster.

        Input objects are never mutated.
        """

        result = RecoveryClusterAssessment()

        if not evidence:
            result.warnings.append(
                "No recovery cluster evidence supplied."
            )
            return result

        # --------------------------------------------------
        # Cluster Identity
        # --------------------------------------------------

        RecoveryClusterEngine._populate_identity(
            result,
            evidence,
        )

        # --------------------------------------------------
        # Basic Counts
        # --------------------------------------------------

        result.total_recovery_assessments = len(
            evidence
        )

        # --------------------------------------------------
        # Direction Counts
        # --------------------------------------------------

        RecoveryClusterEngine._populate_direction_counts(
            result,
            evidence,
        )

        # --------------------------------------------------
        # Independent Evidence
        # --------------------------------------------------

        RecoveryClusterEngine._populate_independence(
            result,
            evidence,
        )

        # --------------------------------------------------
        # Recovery Breadth
        # --------------------------------------------------

        result.stabilization_breadth = (
            RecoveryClusterEngine._stage_breadth(
                evidence,
                (
                    RecoveryStage.STABILIZING,
                    RecoveryStage.EARLY_INFLECTION,
                    RecoveryStage.EARLY_RECOVERY,
                    RecoveryStage.CONFIRMED_RECOVERY,
                ),
            )
        )

        result.inflection_breadth = (
            RecoveryClusterEngine._stage_breadth(
                evidence,
                (
                    RecoveryStage.EARLY_INFLECTION,
                    RecoveryStage.EARLY_RECOVERY,
                    RecoveryStage.CONFIRMED_RECOVERY,
                ),
            )
        )

        result.reversal_breadth = (
            RecoveryClusterEngine._reversal_breadth(
                evidence
            )
        )

        result.persistence_breadth = (
            RecoveryClusterEngine._persistence_breadth(
                evidence
            )
        )

        # --------------------------------------------------
        # Quality Scores
        # --------------------------------------------------

        result.breadth_score = (
            RecoveryClusterEngine._breadth_score(
                result
            )
        )

        result.corroboration_score = (
            RecoveryClusterEngine._corroboration_score(
                result
            )
        )

        result.temporal_score = (
            RecoveryClusterEngine._temporal_score(
                evidence
            )
        )

        result.contradiction_score = (
            RecoveryClusterEngine._contradiction_score(
                result
            )
        )

        result.coherence_score = (
            RecoveryClusterEngine._coherence_score(
                result
            )
        )

        # --------------------------------------------------
        # Cluster Characteristics
        # --------------------------------------------------

        result.emerging_cluster = (
            RecoveryClusterEngine._is_emerging(
                result
            )
        )

        result.stabilizing_cluster = (
            RecoveryClusterEngine._is_stabilizing(
                result
            )
        )

        result.early_recovery_cluster = (
            RecoveryClusterEngine._is_early_recovery(
                result
            )
        )

        result.confirmed_recovery_cluster = (
            RecoveryClusterEngine._is_confirmed_recovery(
                result
            )
        )

        result.broad_based = (
            result.breadth_score >= 60.0
        )

        result.cross_domain_confirmation = (
            result.independent_domains >= 2
        )

        # --------------------------------------------------
        # Direction
        # --------------------------------------------------

        result.direction = (
            RecoveryClusterEngine._direction(
                result
            )
        )

        # --------------------------------------------------
        # Stage
        # --------------------------------------------------

        result.stage = (
            RecoveryClusterEngine._stage(
                result
            )
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = (
            RecoveryClusterEngine._confidence(
                result
            )
        )

        # --------------------------------------------------
        # Reasoning
        # --------------------------------------------------

        RecoveryClusterEngine._build_reasons(
            result
        )

        return result

    # ======================================================
    # IDENTITY
    # ======================================================

    @staticmethod
    def _populate_identity(
        result: RecoveryClusterAssessment,
        evidence: List[RecoveryClusterEvidence],
    ) -> None:

        first = evidence[0]

        result.cluster_id = first.cluster_key
        result.cluster_name = first.cluster_name
        result.cluster_type = first.cluster_type

    # ======================================================
    # DIRECTION COUNTS
    # ======================================================

    @staticmethod
    def _populate_direction_counts(
        result: RecoveryClusterAssessment,
        evidence: List[RecoveryClusterEvidence],
    ) -> None:

        for item in evidence:

            if item.recovery_evidence is None:
                continue

            assessment = (
                item.recovery_evidence.recovery_assessment
            )

            if assessment is None:
                continue

            direction = assessment.direction

            if direction == RecoveryDirection.POSITIVE:
                result.supporting_assessments += 1

            elif direction == RecoveryDirection.STABILIZING:
                result.stabilizing_assessments += 1

            elif direction == RecoveryDirection.NEGATIVE:
                result.deteriorating_assessments += 1

    # ======================================================
    # INDEPENDENCE
    # ======================================================

    @staticmethod
    def _populate_independence(
        result: RecoveryClusterAssessment,
        evidence: List[RecoveryClusterEvidence],
    ) -> None:

        source_keys = set()
        signal_ids = set()
        domains = set()

        for item in evidence:

            recovery_evidence = (
                item.recovery_evidence
            )

            if recovery_evidence is None:
                continue

            if recovery_evidence.source_key:
                source_keys.add(
                    recovery_evidence.source_key
                )

            if recovery_evidence.signal_id:
                signal_ids.add(
                    recovery_evidence.signal_id
                )

            metadata = getattr(
                recovery_evidence,
                "metadata",
                None,
            )

            if isinstance(metadata, dict):

                domain = metadata.get(
                    "domain"
                )

                if domain:
                    domains.add(
                        str(domain)
                    )

        result.source_keys = sorted(
            source_keys
        )

        result.independent_sources = len(
            source_keys
        )

        result.independent_signals = len(
            signal_ids
        )

        result.domains = sorted(
            domains
        )

        result.independent_domains = len(
            domains
        )

        result.supporting_signal_ids = sorted(
            {
                item.recovery_evidence.signal_id
                for item in evidence
                if (
                    item.recovery_evidence
                    and item.recovery_evidence.signal_id
                    and item.recovery_evidence.recovery_assessment
                    and item.recovery_evidence.recovery_assessment.direction
                    in (
                        RecoveryDirection.POSITIVE,
                        RecoveryDirection.STABILIZING,
                    )
                )
            }
        )

        result.contradictory_signal_ids = sorted(
            {
                item.recovery_evidence.signal_id
                for item in evidence
                if (
                    item.recovery_evidence
                    and item.recovery_evidence.signal_id
                    and item.recovery_evidence.recovery_assessment
                    and item.recovery_evidence.recovery_assessment.direction
                    == RecoveryDirection.NEGATIVE
                )
            }
        )

    # ======================================================
    # STAGE BREADTH
    # ======================================================

    @staticmethod
    def _stage_breadth(
        evidence: List[RecoveryClusterEvidence],
        stages,
    ) -> float:

        valid = [
            item
            for item in evidence
            if (
                item.recovery_evidence
                and item.recovery_evidence.recovery_assessment
            )
        ]

        if not valid:
            return 0.0

        matching = sum(
            1
            for item in valid
            if (
                item.recovery_evidence
                .recovery_assessment
                .stage
                in stages
            )
        )

        return (
            matching
            / len(valid)
            * 100.0
        )

    # ======================================================
    # REVERSAL BREADTH
    # ======================================================

    @staticmethod
    def _reversal_breadth(
        evidence: List[RecoveryClusterEvidence],
    ) -> float:

        valid = [
            item
            for item in evidence
            if (
                item.recovery_evidence
                and item.recovery_evidence.recovery_assessment
            )
        ]

        if not valid:
            return 0.0

        reversal = sum(
            1
            for item in valid
            if getattr(
                item.recovery_evidence.recovery_assessment,
                "reversal_detected",
                False,
            )
        )

        return (
            reversal
            / len(valid)
            * 100.0
        )

    # ======================================================
    # PERSISTENCE BREADTH
    # ======================================================

    @staticmethod
    def _persistence_breadth(
        evidence: List[RecoveryClusterEvidence],
    ) -> float:

        valid = [
            item
            for item in evidence
            if (
                item.recovery_evidence
                and item.recovery_evidence.recovery_assessment
            )
        ]

        if not valid:
            return 0.0

        persistent = sum(
            1
            for item in valid
            if getattr(
                item.recovery_evidence.recovery_assessment,
                "persistence_detected",
                False,
            )
        )

        return (
            persistent
            / len(valid)
            * 100.0
        )

    # ======================================================
    # BREADTH SCORE
    # ======================================================

    @staticmethod
    def _breadth_score(
        result: RecoveryClusterAssessment,
    ) -> float:

        supportive = (
            result.supporting_assessments
            + result.stabilizing_assessments
        )

        total = result.total_recovery_assessments

        if total <= 0:
            return 0.0

        return min(
            100.0,
            supportive
            / total
            * 100.0,
        )

    # ======================================================
    # CORROBORATION
    # ======================================================

    @staticmethod
    def _corroboration_score(
        result: RecoveryClusterAssessment,
    ) -> float:
        """
        Measure independent corroboration.

        Independent sources are the primary evidence.

        Independent signals provide secondary confirmation.

        Domain diversity is an additional confirmation when
        domain information is actually available.

        Missing domain metadata is NOT negative evidence.

        This is important because an early-stage EIOS signal
        may have several genuinely independent sources before
        formal domain metadata has been attached.
        """

        source_score = min(
            100.0,
            result.independent_sources * 20.0,
        )

        signal_score = min(
            100.0,
            result.independent_signals * 10.0,
        )

        # --------------------------------------------------
        # Domain-aware calculation
        # --------------------------------------------------

        if result.independent_domains > 0:

            domain_score = min(
                100.0,
                result.independent_domains * 25.0,
            )

            return max(
                0.0,
                min(
                    100.0,
                    (
                        source_score * 0.55
                        + domain_score * 0.25
                        + signal_score * 0.20
                    ),
                ),
            )

        # --------------------------------------------------
        # Domain information unavailable
        # --------------------------------------------------

        return max(
            0.0,
            min(
                100.0,
                (
                    source_score * 0.70
                    + signal_score * 0.30
                ),
            ),
        )

    # ======================================================
    # TEMPORAL SCORE
    # ======================================================

    @staticmethod
    def _temporal_score(
        evidence: List[RecoveryClusterEvidence],
    ) -> float:

        values = []

        for item in evidence:

            recovery_evidence = (
                item.recovery_evidence
            )

            if recovery_evidence is None:
                continue

            assessment = (
                recovery_evidence.recovery_assessment
            )

            if assessment is None:
                continue

            value = getattr(
                assessment,
                "temporal_support",
                0.0,
            )

            values.append(
                float(value)
            )

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
    # CONTRADICTION
    # ======================================================

    @staticmethod
    def _contradiction_score(
        result: RecoveryClusterAssessment,
    ) -> float:

        total = result.total_recovery_assessments

        if total <= 0:
            return 0.0

        return min(
            100.0,
            result.deteriorating_assessments
            / total
            * 100.0,
        )

    # ======================================================
    # COHERENCE
    # ======================================================

    @staticmethod
    def _coherence_score(
        result: RecoveryClusterAssessment,
    ) -> float:
        """
        Coherence measures whether the cluster has enough
        internally consistent recovery evidence.

        Rewards:
        - breadth
        - corroboration
        - temporal alignment
        - stabilization breadth

        Penalizes:
        - contradictory evidence
        """

        score = (
            result.breadth_score * 0.35
            + result.corroboration_score * 0.30
            + result.temporal_score * 0.20
            + result.stabilization_breadth * 0.15
        )

        score -= (
            result.contradiction_score
            * 0.35
        )

        return max(
            0.0,
            min(
                100.0,
                score,
            ),
        )

    # ======================================================
    # EMERGING
    # ======================================================

    @staticmethod
    def _is_emerging(
        result: RecoveryClusterAssessment,
    ) -> bool:

        return (
            result.total_recovery_assessments >= 2
            and (
                result.supporting_assessments
                + result.stabilizing_assessments
            ) >= 2
            and result.coherence_score >= 40.0
        )

    # ======================================================
    # STABILIZING
    # ======================================================

    @staticmethod
    def _is_stabilizing(
        result: RecoveryClusterAssessment,
    ) -> bool:

        return (
            result.total_recovery_assessments >= 3
            and result.stabilization_breadth >= 60.0
            and result.coherence_score >= 50.0
        )

    # ======================================================
    # EARLY RECOVERY
    # ======================================================

    @staticmethod
    def _is_early_recovery(
        result: RecoveryClusterAssessment,
    ) -> bool:
        """
        Early Recovery requires:
        - sufficient breadth
        - meaningful inflection
        - independent corroboration
        - temporal support
        - coherent evidence
        - limited contradiction
        """

        return (
            result.total_recovery_assessments >= 3
            and result.breadth_score >= 60.0
            and result.inflection_breadth >= 40.0
            and result.corroboration_score >= 40.0
            and result.temporal_score >= 50.0
            and result.coherence_score >= 60.0
            and result.contradiction_score < 40.0
        )

    # ======================================================
    # CONFIRMED RECOVERY
    # ======================================================

    @staticmethod
    def _is_confirmed_recovery(
        result: RecoveryClusterAssessment,
    ) -> bool:
        """
        Confirmed Recovery requires materially stronger
        breadth, persistence, reversal, corroboration and
        temporal confirmation.
        """

        return (
            result.total_recovery_assessments >= 4
            and result.breadth_score >= 70.0
            and result.inflection_breadth >= 50.0
            and result.reversal_breadth >= 40.0
            and result.persistence_breadth >= 40.0
            and result.corroboration_score >= 60.0
            and result.temporal_score >= 60.0
            and result.coherence_score >= 70.0
            and result.contradiction_score < 30.0
        )

    # ======================================================
    # DIRECTION
    # ======================================================

    @staticmethod
    def _direction(
        result: RecoveryClusterAssessment,
    ) -> RecoveryClusterDirection:

        positive = result.supporting_assessments
        stabilizing = result.stabilizing_assessments
        negative = result.deteriorating_assessments

        supportive = (
            positive
            + stabilizing
        )

        if supportive == 0 and negative == 0:
            return RecoveryClusterDirection.UNKNOWN

        if supportive > 0 and negative > 0:

            if supportive > negative:
                return RecoveryClusterDirection.POSITIVE

            if negative > supportive:
                return RecoveryClusterDirection.NEGATIVE

            return RecoveryClusterDirection.MIXED

        if supportive > 0:

            if positive > stabilizing:
                return RecoveryClusterDirection.POSITIVE

            return RecoveryClusterDirection.STABILIZING

        return RecoveryClusterDirection.NEGATIVE

    # ======================================================
    # STAGE
    # ======================================================

    @staticmethod
    def _stage(
        result: RecoveryClusterAssessment,
    ) -> RecoveryClusterStage:

        if result.total_recovery_assessments == 0:
            return RecoveryClusterStage.INSUFFICIENT_EVIDENCE

        # Highest-confidence state first.
        if result.confirmed_recovery_cluster:
            return RecoveryClusterStage.CONFIRMED_RECOVERY_CLUSTER

        if result.early_recovery_cluster:
            return RecoveryClusterStage.EARLY_RECOVERY_CLUSTER

        if result.stabilizing_cluster:
            return RecoveryClusterStage.STABILIZING_CLUSTER

        if result.emerging_cluster:
            return RecoveryClusterStage.EARLY_CLUSTERING

        return RecoveryClusterStage.INSUFFICIENT_EVIDENCE

    # ======================================================
    # CONFIDENCE
    # ======================================================

    @staticmethod
    def _confidence(
        result: RecoveryClusterAssessment,
    ) -> float:

        confidence = (
            result.coherence_score * 0.30
            + result.breadth_score * 0.20
            + result.corroboration_score * 0.20
            + result.temporal_score * 0.15
            + result.stabilization_breadth * 0.15
        )

        confidence -= (
            result.contradiction_score
            * 0.20
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
        result: RecoveryClusterAssessment,
    ) -> None:

        if result.total_recovery_assessments > 0:
            result.reasons.append(
                f"{result.total_recovery_assessments} "
                "recovery assessments were evaluated."
            )

        if result.supporting_assessments > 0:
            result.reasons.append(
                f"{result.supporting_assessments} assessments "
                "show positive recovery direction."
            )

        if result.stabilizing_assessments > 0:
            result.reasons.append(
                f"{result.stabilizing_assessments} assessments "
                "show stabilization."
            )

        if result.independent_sources >= 2:
            result.reasons.append(
                "Multiple independent sources corroborate "
                "the recovery cluster."
            )

        if result.independent_domains >= 2:
            result.reasons.append(
                "Evidence spans multiple independent domains."
            )

        if result.broad_based:
            result.reasons.append(
                "Recovery evidence is broad-based within "
                "the explicitly defined cluster."
            )

        if result.inflection_breadth >= 40.0:
            result.reasons.append(
                "A meaningful portion of the cluster shows "
                "inflection toward recovery."
            )

        if result.reversal_breadth >= 40.0:
            result.reasons.append(
                "A meaningful portion of the cluster shows "
                "reversal characteristics."
            )

        if result.persistence_breadth >= 40.0:
            result.reasons.append(
                "Recovery characteristics show persistence "
                "across the cluster."
            )

        if result.deteriorating_assessments > 0:
            result.warnings.append(
                f"{result.deteriorating_assessments} "
                "deteriorating assessments create "
                "contradictory evidence."
            )

        if result.contradiction_score >= 30.0:
            result.warnings.append(
                "Contradictory evidence is material and "
                "reduces recovery confidence."
            )

        if (
            result.stage
            == RecoveryClusterStage.STABILIZING_CLUSTER
        ):
            result.warnings.append(
                "The cluster is stabilizing but recovery "
                "is not yet confirmed."
            )

        if (
            result.stage
            == RecoveryClusterStage.EARLY_CLUSTERING
        ):
            result.warnings.append(
                "Early clustering detected; evidence is "
                "not yet sufficient for recovery confirmation."
            )

        if (
            result.stage
            == RecoveryClusterStage.INSUFFICIENT_EVIDENCE
        ):
            result.warnings.append(
                "Evidence is insufficient to establish a "
                "coherent recovery cluster."
            )


__all__ = [
    "RecoveryClusterEngine",
]