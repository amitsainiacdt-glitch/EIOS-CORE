"""
EIOS
Everest Investment Operating System

Catalyst Taxonomy
=================

Canonical catalogue of investment catalyst families.

Purpose
-------
Defines the institutional vocabulary used to classify catalysts.

This module does NOT:
- calculate catalyst scores
- calculate valuation
- rank companies
- make investment recommendations
- mutate source objects

The Catalyst Engine remains responsible for analytical scoring.

Architecture
------------
Signal
    ↓
Catalyst Classification
    ↓
Catalyst Taxonomy
    ↓
Catalyst Engine
    ↓
Expectation Gap
    ↓
Mispricing
"""


from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


# ==========================================================
# CATALYST FAMILY
# ==========================================================


class CatalystFamily(str, Enum):
    """
    Canonical EIOS catalyst families.
    """

    REVENUE_GROWTH = "Revenue Growth"

    VOLUME_GROWTH = "Volume Growth"

    PRICING = "Pricing"

    PRODUCT_MIX = "Product Mix"

    MARGIN_EXPANSION = "Margin Expansion"

    COST_REDUCTION = "Cost Reduction"

    OPERATING_LEVERAGE = "Operating Leverage"

    CAPACITY_EXPANSION = "Capacity Expansion"

    CAPACITY_UTILISATION = "Capacity Utilisation"

    ORDER_CONTRACT = "Order / Contract"

    CUSTOMER_ADDITION = "Customer Addition"

    MARKET_SHARE = "Market Share"

    INDUSTRY_CAPITAL_CYCLE = "Industry Capital Cycle"

    SUPPLY_CONSTRAINT = "Supply Constraint"

    COMPETITIVE_EXIT = "Competitive Exit"

    TECHNOLOGY_ADOPTION = "Technology Adoption"

    NEW_PRODUCT_PLATFORM = "New Product / Platform"

    TAM_EXPANSION = "TAM Expansion"

    REGULATORY_CHANGE = "Regulatory Change"

    GOVERNMENT_POLICY = "Government Policy"

    FISCAL_TAX = "Fiscal / Tax"

    MONETARY_LIQUIDITY = "Monetary / Liquidity"

    COMMODITY = "Commodity"

    CURRENCY = "Currency"

    TRADE_IMPORT_SUBSTITUTION = (
        "Trade / Import Substitution"
    )

    GEOPOLITICAL_SUPPLY_CHAIN = (
        "Geopolitical / Supply Chain"
    )

    CORPORATE_ACTION_MA = (
        "Corporate Action / M&A"
    )

    MANAGEMENT_CAPITAL_ALLOCATION = (
        "Management / Capital Allocation"
    )

    BALANCE_SHEET_CASH_FLOW = (
        "Balance Sheet / Cash Flow"
    )

    MARKET_RECOGNITION_EXPECTATION_RESET = (
        "Market Recognition / Expectation Reset"
    )


# ==========================================================
# CATALYST METADATA
# ==========================================================


@dataclass(frozen=True)
class CatalystDefinition:
    """
    Institutional definition of one catalyst family.
    """

    catalyst_id: str

    family: CatalystFamily

    description: str

    mechanism: str

    typical_earnings_impact: List[str]

    typical_evidence: List[str]

    typical_market_mistake: str

    invalidation_examples: List[str]


# ==========================================================
# TAXONOMY
# ==========================================================


