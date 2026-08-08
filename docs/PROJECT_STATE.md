# PROJECT STATE

Current Phase

Release 3

Current Milestone

Rewrite core/application.py

Current Module

Composition Root

Build Status

In Progress

Architecture Status

Frozen

Documentation Status

Complete

Next Task

Review application.py

After That

Compile

Fix integration

Freeze Release 3

Begin Alpha Foundation

Known Blockers

None

Notes

Do not begin Alpha implementation until Release 3 is fully stable.
# PROJECT_STATE.md

Project: Everest Investment Operating System (EIOS)

Release: 3.0
Status: In Progress

Last Updated: 08 August 2026

---

# Executive Summary

Release 3 migration has reached a major milestone.

The core institutional pipeline now executes successfully from
application startup through Investment Committee evaluation and
Master Dossier generation.

The migration from legacy dictionary-based architecture toward typed
Master Dossier sections has progressed substantially.

Most institutional engines are now integrated with CompanyResearch and
successfully persist their typed outputs.

---

# Completed Today

## Financial Engine

Status:
Completed

Result:
FinancialSection is generated and stored successfully.

---

## Valuation Engine

Status:
Completed

Result:

- Owner Earnings integrated
- DCF integrated
- EPV integrated
- Intrinsic Value Office integrated
- Typed ValuationSection generated
- Decision Office receives intrinsic value correctly

Current Sample Output

Intrinsic Value:
4518.65

---

## Business Engine

Status:
Completed

Migration:

BusinessQualityEngine now returns BusinessSection.

Application temporarily bridges persistence using

research.update_business_quality()

Business section now appears correctly inside Master Dossier.

---

## Management Engine

Status:
Completed

Migration:

ManagementEngine now returns typed ManagementSection.

Application bridges persistence using

research.update_management()

Management section now populates correctly.

---

## Risk Engine

Status:
Completed

Migration:

RiskEngine now returns typed RiskSection.

Application bridges persistence using

research.update_risk()

Risk section now populates correctly.

---

## Competitive Engine

Status:
Completed

Migration:

CompetitiveEngine returns typed CompetitiveSection.

Application bridges persistence using

research.update_competitive()

Investment Committee updated to consume the typed CompetitiveSection
instead of the legacy Competitive Intelligence object.

Committee now correctly evaluates competitive leadership.

Competitive Vote

PASS

Competitive Score

100

---

## Decision Office

Status:
Completed

Decision Office now receives

- Intrinsic Value
- Margin of Safety
- Portfolio Inputs

Decision pipeline executes successfully.

---

## Investment Committee

Status:
Operational

Committee Members

✓ Business

✓ Financial

✓ Management

✓ Ownership

✓ Competitive

✓ Risk

✓ Valuation

✓ Thesis

✓ Portfolio

Current Committee Summary

Final Vote

PASS

Average Score

76.1

---

# Master Dossier Migration

Completed Sections

✓ Business

✓ Financial

✓ Management

✓ Ownership

✓ Risk

✓ Competitive

✓ Valuation

✓ Decision

✓ Committee

Remaining

Macro

Monitoring

Opportunity

Scenario

Portfolio

Presentation

---

# Temporary Release 3 Bridge

Current Release 3 uses temporary bridge methods inside
core/application.py

research.update_business_quality()

research.update_management()

research.update_risk()

research.update_competitive()

These bridges will be removed after AnalysisPackProcessor becomes the
sole persistence layer.

---

# Architecture Status

Typed Master Dossier

Approximately 90–95% complete.

Legacy dictionary flow

Still exists only as compatibility bridges.

Business logic

Contained inside engines.

Persistence

Temporary bridge via CompanyResearch.

Future architecture

AnalysisPackProcessor will become the exclusive persistence layer.

---

# Next Sprint

Priority 1

Replace temporary update_*() bridge calls with AnalysisPackProcessor.

Priority 2

Populate MacroSection.

Priority 3

Implement Monitoring Engine persistence.

Priority 4

Begin Opportunity Engine integration.

Priority 5

Remove remaining legacy dictionary dependencies.

---

# Known Issues

1.

Risk scoring thresholds require calibration.

2.

Valuation committee scoring requires refinement.

3.

Macro section not yet integrated.

4.

Opportunity Engine not yet connected.

---

# Overall Release Progress

Foundation
████████████████████ 100%

Typed Master Dossier
██████████████████░░ 95%

Institutional Engines
████████████████████ 100%

Investment Committee
████████████████████ 100%

AnalysisPack Migration
██████████████░░░░░░ 70%

Opportunity Engine
██░░░░░░░░░░░░░░░░░░ 10%

Overall Release 3 Progress

Approximately 92%

---

Next Major Milestone

Complete AnalysisPackProcessor migration and eliminate all temporary
CompanyResearch update bridges.
# EIOS Opportunity Intelligence Architecture

## Purpose

The Opportunity Engine is EIOS's institutional opportunity-discovery and
mispricing-intelligence system.

It is separate from the Master Dossier.

The Master Dossier determines whether a company is an exceptional
long-term business.

The Opportunity Engine identifies emerging catalysts, changing
fundamentals, sector inflections, macroeconomic changes and market
mispricing that may create attractive investment opportunities.

The Opportunity Engine is not a short-term trading system.

Primary opportunity horizon:
0–5 years, with particular emphasis on emerging opportunities over
approximately 3–36 months.

---

# Core Architecture

                    EIOS
                     │
       ┌─────────────┴─────────────┐
       │                           │
       ▼                           ▼
MASTER DOSSIER              OPPORTUNITY ENGINE
Long-term quality           Mispricing discovery
       │                           │
       │                    ┌──────┴──────┐
       │                    │             │
       │                 DISCOVERY     SIGNAL MESH
       │                    │             │
       │                    │      ┌──────┼──────┐
       │                    │      │      │      │
       │                    │    Macro  Trade  Policy
       │                    │    News   Sector Finance
       │                    │    Micro  Market Accounting
       │                    │
       │                    ▼
       │             Discovery Universe
       │                    │
       │                    ▼
       │             Opportunity Candidates
       │                    │
       │                    ▼
       │             Catalyst Engine
       │                    │
       │                    ▼
       │             Opportunity Score
       │                    │
       │                    ▼
       │              Mispricing Engine
       │                    │
       │                    ▼
       │             Ranked Opportunities
       │                    │
       └────────────────────┤
                            ▼
                     MASTER DOSSIER

---

# Discovery vs Opportunity vs Master Dossier

## Discovery

Question:

"Which companies deserve our attention?"

Discovery builds and filters the investment universe.

It should evaluate:

- TAM
- growth
- financial quality
- management
- moat
- capital allocation
- risk
- valuation
- reinvestment runway
- evidence availability

Discovery should identify candidates worthy of further research.

