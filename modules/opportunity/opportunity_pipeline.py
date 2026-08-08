"""
EIOS
Everest Investment Operating System

Opportunity Pipeline
====================

Thin orchestration layer for the Opportunity Engine.

Pipeline
--------
Signals
    ↓
Catalyst
    ↓
Expectation Gap
    ↓
Mispricing
    ↓
Asymmetry
    ↓
Evidence
    ↓
Synthesis

Design Principles
-----------------
1. Engines own calculations.
2. Pipeline owns orchestration only.
3. No duplicate scoring logic.
4. No invented analytical inputs.
5. Evidence is an institutional qualification gate.
6. Valuation remains authoritative in the Valuation Engine.
7. Pipeline does not mutate source objects.
"""

from dataclasses import dataclass
from typing import Any, List, Optional

from modules.opportunity.catalyst_engine import (
    Catalyst,
    CatalystEngine,
)

from modules.opportunity.expectation_gap_engine import (
    ExpectationGap,
    ExpectationGapEngine,
)

from modules.opportunity.mispricing_engine import (
    MispricingAssessment,
    MispricingEngine,
)

from modules.opportunity.asymmetry_engine import (
    AsymmetryAssessment,
    AsymmetryEngine,
    AsymmetryScenario,
)

from modules.opportunity.evidence_engine import (
    EvidenceItem,
    KillSwitch,
    OpportunityEvidenceEngine,
    OpportunityEvidencePack,
)

from modules.opportunity.opportunity_synthesis_engine import (
    OpportunitySynthesis,
    OpportunitySynthesisEngine,
)

from modules.opportunity.signals.signal_model import (
    Signal,
)

from modules.opportunity.signals.causal_chain_engine import (
    CausalChain,
)


# ==========================================================
# PIPELINE RESULT
# ==========================================================


@dataclass
class OpportunityPipelineResult:
    """
    Complete output produced by the Opportunity Pipeline.
    """

    company: str
    sector: str

    catalyst: Optional[Catalyst] = None

    expectation_gap: Optional[ExpectationGap] = None

    mispricing: Optional[MispricingAssessment] = None

    asymmetry: Optional[AsymmetryAssessment] = None

    evidence: Optional[OpportunityEvidencePack] = None

    synthesis: Optional[OpportunitySynthesis] = None


# ==========================================================
# OPPORTUNITY PIPELINE
# ==========================================================


