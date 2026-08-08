"""
EIOS
Everest Investment Operating System

Signal Validation Engine

Purpose:
Validates the quality and reliability of Opportunity Intelligence
signals before they are allowed to influence catalyst or opportunity
analysis.

Architecture:

Signal
    ↓
SignalValidationEngine
    ↓
ValidationResult
    ↓
Catalyst / Opportunity Engines

Design Principles:
- Performs validation only.
- Does not mutate Signal.
- Does not calculate Opportunity Score.
- Does not perform valuation.
- Does not persist data.
- Confidence and Opportunity Score remain separate.
"""

from dataclasses import dataclass, field
from typing import List

from .signal_model import Signal


# ==========================================================
# VALIDATION RESULT
# ==========================================================


@dataclass
class SignalValidationResult:
    """
    Result of institutional signal validation.

    This is a passive result object.

    The validation engine determines the values.
    """

    valid: bool = False

    score: float = 0.0

    confidence: float = 0.0

    source_quality: float = 0.0

    evidence_quality: float = 0.0

    relevance: float = 0.0

    recency: float = 0.0

    persistence: float = 0.0

    corroboration: float = 0.0

    contradiction_penalty: float = 0.0

    independent_confirmation: int = 0

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    invalidation_reasons: List[str] = field(
        default_factory=list
    )


# ==========================================================
# VALIDATION ENGINE
# ==========================================================