---

## Opportunity Engine

Question:

"Which companies have a potentially mispriced opportunity emerging now?"

The Opportunity Engine should identify:

- emerging catalysts
- earnings inflections
- sector inflections
- macroeconomic changes
- policy changes
- international trade developments
- supply-chain changes
- capital-cycle changes
- valuation dislocations
- market expectation gaps
- early signals before broad market recognition

The Opportunity Engine must not be limited to price momentum.

---

## Master Dossier

Question:

"Is this an exceptional business capable of compounding over the long term?"

The Master Dossier remains the institutional long-term research system.

It contains:

- Business Quality
- Financial Quality
- Management
- Ownership
- Competitive Intelligence
- Risk
- Valuation
- ROIIC
- Financial Evidence Pack
- Peer Benchmark Matrix
- Disconfirming Evidence
- Investment Committee analysis

---

# Opportunity Intelligence Signal Universe

The Opportunity Engine must be capable of incorporating signals from the
entire economic and corporate information system.

## 1. Macro Economy

Monitor:

- GDP
- IIP
- PMI
- CPI
- WPI
- interest rates
- RBI policy
- repo rate
- CRR
- liquidity
- credit growth
- bank lending
- fiscal deficit
- government capex
- private capex
- GST collections
- employment
- consumption
- housing
- power demand
- monetary conditions
- bond yields
- yield curve
- INR/USD
- foreign exchange reserves

---

## 2. International Trade

Monitor:

- imports
- exports
- product-level trade flows
- destination-level exports
- China production
- China exports
- global capacity
- tariffs
- anti-dumping duties
- countervailing duties
- sanctions
- export restrictions
- import restrictions
- FTAs
- trade agreements
- China+1
- supply-chain relocation
- friend-shoring
- near-shoring
- shipping rates
- container rates
- freight rates
- port congestion
- logistics disruptions

The system should map:

Trade Change
→ Industry Impact
→ Company Exposure
→ Earnings Impact
→ Valuation Impact

---

## 3. Government Policy

Monitor:

- Union Budget
- Economic Survey
- ministry notifications
- PLI schemes
- infrastructure policy
- defence procurement
- railway capex
- power policy
- renewable energy policy
- semiconductor policy
- electronics policy
- EV policy
- solar policy
- transmission investment
- healthcare policy
- agriculture policy
- fertilizer policy
- chemical regulation
- import duties
- export duties
- subsidies
- state government industrial policies
- state capex

The system should identify:

Policy
→ Sector
→ Companies
→ Earnings Impact
→ Valuation Impact

---

## 4. Sector Intelligence

Monitor:

- sector revenue growth
- order growth
- order books
- capacity
- capacity utilization
- pricing
- margins
- imports
- exports
- commodity prices
- hiring
- capex
- inventory
- credit
- tender activity
- government spending
- customer spending
- news flow
- institutional ownership
- relative price performance

The system must distinguish:

Price Sector Rotation

from:

Fundamental Sector Rotation

Fundamental sector rotation should incorporate:

- earnings momentum
- order momentum
- capital-cycle momentum
- policy momentum
- liquidity momentum
- fundamental momentum
- price momentum

---

## 5. Company Micro Signals

Monitor:

- order wins
- order cancellations
- tender participation
- tender wins
- order-book growth
- capacity expansion
- new plants
- utilization
- hiring
- senior management hiring
- customer additions
- customer concentration
- exports
- new geographies
- new products
- pricing
- raw-material costs
- inventory
- receivables
- payables
- working capital
- margins
- EBITDA
- EBIT
- PAT
- EPS
- cash flow
- capex
- debt
- interest costs
- ROCE
- ROIC
- ROIIC
- free cash flow
- promoter buying
- promoter selling
- promoter pledge
- FII changes
- DII changes
- insider transactions

Acceleration and direction of these variables are more important than
single-period values.

Example:

5% order growth
→ 12%
→ 25%

is more informative than simply observing 25% order growth.

---

## 6. Financial and Accounting Intelligence

Monitor:

### Income Statement

- revenue acceleration
- margin expansion
- operating leverage
- EPS acceleration
- earnings revisions

### Balance Sheet

- debt reduction
- working-capital improvement
- receivable changes
- inventory normalization
- asset turnover

### Cash Flow

- CFO/PAT conversion
- free cash flow
- capex intensity
- cash generation

### Returns

- ROCE
- ROIC
- ROIIC
- incremental margins
- incremental capital requirements

### Accounting Quality

Detect:

- receivables growing faster than sales
- inventory anomalies
- CFO/PAT divergence
- unusual other income
- capitalized expenses
- contingent liabilities
- related-party transactions
- exceptional items
- tax anomalies
- depreciation anomalies
- working-capital deterioration

The system must distinguish:

Economic Earnings Improvement

from:

Accounting Earnings Improvement.

---

## 7. News Intelligence

News must be converted into structured intelligence.

News
→ Entity
→ Sector
→ Theme
→ Economic Impact
→ Earnings Impact
→ Time Horizon
→ Probability
→ Affected Companies

News should not simply be stored as headlines.

The system should determine whether a news event changes the
investment economics of a company or sector.

---

## 8. Market Intelligence

Monitor:

- price
- volume
- delivery percentage
- relative strength
- sector relative strength
- market breadth
- FII flows
- DII flows
- block deals
- bulk deals
- insider transactions
- 52-week highs/lows
- abnormal volume
- price/earnings divergence
- earnings/price divergence

Price is an input to opportunity analysis, not the investment thesis.

---

# Catalyst Intelligence

Catalysts should be classified into:

- Macro Catalyst
- Trade Catalyst
- Policy Catalyst
- Sector Catalyst
- Earnings Catalyst
- Company Catalyst
- Market Catalyst
- Commodity Catalyst
- Capital-Cycle Catalyst
- Liquidity Catalyst
- Regulatory Catalyst
- Corporate-Action Catalyst

---

# Signal Maturity

Signals should be classified:

LEVEL 0 — Noise

LEVEL 1 — Weak Signal

LEVEL 2 — Emerging Signal

LEVEL 3 — Confirmed Catalyst

LEVEL 4 — Earnings Impact

LEVEL 5 — Market Recognition

The Opportunity Engine should focus particularly on Levels 1–3,
because the objective is to identify opportunities before widespread
market recognition.

---

# Signal → Catalyst → Company Framework

EIOS should convert external observations into investment implications.

Example:

China production cuts
→ Global supply reduction
→ Commodity price improvement
→ Indian producer economics improve
→ Sector margins potentially expand
→ Identify exposed companies
→ Estimate earnings sensitivity
→ Compare valuation
→ Estimate expected return
→ Opportunity Score

The system should identify the entire causal chain rather than merely
recording the original news event.

---

