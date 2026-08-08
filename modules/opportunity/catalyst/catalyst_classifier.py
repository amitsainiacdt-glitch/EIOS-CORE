"""
EIOS
Everest Investment Operating System

Catalyst Classifier
===================

Maps validated Opportunity signals and causal-chain information
to the canonical EIOS Catalyst Taxonomy.

Responsibilities
----------------
- Identify candidate catalyst families.
- Select a primary catalyst.
- Identify secondary catalysts.
- Calculate classification confidence.
- Preserve classification reasoning.
- Report unclassified signals.

Non-responsibilities
--------------------
- Catalyst scoring.
- Valuation.
- Opportunity ranking.
- Investment recommendation.
- Evidence scoring.
- Mutation of source Signal objects.

Architecture
------------

Signal
    ↓
Catalyst Classifier
    ↓
Primary Catalyst
Secondary Catalysts
Classification Confidence
    ↓
Catalyst Engine
"""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystDefinition,
    CatalystFamily,
    CatalystRegistry,
)

from modules.opportunity.signals.signal_model import (
    Signal,
)


# ==========================================================
# CLASSIFICATION RESULT
# ==========================================================


@dataclass(frozen=True)
class CatalystClassification:
    """
    Immutable result of catalyst classification.
    """

    primary: Optional[CatalystDefinition] = None

    secondary: Tuple[
        CatalystDefinition,
        ...
    ] = ()

    confidence: float = 0.0

    reasoning: Tuple[str, ...] = ()

    matched_signals: Tuple[str, ...] = ()

    unclassified_signals: Tuple[str, ...] = ()

    warnings: Tuple[str, ...] = ()

    @property
    def is_classified(self) -> bool:
        """
        True when a primary catalyst has been identified.
        """

        return self.primary is not None


# ==========================================================
# CLASSIFIER
# ==========================================================


