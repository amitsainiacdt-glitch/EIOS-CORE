"""
EIOS
Everest Investment Operating System

Causal Chain Engine

Purpose:
Maps relationships between signals and identifies the
economic transmission mechanism from an external change
to a potential company-level consequence.

Architecture:

External Event
      ↓
Economic Mechanism
      ↓
Supply / Demand
      ↓
Sector Impact
      ↓
Company Exposure
      ↓
Revenue
      ↓
Margins
      ↓
Cash Flow
      ↓
Earnings
      ↓
Valuation
      ↓
Opportunity

Design Principles:
- No persistence.
- No valuation calculation.
- No investment recommendation.
- No mutation of Signal objects.
- Explicit causal reasoning.
- Supports multi-step causal chains.
- Contradictory links reduce confidence.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .signal_model import (
    Signal,
    SignalDirection,
)


# ==========================================================
# CAUSAL LINK
# ==========================================================


@dataclass
class CausalLink:
    """
    One relationship between two economic observations.
    """

    cause: str = ""

    effect: str = ""

    mechanism: str = ""

    direction: SignalDirection = (
        SignalDirection.UNKNOWN
    )

    strength: float = 0.0

    confidence: float = 0.0

    evidence: List[str] = field(
        default_factory=list
    )

    assumptions: List[str] = field(
        default_factory=list
    )

    contradictions: List[str] = field(
        default_factory=list
    )


# ==========================================================
# CAUSAL CHAIN
# ==========================================================


@dataclass
class CausalChain:
    """
    Complete economic transmission chain.
    """

    chain_id: str = ""

    title: str = ""

    links: List[CausalLink] = field(
        default_factory=list
    )

    signals: List[Signal] = field(
        default_factory=list
    )

    origin: str = ""

    sector_impacts: List[str] = field(
        default_factory=list
    )

    company_impacts: List[str] = field(
        default_factory=list
    )

    earnings_impacts: List[str] = field(
        default_factory=list
    )

    valuation_impacts: List[str] = field(
        default_factory=list
    )

    strongest_link: Optional[CausalLink] = None

    weakest_link: Optional[CausalLink] = None

    chain_score: float = 0.0

    confidence: float = 0.0

    complete: bool = False

    reasons: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )


# ==========================================================
# CAUSAL CHAIN ENGINE
# ==========================================================


class CausalChainEngine:
    """
    Builds and evaluates economic causal chains.

    The engine does not decide whether the chain represents
    an investable opportunity.
    """

    # ======================================================
    # BUILD
    # ======================================================

    def build(
        self,
        *,
        chain_id: str,
        title: str,
        signals: List[Signal],
        links: List[CausalLink],
        origin: str = "",
        sector_impacts: Optional[List[str]] = None,
        company_impacts: Optional[List[str]] = None,
        earnings_impacts: Optional[List[str]] = None,
        valuation_impacts: Optional[List[str]] = None,
    ) -> CausalChain:
        """
        Construct a causal chain from validated relationships.
        """

        chain = CausalChain()

        chain.chain_id = chain_id
        chain.title = title
        chain.signals = list(signals)
        chain.links = list(links)
        chain.origin = origin

        chain.sector_impacts = (
            list(sector_impacts or [])
        )

        chain.company_impacts = (
            list(company_impacts or [])
        )

        chain.earnings_impacts = (
            list(earnings_impacts or [])
        )

        chain.valuation_impacts = (
            list(valuation_impacts or [])
        )

        if not links:
            chain.warnings.append(
                "No causal links supplied."
            )

            return chain

        # --------------------------------------------------
        # Link Assessment
        # --------------------------------------------------

        chain.strongest_link = max(
            links,
            key=lambda link: link.strength,
        )

        chain.weakest_link = min(
            links,
            key=lambda link: link.strength,
        )

        # --------------------------------------------------
        # Chain Score
        # --------------------------------------------------

        chain.chain_score = (
            self._chain_score(links)
        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        chain.confidence = (
            self._confidence(links)
        )

        # --------------------------------------------------
        # Completeness
        # --------------------------------------------------

        chain.complete = (
            self._is_complete(chain)
        )

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        self._build_reasons(chain)

        return chain

    # ======================================================
    # SCORE
    # ======================================================

    def _chain_score(
        self,
        links: List[CausalLink],
    ) -> float:
        """
        Calculate chain strength from individual links.

        The weakest link receives additional weight because
        a causal chain is only as strong as its least-supported
        critical transmission step.
        """

        if not links:
            return 0.0

        strengths = [
            max(
                0.0,
                min(
                    100.0,
                    link.strength,
                ),
            )
            for link in links
        ]

        average = (
            sum(strengths)
            / len(strengths)
        )

        weakest = min(strengths)

        return (
            average * 0.70
            + weakest * 0.30
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    def _confidence(
        self,
        links: List[CausalLink],
    ) -> float:
        """
        Calculate confidence in the causal chain.
        """

        if not links:
            return 0.0

        values = [
            max(
                0.0,
                min(
                    100.0,
                    link.confidence,
                ),
            )
            for link in links
        ]

        average = (
            sum(values)
            / len(values)
        )

        contradiction_count = sum(
            len(link.contradictions)
            for link in links
        )

        contradiction_penalty = min(
            40.0,
            contradiction_count * 5.0,
        )

        return max(
            0.0,
            min(
                100.0,
                average
                - contradiction_penalty,
            ),
        )

    # ======================================================
    # COMPLETENESS
    # ======================================================

    def _is_complete(
        self,
        chain: CausalChain,
    ) -> bool:
        """
        Determine whether the causal chain reaches at least
        the sector/company economic impact level.
        """

        has_origin = bool(
            chain.origin
        )

        has_links = (
            len(chain.links) >= 2
        )

        has_sector = bool(
            chain.sector_impacts
        )

        has_company = bool(
            chain.company_impacts
        )

        return (
            has_origin
            and has_links
            and has_sector
            and has_company
        )

    # ======================================================
    # REASONS
    # ======================================================

    def _build_reasons(
        self,
        chain: CausalChain,
    ) -> None:
        """
        Generate transparent causal-chain reasoning.
        """

        if len(chain.links) >= 2:
            chain.reasons.append(
                "Multiple causal transmission steps identified."
            )

        if chain.strongest_link:
            chain.reasons.append(
                "Strongest causal link: "
                f"{chain.strongest_link.cause} → "
                f"{chain.strongest_link.effect}"
            )

        if chain.weakest_link:
            chain.warnings.append(
                "Weakest causal link: "
                f"{chain.weakest_link.cause} → "
                f"{chain.weakest_link.effect}"
            )

        if chain.complete:
            chain.reasons.append(
                "Causal chain reaches company-level impact."
            )
        else:
            chain.warnings.append(
                "Causal chain is incomplete."
            )

        if chain.confidence >= 75:
            chain.reasons.append(
                "Causal chain has high supporting confidence."
            )

        elif chain.confidence < 50:
            chain.warnings.append(
                "Causal chain confidence is below institutional threshold."
            )