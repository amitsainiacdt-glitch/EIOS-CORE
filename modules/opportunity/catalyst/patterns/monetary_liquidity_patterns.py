"""
EIOS
Everest Investment Operating System

Monetary / Liquidity Catalyst Patterns

Purpose:
Canonical machine-readable catalyst patterns for the
Monetary / Liquidity catalyst family.

Architecture:

    Catalyst Taxonomy
            ↓
    Monetary / Liquidity Patterns
            ↓
    Catalyst Pattern Registry
            ↓
    Opportunity Engine

Design Principles:

- Passive data only.
- No scoring.
- No ranking.
- No valuation.
- No investment decision logic.
- Each pattern represents a distinct transmission mechanism.
"""

from modules.opportunity.catalyst.catalyst_patterns import (
    CatalystPattern,
)

from modules.opportunity.catalyst.catalyst_taxonomy import (
    CatalystFamily,
)


MONETARY_LIQUIDITY_PATTERNS = [

    # ======================================================
    # 1. POLICY RATE CHANGE
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-MONETARY-LIQUIDITY-POLICY-RATE-CHANGE"
        ),

        family=CatalystFamily.MONETARY_LIQUIDITY,

        name=(
            "Policy Rate Change"
        ),

        description=(
            "A change in policy interest rates materially "
            "alters financing costs, demand conditions, "
            "or valuation multiples."
        ),

        trigger_signals=[
            "Central-bank rate decision",
            "Policy guidance change",
            "Rate-cut cycle",
            "Rate-hike cycle",
        ],

        mechanism=(
            "Policy rate change → funding cost / demand "
            "change → earnings and valuation impact."
        ),

        transmission_channels=[
            "Borrowing cost",
            "Consumer demand",
            "Corporate investment",
            "Valuation multiples",
        ],

        leading_indicators=[
            "Central-bank guidance",
            "Forward-rate expectations",
            "Bond-yield movement",
            "Credit-spread movement",
        ],

        confirmation_indicators=[
            "Lower borrowing rates",
            "Higher credit growth",
            "Improved demand",
            "Reduced interest expense",
        ],

        typical_time_horizon=(
            "3–18 months"
        ),

        earnings_channels=[
            "Financing Cost",
            "Demand",
            "Net Profit",
            "Valuation",
        ],

        market_mistake=(
            "Market underestimates the duration or magnitude "
            "of rate transmission into company economics."
        ),

        second_order_effects=[
            "Higher capital expenditure",
            "Improved housing or auto demand",
            "Higher asset prices",
            "Improved refinancing capacity",
        ],

        disconfirming_evidence=[
            "Inflation remains elevated",
            "Credit transmission remains weak",
            "Demand fails to respond",
            "Policy reversal",
        ],

        kill_switch=(
            "Rate changes fail to transmit into financing "
            "conditions or underlying economic demand."
        ),
    ),

    # ======================================================
    # 2. LIQUIDITY INFUSION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-MONETARY-LIQUIDITY-LIQUIDITY-INFUSION"
        ),

        family=CatalystFamily.MONETARY_LIQUIDITY,

        name=(
            "Liquidity Infusion"
        ),

        description=(
            "A material increase in system liquidity improves "
            "credit availability, financial conditions, or "
            "asset-market liquidity."
        ),

        trigger_signals=[
            "Liquidity injection",
            "Open-market operations",
            "Reserve-system liquidity increase",
            "Government or central-bank liquidity support",
        ],

        mechanism=(
            "System liquidity increase → easier financial "
            "conditions → credit / demand / valuation impact."
        ),

        transmission_channels=[
            "Bank liquidity",
            "Credit availability",
            "Financial conditions",
            "Asset valuations",
        ],

        leading_indicators=[
            "System liquidity",
            "Money-market rates",
            "Central-bank operations",
            "Bank funding conditions",
        ],

        confirmation_indicators=[
            "Credit growth",
            "Lower funding spreads",
            "Higher lending activity",
            "Improved financial conditions",
        ],

        typical_time_horizon=(
            "3–12 months"
        ),

        earnings_channels=[
            "Demand",
            "Financing Cost",
            "Credit Growth",
            "Valuation",
        ],

        market_mistake=(
            "Market underestimates the economic impact of "
            "persistent liquidity improvement."
        ),

        second_order_effects=[
            "Higher investment",
            "Improved working-capital availability",
            "Asset-price appreciation",
            "Stronger business confidence",
        ],

        disconfirming_evidence=[
            "Liquidity remains trapped in financial institutions",
            "Credit demand remains weak",
            "Inflation forces tightening",
            "Liquidity withdrawal begins",
        ],

        kill_switch=(
            "Additional liquidity fails to improve credit "
            "conditions or economic activity."
        ),
    ),

    # ======================================================
    # 3. CREDIT CYCLE EASING
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-MONETARY-LIQUIDITY-CREDIT-CYCLE-EASING"
        ),

        family=CatalystFamily.MONETARY_LIQUIDITY,

        name=(
            "Credit Cycle Easing"
        ),

        description=(
            "Easing credit conditions unlock borrowing, "
            "investment, consumption, or refinancing activity."
        ),

        trigger_signals=[
            "Bank lending standards ease",
            "Credit spreads narrow",
            "Loan growth accelerates",
            "Funding availability improves",
        ],

        mechanism=(
            "Credit conditions improve → borrowing increases → "
            "economic activity and company earnings improve."
        ),

        transmission_channels=[
            "Corporate credit",
            "Consumer credit",
            "Working capital",
            "Capital expenditure",
        ],

        leading_indicators=[
            "Loan approvals",
            "Credit spreads",
            "Bank lending surveys",
            "Commercial-paper rates",
        ],

        confirmation_indicators=[
            "Loan growth",
            "Capex recovery",
            "Working-capital expansion",
            "Improved sales activity",
        ],

        typical_time_horizon=(
            "6–24 months"
        ),

        earnings_channels=[
            "Revenue Growth",
            "Demand",
            "Financing Cost",
            "Operating Leverage",
        ],

        market_mistake=(
            "Market focuses on current credit weakness and "
            "misses the beginning of a new credit cycle."
        ),

        second_order_effects=[
            "Capacity expansion",
            "Employment growth",
            "Higher consumer spending",
            "Improved asset utilization",
        ],

        disconfirming_evidence=[
            "Credit standards tighten",
            "Loan demand remains weak",
            "Defaults accelerate",
            "Funding spreads widen",
        ],

        kill_switch=(
            "Credit availability fails to improve or credit "
            "demand deteriorates materially."
        ),
    ),

    # ======================================================
    # 4. LIQUIDITY WITHDRAWAL / TIGHTENING
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-MONETARY-LIQUIDITY-TIGHTENING"
        ),

        family=CatalystFamily.MONETARY_LIQUIDITY,

        name=(
            "Liquidity Tightening"
        ),

        description=(
            "A reduction in system liquidity or tightening "
            "financial conditions materially changes economic "
            "or valuation conditions."
        ),

        trigger_signals=[
            "Liquidity withdrawal",
            "Balance-sheet reduction",
            "Reserve tightening",
            "Funding stress",
        ],

        mechanism=(
            "Liquidity withdrawal → tighter financial conditions "
            "→ higher funding cost / weaker demand / lower multiples."
        ),

        transmission_channels=[
            "Funding cost",
            "Credit availability",
            "Demand",
            "Valuation multiples",
        ],

        leading_indicators=[
            "Money-market stress",
            "Credit spreads",
            "Bank liquidity",
            "Central-bank balance sheet",
        ],

        confirmation_indicators=[
            "Slower credit growth",
            "Higher borrowing costs",
            "Lower investment",
            "Multiple compression",
        ],

        typical_time_horizon=(
            "3–18 months"
        ),

        earnings_channels=[
            "Financing Cost",
            "Demand",
            "Net Profit",
            "Valuation",
        ],

        market_mistake=(
            "Market underestimates the lag between monetary "
            "tightening and corporate earnings deterioration."
        ),

        second_order_effects=[
            "Capex postponement",
            "Inventory correction",
            "Higher defaults",
            "Lower asset prices",
        ],

        disconfirming_evidence=[
            "Liquidity conditions stabilize",
            "Credit growth remains strong",
            "Policy reverses toward easing",
            "Demand remains resilient",
        ],

        kill_switch=(
            "Tightening fails to transmit into credit, demand, "
            "or valuation conditions."
        ),
    ),

    # ======================================================
    # 5. MONETARY TRANSMISSION INFLECTION
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-MONETARY-LIQUIDITY-TRANSMISSION-INFLECTION"
        ),

        family=CatalystFamily.MONETARY_LIQUIDITY,

        name=(
            "Monetary Transmission Inflection"
        ),

        description=(
            "A previously delayed monetary-policy change begins "
            "to transmit materially into borrowing costs, credit, "
            "demand, or company economics."
        ),

        trigger_signals=[
            "Lending-rate repricing",
            "Deposit-rate repricing",
            "Credit transmission improvement",
            "Borrowing-cost inflection",
        ],

        mechanism=(
            "Policy change → transmission improves → "
            "company financing and demand conditions change."
        ),

        transmission_channels=[
            "Lending rates",
            "Deposit rates",
            "Credit growth",
            "Consumer demand",
        ],

        leading_indicators=[
            "Bank lending rates",
            "Deposit rates",
            "Credit spreads",
            "Loan repricing",
        ],

        confirmation_indicators=[
            "Lower effective borrowing cost",
            "Higher loan demand",
            "Improved corporate finance",
            "Demand recovery",
        ],

        typical_time_horizon=(
            "3–15 months"
        ),

        earnings_channels=[
            "Financing Cost",
            "Revenue Growth",
            "Demand",
            "Net Profit",
        ],

        market_mistake=(
            "Market assumes policy changes have already been "
            "fully priced despite delayed transmission."
        ),

        second_order_effects=[
            "Refinancing benefits",
            "Higher investment",
            "Improved consumer affordability",
            "Stronger credit cycle",
        ],

        disconfirming_evidence=[
            "Transmission remains weak",
            "Banks retain high lending rates",
            "Credit demand remains subdued",
            "Inflation causes reversal",
        ],

        kill_switch=(
            "Expected monetary transmission fails to appear "
            "within the relevant economic cycle."
        ),
    ),

    # ======================================================
    # 6. LIQUIDITY-DRIVEN VALUATION RE-RATING
    # ======================================================

    CatalystPattern(
        pattern_id=(
            "PAT-MONETARY-LIQUIDITY-VALUATION-RERATING"
        ),

        family=CatalystFamily.MONETARY_LIQUIDITY,

        name=(
            "Liquidity-Driven Valuation Re-rating"
        ),

        description=(
            "Improving monetary and liquidity conditions cause "
            "investors to assign higher valuation multiples to "
            "businesses whose earnings remain resilient or improve."
        ),

        trigger_signals=[
            "Falling bond yields",
            "Improving liquidity",
            "Lower risk-free rate",
            "Improving risk appetite",
        ],

        mechanism=(
            "Lower discount rate / better liquidity → "
            "higher valuation multiples → equity re-rating."
        ),

        transmission_channels=[
            "Discount rate",
            "Risk appetite",
            "Equity multiples",
            "Capital flows",
        ],

        leading_indicators=[
            "Bond yields",
            "Real yields",
            "Liquidity conditions",
            "Equity fund flows",
        ],

        confirmation_indicators=[
            "Multiple expansion",
            "Sector re-rating",
            "Higher institutional participation",
            "Improved market breadth",
        ],

        typical_time_horizon=(
            "3–18 months"
        ),

        earnings_channels=[
            "Valuation",
            "Cost of Capital",
            "Equity Multiple",
        ],

        market_mistake=(
            "Market underestimates the speed at which changing "
            "discount rates can alter valuation."
        ),

        second_order_effects=[
            "Lower cost of equity",
            "Higher investment appetite",
            "Improved capital raising conditions",
            "Sector-wide re-rating",
        ],

        disconfirming_evidence=[
            "Risk-free rates rise",
            "Liquidity deteriorates",
            "Risk appetite collapses",
            "Earnings fail to support valuations",
        ],

        kill_switch=(
            "Liquidity improvement does not translate into "
            "sustainable valuation expansion."
        ),
    ),
]


__all__ = [
    "MONETARY_LIQUIDITY_PATTERNS",
]