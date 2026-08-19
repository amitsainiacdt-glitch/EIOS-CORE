"""
EIOS
Everest Investment Operating System

Signal Interpretation Engine
============================

Purpose
-------
Converts an EvidenceItem plus an explicit
SignalInterpretation into the canonical Signal model.

Architecture

EvidenceItem
     ↓
SignalInterpretation
     ↓
SignalInterpretationEngine
     ↓
Signal
     ↓
SignalValidationEngine

Design Principles
-----------------
- Deterministic.
- Explicit interpretation only.
- No semantic guessing.
- No AI.
- No persistence.
- No valuation.
- No opportunity scoring.
- No catalyst analysis.
- Does not modify EvidenceItem.
- Preserves evidence provenance.
"""

from __future__ import annotations

from dataclasses import dataclass

from modules.opportunity.evidence_engine import (
    EvidenceItem,
)

from .signal_interpretation import (
    SignalInterpretation,
)

from .signal_model import (
    EvidenceQuality,
    Signal,
)


# ==========================================================
# RESULT
# ==========================================================


@dataclass(frozen=True)
class SignalInterpretationResult:
    """
    Result of converting EvidenceItem into a Signal.

    The result is immutable and explicitly records whether
    Signal creation was accepted.
    """

    accepted: bool

    reason: str

    signal: Signal | None = None


# ==========================================================
# ENGINE
# ==========================================================


class SignalInterpretationEngine:
    """
    Converts explicitly interpreted EvidenceItem objects into
    canonical Signals.

    This engine does not perform interpretation itself.

    The caller must supply SignalInterpretation explicitly.
    """

    # ======================================================
    # PUBLIC API
    # ======================================================

    def create(
        self,
        *,
        evidence: EvidenceItem,
        interpretation: SignalInterpretation,
        signal_id: str,
    ) -> SignalInterpretationResult:
        """
        Create a canonical Signal from an EvidenceItem and
        explicit SignalInterpretation.
        """

        if evidence is None:
            raise ValueError(
                "evidence must not be None"
            )

        if interpretation is None:
            raise ValueError(
                "interpretation must not be None"
            )

        if not signal_id or not signal_id.strip():
            raise ValueError(
                "signal_id must not be empty"
            )

        validation_error = (
            self._validate(
                evidence=evidence,
                interpretation=interpretation,
            )
        )

        if validation_error is not None:

            return SignalInterpretationResult(
                accepted=False,
                reason=validation_error,
                signal=None,
            )

        signal = Signal(
            signal_id=signal_id,

            title=interpretation.title,

            description=interpretation.description,

            domain=interpretation.domain,

            signal_type=interpretation.signal_type,

            direction=interpretation.direction,

            stage=interpretation.stage,

            horizon=interpretation.horizon,

            # --------------------------------------------------
            # ORIGIN
            # --------------------------------------------------

            source=evidence.source,

            source_type=(
                "Primary"
                if evidence.is_primary_source
                else "Secondary"
            ),

            source_date="",

            detected_date=(
                interpretation.detected_date
            ),

            # --------------------------------------------------
            # ENTITIES
            # --------------------------------------------------

            countries=list(
                interpretation.countries
            ),

            sectors=list(
                interpretation.sectors
            ),

            companies=list(
                interpretation.companies
            ),

            commodities=list(
                interpretation.commodities
            ),

            themes=list(
                interpretation.themes
            ),

            # --------------------------------------------------
            # ECONOMIC MEANING
            # --------------------------------------------------

            economic_mechanism=(
                interpretation.economic_mechanism
            ),

            supply_demand_impact=(
                interpretation.supply_demand_impact
            ),

            earnings_impact=(
                interpretation.earnings_impact
            ),

            valuation_impact=(
                interpretation.valuation_impact
            ),

            # --------------------------------------------------
            # SIGNAL STRENGTH
            # --------------------------------------------------

            magnitude=(
                interpretation.magnitude
            ),

            probability=(
                interpretation.probability
            ),

            persistence=(
                interpretation.persistence
            ),

            relevance=(
                interpretation.relevance
            ),

            corroboration=float(
                evidence.independent_confirmation
            ),

            confidence=evidence.confidence,

            evidence_quality=(
                self._evidence_quality(
                    evidence
                )
            ),

            # --------------------------------------------------
            # EVIDENCE
            # --------------------------------------------------

            evidence=[
                evidence.evidence_id
            ],

            supporting_sources=[
                evidence.source
            ],

            contradictory_evidence=[],

            assumptions=[],

            # --------------------------------------------------
            # MARKET CONTEXT
            # --------------------------------------------------

            market_expectation=(
                interpretation.market_expectation
            ),

            market_recognition=(
                interpretation.market_recognition
            ),

            price_reaction=(
                interpretation.price_reaction
            ),

            # --------------------------------------------------
            # CAUSAL CHAIN
            # --------------------------------------------------

            causal_chain=list(
                interpretation.causal_chain
            ),

            beneficiaries=list(
                interpretation.beneficiaries
            ),

            adversely_affected=list(
                interpretation.adversely_affected
            ),

            # --------------------------------------------------
            # VALIDATION METADATA
            # --------------------------------------------------

            independent_confirmation=(
                evidence.independent_confirmation
            ),

            historical_precedent=(
                interpretation.historical_precedent
            ),

            invalidation_conditions=list(
                interpretation.invalidation_conditions
            ),

            # --------------------------------------------------
            # PROVENANCE METADATA
            # --------------------------------------------------

            metadata={
                "evidence_id": (
                    evidence.evidence_id
                ),

                "evidence_source": (
                    evidence.source
                ),

                "evidence_category": (
                    evidence.category
                ),
            },
        )

        return SignalInterpretationResult(
            accepted=True,
            reason=(
                "EvidenceItem successfully converted "
                "into a canonical Signal."
            ),
            signal=signal,
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def _validate(
        self,
        *,
        evidence: EvidenceItem,
        interpretation: SignalInterpretation,
    ) -> str | None:
        """
        Validate the explicit interpretation boundary.
        """

        if not evidence.evidence_id:
            return (
                "EvidenceItem must have an evidence_id."
            )

        if not evidence.source:
            return (
                "EvidenceItem must have a source."
            )

        if not evidence.statement:
            return (
                "EvidenceItem must have a statement."
            )

        if not interpretation.title.strip():
            return (
                "Signal interpretation requires a title."
            )

        if not interpretation.description.strip():
            return (
                "Signal interpretation requires a description."
            )

        return None

    # ======================================================
    # EVIDENCE QUALITY
    # ======================================================

    @staticmethod
    def _evidence_quality(
        evidence: EvidenceItem,
    ) -> EvidenceQuality:
        """
        Translate explicit EvidenceItem strength into the
        existing canonical EvidenceQuality enum.

        This is classification only; no new evidence score
        is calculated.
        """

        strength = evidence.strength

        if strength >= 90:
            return EvidenceQuality.A_PLUS

        if strength >= 80:
            return EvidenceQuality.A

        if strength >= 65:
            return EvidenceQuality.B

        if strength >= 50:
            return EvidenceQuality.C

        return EvidenceQuality.D


__all__ = [
    "SignalInterpretationResult",
    "SignalInterpretationEngine",
]