# Opportunity Time Horizons

Opportunities should be classified into:

0–3 months
- policy events
- order surprises
- news catalysts
- corporate actions

3–12 months
- earnings inflections
- margin expansion
- order-book conversion
- capacity utilization

1–3 years
- sector cycles
- capacity cycles
- capital expenditure cycles
- structural industry changes

3–5 years
- major industry transformation
- technology transitions
- structural policy changes

---

# Architectural Rule

Do NOT put all Opportunity Intelligence logic into DiscoveryEngine.

DiscoveryEngine is an orchestration layer.

Individual engines should produce structured signals.

Examples:

SignalEngine
CatalystEngine
MacroIntelligenceEngine
TradeIntelligenceEngine
PolicyIntelligenceEngine
SectorRotationEngine
NewsIntelligenceEngine
AccountingSignalEngine
MarketIntelligenceEngine

These signals should ultimately feed the Opportunity Engine.

The Opportunity Score Engine should combine validated signals; it should
not perform all underlying research itself.

---

# Core Principle

EIOS should continuously search for:

"What changed?"

"What is changing?"

"What is changing faster than expected?"

"What is the market not yet pricing?"

"What could cause earnings estimates to change?"

"What could cause the valuation multiple to change?"

"What evidence would confirm the opportunity?"

"What evidence would invalidate it?"

The ultimate objective is:

EARLY SIGNAL
→ CAUSAL UNDERSTANDING
→ CATALYST
→ COMPANY EXPOSURE
→ EARNINGS IMPACT
→ VALUATION GAP
→ ASYMMETRIC OPPORTUNITY
→ MASTER DOSSIER
→ INVESTMENT COMMITTEE
# OPPORTUNITY INTELLIGENCE OFFICE

## Permanent Architecture & Research Scope

### Status

**Design Status:** Architecture Defined
**Implementation Status:** Deferred until Platform Stabilization is complete
**Purpose:** Institutional discovery of emerging investment opportunities and market mispricing
**Relationship:** Separate from Master Dossier and Discovery Office

---

# 1. PURPOSE

The Opportunity Intelligence Office is an institutional intelligence system designed to identify:

> **Emerging economic, industry, company and market changes that can create mispriced investment opportunities before those opportunities become fully recognized by the market.**

The objective is NOT simply to find:

* good companies
* cheap companies
* high-growth companies
* momentum stocks
* short-term trading opportunities

The objective is to identify:

**CHANGE → CAUSALITY → BENEFICIARY → EARNINGS IMPACT → MARKET EXPECTATION GAP → MISPRICING → ASYMMETRY**

---

# 2. PERMANENT SEPARATION FROM OTHER EIOS SYSTEMS

## Discovery Office

Primary question:

> Which companies deserve institutional research attention?

Discovery builds and ranks the **Discovery Universe**.

---

## Opportunity Intelligence Office

Primary question:

> What is changing, why does it matter, who benefits, what is the earnings impact, what has the market priced, and is there an asymmetric opportunity?

---

## Master Dossier

Primary question:

> Is the underlying company a sufficiently high-quality long-term business to justify ownership?

---

## Relationship

```text
DISCOVERY UNIVERSE
        ↓
OPPORTUNITY INTELLIGENCE
        ↓
HIGH-CONVICTION OPPORTUNITY
        ↓
MASTER DOSSIER
        ↓
INVESTMENT COMMITTEE
```

No system should duplicate the responsibilities of another.

---

# 3. INVESTMENT HORIZONS

Opportunity Intelligence must support multiple horizons.

### Short-Term

**0–3 months**

Examples:

* policy announcements
* regulatory decisions
* earnings surprises
* order wins
* commodity shocks
* corporate actions
* sudden supply disruptions

### Medium-Term

**3–12 months**

Examples:

* earnings inflection
* margin recovery
* order-book conversion
* capacity utilization
* pricing improvement
* working-capital normalization
* sector recovery

### Structural

**1–3 years**

Examples:

* capex cycles
* China+1
* import substitution
* manufacturing relocation
* industry consolidation
* technology adoption
* structural sector growth

### Long-Term Structural

**3–5+ years**

Examples:

* energy transition
* demographic changes
* major infrastructure cycles
* strategic industrial policy
* global supply-chain restructuring
* technological transformation

The Opportunity Office is therefore **not a short-term trading engine**.

---

# 4. COMPLETE INTELLIGENCE UNIVERSE

The Opportunity Office must eventually be capable of detecting relevant signals from:

1. Macro Economy
2. Monetary Policy
3. Fiscal Policy
4. Banking & Credit
5. Interest Rates
6. Liquidity
7. International Trade
8. Tariffs
9. Sanctions
10. Export Restrictions
11. Import Restrictions
12. Free Trade Agreements
13. Geopolitics
14. Commodities
15. Energy
16. Shipping
17. Logistics
18. Government Policy
19. Regulation
20. Industrial Policy
21. Infrastructure
22. Defence
23. Manufacturing
24. Capital Expenditure
25. Sector Economics
26. Sector Rotation
27. Company Fundamentals
28. Order Flow
29. Tender Activity
30. Customer Capex
31. Capacity Expansion
32. Capacity Utilization
33. Hiring
34. Pricing
35. Inventory
36. Working Capital
37. Earnings
38. Management Guidance
39. Analyst Expectations
40. Accounting Quality
41. Cash Flow
42. Capital Allocation
43. Promoter Behaviour
44. Institutional Ownership
45. News Flow
46. Technology
47. Corporate Actions
48. Market Price
49. Volume
50. Market Positioning
51. Valuation
52. Investor Expectations

This list is extensible.

---

# 5. MACRO INTELLIGENCE

Monitor:

* GDP
* GVA
* IIP
* PMI
* CPI
* WPI
* inflation expectations
* interest rates
* repo rate
* CRR
* SLR
* liquidity
* money supply
* credit growth
* bank lending
* deposit growth
* bond yields
* yield curve
* real interest rates
* fiscal deficit
* government expenditure
* government capex
* private capex
* GST collections
* employment
* wages
* consumption
* housing
* automobile demand
* electricity demand
* freight activity
* railway freight
* port activity
* currency
* foreign-exchange reserves
* global liquidity

The system must detect:

* acceleration
* deceleration
* trend reversal
* divergence
* surprise
* regime change

---

# 6. MONETARY & FINANCIAL SYSTEM

Monitor:

* RBI liquidity
* credit growth
* deposit growth
* loan growth
* credit spreads
* corporate borrowing
* bond yields
* yield curve
* bank NIM environment
* asset quality
* provisioning
* refinancing conditions
* housing finance
* consumer finance
* corporate finance

Map:

```text
Financial Change
        ↓
Affected Sector
        ↓
Affected Company
        ↓
Financial Impact
```

---

