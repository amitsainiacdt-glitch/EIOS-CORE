"""
EIOS
Everest Investment Operating System

Customer Addition Catalyst Patterns

Purpose:
Canonical catalyst patterns for the Customer Addition
catalyst family.

Architecture:

Catalyst Taxonomy
        ↓
Customer Addition Patterns
        ↓
Catalyst Pattern Registry
        ↓
Opportunity Engine

Design Principles:

- Patterns are passive definitions.
- No scoring.
- No ranking.
- No valuation.
- No company-specific logic.
- Each pattern contains observable evidence.
- Each pattern contains disconfirming evidence.
- Each pattern contains a kill switch.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


# ==========================================================
# CUSTOMER ADDITION PATTERNS
# ==========================================================

CUSTOMER_ADDITION_PATTERNS = [

    # ------------------------------------------------------
    # 1. STRATEGIC CUSTOMER WIN
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-CUSTOMER-ADDITION-"
            "STRATEGIC-CUSTOMER-WIN"
        ),
        name=(
            "Strategic Customer Win"
        ),
        family=(
            CatalystFamily.CUSTOMER_ADDITION
        ),
        description=(
            "Addition of a strategically important "
            "customer creates new revenue visibility "
            "and validates the company's offering."
        ),
        mechanism=(
            "Customer win → initial revenue visibility → "
            "credibility → potential repeat business."
        ),
        trigger_signals=[
            "New customer announcement",
            "Strategic customer onboarding",
            "Large customer qualification",
        ],
        leading_indicators=[
            "Qualification progress",
            "Pilot completion",
            "Initial purchase order",
            "Customer onboarding",
        ],
        confirmation_indicators=[
            "Commercial shipments",
            "Repeat purchase",
            "Revenue contribution",
            "Customer retention",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Customer diversification",
        ],
        market_mistake=(
            "Market treats the customer win as a "
            "one-off event rather than evidence of "
            "broader customer acceptance."
        ),
        disconfirming_evidence=[
            "Customer order cancellation",
            "Delayed commercialisation",
            "No meaningful revenue conversion",
        ],
        kill_switch=(
            "Strategic customer fails to convert "
            "qualification or initial engagement "
            "into commercial revenue."
        ),
    ),

    # ------------------------------------------------------
    # 2. CUSTOMER QUALIFICATION INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-CUSTOMER-ADDITION-"
            "CUSTOMER-QUALIFICATION-INFLECTION"
        ),
        name=(
            "Customer Qualification Inflection"
        ),
        family=(
            CatalystFamily.CUSTOMER_ADDITION
        ),
        description=(
            "Successful qualification with new "
            "customers expands the company's "
            "addressable customer base."
        ),
        mechanism=(
            "Qualification → approved supplier status → "
            "addressable customer base expansion → "
            "future order potential."
        ),
        trigger_signals=[
            "Qualification approval",
            "Vendor registration",
            "Product validation",
        ],
        leading_indicators=[
            "Qualification milestones",
            "Testing completion",
            "Approved vendor status",
            "Customer technical acceptance",
        ],
        confirmation_indicators=[
            "First commercial order",
            "Production allocation",
            "Repeat orders",
            "Growing customer volumes",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Customer diversification",
        ],
        market_mistake=(
            "Market ignores qualification as an "
            "early indicator of future customer revenue."
        ),
        disconfirming_evidence=[
            "Qualification failure",
            "Extended qualification delays",
            "No subsequent commercial order",
        ],
        kill_switch=(
            "Customer qualification does not progress "
            "to commercial adoption within the expected "
            "time horizon."
        ),
    ),

    # ------------------------------------------------------
    # 3. CUSTOMER CONCENTRATION DILUTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-CUSTOMER-ADDITION-"
            "CONCENTRATION-DILUTION"
        ),
        name=(
            "Customer Concentration Dilution"
        ),
        family=(
            CatalystFamily.CUSTOMER_ADDITION
        ),
        description=(
            "Addition of meaningful customers reduces "
            "dependence on existing major customers."
        ),
        mechanism=(
            "New customers → revenue diversification → "
            "lower concentration risk → stronger "
            "earnings resilience."
        ),
        trigger_signals=[
            "New customer additions",
            "Expansion into additional accounts",
            "Customer mix diversification",
        ],
        leading_indicators=[
            "New account wins",
            "Customer pipeline",
            "Qualification breadth",
            "Account activation",
        ],
        confirmation_indicators=[
            "Lower customer concentration",
            "Higher share of revenue from new accounts",
            "Stable legacy customer revenue",
            "Broader recurring revenue base",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Customer Concentration",
        ],
        market_mistake=(
            "Market focuses on near-term revenue and "
            "underestimates the value of a more diversified "
            "customer base."
        ),
        disconfirming_evidence=[
            "Existing customer concentration remains high",
            "New accounts remain immaterial",
            "Loss of major legacy customers",
        ],
        kill_switch=(
            "New customer additions fail to materially "
            "reduce customer concentration."
        ),
    ),

    # ------------------------------------------------------
    # 4. REPEAT ORDER INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-CUSTOMER-ADDITION-"
            "REPEAT-ORDER-INFLECTION"
        ),
        name=(
            "Repeat Order Inflection"
        ),
        family=(
            CatalystFamily.CUSTOMER_ADDITION
        ),
        description=(
            "Newly acquired customers progress from "
            "initial purchases to repeat commercial orders."
        ),
        mechanism=(
            "Initial customer win → successful delivery → "
            "customer satisfaction → repeat orders → "
            "higher revenue durability."
        ),
        trigger_signals=[
            "Second order",
            "Repeat purchase",
            "Expanded customer engagement",
        ],
        leading_indicators=[
            "Initial delivery success",
            "Customer feedback",
            "Follow-on discussions",
            "Additional product qualification",
        ],
        confirmation_indicators=[
            "Recurring orders",
            "Increasing order frequency",
            "Higher customer volumes",
            "Longer customer relationship duration",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Recurring business",
        ],
        market_mistake=(
            "Market assumes the initial customer win "
            "will not become recurring business."
        ),
        disconfirming_evidence=[
            "No repeat orders",
            "Order frequency declines",
            "Customer churn",
        ],
        kill_switch=(
            "Newly acquired customers fail to generate "
            "repeat commercial orders."
        ),
    ),

    # ------------------------------------------------------
    # 5. CUSTOMER LIFETIME VALUE INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-CUSTOMER-ADDITION-"
            "CUSTOMER-LIFETIME-VALUE-INFLECTION"
        ),
        name=(
            "Customer Lifetime Value Inflection"
        ),
        family=(
            CatalystFamily.CUSTOMER_ADDITION
        ),
        description=(
            "New customer relationships demonstrate "
            "higher-than-expected duration, volume or "
            "economic value."
        ),
        mechanism=(
            "Customer acquisition → retention → "
            "repeat purchases → relationship expansion → "
            "higher lifetime value."
        ),
        trigger_signals=[
            "Higher repeat rates",
            "Customer expansion",
            "Longer relationship duration",
        ],
        leading_indicators=[
            "Repeat purchase frequency",
            "Customer retention",
            "Cross-selling",
            "Account expansion",
        ],
        confirmation_indicators=[
            "Increasing revenue per customer",
            "Longer customer tenure",
            "Higher repeat revenue",
            "Expanding customer wallet share",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Customer Lifetime Value",
        ],
        market_mistake=(
            "Market underestimates the lifetime economic "
            "value of newly acquired customers."
        ),
        disconfirming_evidence=[
            "Weak retention",
            "Low repeat purchase rates",
            "Customer wallet share stagnation",
        ],
        kill_switch=(
            "Customer relationships fail to generate "
            "durable repeat economics."
        ),
    ),

    # ------------------------------------------------------
    # 6. CUSTOMER BASE SCALE INFLECTION
    # ------------------------------------------------------

    CatalystPattern(
        pattern_id=(
            "PAT-CUSTOMER-ADDITION-"
            "CUSTOMER-BASE-SCALE-INFLECTION"
        ),
        name=(
            "Customer Base Scale Inflection"
        ),
        family=(
            CatalystFamily.CUSTOMER_ADDITION
        ),
        description=(
            "Customer additions reach sufficient scale "
            "to materially alter the company's growth "
            "trajectory and revenue diversification."
        ),
        mechanism=(
            "Customer additions → broader account base → "
            "higher aggregate volume → revenue growth → "
            "greater business credibility."
        ),
        trigger_signals=[
            "Rapid customer additions",
            "Customer base expansion",
            "Increasing active accounts",
        ],
        leading_indicators=[
            "New account additions",
            "Customer pipeline conversion",
            "Account activation rate",
            "Customer retention",
        ],
        confirmation_indicators=[
            "Material revenue contribution from new customers",
            "Higher active customer count",
            "Increasing aggregate customer volumes",
            "Reduced customer concentration",
        ],
        earnings_channels=[
            "Revenue",
            "Volume",
            "Customer Concentration",
        ],
        market_mistake=(
            "Market fails to recognise that customer "
            "base expansion can create a durable change "
            "in the company's growth trajectory."
        ),
        disconfirming_evidence=[
            "Customer additions stagnate",
            "Low customer activation",
            "High customer churn",
            "No material revenue contribution",
        ],
        kill_switch=(
            "Customer base expansion fails to translate "
            "into meaningful commercial revenue or "
            "durable customer relationships."
        ),
    ),
]


__all__ = [
    "CUSTOMER_ADDITION_PATTERNS",
]