class CatalystClassifier:
    """
    Deterministic classifier for canonical EIOS catalysts.
    """

    # ------------------------------------------------------
    # KEYWORD MAP
    # ------------------------------------------------------

    KEYWORD_MAP = {

        CatalystFamily.REVENUE_GROWTH: (
            "revenue",
            "sales growth",
            "top line",
            "turnover",
        ),

        CatalystFamily.VOLUME_GROWTH: (
            "volume",
            "volumes",
            "dispatch",
            "throughput",
            "units",
        ),

        CatalystFamily.PRICING: (
            "price",
            "pricing",
            "realisation",
            "realization",
            "price hike",
        ),

        CatalystFamily.PRODUCT_MIX: (
            "mix",
            "premium product",
            "product mix",
            "higher value",
        ),

        CatalystFamily.MARGIN_EXPANSION: (
            "margin",
            "ebitda margin",
            "operating margin",
            "margin expansion",
        ),

        CatalystFamily.COST_REDUCTION: (
            "cost reduction",
            "cost saving",
            "cost savings",
            "efficiency",
            "procurement saving",
        ),

        CatalystFamily.OPERATING_LEVERAGE: (
            "operating leverage",
            "fixed cost",
            "incremental margin",
        ),

        CatalystFamily.CAPACITY_EXPANSION: (
            "capacity expansion",
            "new capacity",
            "capacity addition",
            "capex expansion",
            "plant expansion",
        ),

        CatalystFamily.CAPACITY_UTILISATION: (
            "capacity utilisation",
            "capacity utilization",
            "utilisation",
            "utilization",
        ),

        CatalystFamily.ORDER_CONTRACT: (
            "order",
            "orders",
            "order book",
            "contract",
            "tender",
            "booking",
        ),

        CatalystFamily.CUSTOMER_ADDITION: (
            "new customer",
            "customer addition",
            "customer win",
            "client addition",
        ),

        CatalystFamily.MARKET_SHARE: (
            "market share",
            "share gain",
            "share gains",
        ),

        CatalystFamily.INDUSTRY_CAPITAL_CYCLE: (
            "capital cycle",
            "industry capex",
            "industry capital expenditure",
            "sector capex",
        ),

        CatalystFamily.SUPPLY_CONSTRAINT: (
            "supply constraint",
            "shortage",
            "scarcity",
            "capacity shortage",
            "tight supply",
        ),

        CatalystFamily.COMPETITIVE_EXIT: (
            "competitor exit",
            "competitor exits",
            "plant closure",
            "capacity closure",
            "industry consolidation",
        ),

        CatalystFamily.TECHNOLOGY_ADOPTION: (
            "technology adoption",
            "adoption",
            "digitisation",
            "digitalization",
            "automation",
            "ai adoption",
        ),

        CatalystFamily.NEW_PRODUCT_PLATFORM: (
            "new product",
            "new platform",
            "product launch",
            "new technology",
        ),

        CatalystFamily.TAM_EXPANSION: (
            "tam",
            "addressable market",
            "new market",
            "market expansion",
            "new application",
        ),

        CatalystFamily.REGULATORY_CHANGE: (
            "regulation",
            "regulatory",
            "regulatory change",
            "compliance",
            "approval",
            "license",
            "licensing",
        ),

        CatalystFamily.GOVERNMENT_POLICY: (
            "government policy",
            "government scheme",
            "government programme",
            "government program",
            "policy support",
        ),

        CatalystFamily.FISCAL_TAX: (
            "tax",
            "tax rate",
            "tax incentive",
            "fiscal",
            "budget",
        ),

        CatalystFamily.MONETARY_LIQUIDITY: (
            "interest rate",
            "interest rates",
            "rate cut",
            "rate hike",
            "liquidity",
            "monetary policy",
            "credit cycle",
        ),

        CatalystFamily.COMMODITY: (
            "commodity",
            "crude",
            "oil price",
            "metal price",
            "raw material",
            "input cost",
        ),

        CatalystFamily.CURRENCY: (
            "currency",
            "rupee",
            "usd",
            "forex",
            "foreign exchange",
            "exchange rate",
        ),

        CatalystFamily.TRADE_IMPORT_SUBSTITUTION: (
            "import substitution",
            "imports",
            "exports",
            "tariff",
            "trade",
            "local manufacturing",
        ),

        CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN: (
            "geopolitical",
            "geopolitics",
            "supply chain",
            "china plus one",
            "china+1",
            "relocation",
            "sanctions",
        ),

        CatalystFamily.CORPORATE_ACTION_MA: (
            "merger",
            "m&a",
            "acquisition",
            "demerger",
            "buyback",
            "spin off",
            "spinoff",
        ),

        CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION: (
            "capital allocation",
            "management change",
            "management improvement",
            "buyback",
            "dividend",
            "asset sale",
        ),

        CatalystFamily.BALANCE_SHEET_CASH_FLOW: (
            "deleveraging",
            "debt reduction",
            "debt repayment",
            "working capital",
            "cash flow",
            "free cash flow",
            "balance sheet",
        ),

        CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET: (
            "consensus",
            "estimate revision",
            "earnings surprise",
            "expectation reset",
            "market recognition",
            "analyst upgrade",
        ),
    }

    # ------------------------------------------------------
    # SCORE WEIGHTS
    # ------------------------------------------------------

    PRIMARY_THRESHOLD = 2

    # ======================================================
    # PUBLIC API
    # ======================================================

    def classify(
        self,
        *,
        signals: Sequence[Signal],
        causal_chain: object = None,
    ) -> CatalystClassification:
        """
        Classify a collection of signals.

        The classifier does not modify the Signal objects.
        """

        signal_list = list(signals)

        if not signal_list:

            return CatalystClassification(
                confidence=0.0,
                reasoning=(
                    "No signals were supplied.",
                ),
                warnings=(
                    "Catalyst classification cannot proceed "
                    "without signals.",
                ),
            )

        scores = {
            family: 0
            for family in CatalystFamily
        }

        matched_signal_ids = set()

        unclassified = []

        reasoning = []

        # --------------------------------------------------
        # SIGNAL CLASSIFICATION
        # --------------------------------------------------

        for signal in signal_list:

            text = self._signal_text(
                signal
            )

            matches = (
                self._match_signal(
                    text
                )
            )

            if not matches:

                unclassified.append(
                    signal.signal_id
                    or signal.title
                    or "UNKNOWN"
                )

                continue

            for family, strength in matches:

                scores[family] += strength

                matched_signal_ids.add(
                    signal.signal_id
                    or signal.title
                    or "UNKNOWN"
                )

        # --------------------------------------------------
        # CAUSAL CHAIN SUPPORT
        # --------------------------------------------------

        if causal_chain is not None:

            chain_text = (
                self._object_text(
                    causal_chain
                )
            )

            chain_matches = (
                self._match_text(
                    chain_text
                )
            )

            for family in chain_matches:

                scores[family] += 1

        # --------------------------------------------------
        # RANK
        # --------------------------------------------------

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        ranked = [
            item
            for item in ranked
            if item[1] > 0
        ]

        if not ranked:

            return CatalystClassification(
                confidence=0.0,
                reasoning=(
                    "No catalyst family could be "
                    "classified from the supplied signals.",
                ),
                unclassified_signals=tuple(
                    unclassified
                ),
                warnings=(
                    "Signals require manual catalyst classification.",
                ),
            )

        primary_family, primary_score = (
            ranked[0]
        )

        primary = CatalystRegistry.get(
            primary_family
        )

        # --------------------------------------------------
        # SECONDARY CATALYSTS
        # --------------------------------------------------

        secondary = []

        for family, score in ranked[1:]:

            if score <= 0:
                continue

            if (
                score
                >= max(
                    1,
                    primary_score // 2,
                )
            ):

                secondary.append(
                    CatalystRegistry.get(
                        family
                    )
                )

        # --------------------------------------------------
        # CONFIDENCE
        # --------------------------------------------------

        confidence = (
            self._confidence(
                primary_score=primary_score,
                ranked=ranked,
                total_signals=len(
                    signal_list
                ),
                unclassified=len(
                    unclassified
                ),
            )
        )

        # --------------------------------------------------
        # REASONING
        # --------------------------------------------------

        reasoning.append(
            (
                f"Primary catalyst classified as "
                f"{primary.family.value}."
            )
        )

        reasoning.append(
            (
                f"Classification strength: "
                f"{primary_score}."
            )
        )

        if secondary:

            reasoning.append(
                (
                    "Secondary catalyst families were "
                    "identified from overlapping evidence."
                )
            )

        if unclassified:

            reasoning.append(
                (
                    f"{len(unclassified)} signal(s) "
                    "could not be mapped to a canonical "
                    "catalyst family."
                )
            )

        warnings = []

        if confidence < 60.0:

            warnings.append(
                "Catalyst classification confidence "
                "is below the institutional threshold."
            )

        if unclassified:

            warnings.append(
                "Some signals remain unclassified."
            )

        return CatalystClassification(
            primary=primary,
            secondary=tuple(
                secondary
            ),
            confidence=confidence,
            reasoning=tuple(
                reasoning
            ),
            matched_signals=tuple(
                sorted(
                    matched_signal_ids
                )
            ),
            unclassified_signals=tuple(
                unclassified
            ),
            warnings=tuple(
                warnings
            ),
        )

    # ======================================================
    # INTERNAL HELPERS
    # ======================================================

    @staticmethod
    def _signal_text(
        signal: Signal,
    ) -> str:
        """
        Build searchable text from a Signal.
        """

        values = [

            signal.title,

            signal.description,

            signal.economic_mechanism,

            signal.supply_demand_impact,

            signal.earnings_impact,

            signal.source,

            signal.source_type,

            " ".join(
                signal.themes
            ),

            " ".join(
                signal.sectors
            ),
        ]

        return " ".join(
            value
            for value in values
            if value
        ).lower()

    @staticmethod
    def _object_text(
        value: object,
    ) -> str:
        """
        Safely convert an arbitrary causal-chain object
        into searchable text.
        """

        return str(
            value
        ).lower()

    def _match_signal(
        self,
        text: str,
    ) -> List[
        Tuple[CatalystFamily, int]
    ]:
        """
        Return matching catalyst families and scores.
        """

        matches = []

        for family, keywords in (
            self.KEYWORD_MAP.items()
        ):

            strength = 0

            for keyword in keywords:

                if keyword in text:

                    strength += 1

            if strength > 0:

                matches.append(
                    (
                        family,
                        strength,
                    )
                )

        return matches

    def _match_text(
        self,
        text: str,
    ) -> List[CatalystFamily]:
        """
        Match arbitrary text against the taxonomy.
        """

        matches = []

        for family, keywords in (
            self.KEYWORD_MAP.items()
        ):

            if any(
                keyword in text
                for keyword in keywords
            ):

                matches.append(
                    family
                )

        return matches

    @staticmethod
    def _confidence(
        *,
        primary_score: int,
        ranked: List[
            Tuple[CatalystFamily, int]
        ],
        total_signals: int,
        unclassified: int,
    ) -> float:
        """
        Calculate classification confidence.

        This is classification confidence only.
        It is NOT catalyst strength.
        """

        if primary_score <= 0:

            return 0.0

        second_score = (
            ranked[1][1]
            if len(ranked) > 1
            else 0
        )

        separation = (
            primary_score
            - second_score
        )

        base = 55.0

        base += min(
            25.0,
            primary_score * 5.0,
        )

        base += min(
            15.0,
            separation * 5.0,
        )

        if total_signals > 0:

            coverage = (
                (
                    total_signals
                    - unclassified
                )
                / total_signals
            )

            base *= (
                0.75
                + 0.25 * coverage
            )

        return round(
            max(
                0.0,
                min(
                    100.0,
                    base,
                ),
            ),
            2,
        )


# ==========================================================
# PUBLIC API
# ==========================================================


__all__ = [
    "CatalystClassifier",
    "CatalystClassification",
]