# 7. INTERNATIONAL TRADE INTELLIGENCE

Monitor:

* Indian exports
* Indian imports
* product-level trade
* country-level trade
* China exports
* China capacity
* global capacity
* inventories
* tariffs
* anti-dumping duties
* countervailing duties
* safeguard duties
* sanctions
* export controls
* import restrictions
* customs duties
* FTAs
* bilateral trade agreements
* China+1
* friend-shoring
* near-shoring
* supply-chain relocation
* import substitution
* localization

Also monitor:

* container rates
* shipping rates
* freight rates
* port congestion
* transit times
* logistics costs
* trade-route disruptions

---

# 8. GOVERNMENT & POLICY INTELLIGENCE

Monitor:

* Union Budget
* Economic Survey
* ministry notifications
* industrial policy
* PLI
* infrastructure policy
* defence procurement
* railway spending
* power policy
* renewable policy
* semiconductor policy
* electronics policy
* EV policy
* solar policy
* transmission policy
* healthcare policy
* agricultural policy
* fertilizer policy
* chemical regulation
* environmental regulation
* import duties
* export duties
* taxation

Also monitor state-level:

* industrial policies
* subsidies
* state capex
* infrastructure
* electricity policy
* manufacturing incentives
* procurement

---

# 9. COMMODITY INTELLIGENCE

Monitor:

* crude oil
* natural gas
* coal
* steel
* iron ore
* aluminium
* copper
* zinc
* nickel
* lithium
* polymers
* chemicals
* agricultural commodities
* fertilizer inputs
* energy prices

Track:

* spot prices
* futures curves
* inventories
* production
* capacity
* shutdowns
* new capacity
* imports
* exports
* freight
* regional spreads

Determine whether the movement affects:

* revenue
* margins
* working capital
* cash flow
* earnings

---

# 10. SECTOR INTELLIGENCE

Every important sector should have a dynamic intelligence profile.

Monitor:

* sector revenue
* earnings
* order inflows
* order backlog
* order cancellations
* capacity
* utilization
* pricing
* margins
* inventory
* imports
* exports
* customer capex
* government spending
* private capex
* hiring
* tender activity
* regulation
* credit availability
* valuation
* institutional flows
* news flow

---

# 11. SECTOR ROTATION EARLY-WARNING SYSTEM

The system must distinguish:

### Price Rotation

Stocks are rising.

from:

### Fundamental Rotation

Underlying sector economics are improving.

Sector rotation analysis should combine:

* earnings momentum
* revenue momentum
* order momentum
* pricing momentum
* margin momentum
* capacity momentum
* capex momentum
* policy momentum
* trade momentum
* liquidity momentum
* institutional momentum
* valuation momentum
* price momentum

Identify:

* emerging sectors
* accelerating sectors
* inflecting sectors
* decelerating sectors
* crowded sectors
* deteriorating sectors

---

# 12. COMPANY MICRO INTELLIGENCE

Monitor:

* order wins
* order cancellations
* order-book growth
* tender participation
* tender wins
* capacity additions
* plant commissioning
* utilization
* hiring
* customer additions
* customer concentration
* exports
* geographic expansion
* new products
* pricing
* raw-material costs
* inventory
* receivables
* payables
* working capital
* margins
* EBITDA
* EBIT
* PAT
* EPS
* cash flow
* capex
* debt
* interest cost
* ROCE
* ROIC
* ROIIC
* FCF
* promoter buying
* promoter selling
* promoter pledge
* FII changes
* DII changes
* insider transactions

The engine should emphasize:

**CHANGE → ACCELERATION → INFLECTION**

rather than static numbers alone.

---

# 13. ACCOUNTING & FINANCIAL QUALITY INTELLIGENCE

Monitor:

### Income Statement

* revenue acceleration
* margin expansion
* margin contraction
* operating leverage
* EPS acceleration
* earnings surprises

### Balance Sheet

* debt
* receivables
* inventory
* working capital
* asset turnover
* capital intensity

### Cash Flow

* CFO/PAT
* FCF
* capex
* cash conversion
* cash burn

### Returns

* ROCE
* ROIC
* ROIIC
* incremental margins
* incremental capital requirements

### Accounting Quality

Detect:

* receivables growing faster than sales
* inventory anomalies
* CFO/PAT divergence
* unusual other income
* capitalization anomalies
* contingent liabilities
* related-party transactions
* exceptional items
* tax anomalies
* depreciation anomalies
* working-capital deterioration

Distinguish:

**Economic Earnings Improvement**

from:

**Accounting Earnings Improvement**

---

# 14. EARNINGS INTELLIGENCE

Monitor:

* quarterly results
* annual results
* earnings surprises
* management guidance
* guidance changes
* consensus estimates
* analyst revisions
* revenue expectations
* margin expectations
* EPS expectations
* order-book conversion
* management commentary

Core principle:

> Actual outcome must always be compared with market expectation.

---

# 15. NEWS INTELLIGENCE

News must be converted into structured intelligence.

```text
NEWS
 ↓
EVENT
 ↓
ENTITY
 ↓
SECTOR
 ↓
THEME
 ↓
ECONOMIC MECHANISM
 ↓
EARNINGS IMPACT
 ↓
TIME HORIZON
 ↓
PROBABILITY
 ↓
COMPANY EXPOSURE
 ↓
MARKET EXPECTATION
```

Classify news as:

* Noise
* Informational
* Weak Signal
* Emerging Signal
* Catalyst
* Confirmed Catalyst
* Earnings Impact
* Structural Event
* Market Recognition

Avoid counting multiple reports of the same underlying event as independent evidence.

---

# 16. MARKET INTELLIGENCE

Monitor:

* price
* volume
* delivery
* volatility
* relative strength
* sector relative strength
* breadth
* FII flows
* DII flows
* block deals
* bulk deals
* insider transactions
* 52-week highs
* 52-week lows
* abnormal volume
* price/earnings divergence
* earnings/price divergence
* valuation re-rating
* valuation de-rating
* positioning
* crowdedness

Market price is an input.

Market price must never automatically become the investment thesis.

---

# 17. SIGNAL MATURITY

Every signal should have a maturity level:

### Level 0 — Noise

Insufficient evidence.

### Level 1 — Weak Signal

Initial indication.

### Level 2 — Emerging Signal

Multiple supporting observations.

### Level 3 — Confirmed Catalyst

Strong corroborated evidence.

### Level 4 — Earnings Impact

Financial statements begin reflecting the change.

### Level 5 — Market Recognition

Market has substantially incorporated the change.

Priority should generally be given to:

**Levels 1–3.**

---

# 18. SIGNAL QUALITY

Every signal must evaluate:

* source quality
* evidence quality
* relevance
* independence
* recency
* persistence
* magnitude
* direction
* corroboration
* contradiction
* historical reliability