class SignalValidationEngine:
    """
    Institutional Signal Validation Engine.

    Determines whether an observed signal contains enough
    evidence to proceed to higher-level Opportunity analysis.
    """

    MINIMUM_VALID_SCORE = 50.0

    # ======================================================
    # VALIDATE
    # ======================================================

    def validate(
        self,
        signal: Signal,
    ) -> SignalValidationResult:
        """
        Validate a canonical Signal.

        No mutation of the Signal object occurs.
        """

        result = SignalValidationResult()

        # --------------------------------------------------
        # Source Quality
        # --------------------------------------------------

        result.source_quality = (
            self._source_quality(signal)
        )

        # --------------------------------------------------
        # Evidence Quality
        # --------------------------------------------------

        result.evidence_quality = (
            self._evidence_quality(signal)
        )

        # --------------------------------------------------
        # Relevance
        # --------------------------------------------------

        result.relevance = (
            self._relevance(signal)
        )

        # --------------------------------------------------
        # Recency
        # --------------------------------------------------

        result.recency = (
            self._recency(signal)
        )

        # --------------------------------------------------
        # Persistence
        # --------------------------------------------------

        result.persistence = (
            self._persistence(signal)
        )

        # --------------------------------------------------
        # Corroboration
        # --------------------------------------------------

        result.corroboration = (
            self._corroboration(signal)
        )

        # --------------------------------------------------
        # Contradiction
        # --------------------------------------------------

        result.contradiction_penalty = (
            self._contradiction_penalty(signal)
        )

        # --------------------------------------------------
        # Independent Confirmation
        # --------------------------------------------------

        result.independent_confirmation = (
            signal.independent_confirmation
        )

        # --------------------------------------------------
        # Overall Score
        # --------------------------------------------------

        positive_score = (
            result.source_quality
            + result.evidence_quality
            + result.relevance
            + result.recency
            + result.persistence
            + result.corroboration
        ) / 6.0

        result.score = max(
            0.0,
            min(
                100.0,
                positive_score
                - result.contradiction_penalty,
            ),
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        result.confidence = self._confidence(
            result
        )

        # --------------------------------------------------
        # Reasons
        # --------------------------------------------------

        self._build_reasons(
            signal,
            result,
        )

        # --------------------------------------------------
        # Final Validation
        # --------------------------------------------------

        if result.score >= self.MINIMUM_VALID_SCORE:

            result.valid = True

        else:

            result.valid = False

            result.invalidation_reasons.append(
                "Signal does not meet minimum validation threshold."
            )

        return result

    # ======================================================
    # SOURCE QUALITY
    # ======================================================

    def _source_quality(
        self,
        signal: Signal,
    ) -> float:
        """
        Assess source quality.

        This deliberately uses explicit source information
        rather than assuming every source is equally reliable.
        """

        if not signal.source:
            return 0.0

        if signal.supporting_sources:
            return 100.0

        return 60.0

    # ======================================================
    # EVIDENCE QUALITY
    # ======================================================

    def _evidence_quality(
        self,
        signal: Signal,
    ) -> float:
        """
        Assess the breadth of supporting evidence.
        """

        evidence_count = len(
            signal.evidence
        )

        if evidence_count >= 5:
            return 100.0

        if evidence_count >= 3:
            return 80.0

        if evidence_count >= 2:
            return 65.0

        if evidence_count == 1:
            return 45.0

        return 0.0

    # ======================================================
    # RELEVANCE
    # ======================================================

    def _relevance(
        self,
        signal: Signal,
    ) -> float:
        """
        Use the explicit relevance supplied by the
        intelligence layer.

        A missing relevance assessment receives zero.
        """

        return max(
            0.0,
            min(
                100.0,
                signal.relevance,
            ),
        )

    # ======================================================
    # RECENCY
    # ======================================================

    def _recency(
        self,
        signal: Signal,
    ) -> float:
        """
        Use the explicit recency assessment.

        Date parsing and time-series logic will be handled
        by a dedicated temporal intelligence layer later.
        """

        if signal.detected_date:
            return 100.0

        return 0.0

    # ======================================================
    # PERSISTENCE
    # ======================================================

    def _persistence(
        self,
        signal: Signal,
    ) -> float:
        """
        Assess whether the signal appears persistent.

        Detailed time-series persistence analysis belongs
        to a later signal intelligence engine.
        """

        return max(
            0.0,
            min(
                100.0,
                signal.persistence,
            ),
        )

    # ======================================================
    # CORROBORATION
    # ======================================================

    def _corroboration(
        self,
        signal: Signal,
    ) -> float:
        """
        Assess independent corroboration.
        """

        if signal.independent_confirmation >= 3:
            return 100.0

        if signal.independent_confirmation == 2:
            return 80.0

        if signal.independent_confirmation == 1:
            return 55.0

        if signal.supporting_sources:
            return 40.0

        return 0.0

    # ======================================================
    # CONTRADICTION PENALTY
    # ======================================================

    def _contradiction_penalty(
        self,
        signal: Signal,
    ) -> float:
        """
        Penalize contradictory evidence.

        Contradiction is not automatically fatal.
        It reduces confidence until resolved.
        """

        count = len(
            signal.contradictory_evidence
        )

        if count >= 5:
            return 40.0

        if count >= 3:
            return 30.0

        if count == 2:
            return 20.0

        if count == 1:
            return 10.0

        return 0.0

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        result: SignalValidationResult,
    ) -> float:
        """
        Calculate validation confidence.

        Confidence is deliberately separate from the
        Opportunity Score.
        """

        confidence = (
            result.score * 0.70
            + result.corroboration * 0.20
            + result.evidence_quality * 0.10
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

    def _build_reasons(
        self,
        signal: Signal,
        result: SignalValidationResult,
    ) -> None:
        """
        Build human-readable validation reasoning.
        """

        if result.source_quality >= 80:
            result.reasons.append(
                "Strong supporting source evidence."
            )

        elif result.source_quality > 0:
            result.warnings.append(
                "Source evidence exists but requires further corroboration."
            )

        else:
            result.warnings.append(
                "No identifiable source evidence."
            )

        if result.evidence_quality >= 80:
            result.reasons.append(
                "Multiple supporting evidence items identified."
            )

        elif result.evidence_quality < 50:
            result.warnings.append(
                "Evidence base is currently weak."
            )

        if result.corroboration >= 80:
            result.reasons.append(
                "Signal has independent corroboration."
            )

        elif result.corroboration < 50:
            result.warnings.append(
                "Independent corroboration is limited."
            )

        if result.contradiction_penalty > 0:
            result.warnings.append(
                "Contradictory evidence requires investigation."
            )