CATALYST_TAXONOMY: Dict[
    CatalystFamily,
    CatalystDefinition,
] = {

    # ------------------------------------------------------
    # OPERATING / EARNINGS
    # ------------------------------------------------------

    CatalystFamily.REVENUE_GROWTH: CatalystDefinition(
        catalyst_id="CAT-REV-GROWTH",
        family=CatalystFamily.REVENUE_GROWTH,
        description=(
            "Acceleration or inflection in company revenue."
        ),
        mechanism=(
            "Demand improvement → revenue growth → "
            "earnings growth."
        ),
        typical_earnings_impact=[
            "Revenue",
            "EBITDA",
            "EPS",
            "Free Cash Flow",
        ],
        typical_evidence=[
            "Order growth",
            "Customer demand",
            "Volume data",
            "Management commentary",
        ],
        typical_market_mistake=(
            "Market assumes revenue acceleration "
            "is temporary or consensus remains stale."
        ),
        invalidation_examples=[
            "Demand deterioration",
            "Order cancellations",
            "Growth deceleration",
        ],
    ),

    CatalystFamily.VOLUME_GROWTH: CatalystDefinition(
        catalyst_id="CAT-VOLUME-GROWTH",
        family=CatalystFamily.VOLUME_GROWTH,
        description=(
            "Material increase in units, transactions "
            "or physical throughput."
        ),
        mechanism=(
            "Higher volumes → fixed-cost absorption → "
            "operating leverage → earnings growth."
        ),
        typical_earnings_impact=[
            "Revenue",
            "Utilisation",
            "EBITDA Margin",
            "EPS",
        ],
        typical_evidence=[
            "Volume data",
            "Production data",
            "Dispatches",
            "Industry demand",
        ],
        typical_market_mistake=(
            "Market underestimates duration or "
            "operating leverage."
        ),
        invalidation_examples=[
            "Volume decline",
            "Demand weakness",
        ],
    ),

    CatalystFamily.PRICING: CatalystDefinition(
        catalyst_id="CAT-PRICING",
        family=CatalystFamily.PRICING,
        description=(
            "Improvement in realised pricing or pricing power."
        ),
        mechanism=(
            "Pricing improvement → revenue per unit ↑ → "
            "margin and earnings improvement."
        ),
        typical_earnings_impact=[
            "Realisation",
            "Gross Margin",
            "EBITDA",
            "EPS",
        ],
        typical_evidence=[
            "Price increases",
            "Contract renewals",
            "Industry pricing",
            "Competitor capacity",
        ],
        typical_market_mistake=(
            "Market underestimates pricing durability."
        ),
        invalidation_examples=[
            "Price reversal",
            "Demand elasticity",
            "Competitive undercutting",
        ],
    ),

    CatalystFamily.PRODUCT_MIX: CatalystDefinition(
        catalyst_id="CAT-PRODUCT-MIX",
        family=CatalystFamily.PRODUCT_MIX,
        description=(
            "Shift toward higher-margin or higher-value products."
        ),
        mechanism=(
            "Premium mix → higher realisation → "
            "margin expansion → higher earnings quality."
        ),
        typical_earnings_impact=[
            "Gross Margin",
            "EBITDA Margin",
            "ROCE",
            "EPS",
        ],
        typical_evidence=[
            "Segment mix",
            "Premium product growth",
            "Management commentary",
        ],
        typical_market_mistake=(
            "Market focuses on headline revenue rather "
            "than mix-driven profitability."
        ),
        invalidation_examples=[
            "Mix reversal",
            "Premium demand weakness",
        ],
    ),

    CatalystFamily.MARGIN_EXPANSION: CatalystDefinition(
        catalyst_id="CAT-MARGIN",
        family=CatalystFamily.MARGIN_EXPANSION,
        description=(
            "Structural or cyclical improvement in margins."
        ),
        mechanism=(
            "Revenue/mix/pricing/cost improvement → "
            "margin expansion → disproportionate EPS growth."
        ),
        typical_earnings_impact=[
            "EBITDA Margin",
            "EBIT Margin",
            "EPS",
            "FCF",
        ],
        typical_evidence=[
            "Gross margin trend",
            "Operating leverage",
            "Cost data",
            "Product mix",
        ],
        typical_market_mistake=(
            "Market treats margin improvement as temporary."
        ),
        invalidation_examples=[
            "Input-cost inflation",
            "Pricing pressure",
            "Margin reversal",
        ],
    ),

    CatalystFamily.COST_REDUCTION: CatalystDefinition(
        catalyst_id="CAT-COST-REDUCTION",
        family=CatalystFamily.COST_REDUCTION,
        description=(
            "Sustainable reduction in operating or input costs."
        ),
        mechanism=(
            "Lower unit cost → margin improvement → "
            "higher earnings and cash generation."
        ),
        typical_earnings_impact=[
            "EBITDA Margin",
            "EBIT",
            "FCF",
        ],
        typical_evidence=[
            "Cost programme",
            "Automation",
            "Procurement savings",
            "Operating data",
        ],
        typical_market_mistake=(
            "Market doubts savings durability."
        ),
        invalidation_examples=[
            "Savings fail to materialise",
            "Cost inflation",
        ],
    ),

    CatalystFamily.OPERATING_LEVERAGE: CatalystDefinition(
        catalyst_id="CAT-OPERATING-LEVERAGE",
        family=CatalystFamily.OPERATING_LEVERAGE,
        description=(
            "Fixed-cost absorption creates disproportionate "
            "earnings growth."
        ),
        mechanism=(
            "Revenue growth → fixed-cost absorption → "
            "margin expansion → EPS acceleration."
        ),
        typical_earnings_impact=[
            "EBITDA Margin",
            "EPS",
            "ROCE",
            "ROIIC",
        ],
        typical_evidence=[
            "Utilisation",
            "Revenue growth",
            "Cost structure",
            "Historical margin behaviour",
        ],
        typical_market_mistake=(
            "Market underestimates incremental margins."
        ),
        invalidation_examples=[
            "Utilisation deterioration",
            "Weak revenue growth",
        ],
    ),

    # ------------------------------------------------------
    # CAPACITY / DEMAND
    # ------------------------------------------------------

    CatalystFamily.CAPACITY_EXPANSION: CatalystDefinition(
        catalyst_id="CAT-CAPACITY-EXPANSION",
        family=CatalystFamily.CAPACITY_EXPANSION,
        description=(
            "New capacity unlocks additional addressable demand."
        ),
        mechanism=(
            "Capacity addition → volume opportunity → "
            "revenue growth → incremental returns."
        ),
        typical_earnings_impact=[
            "Revenue",
            "EBITDA",
            "ROCE",
            "ROIIC",
        ],
        typical_evidence=[
            "Capex announcements",
            "Commissioning",
            "Capacity utilisation",
            "Customer demand",
        ],
        typical_market_mistake=(
            "Market discounts future capacity economics."
        ),
        invalidation_examples=[
            "Project delays",
            "Demand shortfall",
            "Cost overruns",
        ],
    ),

    CatalystFamily.CAPACITY_UTILISATION: CatalystDefinition(
        catalyst_id="CAT-CAPACITY-UTILISATION",
        family=CatalystFamily.CAPACITY_UTILISATION,
        description=(
            "Existing capacity moves toward higher utilisation."
        ),
        mechanism=(
            "Utilisation ↑ → fixed-cost absorption → "
            "margin ↑ → ROCE/ROIIC ↑."
        ),
        typical_earnings_impact=[
            "Revenue",
            "EBITDA Margin",
            "ROCE",
            "ROIIC",
        ],
        typical_evidence=[
            "Utilisation data",
            "Order book",
            "Production",
            "Customer capex",
        ],
        typical_market_mistake=(
            "Market fails to recognise operating leverage."
        ),
        invalidation_examples=[
            "Demand slowdown",
            "Utilisation decline",
        ],
    ),

    CatalystFamily.ORDER_CONTRACT: CatalystDefinition(
        catalyst_id="CAT-ORDER-CONTRACT",
        family=CatalystFamily.ORDER_CONTRACT,
        description=(
            "Material order, contract or project win."
        ),
        mechanism=(
            "Order visibility → future revenue → "
            "earnings visibility."
        ),
        typical_earnings_impact=[
            "Revenue Visibility",
            "Order Book",
            "EPS",
        ],
        typical_evidence=[
            "Order announcements",
            "Tender wins",
            "Contract awards",
            "Backlog",
        ],
        typical_market_mistake=(
            "Market underestimates conversion probability "
            "or duration."
        ),
        invalidation_examples=[
            "Cancellation",
            "Execution delays",
            "Margin deterioration",
        ],
    ),

    CatalystFamily.CUSTOMER_ADDITION: CatalystDefinition(
        catalyst_id="CAT-CUSTOMER-ADDITION",
        family=CatalystFamily.CUSTOMER_ADDITION,
        description=(
            "Addition of strategically important customers."
        ),
        mechanism=(
            "Customer addition → revenue diversification → "
            "volume growth → credibility."
        ),
        typical_earnings_impact=[
            "Revenue",
            "Volume",
            "Customer Concentration",
        ],
        typical_evidence=[
            "Customer wins",
            "Qualification",
            "Contracts",
            "Repeat orders",
        ],
        typical_market_mistake=(
            "Market underestimates customer lifetime value."
        ),
        invalidation_examples=[
            "Customer loss",
            "Low repeat business",
        ],
    ),

    CatalystFamily.MARKET_SHARE: CatalystDefinition(
        catalyst_id="CAT-MARKET-SHARE",
        family=CatalystFamily.MARKET_SHARE,
        description=(
            "Company gains share in an existing market."
        ),
        mechanism=(
            "Competitive advantage → share gain → "
            "volume/revenue growth."
        ),
        typical_earnings_impact=[
            "Revenue Growth",
            "Volume",
            "ROIC",
        ],
        typical_evidence=[
            "Market-share data",
            "Competitor commentary",
            "Customer wins",
        ],
        typical_market_mistake=(
            "Market assumes industry growth is the only driver."
        ),
        invalidation_examples=[
            "Share loss",
            "Competitive response",
        ],
    ),

    # ------------------------------------------------------
    # INDUSTRY STRUCTURE
    # ------------------------------------------------------

    CatalystFamily.INDUSTRY_CAPITAL_CYCLE: CatalystDefinition(
        catalyst_id="CAT-CAPITAL-CYCLE",
        family=CatalystFamily.INDUSTRY_CAPITAL_CYCLE,
        description=(
            "Industry investment cycle changes supply-demand economics."
        ),
        mechanism=(
            "Capex cycle → supply discipline/expansion → "
            "pricing → margins → returns."
        ),
        typical_earnings_impact=[
            "Utilisation",
            "Pricing",
            "Margins",
            "ROCE",
            "ROIIC",
        ],
        typical_evidence=[
            "Industry capex",
            "Capacity additions",
            "Utilisation",
            "Competitor behaviour",
        ],
        typical_market_mistake=(
            "Market mistakes cyclical inflection for normality."
        ),
        invalidation_examples=[
            "Excess capacity",
            "Demand collapse",
            "Aggressive competitor capex",
        ],
    ),

    CatalystFamily.SUPPLY_CONSTRAINT: CatalystDefinition(
        catalyst_id="CAT-SUPPLY-CONSTRAINT",
        family=CatalystFamily.SUPPLY_CONSTRAINT,
        description=(
            "Supply scarcity creates pricing or volume advantage."
        ),
        mechanism=(
            "Supply shortage → pricing power/utilisation → "
            "higher earnings."
        ),
        typical_earnings_impact=[
            "Pricing",
            "Margins",
            "Utilisation",
        ],
        typical_evidence=[
            "Capacity data",
            "Lead times",
            "Inventory",
            "Pricing",
        ],
        typical_market_mistake=(
            "Market assumes shortage will normalize quickly."
        ),
        invalidation_examples=[
            "New capacity",
            "Demand collapse",
        ],
    ),

    CatalystFamily.COMPETITIVE_EXIT: CatalystDefinition(
        catalyst_id="CAT-COMPETITIVE-EXIT",
        family=CatalystFamily.COMPETITIVE_EXIT,
        description=(
            "Competitor exits or becomes economically unviable."
        ),
        mechanism=(
            "Competitor exit → supply rationalisation → "
            "share/pricing opportunity."
        ),
        typical_earnings_impact=[
            "Market Share",
            "Pricing",
            "Margins",
        ],
        typical_evidence=[
            "Plant closures",
            "Financial stress",
            "Industry consolidation",
        ],
        typical_market_mistake=(
            "Market ignores structural supply rationalisation."
        ),
        invalidation_examples=[
            "New entrant",
            "Competitor re-entry",
        ],
    ),

    # ------------------------------------------------------
    # TECHNOLOGY / TAM
    # ------------------------------------------------------

    CatalystFamily.TECHNOLOGY_ADOPTION: CatalystDefinition(
        catalyst_id="CAT-TECH-ADOPTION",
        family=CatalystFamily.TECHNOLOGY_ADOPTION,
        description=(
            "Accelerating adoption of a technology changes demand."
        ),
        mechanism=(
            "Technology adoption → TAM growth → "
            "company revenue/earnings opportunity."
        ),
        typical_earnings_impact=[
            "Revenue",
            "TAM",
            "Margins",
            "ROIIC",
        ],
        typical_evidence=[
            "Adoption rates",
            "Customer deployments",
            "Technology cost curve",
        ],
        typical_market_mistake=(
            "Market underestimates adoption curve."
        ),
        invalidation_examples=[
            "Adoption stalls",
            "Technology displacement",
        ],
    ),

    CatalystFamily.NEW_PRODUCT_PLATFORM: CatalystDefinition(
        catalyst_id="CAT-NEW-PRODUCT",
        family=CatalystFamily.NEW_PRODUCT_PLATFORM,
        description=(
            "New product or platform creates incremental economics."
        ),
        mechanism=(
            "Product launch → customer adoption → "
            "revenue/margin expansion."
        ),
        typical_earnings_impact=[
            "Revenue",
            "Gross Margin",
            "TAM",
        ],
        typical_evidence=[
            "Launch",
            "Customer qualification",
            "Bookings",
            "Repeat orders",
        ],
        typical_market_mistake=(
            "Market underestimates product adoption."
        ),
        invalidation_examples=[
            "Product failure",
            "Poor adoption",
        ],
    ),

    CatalystFamily.TAM_EXPANSION: CatalystDefinition(
        catalyst_id="CAT-TAM-EXPANSION",
        family=CatalystFamily.TAM_EXPANSION,
        description=(
            "Addressable market expands materially."
        ),
        mechanism=(
            "New application/geography/customer class → "
            "larger TAM → longer growth runway."
        ),
        typical_earnings_impact=[
            "Revenue Growth",
            "Reinvestment Runway",
            "ROIIC",
        ],
        typical_evidence=[
            "New applications",
            "Market studies",
            "Customer adoption",
            "Geographic expansion",
        ],
        typical_market_mistake=(
            "Market anchors on the legacy market size."
        ),
        invalidation_examples=[
            "New market fails to develop",
        ],
    ),

    # ------------------------------------------------------
    # POLICY / REGULATORY
    # ------------------------------------------------------

    CatalystFamily.REGULATORY_CHANGE: CatalystDefinition(
        catalyst_id="CAT-REGULATORY",
        family=CatalystFamily.REGULATORY_CHANGE,
        description=(
            "Regulatory change alters industry economics."
        ),
        mechanism=(
            "Regulation → supply/demand/cost structure → "
            "earnings impact."
        ),
        typical_earnings_impact=[
            "Revenue",
            "Costs",
            "Margins",
            "Market Share",
        ],
        typical_evidence=[
            "Regulatory notification",
            "Implementation timeline",
            "Industry response",
        ],
        typical_market_mistake=(
            "Market underestimates economic consequences."
        ),
        invalidation_examples=[
            "Policy reversal",
            "Delayed implementation",
        ],
    ),

    CatalystFamily.GOVERNMENT_POLICY: CatalystDefinition(
        catalyst_id="CAT-GOV-POLICY",
        family=CatalystFamily.GOVERNMENT_POLICY,
        description=(
            "Government policy materially changes demand or economics."
        ),
        mechanism=(
            "Policy → incentives/restrictions → "
            "industry demand/supply → earnings."
        ),
        typical_earnings_impact=[
            "Demand",
            "Pricing",
            "Capacity",
            "Margins",
        ],
        typical_evidence=[
            "Policy notification",
            "Budget",
            "Government programme",
            "Implementation data",
        ],
        typical_market_mistake=(
            "Market underestimates duration or implementation."
        ),
        invalidation_examples=[
            "Policy reversal",
            "Poor implementation",
        ],
    ),

    CatalystFamily.FISCAL_TAX: CatalystDefinition(
        catalyst_id="CAT-FISCAL-TAX",
        family=CatalystFamily.FISCAL_TAX,
        description=(
            "Tax or fiscal changes alter company economics."
        ),
        mechanism=(
            "Tax/fiscal change → cash-flow change → "
            "earnings/valuation impact."
        ),
        typical_earnings_impact=[
            "Net Profit",
            "FCF",
            "ROIC",
        ],
        typical_evidence=[
            "Budget",
            "Tax notification",
            "Legislation",
        ],
        typical_market_mistake=(
            "Market fails to incorporate second-order effects."
        ),
        invalidation_examples=[
            "Policy reversal",
            "Implementation failure",
        ],
    ),

    # ------------------------------------------------------
    # MACRO
    # ------------------------------------------------------

    CatalystFamily.MONETARY_LIQUIDITY: CatalystDefinition(
        catalyst_id="CAT-MONETARY",
        family=CatalystFamily.MONETARY_LIQUIDITY,
        description=(
            "Changes in monetary policy or liquidity alter economics."
        ),
        mechanism=(
            "Rates/liquidity → financing/demand/valuation → "
            "earnings or multiples."
        ),
        typical_earnings_impact=[
            "Demand",
            "Financing Cost",
            "Valuation",
        ],
        typical_evidence=[
            "Central-bank policy",
            "Liquidity data",
            "Credit conditions",
        ],
        typical_market_mistake=(
            "Market underestimates transmission lag."
        ),
        invalidation_examples=[
            "Policy reversal",
            "Unexpected inflation",
        ],
    ),

    CatalystFamily.COMMODITY: CatalystDefinition(
        catalyst_id="CAT-COMMODITY",
        family=CatalystFamily.COMMODITY,
        description=(
            "Commodity-price changes materially alter company economics."
        ),
        mechanism=(
            "Commodity price → input/output economics → "
            "margin/earnings."
        ),
        typical_earnings_impact=[
            "Input Costs",
            "Realisation",
            "Margins",
            "FCF",
        ],
        typical_evidence=[
            "Commodity prices",
            "Inventory",
            "Supply-demand balance",
        ],
        typical_market_mistake=(
            "Market extrapolates commodity prices incorrectly."
        ),
        invalidation_examples=[
            "Commodity reversal",
            "Supply shock",
        ],
    ),

    CatalystFamily.CURRENCY: CatalystDefinition(
        catalyst_id="CAT-CURRENCY",
        family=CatalystFamily.CURRENCY,
        description=(
            "Currency movements materially affect company economics."
        ),
        mechanism=(
            "FX change → revenue/input/cost translation → "
            "earnings impact."
        ),
        typical_earnings_impact=[
            "Revenue",
            "Input Costs",
            "Margins",
            "FCF",
        ],
        typical_evidence=[
            "FX movement",
            "Hedging",
            "Export/import exposure",
        ],
        typical_market_mistake=(
            "Market underestimates operating exposure."
        ),
        invalidation_examples=[
            "FX reversal",
            "Effective hedging",
        ],
    ),

    # ------------------------------------------------------
    # TRADE / GEOPOLITICS
    # ------------------------------------------------------

    CatalystFamily.TRADE_IMPORT_SUBSTITUTION: CatalystDefinition(
        catalyst_id="CAT-TRADE",
        family=CatalystFamily.TRADE_IMPORT_SUBSTITUTION,
        description=(
            "Trade changes create domestic substitution or export opportunities."
        ),
        mechanism=(
            "Trade policy → supply relocation → "
            "domestic demand/export opportunity."
        ),
        typical_earnings_impact=[
            "Volume",
            "Market Share",
            "Capacity Utilisation",
            "Revenue",
        ],
        typical_evidence=[
            "Import data",
            "Export data",
            "Tariffs",
            "Customer relocation",
        ],
        typical_market_mistake=(
            "Market underestimates structural supply-chain relocation."
        ),
        invalidation_examples=[
            "Trade normalisation",
            "Competitive substitution",
        ],
    ),

    CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN: CatalystDefinition(
        catalyst_id="CAT-GEOPOLITICAL",
        family=CatalystFamily.GEOPOLITICAL_SUPPLY_CHAIN,
        description=(
            "Geopolitical developments change supply chains or strategic spending."
        ),
        mechanism=(
            "Geopolitical change → supply-chain shift or "
            "strategic spending → company opportunity."
        ),
        typical_earnings_impact=[
            "Orders",
            "Capacity",
            "Revenue",
            "TAM",
        ],
        typical_evidence=[
            "Government policy",
            "Procurement",
            "Trade flows",
            "Supply-chain relocation",
        ],
        typical_market_mistake=(
            "Market treats structural change as temporary."
        ),
        invalidation_examples=[
            "Geopolitical normalisation",
            "Supply-chain reversal",
        ],
    ),

    # ------------------------------------------------------
    # CORPORATE / FINANCIAL
    # ------------------------------------------------------

    CatalystFamily.CORPORATE_ACTION_MA: CatalystDefinition(
        catalyst_id="CAT-CORPORATE-ACTION",
        family=CatalystFamily.CORPORATE_ACTION_MA,
        description=(
            "M&A, demergers or corporate actions unlock value."
        ),
        mechanism=(
            "Corporate action → asset/business separation or "
            "synergy → value realisation."
        ),
        typical_earnings_impact=[
            "EPS",
            "FCF",
            "ROCE",
            "Valuation",
        ],
        typical_evidence=[
            "Board approval",
            "Transaction announcement",
            "Regulatory approval",
        ],
        typical_market_mistake=(
            "Market discounts value-unlocking potential."
        ),
        invalidation_examples=[
            "Deal failure",
            "Regulatory rejection",
            "Poor execution",
        ],
    ),

    CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION: CatalystDefinition(
        catalyst_id="CAT-MANAGEMENT",
        family=CatalystFamily.MANAGEMENT_CAPITAL_ALLOCATION,
        description=(
            "Improved management or capital allocation changes intrinsic value."
        ),
        mechanism=(
            "Better allocation → higher incremental returns → "
            "higher FCF/ROIC/ROIIC."
        ),
        typical_earnings_impact=[
            "ROCE",
            "ROIIC",
            "FCF",
            "EPS",
        ],
        typical_evidence=[
            "Capital allocation history",
            "Management actions",
            "Buybacks",
            "Divestments",
        ],
        typical_market_mistake=(
            "Market assumes historical allocation behaviour persists."
        ),
        invalidation_examples=[
            "Poor capital allocation",
            "Governance deterioration",
        ],
    ),

    CatalystFamily.BALANCE_SHEET_CASH_FLOW: CatalystDefinition(
        catalyst_id="CAT-BALANCE-SHEET",
        family=CatalystFamily.BALANCE_SHEET_CASH_FLOW,
        description=(
            "Balance-sheet improvement or cash-flow release changes economics."
        ),
        mechanism=(
            "Deleveraging/working-capital release → FCF ↑ → "
            "financial risk ↓ → valuation support."
        ),
        typical_earnings_impact=[
            "Interest Cost",
            "FCF",
            "ROCE",
            "Balance Sheet",
        ],
        typical_evidence=[
            "Debt reduction",
            "Working capital",
            "Cash flow",
            "Asset monetisation",
        ],
        typical_market_mistake=(
            "Market underestimates balance-sheet inflection."
        ),
        invalidation_examples=[
            "Debt increase",
            "Working-capital deterioration",
        ],
    ),

    # ------------------------------------------------------
    # MARKET / EXPECTATIONS
    # ------------------------------------------------------

    CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET: CatalystDefinition(
        catalyst_id="CAT-EXPECTATION-RESET",
        family=(
            CatalystFamily.MARKET_RECOGNITION_EXPECTATION_RESET
        ),
        description=(
            "Market expectations change materially as evidence becomes recognized."
        ),
        mechanism=(
            "New information → expectations reset → "
            "earnings/valuation estimates change."
        ),
        typical_earnings_impact=[
            "Consensus Estimates",
            "EPS Expectations",
            "Valuation Multiple",
        ],
        typical_evidence=[
            "Estimate revisions",
            "Guidance",
            "Earnings surprise",
            "Institutional recognition",
        ],
        typical_market_mistake=(
            "Market remains anchored to outdated expectations."
        ),
        invalidation_examples=[
            "Evidence fails",
            "Consensus already incorporates change",
        ],
    ),
}


# ==========================================================
# REGISTRY ACCESS
# ==========================================================


class CatalystRegistry:
    """
    Read-only access to the canonical Catalyst Taxonomy.
    """

    @staticmethod
    def all() -> List[CatalystDefinition]:
        """
        Return all registered catalyst definitions.
        """

        return list(
            CATALYST_TAXONOMY.values()
        )

    @staticmethod
    def get(
        family: CatalystFamily,
    ) -> CatalystDefinition:
        """
        Return the definition for a catalyst family.
        """

        return CATALYST_TAXONOMY[family]

    @staticmethod
    def get_by_id(
        catalyst_id: str,
    ) -> CatalystDefinition | None:
        """
        Return a catalyst definition by canonical ID.
        """

        for definition in (
            CATALYST_TAXONOMY.values()
        ):
            if definition.catalyst_id == catalyst_id:
                return definition

        return None

    @staticmethod
    def count() -> int:
        """
        Return the number of registered catalyst families.
        """

        return len(
            CATALYST_TAXONOMY
        )


# ==========================================================
# PUBLIC API
# ==========================================================


__all__ = [
    "CatalystFamily",
    "CatalystDefinition",
    "CatalystRegistry",
    "CATALYST_TAXONOMY",
]