Repeated reporting of one source must not artificially increase confidence.

---

# 19. CATALYST INTELLIGENCE

Catalysts include:

* Macro
* Monetary
* Fiscal
* Trade
* Policy
* Regulatory
* Commodity
* Sector
* Capital Cycle
* Earnings
* Company
* Technology
* Liquidity
* Corporate Action
* Market
* Geopolitical

Every catalyst must identify:

* cause
* mechanism
* affected sectors
* affected companies
* direction
* magnitude
* probability
* time horizon
* evidence
* market recognition
* expected earnings impact
* expected valuation impact
* invalidation condition

---

# 20. CAUSAL CHAIN

The Opportunity Office must attempt to establish:

```text
WORLD EVENT
 ↓
ECONOMIC CHANGE
 ↓
SUPPLY / DEMAND
 ↓
SECTOR ECONOMICS
 ↓
COMPANY EXPOSURE
 ↓
REVENUE / MARGIN
 ↓
EARNINGS
 ↓
CASH FLOW
 ↓
VALUATION
 ↓
MARKET EXPECTATION
 ↓
MISPRICING
```

A headline without a credible causal mechanism should not receive high conviction.

---

# 21. MARKET EXPECTATION GAP

A catalyst alone does not constitute an opportunity.

The system must determine:

> What does the market already expect?

Compare:

* actual fundamentals
* likely future fundamentals
* consensus expectations
* implied growth
* implied margins
* valuation
* historical valuation
* peer valuation
* positioning
* price reaction

Core concept:

**Fundamental Outcome − Market-Implied Outcome = Expectation Gap**

---

# 22. MISPRICING ENGINE

Identify:

### Cheap but deteriorating

### Expensive but improving

### Improving and mispriced

Primary target:

**Improving + Mispriced + High Asymmetry**

The engine should assess:

* fundamental change
* catalyst
* earnings sensitivity
* expectation gap
* valuation gap
* time to recognition
* probability
* downside

---

# 23. ASYMMETRY ENGINE

Every serious opportunity must estimate:

* probability of upside
* magnitude of upside
* probability of permanent capital loss
* magnitude of downside
* expected time to thesis
* catalyst probability
* evidence confidence

Core question:

> Is the probability-weighted upside materially greater than the probability-weighted permanent downside?

---

# 24. CONTRADICTION ENGINE

Every opportunity must actively search for disconfirming evidence.

Ask:

* What evidence contradicts the thesis?
* Is the catalyst temporary?
* Is the industry already over-earning?
* Is the catalyst already priced?
* Can competitors respond?
* Can capacity destroy pricing?
* Can policy reverse?
* Can management fail to execute?
* Is accounting quality deteriorating?
* Is demand merely pulled forward?

Every opportunity must contain:

**Reasons We Could Be Wrong**

---

# 25. OPPORTUNITY KILL SWITCH

Every opportunity requires explicit invalidation conditions.

Examples:

* order growth fails
* margin expansion fails
* policy cancelled
* commodity economics reverse
* capacity exceeds demand
* customer concentration deteriorates
* cash flow deteriorates
* promoter behaviour deteriorates
* valuation becomes excessive
* catalyst becomes fully priced

The engine must be able to conclude:

**OPPORTUNITY INVALIDATED**

or:

**INSUFFICIENT EVIDENCE**

It must never force a positive investment conclusion.

---

# 26. OPPORTUNITY SCORE

The final score should eventually incorporate:

* catalyst strength
* catalyst probability
* earnings sensitivity
* fundamental momentum
* sector momentum
* market expectation gap
* valuation
* institutional positioning
* timing
* risk
* evidence confidence
* asymmetry

Opportunity Score and Confidence are separate concepts.

**Confidence must never simply equal Opportunity Score.**

---

# 27. RESEARCH PRIORITY

Opportunity Engine must allocate research resources intelligently.

Research priority should consider:

**Opportunity Magnitude × Probability × Evidence Confidence × Time Sensitivity × Potential Wealth Creation ÷ Research Cost**

The system should identify the opportunities where deeper research has the highest expected value.

---

# 28. OPPORTUNITY LIFECYCLE

```text
DISCOVERED
 ↓
SIGNAL DETECTED
 ↓
SIGNAL VALIDATED
 ↓
CATALYST IDENTIFIED
 ↓
COMPANY MAPPED
 ↓
EXPECTATION GAP IDENTIFIED
 ↓
MISPRICING IDENTIFIED
 ↓
ASYMMETRY ANALYZED
 ↓
SHORTLISTED
 ↓
UNDER RESEARCH
 ↓
MASTER DOSSIER
 ↓
COMMITTEE REVIEW
 ↓
APPROVED
 ↓
ACTIVE
 ↓
TARGET HIT / INVALIDATED / EXITED
```

---

# 29. OPPORTUNITY VS DISCOVERY

Discovery asks:

> **Which companies are worth studying?**

Opportunity asks:

> **Why might this company become mispriced now?**

A company can therefore:

* pass Discovery but have no current Opportunity
* fail to rank highly in Discovery but emerge from a major external catalyst and warrant review
* have a strong Opportunity but fail Master Dossier quality
* pass both Discovery and Opportunity and be promoted to Master Dossier

These systems must remain distinct.

---

# 30. OPPORTUNITY VS MASTER DOSSIER

Opportunity Engine identifies:

**WHY NOW**

Master Dossier establishes:

**WHY THIS BUSINESS**

The Opportunity Engine must not replace Master Dossier research.

The Master Dossier must independently validate:

* business quality
* moat
* management
* financial quality
* ROIIC
* valuation
* competitive position
* risks
* evidence
* disconfirming evidence

---

# 31. REQUIRED OPPORTUNITY OUTPUT

Every high-conviction opportunity should ultimately answer:

1. What changed?
2. Why now?
3. What is the catalyst?
4. What is the causal mechanism?
5. Which sectors benefit?
6. Which companies benefit?
7. What is the earnings impact?
8. What does the market currently expect?
9. What is the expectation gap?
10. What is the valuation gap?
11. What is the expected return?
12. What is the time to recognition?
13. What is the downside?
14. What is the probability of permanent capital loss?
15. What evidence supports the thesis?
16. What evidence contradicts it?
17. What would invalidate the thesis?
18. How confident are we?
19. What is the research priority?
20. Why is this better than the next-best opportunity?

---

# 32. PROPOSED FUTURE MODULE STRUCTURE

Implementation should eventually evolve toward:

```text
modules/opportunity/

├── signals/
│   ├── signal_model.py
│   ├── signal_registry.py
│   ├── signal_validation.py
│   └── signal_confidence.py
│
├── macro/
├── monetary/
├── fiscal/
├── trade/
├── policy/
├── regulatory/
├── commodity/
├── geopolitical/
├── sector/
├── company/
├── earnings/
├── accounting/
├── capital_cycle/
├── technology/
├── news/
├── market/
│
├── catalyst/
├── expectation/
├── mispricing/
├── asymmetry/
├── contradiction/
├── ranking/
│
├── opportunity_models.py
├── opportunity_section.py
├── opportunity_score_engine.py
└── opportunity_engine.py
```

This is a target architecture, not an instruction to create all folders immediately.

---

# 33. ENGINEERING RULES

1. Architecture before implementation.
2. No company-specific hardcoding.
3. No duplicate engines.
4. One module = one responsibility.
5. Typed models remain passive.
6. Engines perform calculations.
7. Orchestrators coordinate only.
8. ResearchContext remains the intelligence bus.
9. Repository layer owns persistence.
10. Evidence must accompany major conclusions.
11. Contradictory evidence is mandatory.
12. Every opportunity requires invalidation conditions.
13. Opportunity Score and Confidence remain separate.
14. Signals must be time-aware.
15. Signals must be deduplicated.
16. External events must be mapped through causal mechanisms.
17. Market price must not substitute for fundamental reasoning.
18. No forced conclusions when evidence is inadequate.
19. Refactor existing functionality before duplicating it.
20. No new Opportunity modules should be implemented until platform-stabilization requirements are satisfied.

---

# 34. IMPLEMENTATION STRATEGY

Opportunity Office implementation will proceed only after the current platform stabilization release is complete.

Planned sequence:

```text
PHASE 1
Architecture Audit
        ↓
PHASE 2
Canonical Signal Model
        ↓
PHASE 3
Signal Registry + Evidence
        ↓
PHASE 4
Macro / Monetary / Fiscal Intelligence
        ↓
PHASE 5
Trade / Policy / Commodity / Geopolitical Intelligence
        ↓
PHASE 6
Sector Intelligence + Sector Rotation
        ↓
PHASE 7
Company + Earnings + Accounting Intelligence
        ↓
PHASE 8
News + Market Intelligence
        ↓
PHASE 9
Catalyst Engine
        ↓
PHASE 10
Expectation Gap Engine
        ↓
PHASE 11
Mispricing Engine
        ↓
PHASE 12
Asymmetry + Contradiction Engine
        ↓
PHASE 13
Opportunity Ranking
        ↓
PHASE 14
Discovery → Opportunity Integration
        ↓
PHASE 15
Opportunity → Master Dossier Promotion
        ↓
PHASE 16
Investment Committee Integration
```

---

# 35. NON-NEGOTIABLE INVESTMENT PHILOSOPHY

The Opportunity Office is designed to find:

**CHANGE BEFORE CONSENSUS**

not:

**STOCKS THAT ARE ALREADY POPULAR**

The system should prefer:

* early signals over headlines
* causal evidence over narratives
* acceleration over static numbers
* expectation gaps over simple cheapness
* earnings inflections over price momentum alone
* structural change over temporary excitement
* asymmetric opportunities over high-confidence mediocre returns
* evidence over assumptions
* intellectual humility over forced conviction

The ultimate objective is:

> **Detect meaningful change before market recognition, understand the economic transmission mechanism, identify the best exposed businesses, quantify the likely earnings impact, determine what is already priced, and allocate research effort toward the opportunities with the greatest probability-adjusted long-term wealth creation.**
# EIOS — PROJECT STATE

## Everest Investment Operating System

**Project:** EIOS — Everest Investment Operating System
**Current Branch:** `main`
**Current HEAD:** `4cfe346`
**Working Tree:** CLEAN
**Last Updated:** 2026-08-08

---

# 1. CURRENT DEVELOPMENT POSITION

EIOS has completed the core analytical architecture of the new **Opportunity Engine** through the first competitive-selection layer.

The Opportunity Engine is being developed as a module separate from the long-term **Master Dossier** architecture.

Its purpose is to discover, qualify, analyze and rank potentially mispriced investment opportunities before they become fully recognized by the market.

The current architecture has progressed from raw intelligence signals through:

```text
Signals
   ↓
Signal Intelligence
   ↓
Signal Aggregation
   ↓
Causal Chain
   ↓
Catalyst Classification
   ↓
Catalyst Engine
   ↓
Expectation Gap
   ↓
Mispricing
   ↓
Asymmetry
   ↓
Evidence
   ↓
Opportunity Synthesis
   ↓
Opportunity Ranking
```

The next development stage is integration of the Ranking layer with real Opportunity Synthesis outputs.

---

# 2. COMPLETED OPPORTUNITY ENGINE COMPONENTS

## 2.1 Signal Foundation

Status: COMPLETE

The Opportunity Engine has a canonical Signal model supporting:

* Signal domain
* Signal type
* Signal direction
* Signal stage
* Time horizon
* Source
* Source type
* Source date
* Companies
* Sectors
* Countries
* Commodities
* Themes
* Economic mechanism
* Supply/demand impact
* Earnings impact
* Valuation impact

Signals are treated as passive data models.

Analytical calculations remain inside engines.

---

# 3. SIGNAL INTELLIGENCE

Status: COMPLETE

Completed components include:

```text
Signal Intelligence
Signal Aggregation
Signal Validation
Signal Registry
Canonical Signal Model
```

The architecture supports conversion of raw observations into structured investment intelligence.

The Signal layer is intended to monitor macro, sector, company and market developments rather than relying solely on conventional financial statements.

---

# 4. CAUSAL CHAIN ENGINE

Status: COMPLETE

The Causal Chain layer connects observed signals to economic and investment consequences.

Conceptual structure:

```text
Signal
   ↓
Economic Mechanism
   ↓
Supply/Demand Effect
   ↓
Earnings Effect
   ↓
Valuation Effect
   ↓
Company Impact
```

This prevents EIOS from treating isolated observations as catalysts without establishing a mechanism.

---

# 5. CATALYST TAXONOMY

Status: COMPLETE

Catalyst Taxonomy has now been implemented.

The Catalyst architecture includes:

```text
Catalyst Taxonomy
Catalyst Registry
Catalyst Classifier
Catalyst Engine
Catalyst Classification Confidence
Primary Catalyst
Secondary Catalysts
Unclassified Signals
```

The classifier has been tested against:

```text
Revenue Catalyst              PASS
Capital Cycle Catalyst        PASS
Regulatory Catalyst           PASS
Multi-Catalyst                PASS
Unknown Signal                PASS
No Signals                    PASS
Signal Immutability           PASS
```

The Catalyst Engine converts classified signals and causal chains into an institutional Catalyst assessment.

It evaluates:

* Direction
* Horizon
* Magnitude
* Probability
* Persistence
* Market Recognition
* Catalyst Score
* Catalyst Confidence
* Evidence
* Contradictory Evidence
* Assumptions
* Invalidation Conditions
* Warnings

