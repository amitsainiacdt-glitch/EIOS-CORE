"""
EIOS - Everest Investment Operating System

Opportunity Evidence Engine
Release J

Purpose
-------
Build an auditable evidence pack for an Opportunity.

The engine evaluates:

    Supporting Evidence
    Contradictory Evidence
    Evidence Quality
    Evidence Breadth
    Primary Sources
    Independent Confirmation
    Assumptions
    Kill Switches
    Monitoring Requirements

The engine does NOT perform:

    - Valuation
    - Opportunity ranking
    - Portfolio allocation
    - Trade execution
"""


from dataclasses import dataclass, field
from typing import List


# ==========================================================
# DATA MODELS
# ==========================================================


@dataclass
class EvidenceItem:
    """
    One supporting or contradictory evidence item.
    """

    evidence_id: str = ""

    statement: str = ""

    source: str = ""

    category: str = ""

    direction: str = "Supporting"

    strength: float = 0.0

    confidence: float = 0.0

    independent_confirmation: int = 0

    is_primary_source: bool = False

    is_time_sensitive: bool = False

    notes: str = ""


@dataclass
class KillSwitch:
    """
    Explicit condition capable of invalidating the thesis.
    """

    name: str = ""

    condition: str = ""

    severity: str = "High"

    measurable: bool = False

    threshold: str = ""

    monitoring_frequency: str = ""

    rationale: str = ""

    triggered: bool = False


@dataclass
class OpportunityEvidencePack:
    """
    Complete institutional evidence record.
    """

    company: str = ""

    supporting_evidence: List[EvidenceItem] = field(
        default_factory=list
    )

    contradictory_evidence: List[EvidenceItem] = field(
        default_factory=list
    )

    evidence_gaps: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    kill_switches: List[KillSwitch] = field(
        default_factory=list
    )

    monitoring_signals: List[str] = field(
        default_factory=list
    )

    evidence_score: float = 0.0

    confidence: float = 0.0

    sufficiently_supported: bool = False

    strengths: List[str] = field(
        default_factory=list
    )

    weaknesses: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# OPPORTUNITY EVIDENCE ENGINE
# ==========================================================


