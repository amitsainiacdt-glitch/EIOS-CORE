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