---

# 6. EXPECTATION GAP ENGINE

Status: COMPLETE

The Expectation Gap Engine compares:

```text
Market Expectations
        vs
EIOS Expectations
```

including earnings expectations.

The purpose is to identify situations where the market may be systematically underestimating or overestimating future business outcomes.

This is a central component of the Opportunity Engine because the objective is not simply to find good businesses.

The objective is to identify **mispriced expectations**.

---

# 7. MISPRICING ENGINE

Status: COMPLETE

The Mispricing Engine evaluates the relationship between:

```text
Current Market Price
        vs
Authoritative Valuation
```

while incorporating Catalyst and Expectation Gap information.

Valuation remains authoritative in the Valuation Engine.

The Opportunity Engine does not replace the valuation architecture.

---

# 8. ASYMMETRY ENGINE

Status: COMPLETE

The Asymmetry Engine evaluates:

* Probability-weighted return
* Upside probability
* Downside probability
* Permanent-loss probability
* Best-case return
* Worst-case return
* Expected time to thesis
* Asymmetry ratio
* Asymmetry score
* Confidence
* Assumptions
* Disconfirming evidence
* Invalidation conditions

The engine explicitly separates:

```text
Potential upside
        from
Permanent capital-loss risk
```

This is a mandatory component of the Opportunity architecture.

---

# 9. EVIDENCE ENGINE

Status: COMPLETE

The Opportunity Evidence Engine provides the evidence qualification layer.

It supports:

* Supporting evidence
* Contradictory evidence
* Evidence strength
* Evidence confidence
* Primary-source assessment
* Independent confirmation
* Time sensitivity
* Evidence gaps
* Kill switches
* Monitoring signals
* Evidence sufficiency

Evidence is treated as a **qualification gate**, rather than simply another score that can be compensated for by other attractive metrics.

This is an important institutional design principle.

---

# 10. OPPORTUNITY SYNTHESIS

Status: COMPLETE

The Opportunity Synthesis Engine combines the outputs of:

```text
Catalyst
Expectation Gap
Mispricing
Asymmetry
Evidence
```

into an individual Opportunity assessment.

The current synthesis architecture separates:

### Opportunity Attractiveness

```text
Catalyst
20%

Expectation Gap
20%

Mispricing
30%

Asymmetry
30%
```

from:

### Confidence

Confidence is calculated independently and incorporates analytical and evidence confidence.

### Evidence Qualification

Evidence sufficiency is treated separately from the Opportunity Score.

### Risk

Permanent-loss probability is explicitly incorporated into the synthesis decision.

The Synthesis layer also carries:

* Evidence gaps
* Disconfirming evidence
* Kill switches
* Invalidation conditions
* Assumptions
* Warnings
* Expected return
* Expected time to thesis
* Decision status

Possible synthesis decisions include:

```text
REJECT
WATCH
RESEARCH
HIGH CONVICTION CANDIDATE
```

---

# 11. OPPORTUNITY PIPELINE

Status: COMPLETE

The Opportunity Pipeline orchestrates:

```text
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
```

The pipeline deliberately contains orchestration rather than analytical calculations.

This preserves separation of responsibilities.

---

# 12. NEGATIVE-PATH TESTING

Status: COMPLETE

The Opportunity Pipeline has dedicated negative-path testing.

Current cases:

```text
Strong Opportunity          PASS
No Evidence Gate            PASS
No Kill Switch              PASS
Permanent Loss              PASS
Weak Valuation              PASS
```

This confirms that the Opportunity Engine does not simply succeed on ideal inputs.

Failure conditions are explicitly tested.

---

# 13. OPPORTUNITY RANKING ENGINE

Status: COMPLETE — STANDALONE

The Opportunity Ranking Engine is the newest completed subsystem.

Git commit:

```text
4cfe346 Add opportunity ranking engine
```

Files:

```text
modules/opportunity/ranking/ranking_engine.py
modules/opportunity/ranking/ranking_models.py
modules/opportunity/ranking/test_ranking_engine.py
```

The Ranking Engine is deliberately separate from Opportunity Synthesis.

### Synthesis asks:

> Is this individual opportunity attractive?

### Ranking asks:

> Which opportunities deserve scarce EIOS research capacity relative to the alternatives?

This distinction is fundamental to the Elephant Pipeline architecture.

---

# 14. RANKING ENGINE DESIGN

The Ranking Engine does NOT recalculate:

* Catalyst
* Expectation Gap
* Mispricing
* Asymmetry
* Evidence

Those engines remain authoritative for their respective analytical responsibilities.

Ranking consumes the resulting Synthesis outputs.

The Ranking Engine evaluates:

```text
Opportunity Score
Confidence
Evidence
Risk-adjusted attractiveness
Research efficiency
Permanent-loss risk
Research priority
```

It also applies hard qualification gates.

---

# 15. RANKING GATES

The current standalone Ranking Engine includes:

### Evidence Gate

Requires sufficient evidence and evidence confidence.

### Permanent-Loss Gate

Prevents excessive permanent-capital-loss probability from being hidden by a high Opportunity Score.

### Confidence Gate

Requires minimum analytical confidence.

### Kill-Switch Gate

Requires explicit thesis invalidation logic.

These gates prevent a superficially high-scoring opportunity from automatically becoming a research priority.

---

# 16. RESEARCH EFFICIENCY

The Ranking Engine introduces a separate concept:

```text
Opportunity Attractiveness
        vs
Research Priority
```

Research efficiency considers expected return relative to expected time to thesis.

This is important because EIOS has finite research capacity.

A potentially excellent opportunity requiring many years to resolve should not automatically outrank a similarly attractive opportunity where the thesis can be tested much sooner.

---

# 17. RANKING TEST RESULTS

Standalone Ranking Engine testing is COMPLETE.

All 10 tests passed:

```text
Case 1 — Strong Opportunity          PASS
Case 2 — Weak Opportunity            PASS
Case 3 — No Evidence Gate            PASS
Case 4 — Permanent Loss              PASS
Case 5 — No Kill Switch              PASS
Case 6 — Low Confidence              PASS
Case 7 — Research Efficiency         PASS
Case 8 — Competitive Ranking         PASS
Case 9 — High Score / Bad Risk       PASS
Case 10 — Empty Input                PASS
```

Result:

```text
EIOS OPPORTUNITY RANKING ENGINE : PASS
```

---

# 18. CURRENT GIT CHECKPOINTS

Latest commits:

```text
4cfe346 Add opportunity ranking engine
bd27798 Integrate catalyst taxonomy and classifier
```

The current working tree is CLEAN.

The Ranking package has been committed separately from the Catalyst milestone.

This preserves safe rollback points.

---

