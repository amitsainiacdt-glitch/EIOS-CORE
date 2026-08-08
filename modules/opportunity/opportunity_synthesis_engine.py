"""
EIOS
Everest Investment Operating System

Opportunity Synthesis Engine
Release K

Purpose
-------
Combines:

    Catalyst
    Expectation Gap
    Mispricing
    Asymmetry
    Evidence

into a single research-stage Opportunity assessment.

The engine does NOT:

    - perform valuation
    - replace the Valuation Engine
    - make portfolio decisions
    - execute trades
    - persist data

The engine DOES:

    - synthesize independent analytical outputs
    - incorporate institutional evidence qualification
    - expose contradictions
    - measure confidence
    - enforce evidence sufficiency
    - enforce kill-switch requirements
    - produce an explicit research decision
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from modules.opportunity.catalyst_engine import Catalyst
from modules.opportunity.expectation_gap_engine import (
    ExpectationGap,
)
from modules.opportunity.mispricing_engine import (
    MispricingAssessment,
)
from modules.opportunity.asymmetry_engine import (
    AsymmetryAssessment,
)
from modules.opportunity.evidence_engine import (
    OpportunityEvidencePack,
)


# ==========================================================
# OPPORTUNITY DECISION
# ==========================================================


class OpportunityDecision(Enum):
    """
    Research-stage Opportunity Office decision.
    """

    REJECT = "Reject"
    WATCH = "Watch"
    RESEARCH = "Research"
    HIGH_CONVICTION_CANDIDATE = (
        "High Conviction Candidate"
    )


# ==========================================================
# OPPORTUNITY SYNTHESIS
# ==========================================================


@dataclass
class OpportunitySynthesis:
    """
    Institutional Opportunity synthesis.

    This is a decision-preparation object.
    It is not an Investment Committee decision.
    """

    company: str = ""

    sector: str = ""

    decision: OpportunityDecision = (
        OpportunityDecision.WATCH
    )

    # ------------------------------------------------------
    # Component Scores
    # ------------------------------------------------------

    catalyst_score: float = 0.0

    expectation_gap_score: float = 0.0

    mispricing_score: float = 0.0

    asymmetry_score: float = 0.0

    # ------------------------------------------------------
    # Composite Intelligence
    # ------------------------------------------------------

    opportunity_score: float = 0.0

    confidence: float = 0.0

    # ------------------------------------------------------
    # Evidence Qualification
    # ------------------------------------------------------

    evidence_score: float = 0.0

    evidence_confidence: float = 0.0

    evidence_sufficient: bool = False

    evidence_gaps: List[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------
    # Risk
    # ------------------------------------------------------

    permanent_loss_probability: float = 0.0

    downside_probability: float = 0.0

    expected_return: float = 0.0

    expected_time_months: float = 0.0

    # ------------------------------------------------------
    # Evidence
    # ------------------------------------------------------

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    disconfirming_evidence: List[str] = field(
        default_factory=list
    )

    invalidation_conditions: List[str] = field(
        default_factory=list
    )

    kill_switches: List[str] = field(
        default_factory=list
    )

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# SYNTHESIS ENGINE
# ==========================================================


class OpportunitySynthesisEngine:
    """
    Synthesizes Opportunity Office intelligence.

    Evidence qualification is a hard institutional gate.

    A high Opportunity Intelligence score alone cannot
    produce High Conviction Candidate status.
    """

    # ======================================================
    # THRESHOLDS
    # ======================================================

    REJECT_SCORE = 40.0

    WATCH_SCORE = 50.0

    RESEARCH_SCORE = 60.0

    HIGH_CONVICTION_SCORE = 75.0

    MAX_PERMANENT_LOSS = 30.0

    MIN_CONFIDENCE = 60.0

    MIN_EVIDENCE_SCORE = 60.0

    MIN_EVIDENCE_CONFIDENCE = 60.0

    # ======================================================
    # ANALYZE
    # ======================================================

    def analyze(
        self,
        *,
        company: str,
        sector: str,
        catalyst: Optional[Catalyst] = None,
        expectation_gap: Optional[
            ExpectationGap
        ] = None,
        mispricing: Optional[
            MispricingAssessment
        ] = None,
        asymmetry: Optional[
            AsymmetryAssessment
        ] = None,
        evidence_pack: Optional[
            OpportunityEvidencePack
        ] = None,
        assumptions: Optional[
            List[str]
        ] = None,
        invalidation_conditions: Optional[
            List[str]
        ] = None,
        kill_switches: Optional[
            List[str]
        ] = None,
    ) -> OpportunitySynthesis:
        """
        Produce a research-stage Opportunity synthesis.
        """

        result = OpportunitySynthesis()

        result.company = company

        result.sector = sector

        result.assumptions = list(
            assumptions or []
        )

        result.invalidation_conditions = list(
            invalidation_conditions or []
        )

        result.kill_switches = list(
            kill_switches or []
        )

        # ==================================================
        # CATALYST
        # ==================================================

        if catalyst:

            result.catalyst_score = (
                catalyst.catalyst_score
            )

            result.evidence.extend(
                catalyst.evidence
            )

            result.disconfirming_evidence.extend(
                catalyst.contradictory_evidence
            )

            result.warnings.extend(
                catalyst.warnings
            )

        # ==================================================
        # EXPECTATION GAP
        # ==================================================

        if expectation_gap:

            result.expectation_gap_score = (
                expectation_gap.gap_score
            )

            result.evidence.extend(
                expectation_gap.evidence
            )

            result.disconfirming_evidence.extend(
                expectation_gap.disconfirming_evidence
            )

            result.warnings.extend(
                expectation_gap.warnings
            )

        # ==================================================
        # MISPRICING
        # ==================================================

        if mispricing:

            result.mispricing_score = (
                mispricing.mispricing_score
            )

            result.evidence.extend(
                mispricing.evidence
            )

            result.disconfirming_evidence.extend(
                mispricing.disconfirming_evidence
            )

            result.warnings.extend(
                mispricing.warnings
            )

        # ==================================================
        # ASYMMETRY
        # ==================================================

        if asymmetry:

            result.asymmetry_score = (
                asymmetry.asymmetry_score
            )

            result.permanent_loss_probability = (
                asymmetry.permanent_loss_probability
            )

            result.downside_probability = (
                asymmetry.downside_probability
            )

            result.expected_return = (
                asymmetry.expected_return
            )

            result.expected_time_months = (
                asymmetry.expected_time_months
            )

            result.warnings.extend(
                asymmetry.warnings
            )

        # ==================================================
        # EVIDENCE PACK
        # ==================================================

        if evidence_pack:

            result.evidence_score = (
                evidence_pack.evidence_score
            )

            result.evidence_confidence = (
                evidence_pack.confidence
            )

            result.evidence_sufficient = (
                evidence_pack.sufficiently_supported
            )

            result.evidence_gaps = list(
                evidence_pack.evidence_gaps
            )

            result.evidence.extend(
                item.statement
                for item
                in evidence_pack.supporting_evidence
                if item.statement
            )

            result.disconfirming_evidence.extend(
                item.statement
                for item
                in evidence_pack.contradictory_evidence
                if item.statement
            )

            result.assumptions.extend(
                evidence_pack.assumptions
            )

            result.warnings.extend(
                evidence_pack.warnings
            )

            result.kill_switches.extend(
                kill.name
                for kill
                in evidence_pack.kill_switches
                if kill.name
            )

        else:

            result.warnings.append(
                "No Opportunity Evidence Pack supplied."
            )

            result.evidence_sufficient = False

        # ==================================================
        # DEDUPLICATION
        # ==================================================

        result.evidence = list(
            dict.fromkeys(
                result.evidence
            )
        )

        result.disconfirming_evidence = list(
            dict.fromkeys(
                result.disconfirming_evidence
            )
        )

        result.assumptions = list(
            dict.fromkeys(
                result.assumptions
            )
        )

        result.invalidation_conditions = list(
            dict.fromkeys(
                result.invalidation_conditions
            )
        )

        result.kill_switches = list(
            dict.fromkeys(
                result.kill_switches
            )
        )

        result.warnings = list(
            dict.fromkeys(
                result.warnings
            )
        )

        # ==================================================
        # OPPORTUNITY SCORE
        # ==================================================

        result.opportunity_score = (
            self._opportunity_score(
                result
            )
        )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        result.confidence = (
            self._confidence(
                result,
                catalyst,
                expectation_gap,
                mispricing,
                asymmetry,
            )
        )

        # ==================================================
        # DECISION
        # ==================================================

        result.decision = (
            self._decision(
                result
            )
        )

        # ==================================================
        # REASONING
        # ==================================================

        self._build_reasoning(
            result
        )

        return result

    # ======================================================
    # OPPORTUNITY SCORE
    # ======================================================

    def _opportunity_score(
        self,
        result: OpportunitySynthesis,
    ) -> float:
        """
        Composite Opportunity Intelligence score.

        Evidence is deliberately NOT included directly
        in this score.

        Evidence acts as an independent qualification gate.
        This prevents evidence quality from being double-counted.
        """

        score = (
            result.catalyst_score * 0.20
            + result.expectation_gap_score * 0.20
            + result.mispricing_score * 0.30
            + result.asymmetry_score * 0.30
        )

        # --------------------------------------------------
        # Permanent-loss penalty
        # --------------------------------------------------

        if (
            result.permanent_loss_probability
            > self.MAX_PERMANENT_LOSS
        ):

            penalty = min(
                30.0,
                (
                    result.permanent_loss_probability
                    - self.MAX_PERMANENT_LOSS
                ) * 0.50,
            )

            score -= penalty

        return self._clamp(
            score
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        result: OpportunitySynthesis,
        catalyst,
        expectation_gap,
        mispricing,
        asymmetry,
    ) -> float:
        """
        Confidence combines analytical component confidence
        with the independent Evidence Engine confidence.

        Evidence confidence receives meaningful weight but
        does not replace analytical confidence.
        """

        confidence_values = []

        if catalyst:

            confidence_values.append(
                catalyst.confidence
            )

        if expectation_gap:

            confidence_values.append(
                expectation_gap.confidence
            )

        if mispricing:

            confidence_values.append(
                mispricing.confidence
            )

        if asymmetry:

            confidence_values.append(
                asymmetry.confidence
            )

        if not confidence_values:

            return 0.0

        analytical_confidence = (
            sum(confidence_values)
            / len(confidence_values)
        )

        # --------------------------------------------------
        # Evidence confidence integration
        # --------------------------------------------------

        if result.evidence_sufficient:

            base = (
                analytical_confidence * 0.70
                + result.evidence_confidence * 0.30
            )

        else:

            # Insufficient evidence limits confidence.
            base = min(
                analytical_confidence,
                result.evidence_confidence,
            )

        # --------------------------------------------------
        # Evidence breadth
        # --------------------------------------------------

        if len(result.evidence) >= 5:

            base += 5.0

        elif len(result.evidence) < 2:

            base -= 15.0

        # --------------------------------------------------
        # Contradictions
        # --------------------------------------------------

        contradiction_penalty = min(
            25.0,
            len(
                result.disconfirming_evidence
            ) * 3.0,
        )

        base -= contradiction_penalty

        return self._clamp(
            base
        )

    # ======================================================
    # DECISION
    # ======================================================

    def _decision(
        self,
        result: OpportunitySynthesis,
    ) -> OpportunityDecision:
        """
        Determine research-stage decision.

        Evidence sufficiency is a hard gate.

        Insufficient evidence can never produce:

            High Conviction Candidate
        """

        # --------------------------------------------------
        # Hard rejection
        # --------------------------------------------------

        if (
            result.opportunity_score
            < self.REJECT_SCORE
        ):

            return OpportunityDecision.REJECT

        if (
            result.permanent_loss_probability
            > self.MAX_PERMANENT_LOSS
        ):

            return OpportunityDecision.REJECT

        # --------------------------------------------------
        # Evidence gate
        # --------------------------------------------------

        evidence_gate_failed = (
            not result.evidence_sufficient
            or result.evidence_score
            < self.MIN_EVIDENCE_SCORE
            or result.evidence_confidence
            < self.MIN_EVIDENCE_CONFIDENCE
        )

        if evidence_gate_failed:

            return OpportunityDecision.WATCH

        # --------------------------------------------------
        # Confidence gate
        # --------------------------------------------------

        if (
            result.confidence
            < self.MIN_CONFIDENCE
        ):

            return OpportunityDecision.WATCH

        # --------------------------------------------------
        # High conviction candidate
        # --------------------------------------------------

        if (
            result.opportunity_score
            >= self.HIGH_CONVICTION_SCORE
            and result.confidence
            >= 75.0
            and result.permanent_loss_probability
            < self.MAX_PERMANENT_LOSS
        ):

            return (
                OpportunityDecision
                .HIGH_CONVICTION_CANDIDATE
            )

        # --------------------------------------------------
        # Research
        # --------------------------------------------------

        if (
            result.opportunity_score
            >= self.RESEARCH_SCORE
        ):

            return OpportunityDecision.RESEARCH

        # --------------------------------------------------
        # Watch
        # --------------------------------------------------

        if (
            result.opportunity_score
            >= self.WATCH_SCORE
        ):

            return OpportunityDecision.WATCH

        return OpportunityDecision.REJECT

    # ======================================================
    # REASONING
    # ======================================================

    def _build_reasoning(
        self,
        result: OpportunitySynthesis,
    ) -> None:

        if result.catalyst_score >= 60:

            result.reasons.append(
                "Catalyst evidence is sufficiently developed."
            )

        else:

            result.warnings.append(
                "Catalyst evidence remains weak."
            )

        if result.expectation_gap_score >= 60:

            result.reasons.append(
                "Expectation-gap evidence is material."
            )

        else:

            result.warnings.append(
                "Expectation gap is not yet sufficiently strong."
            )

        if result.mispricing_score >= 60:

            result.reasons.append(
                "Potential mispricing is supported by the evidence."
            )

        else:

            result.warnings.append(
                "Mispricing evidence remains insufficient."
            )

        if result.asymmetry_score >= 60:

            result.reasons.append(
                "Scenario asymmetry is attractive."
            )

        else:

            result.warnings.append(
                "Scenario asymmetry is not yet sufficiently attractive."
            )

        # --------------------------------------------------
        # Evidence
        # --------------------------------------------------

        if result.evidence_sufficient:

            result.reasons.append(
                "Evidence pack meets the institutional "
                "sufficiency threshold."
            )

        else:

            result.warnings.append(
                "Evidence pack does not meet the institutional "
                "sufficiency threshold."
            )

        if result.evidence_gaps:

            result.warnings.append(
                "Evidence gaps remain unresolved."
            )

        # --------------------------------------------------
        # Permanent loss
        # --------------------------------------------------

        if (
            result.permanent_loss_probability
            >= self.MAX_PERMANENT_LOSS
        ):

            result.warnings.append(
                "Permanent capital-loss risk is elevated."
            )

        # --------------------------------------------------
        # Kill switch
        # --------------------------------------------------

        if not result.kill_switches:

            result.warnings.append(
                "No explicit kill switch has been supplied."
            )

        # --------------------------------------------------
        # Decision
        # --------------------------------------------------

        if result.decision == (
            OpportunityDecision
            .HIGH_CONVICTION_CANDIDATE
        ):

            result.reasons.append(
                "Opportunity qualifies for high-conviction "
                "candidate status pending Investment Committee review."
            )

        elif result.decision == (
            OpportunityDecision.RESEARCH
        ):

            result.reasons.append(
                "Opportunity merits deeper institutional research."
            )

        elif result.decision == (
            OpportunityDecision.WATCH
        ):

            result.reasons.append(
                "Opportunity should remain under observation "
                "until evidence or analytical confidence strengthens."
            )

        else:

            result.warnings.append(
                "Opportunity does not currently meet the "
                "required institutional threshold."
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

        return max(
            minimum,
            min(
                maximum,
                value,
            ),
        )