class OpportunityPipeline:
    """
    Coordinates all Opportunity analytical engines.

    The pipeline contains no analytical formulas.
    Each specialized engine remains responsible for
    its own calculations, scoring and validation.
    """

    def __init__(self) -> None:
        """
        Initialize all Opportunity engines.
        """

        self.catalyst_engine = CatalystEngine()

        self.expectation_gap_engine = (
            ExpectationGapEngine()
        )

        self.mispricing_engine = MispricingEngine()

        self.asymmetry_engine = AsymmetryEngine()

        self.evidence_engine = (
            OpportunityEvidenceEngine()
        )

        self.synthesis_engine = (
            OpportunitySynthesisEngine()
        )

    # ======================================================
    # RUN
    # ======================================================

    def run(
        self,
        *,
        company: str,
        sector: str,
        cmp: float,
        signals: List[Signal],
        causal_chain: Optional[CausalChain],
        catalyst_id: str,
        catalyst_title: str,
        catalyst_trigger: str,
        market_expectation: float,
        eios_expectation: float,
        market_earnings_expectation: float,
        eios_earnings_expectation: float,
        valuation: Any,
        asymmetry_scenarios: List[AsymmetryScenario],
        supporting_evidence: List[EvidenceItem],
        contradictory_evidence: List[EvidenceItem],
        assumptions: List[str],
        kill_switches: List[KillSwitch],
        monitoring_signals: List[str],
        invalidation_conditions: Optional[List[str]] = None,
        affected_sectors: Optional[List[str]] = None,
        affected_companies: Optional[List[str]] = None,
        description: str = "",
        economic_impact: str = "",
        earnings_impact: str = "",
        valuation_impact: str = "",
    ) -> OpportunityPipelineResult:
        """
        Execute the complete Opportunity pipeline.

        The method only coordinates specialized engines.
        It does not perform independent scoring.
        """

        # ==================================================
        # NORMALIZE OPTIONAL INPUTS
        # ==================================================

        invalidation_conditions = list(
            invalidation_conditions or []
        )

        affected_sectors = list(
            affected_sectors or []
        )

        affected_companies = list(
            affected_companies or []
        )

        assumptions = list(
            assumptions or []
        )

        # ==================================================
        # 1. CATALYST ENGINE
        # ==================================================

        catalyst = self.catalyst_engine.analyze(
            catalyst_id=catalyst_id,
            title=catalyst_title,
            trigger=catalyst_trigger,
            signals=signals,
            causal_chain=causal_chain,
            description=description,
            economic_impact=economic_impact,
            earnings_impact=earnings_impact,
            valuation_impact=valuation_impact,
            affected_sectors=affected_sectors,
            affected_companies=affected_companies,
            assumptions=assumptions,
            invalidation_conditions=(
                invalidation_conditions
            ),
        )

        # ==================================================
        # 2. EXPECTATION GAP ENGINE
        # ==================================================

        expectation_gap = (
            self.expectation_gap_engine.analyze(
                gap_id=(
                    f"{company}-EXPECTATION-GAP"
                ),
                company=company,
                sector=sector,
                catalyst=catalyst,
                market_expectation=(
                    market_expectation
                ),
                eios_expectation=(
                    eios_expectation
                ),
                market_earnings_expectation=(
                    market_earnings_expectation
                ),
                eios_earnings_expectation=(
                    eios_earnings_expectation
                ),
                assumptions=assumptions,
                invalidation_conditions=(
                    invalidation_conditions
                ),
            )
        )

        # ==================================================
        # 3. MISPRICING ENGINE
        # ==================================================

        mispricing = (
            self.mispricing_engine.analyze(
                company=company,
                cmp=cmp,
                valuation=valuation,
                catalyst=catalyst,
                expectation_gap=(
                    expectation_gap
                ),
                assumptions=assumptions,
                invalidation_conditions=(
                    invalidation_conditions
                ),
            )
        )

        # ==================================================
        # 4. ASYMMETRY ENGINE
        # ==================================================

        asymmetry = (
            self.asymmetry_engine.analyze(
                company=company,
                scenarios=asymmetry_scenarios,
                assumptions=assumptions,
                invalidation_conditions=(
                    invalidation_conditions
                ),
                disconfirming_evidence=[
                    item.statement
                    for item in contradictory_evidence
                    if item.statement
                ],
            )
        )

        # ==================================================
        # 5. EVIDENCE ENGINE
        # ==================================================

        evidence = (
            self.evidence_engine.analyze(
                company=company,
                supporting_evidence=(
                    supporting_evidence
                ),
                contradictory_evidence=(
                    contradictory_evidence
                ),
                assumptions=assumptions,
                kill_switches=kill_switches,
                monitoring_signals=(
                    monitoring_signals
                ),
            )
        )

        # ==================================================
        # 6. SYNTHESIS ENGINE
        # ==================================================

        synthesis = (
            self.synthesis_engine.analyze(
                company=company,
                sector=sector,
                catalyst=catalyst,
                expectation_gap=(
                    expectation_gap
                ),
                mispricing=mispricing,
                asymmetry=asymmetry,
                evidence_pack=evidence,
                assumptions=assumptions,
                invalidation_conditions=(
                    invalidation_conditions
                ),
                kill_switches=[
                    kill.name
                    for kill in kill_switches
                    if kill.name
                ],
            )
        )

        # ==================================================
        # FINAL PIPELINE RESULT
        # ==================================================

        return OpportunityPipelineResult(
            company=company,
            sector=sector,
            catalyst=catalyst,
            expectation_gap=expectation_gap,
            mispricing=mispricing,
            asymmetry=asymmetry,
            evidence=evidence,
            synthesis=synthesis,
        )


# ==========================================================
# PUBLIC API
# ==========================================================


__all__ = [
    "OpportunityPipeline",
    "OpportunityPipelineResult",
]