# 19. ARCHITECTURAL PRINCIPLE

The Opportunity Engine now has two distinct analytical levels.

## Level A — Individual Opportunity Analysis

```text
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
```

This determines whether an individual opportunity is compelling.

## Level B — Competitive Opportunity Selection

```text
Multiple Synthesized Opportunities
             ↓
     Opportunity Ranking
             ↓
     Research Priority
```

This determines which opportunities deserve scarce EIOS research resources.

This separation must be preserved.

---

# 20. LEGACY OPPORTUNITY SCORE ENGINE

The existing legacy Opportunity Score Engine remains in the repository.

It currently uses a simple additive model involving:

```text
Catalyst
Earnings
Sector
Valuation
Institutional
Expansion
Risk
```

It should NOT yet be deleted.

Reason:

The EIOS migration principle is:

```text
New Architecture
      ↓
Prove Replacement
      ↓
Regression Testing
      ↓
Migration
      ↓
Remove Legacy
```

The legacy score architecture should therefore remain until the new Synthesis/Ranking architecture has fully replaced all consumers.

A particularly important future cleanup is separating:

```text
Score
```

from:

```text
Confidence
```

Confidence must never simply equal an opportunity score.

---

# 21. CURRENT STATUS

## Opportunity Engine

**STATUS: ADVANCED DEVELOPMENT / CORE ANALYTICAL ARCHITECTURE COMPLETE**

Completed:

```text
Signal Foundation                 ✅
Signal Intelligence               ✅
Signal Aggregation                ✅
Signal Validation                 ✅
Causal Chain                      ✅

Catalyst Taxonomy                 ✅
Catalyst Registry                 ✅
Catalyst Classifier               ✅
Catalyst Engine                   ✅

Expectation Gap                   ✅
Mispricing                        ✅
Asymmetry                         ✅
Evidence                          ✅
Synthesis                         ✅

Opportunity Pipeline              ✅
Negative-path testing             ✅

Opportunity Ranking               ✅
Ranking standalone tests          ✅
```

---

# 22. NOT YET COMPLETE

The following work remains deliberately unimplemented:

```text
Ranking → Synthesis Integration
Competitive Research Queue
Discovery → Opportunity Ranking Integration
Ranking → Master Dossier Promotion
Opportunity Committee Integration
Portfolio Engine Integration
Continuous Monitoring Integration
Quarterly Delta Integration
Legacy Opportunity Score Migration
Full end-to-end Opportunity workflow
```

These should be implemented sequentially rather than simultaneously.

---

# 23. NEXT DEVELOPMENT STEP

The immediate next task is:

## Ranking Integration Test

The Ranking Engine must first be tested against real Opportunity Synthesis objects.

Target architecture:

```text
Opportunity Pipeline
        ↓
Opportunity Synthesis
        ↓
Opportunity Ranking
        ↓
Competitive Research Priority
```

The Ranking Engine should initially be connected through a dedicated integration test.

The production Opportunity Pipeline should NOT be modified until this integration test passes.

---

# 24. NEXT DEVELOPMENT SEQUENCE

Recommended sequence:

```text
1. Ranking Integration Test
        ↓
2. Validate real Synthesis → Ranking data flow
        ↓
3. Integrate Ranking into Opportunity orchestration
        ↓
4. Full Opportunity Pipeline regression
        ↓
5. Competitive Research Queue
        ↓
6. Discovery → Ranking integration
        ↓
7. Promotion Gate
        ↓
8. Master Dossier hand-off
        ↓
9. Opportunity Committee integration
        ↓
10. Monitoring / Quarterly Delta integration
```

---

# 25. ENGINEERING RULES TO PRESERVE

EIOS development must continue to follow:

1. Architecture before implementation.
2. One engine = one responsibility.
3. Engines own calculations.
4. Data models remain passive.
5. Pipeline owns orchestration only.
6. No company-specific hardcoding.
7. Do not duplicate scoring logic.
8. Do not silently override authoritative engines.
9. Evidence must remain independently visible.
10. Disconfirming evidence must remain visible.
11. Kill switches must remain explicit.
12. Permanent-loss risk must remain explicit.
13. Confidence must remain separate from score.
14. Legacy code is removed only after safe migration.
15. Every major capability receives standalone tests.
16. Negative-path testing is mandatory.
17. Every stable architectural milestone should be committed.
18. EIOS must prefer intellectual honesty over forced conclusions.

---

# 26. CURRENT RESUME POINT

When development resumes, begin here:

```text
Git HEAD:
4cfe346 Add opportunity ranking engine

Working Tree:
CLEAN

Next Task:
Build Ranking → Synthesis integration test.

Do NOT:
- modify the existing Opportunity Pipeline yet
- remove the legacy Opportunity Score Engine
- add another scoring engine
- integrate Ranking into Master Dossier yet
```

The immediate objective is to prove that the newly created Ranking Engine can consume the actual Opportunity Synthesis output correctly and safely.

---

# 27. CURRENT ARCHITECTURAL MAP

```text
                    EIOS OPPORTUNITY ENGINE
                           │
                           ▼
                  SIGNAL INTELLIGENCE
                           │
                           ▼
                     CAUSAL CHAIN
                           │
                           ▼
                 CATALYST CLASSIFIER
                           │
                           ▼
                    CATALYST ENGINE
                           │
                           ▼
                  EXPECTATION GAP
                           │
                           ▼
                     MISPRICING
                           │
                           ▼
                     ASYMMETRY
                           │
                           ▼
                      EVIDENCE
                           │
                           ▼
                     SYNTHESIS
                           │
                           ▼
              ┌────────────────────────┐
              │ OPPORTUNITY RANKING    │
              │                        │
              │ Competitive Selection  │
              └────────────────────────┘
                           │
                           ▼
                  RESEARCH PRIORITY
                           │
                           ▼
                 TOP OPPORTUNITIES
                           │
                           ▼
                   MASTER DOSSIER
```

---

# 28. END-OF-SESSION CHECKPOINT

**EIOS Opportunity Engine has successfully moved beyond isolated analytical engines into a structured competitive-selection architecture.**

The most important completed transition is:

```text
"Is this opportunity attractive?"
              ↓
       Synthesis Engine

"Is this one of the best opportunities available?"
              ↓
       Ranking Engine
```

This is the current institutional architecture and should be treated as the baseline for the next development session.
Opportunity Engine — Committee Layer
- Opportunity Committee Engine implemented.
- Converts Opportunity Ranking results into Committee Review, Watchlist, or Reject decisions.
- No duplicate scoring, valuation, or ranking logic.
- Automatic approval is explicitly prohibited.
- Standalone Committee test: PASS.
- Synthesis → Ranking → Committee integration test: PASS.
- Evidence failure, permanent-loss failure, and missing kill-switch paths verified.