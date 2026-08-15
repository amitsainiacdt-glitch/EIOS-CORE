"""
EIOS
Everest Investment Operating System

Catalyst Pattern Registry

Purpose:
Canonical registry assembling catalyst patterns from
family-specific pattern modules.

Architecture:

    Catalyst Taxonomy
            ↓
    Family Pattern Modules
            ↓
    Catalyst Pattern Registry
            ↓
    Opportunity Engine

Design Principles:

- Pattern definitions live in family modules.
- Registry is the canonical access layer.
- Duplicate IDs are rejected.
- Registry performs no analysis.
- Registry performs no scoring.
- Registry performs no ranking.
- Registry performs no valuation.
"""

from typing import Dict, List


from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)


from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# FAMILY PATTERN MODULES
# ==========================================================

from modules.opportunity.catalyst.patterns.capacity_patterns import (
    CAPACITY_PATTERNS,
)

from modules.opportunity.catalyst.patterns.capacity_utilisation_patterns import (
    CAPACITY_UTILISATION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.order_patterns import (
    ORDER_PATTERNS,
)

from modules.opportunity.catalyst.patterns.regulatory_patterns import (
    REGULATORY_PATTERNS,
)

from modules.opportunity.catalyst.patterns.revenue_patterns import (
    REVENUE_PATTERNS,
)

from modules.opportunity.catalyst.patterns.volume_patterns import (
    VOLUME_PATTERNS,
)

from modules.opportunity.catalyst.patterns.pricing_patterns import (
    PRICING_PATTERNS,
)

from modules.opportunity.catalyst.patterns.margin_patterns import (
    MARGIN_PATTERNS,
)

from modules.opportunity.catalyst.patterns.technology_adoption_patterns import (
    TECHNOLOGY_ADOPTION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.market_recognition_expectation_reset_patterns import (
    MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS,
)

from modules.opportunity.catalyst.patterns.product_mix_patterns import (
    PRODUCT_MIX_PATTERNS,
)

from modules.opportunity.catalyst.patterns.cost_reduction_patterns import (
    COST_REDUCTION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.operating_leverage_patterns import (
    OPERATING_LEVERAGE_PATTERNS,
)

from modules.opportunity.catalyst.patterns.customer_addition_patterns import (
    CUSTOMER_ADDITION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.market_share_patterns import (
    MARKET_SHARE_PATTERNS,
)

from modules.opportunity.catalyst.patterns.industry_capital_cycle_patterns import (
    INDUSTRY_CAPITAL_CYCLE_PATTERNS,
)

from modules.opportunity.catalyst.patterns.supply_constraint_patterns import (
    SUPPLY_CONSTRAINT_PATTERNS,
)

from modules.opportunity.catalyst.patterns.competitive_exit_patterns import (
    COMPETITIVE_EXIT_PATTERNS,
)

from modules.opportunity.catalyst.patterns.new_product_platform_patterns import (
    NEW_PRODUCT_PLATFORM_PATTERNS,
)

from modules.opportunity.catalyst.patterns.tam_expansion_patterns import (
    TAM_EXPANSION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.government_policy_patterns import (
    GOVERNMENT_POLICY_PATTERNS,
)

from modules.opportunity.catalyst.patterns.fiscal_tax_patterns import (
    FISCAL_TAX_PATTERNS,
)

from modules.opportunity.catalyst.patterns.monetary_liquidity_patterns import (
    MONETARY_LIQUIDITY_PATTERNS,
)

from modules.opportunity.catalyst.patterns.commodity_patterns import (
    COMMODITY_PATTERNS,
)

from modules.opportunity.catalyst.patterns.currency_patterns import (
    CURRENCY_PATTERNS,
)

from modules.opportunity.catalyst.patterns.trade_import_substitution_patterns import (
    TRADE_IMPORT_SUBSTITUTION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.geopolitical_supply_chain_patterns import (
    GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS,
)

from modules.opportunity.catalyst.patterns.corporate_action_ma_patterns import (
    CORPORATE_ACTION_MA_PATTERNS,
)

from modules.opportunity.catalyst.patterns.management_capital_allocation_patterns import (
    MANAGEMENT_CAPITAL_ALLOCATION_PATTERNS,
)

from modules.opportunity.catalyst.patterns.balance_sheet_cash_flow_patterns import (
    BALANCE_SHEET_CASH_FLOW_PATTERNS,
)


# ==========================================================
# CANONICAL REGISTRY
# ==========================================================

CATALYST_PATTERNS: Dict[
    str,
    CatalystPattern,
] = {}


# ==========================================================
# REGISTRATION
# ==========================================================

def _register(
    patterns: List[CatalystPattern],
) -> None:
    """
    Register canonical catalyst patterns.

    Duplicate pattern IDs are rejected immediately.
    """

    for pattern in patterns:

        if pattern.pattern_id in CATALYST_PATTERNS:

            raise ValueError(
                "Duplicate catalyst pattern ID: "
                f"{pattern.pattern_id}"
            )

        CATALYST_PATTERNS[
            pattern.pattern_id
        ] = pattern


# ==========================================================
# FAMILY REGISTRATION
# ==========================================================

_register(
    CAPACITY_PATTERNS
)

_register(
    CAPACITY_UTILISATION_PATTERNS
)

_register(
    ORDER_PATTERNS
)

_register(
    REGULATORY_PATTERNS
)

_register(
    REVENUE_PATTERNS
)

_register(
    VOLUME_PATTERNS
)

_register(
    PRICING_PATTERNS
)

_register(
    MARGIN_PATTERNS
)

_register(
    TECHNOLOGY_ADOPTION_PATTERNS
)

_register(
    MARKET_RECOGNITION_EXPECTATION_RESET_PATTERNS
)

_register(
    PRODUCT_MIX_PATTERNS
)

_register(
    COST_REDUCTION_PATTERNS
)

_register(
    OPERATING_LEVERAGE_PATTERNS
)

_register(
    CUSTOMER_ADDITION_PATTERNS
)

_register(
    MARKET_SHARE_PATTERNS
)

_register(
    INDUSTRY_CAPITAL_CYCLE_PATTERNS
)

_register(
    SUPPLY_CONSTRAINT_PATTERNS
)

_register(
    COMPETITIVE_EXIT_PATTERNS
)

_register(
    NEW_PRODUCT_PLATFORM_PATTERNS
)

_register(
    TAM_EXPANSION_PATTERNS
)

_register(
    GOVERNMENT_POLICY_PATTERNS
)

_register(
    FISCAL_TAX_PATTERNS
)

_register(
    MONETARY_LIQUIDITY_PATTERNS
)

_register(
    COMMODITY_PATTERNS
)

_register(
    CURRENCY_PATTERNS
)

_register(
    TRADE_IMPORT_SUBSTITUTION_PATTERNS
)

_register(
    GEOPOLITICAL_SUPPLY_CHAIN_PATTERNS
)

_register(
    CORPORATE_ACTION_MA_PATTERNS
)

_register(
    MANAGEMENT_CAPITAL_ALLOCATION_PATTERNS
)

_register(
    BALANCE_SHEET_CASH_FLOW_PATTERNS
)


# ==========================================================
# REGISTRY ACCESS
# ==========================================================

class CatalystPatternRegistry:
    """
    Canonical read-only access to catalyst patterns.
    """

    @staticmethod
    def all() -> List[CatalystPattern]:
        """
        Return all registered catalyst patterns.
        """

        return list(
            CATALYST_PATTERNS.values()
        )

    @staticmethod
    def get(
        pattern_id: str,
    ) -> CatalystPattern:
        """
        Return a catalyst pattern by canonical ID.
        """

        return CATALYST_PATTERNS[
            pattern_id
        ]

    @staticmethod
    def get_by_family(
        family: CatalystFamily,
    ) -> List[CatalystPattern]:
        """
        Return all patterns belonging to a family.
        """

        return [
            pattern
            for pattern in CATALYST_PATTERNS.values()
            if pattern.family == family
        ]

    @staticmethod
    def count() -> int:
        """
        Return total registered pattern count.
        """

        return len(
            CATALYST_PATTERNS
        )


__all__ = [
    "CATALYST_PATTERNS",
    "CatalystPatternRegistry",
]