class OpportunityEvidenceEngine:
    """
    Institutional evidence evaluation engine.
    """

    # ------------------------------------------------------
    # Institutional thresholds
    # ------------------------------------------------------

    MINIMUM_EVIDENCE_SCORE = 60.0

    MINIMUM_SUPPORTING_EVIDENCE = 3

    MINIMUM_CONFIDENCE = 60.0

    MAX_CONTRADICTION_PENALTY = 35.0

    # ======================================================
    # PUBLIC API
    # ======================================================

    def analyze(
        self,
        *,
        company: str,
        supporting_evidence: List[EvidenceItem] | None = None,
        contradictory_evidence: List[EvidenceItem] | None = None,
        assumptions: List[str] | None = None,
        kill_switches: List[KillSwitch] | None = None,
        monitoring_signals: List[str] | None = None,
    ) -> OpportunityEvidencePack:
        """
        Build and evaluate an Opportunity Evidence Pack.
        """

        pack = OpportunityEvidencePack(
            company=company,
            supporting_evidence=list(
                supporting_evidence or []
            ),
            contradictory_evidence=list(
                contradictory_evidence or []
            ),
            assumptions=list(
                assumptions or []
            ),
            kill_switches=list(
                kill_switches or []
            ),
            monitoring_signals=list(
                monitoring_signals or []
            ),
        )

        pack.evidence_gaps = (
            self._identify_gaps(pack)
        )

        pack.evidence_score = (
            self._calculate_evidence_score(pack)
        )

        pack.confidence = (
            self._calculate_confidence(pack)
        )

        pack.sufficiently_supported = (
            self._is_sufficiently_supported(pack)
        )

        self._build_diagnostics(pack)

        return pack

    # ======================================================
    # EVIDENCE GAPS
    # ======================================================

    def _identify_gaps(
        self,
        pack: OpportunityEvidencePack,
    ) -> List[str]:
        """
        Identify missing institutional requirements.
        """

        gaps: List[str] = []

        # Supporting evidence
        if not pack.supporting_evidence:

            gaps.append(
                "No supporting evidence supplied."
            )

        elif len(
            pack.supporting_evidence
        ) < self.MINIMUM_SUPPORTING_EVIDENCE:

            gaps.append(
                "Insufficient independent supporting evidence."
            )

        # Contradictory evidence
        if not pack.contradictory_evidence:

            gaps.append(
                "No contradictory evidence documented."
            )

        # Assumptions
        if not pack.assumptions:

            gaps.append(
                "No explicit assumptions documented."
            )

        # Kill switches
        if not pack.kill_switches:

            gaps.append(
                "No explicit kill switches defined."
            )

        # Monitoring
        if not pack.monitoring_signals:

            gaps.append(
                "No monitoring signals defined."
            )

        # Primary source
        if not any(
            item.is_primary_source
            for item
            in pack.supporting_evidence
        ):

            gaps.append(
                "No primary-source evidence supplied."
            )

        return gaps

    # ======================================================
    # EVIDENCE SCORE
    # ======================================================

    def _calculate_evidence_score(
        self,
        pack: OpportunityEvidencePack,
    ) -> float:
        """
        Calculate quality-weighted evidence score.
        """

        if not pack.supporting_evidence:

            return 0.0

        quality_scores = [
            self._supporting_quality(item)
            for item
            in pack.supporting_evidence
        ]

        support_score = (
            sum(quality_scores)
            / len(quality_scores)
        )

        breadth_bonus = (
            self._breadth_bonus(pack)
        )

        contradiction_penalty = (
            self._contradiction_penalty(pack)
        )

        score = (
            support_score
            + breadth_bonus
            - contradiction_penalty
        )

        return self._clamp(score)

    # ======================================================
    # SUPPORTING EVIDENCE QUALITY
    # ======================================================

    def _supporting_quality(
        self,
        item: EvidenceItem,
    ) -> float:
        """
        Calculate the quality of an individual
        supporting evidence item.
        """

        confirmation_score = min(
            100.0,
            item.independent_confirmation * 20.0,
        )

        score = (
            item.strength * 0.45
            + item.confidence * 0.35
            + confirmation_score * 0.20
        )

        if item.is_primary_source:

            score += 5.0

        return self._clamp(score)

    # ======================================================
    # EVIDENCE BREADTH
    # ======================================================

    def _breadth_bonus(
        self,
        pack: OpportunityEvidencePack,
    ) -> float:
        """
        Reward evidence originating from multiple domains.
        """

        categories = {
            item.category
            for item
            in pack.supporting_evidence
            if item.category
        }

        return min(
            10.0,
            len(categories) * 2.0,
        )

    # ======================================================
    # CONTRADICTION ANALYSIS
    # ======================================================

    def _contradiction_penalty(
        self,
        pack: OpportunityEvidencePack,
    ) -> float:
        """
        Calculate severity-weighted contradiction penalty.

        A serious contradiction matters more than a minor one.

        Primary-source contradictions receive greater weight.
        """

        if not pack.contradictory_evidence:

            return 0.0

        severity_scores: List[float] = []

        for item in pack.contradictory_evidence:

            source_weight = (
                0.60
                if item.is_primary_source
                else 0.40
            )

            severity_scores.append(
                item.strength
                * source_weight
            )

        penalty = (
            sum(severity_scores)
            / len(severity_scores)
        )

        return min(
            self.MAX_CONTRADICTION_PENALTY,
            penalty,
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _calculate_confidence(
        self,
        pack: OpportunityEvidencePack,
    ) -> float:
        """
        Calculate evidence confidence.

        Confidence incorporates:

            - source confidence
            - independent confirmation
            - primary-source evidence
            - contradiction severity
        """

        if not pack.supporting_evidence:

            return 0.0

        base = (
            sum(
                item.confidence
                for item
                in pack.supporting_evidence
            )
            / len(
                pack.supporting_evidence
            )
        )

        # Independent confirmation
        confirmation_count = sum(
            item.independent_confirmation >= 2
            for item
            in pack.supporting_evidence
        )

        if confirmation_count >= 2:

            base += 5.0

        # Primary-source evidence
        if any(
            item.is_primary_source
            for item
            in pack.supporting_evidence
        ):

            base += 5.0

        # Contradiction penalty
        base -= (
            self._contradiction_penalty(pack)
        )

        return self._clamp(base)

    # ======================================================
    # SUFFICIENCY GATE
    # ======================================================

    def _is_sufficiently_supported(
        self,
        pack: OpportunityEvidencePack,
    ) -> bool:
        """
        Determine whether the Opportunity satisfies
        institutional evidence requirements.

        A thesis cannot be considered sufficiently supported
        without:

            1. Adequate supporting evidence
            2. Adequate evidence score
            3. Adequate confidence
            4. Primary-source evidence
            5. Explicit kill switch
            6. Monitoring signals
            7. No critical evidence gap
        """

        return (
            len(
                pack.supporting_evidence
            )
            >= self.MINIMUM_SUPPORTING_EVIDENCE

            and pack.evidence_score
            >= self.MINIMUM_EVIDENCE_SCORE

            and pack.confidence
            >= self.MINIMUM_CONFIDENCE

            and any(
                item.is_primary_source
                for item
                in pack.supporting_evidence
            )

            and bool(
                pack.kill_switches
            )

            and bool(
                pack.monitoring_signals
            )

            and not self._has_critical_gap(
                pack
            )
        )

    # ======================================================
    # CRITICAL GAP DETECTION
    # ======================================================

    def _has_critical_gap(
        self,
        pack: OpportunityEvidencePack,
    ) -> bool:
        """
        Identify evidence gaps that prevent qualification.
        """

        critical_terms = (
            "No supporting evidence",
            "Insufficient independent",
            "No primary-source",
        )

        return any(
            any(
                term.lower()
                in gap.lower()
                for term
                in critical_terms
            )
            for gap
            in pack.evidence_gaps
        )

    # ======================================================
    # DIAGNOSTICS
    # ======================================================

    def _build_diagnostics(
        self,
        pack: OpportunityEvidencePack,
    ) -> None:
        """
        Build concise institutional diagnostics.
        """

        # Supporting evidence
        if len(
            pack.supporting_evidence
        ) >= self.MINIMUM_SUPPORTING_EVIDENCE:

            pack.strengths.append(
                "Multiple supporting evidence items available."
            )

        else:

            pack.weaknesses.append(
                "Supporting evidence breadth is insufficient."
            )

        # Primary sources
        if any(
            item.is_primary_source
            for item
            in pack.supporting_evidence
        ):

            pack.strengths.append(
                "Primary-source evidence is available."
            )

        else:

            pack.weaknesses.append(
                "Primary-source evidence is absent."
            )

        # Contradictions
        if pack.contradictory_evidence:

            pack.warnings.append(
                "Contradictory evidence requires explicit review."
            )

            if any(
                item.strength >= 70.0
                for item
                in pack.contradictory_evidence
            ):

                pack.warnings.append(
                    "High-severity contradictory evidence exists."
                )

        else:

            pack.warnings.append(
                "No contradictory evidence has been documented."
            )

        # Kill switches
        if pack.kill_switches:

            pack.strengths.append(
                "Explicit thesis invalidation conditions are defined."
            )

        else:

            pack.weaknesses.append(
                "No kill switches have been defined."
            )

        # Monitoring
        if pack.monitoring_signals:

            pack.strengths.append(
                "Ongoing monitoring requirements are defined."
            )

        else:

            pack.weaknesses.append(
                "No monitoring requirements are defined."
            )

        # Final status
        if pack.sufficiently_supported:

            pack.strengths.append(
                "Evidence meets the minimum Opportunity threshold."
            )

        else:

            pack.warnings.append(
                "Evidence does not yet meet the institutional "
                "Opportunity threshold."
            )

    # ======================================================
    # UTILITY
    # ======================================================

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 100.0,
    ) -> float:
        """
        Clamp a numerical value to a defined range.
        """

        return max(
            minimum,
            min(
                maximum,
                value,
            ),
        )