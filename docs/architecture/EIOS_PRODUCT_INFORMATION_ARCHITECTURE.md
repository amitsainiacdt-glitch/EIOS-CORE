# EIOS Product Information Architecture

Status: Active design baseline  
Scope: Local EIOS investment application  
Principle: The interface presents governed engine output; it never performs investment reasoning.

## 1. Product model

EIOS contains two independent investment systems sharing one evidence core.

### Long-Term Division

Question: Can this business compound shareholder wealth over many years?

Canonical flow:

```text
Company → Master Dossier → Business Quality → Management → Financials
→ Moat → Risk → Valuation → Investment Committee → Portfolio
```

The Long-Term view must emphasize business durability, ten-year operating history,
capital allocation, management delivery, competitive advantage, permanent-loss risk,
valuation and margin of safety.

### Alpha / Opportunity Division

Question: Is reality changing before market consensus, and is there an investable
3–24 month opportunity?

Canonical flow:

```text
Reality → Observation → Signal → Catalyst → Causality → Industry → Company
→ Financial Impact → Expectation Gap → Mispricing → Ranking → Opportunity Committee
```

The Alpha view must emphasize new evidence, signal maturity, dated catalysts,
causal transmission, market awareness, expectation change, kill switches and monitoring.

### Shared core

Both divisions consume the same governed identity, source, evidence, financial,
company-event, news, valuation and monitoring records. They may reach different
statuses because their questions and time horizons differ. Neither division may
silently overwrite the other.

## 2. Primary user journey

```text
Search company
  → Company cockpit
    → Verdict and confidence boundary
      → Why this status now
        → Long-Term or Alpha lens
          → Ten-year evidence / current change evidence
            → Source document and page-level audit trail
```

The first company viewport must answer five questions without scrolling deeply:

1. What is EIOS's current status?
2. Is this a Long-Term conclusion, an Alpha conclusion, or both?
3. What evidence most strongly supports the status?
4. What evidence contradicts it or remains missing?
5. What changed recently and when will EIOS reassess?

## 3. Navigation

### Global navigation

- Mission Control
- Companies
- Alpha Opportunities
- Long-Term Research
- Monitoring
- Evidence Library
- Portfolio

### Company navigation

- Overview
- Long-Term
- Alpha
- Financials
- Reports
- News & Events
- Valuation
- Evidence
- Monitoring

The company remains the stable context while the analytical lens changes.

## 3A. Permanent EIOS company sequence

This sequence is unique to EIOS and is mandatory across desktop, web and future
mobile views. It adopts progressive disclosure without reproducing another
platform's Snowflake, scorecard or page composition.

```text
1. Decision Now
   ↓
2. What Changed
   ↓
3. Ten-Year Business Story
   ↓
4. Financial Trajectory
   ↓
5. Current Intelligence
   ↓
6. Catalysts & Expectations
   ↓
7. Valuation, Risk & Contradictions
   ↓
8. Evidence Lineage & Monitoring
```

The **Decision Spine** is EIOS's signature navigation device. Every stage shows
its readiness, source freshness and effect on the Long-Term and Alpha systems.
It is a causal research sequence—not a decorative company score.

### Stage 1 — Decision Now

Long-Term status, Alpha status, permitted conclusion, confidence boundary,
human-review status and the top reason for holding or advancing.

### Stage 2 — What Changed

Material deltas since the previous EIOS review: new filing, result, order,
management commitment, risk, price recognition or contradiction.

### Stage 3 — Ten-Year Business Story

One material annual highlight per year, management promise versus delivery,
business-mix evolution, major capital allocation and recurring risks.

### Stage 4 — Financial Trajectory

Revenue, margins, cash conversion, debt, ROCE, ROIIC, per-share value, segment
economics and accounting quality. Charts always retain table and source access.

### Stage 5 — Current Intelligence

Reviewed news, filings, orders, tenders, policy, commodity, weather, supply-chain
and competitive developments ranked by thesis impact rather than popularity.

### Stage 6 — Catalysts & Expectations

Dated catalyst, causal agent, expected earnings channel, market awareness,
expectation baseline, recognition state, disconfirming evidence and kill switch.

### Stage 7 — Valuation, Risk & Contradictions

Scenario valuation and margin of safety beside permanent-loss risks, thesis
breakers and facts that oppose the attractive interpretation.

### Stage 8 — Evidence Lineage & Monitoring

Verdict-to-source audit trail, document/page access, extraction and review state,
last update, next scheduled check and decision-change history.

## 4. Company cockpit

### A. Identity bar

Company name, ticker, sector, latest data time, source freshness and watch status.

### B. Dual-decision strip

Two equally visible cards:

- Long-Term: Research Hold / Review / Committee Ready / Approved / Rejected
- Alpha: Noise / Weak Signal / Emerging / Confirmed Catalyst / Opportunity / Rejected

Each card shows confidence separately from attractiveness or score.

### C. Verdict explanation

- Plain-English conclusion
- Top supporting evidence
- Top contradictory evidence
- Missing mandatory layers
- Last material change
- Next review trigger

Every statement links to evidence IDs and source pages. The UI must never create
verdict language from raw facts.

### D. Ten-year business story

The annual-report experience has three levels:

1. **Ten-year highlight strip** — one card per financial year, showing the most
   material change, financial direction, management promise and risk.
2. **Trend view** — revenue, EBITDA, PAT, cash conversion, debt, ROCE/ROIIC,
   capex, segment mix and per-share value with annual/quarterly selectors.
3. **Report reader** — EIOS summary beside the official report, with page-level
   citations, extracted facts, contradictions and review status.

Missing years remain visibly missing; EIOS may not interpolate authoritative facts.

### E. Current intelligence stream

News must be relevance-ranked, not chronologically dumped. Each event shows:

- event date and source
- event type
- affected Long-Term or Alpha thesis
- causal channel
- supporting or contradicting direction
- materiality and confidence
- verdict impact: none / watch / reassess / status changed

Only reviewed, source-grounded events may be described as a basis for a verdict.

### F. Catalyst and expectation panel

- catalyst
- dated agent
- expected financial transmission
- market expectation before the event
- observed recognition
- disconfirming evidence
- kill switch

### G. Audit drawer

Any output can open its lineage:

```text
Verdict → Engine finding → Evidence item → Extracted fact → Source document/page
```

## 5. Presentation hierarchy

Use progressive disclosure:

- Level 1: decision and material change
- Level 2: analytical explanation and trend
- Level 3: source facts, calculations and documents
- Level 4: technical receipts and governance history

Colour communicates state, never decoration alone:

- emerald: verified positive or complete
- amber: incomplete, uncertain or review required
- rose: contradiction, failure or kill switch
- sky: neutral evidence and source material
- violet: Meta interpretation

## 6. Backend-to-UI contracts

The UI consumes typed read models assembled from canonical repositories.

### CompanyCockpitSnapshot

- identity
- freshness
- long_term_decision
- alpha_decision
- ten_year_summary
- current_intelligence
- catalysts
- valuation
- contradictions
- unresolved_gaps
- monitoring
- evidence_lineage

### DecisionView

- division
- status
- permitted_conclusion
- confidence_percent
- attractiveness_score (optional and never substituted for confidence)
- supporting_evidence_ids
- contradicting_evidence_ids
- mandatory_gaps
- last_changed_at
- next_review_trigger

### AnnualReportYearView

- financial_year
- report_status
- review_status
- financial_highlights
- operating_highlights
- management_promises
- risks
- contradictions
- source_url
- source_pages

### IntelligenceEventView

- event_id
- occurred_at
- source
- event_type
- headline
- causal_channel
- thesis_direction
- materiality
- confidence
- decision_impact
- evidence_ids

## 7. Fail-closed rules

1. No report extraction means no report-derived conclusion.
2. No current news ingestion means the news panel says it is not connected.
3. No ten-year reconciliation means long-term trend language is prohibited.
4. No expectation baseline means mispricing is not assessable.
5. No dated catalyst means Alpha cannot become an Opportunity.
6. No mandatory layer completion means the verdict remains Research Hold.
7. Human review status is always visible.
8. Scores, confidence and verdict are separate fields.

## 8. UX references adapted for EIOS

- Koyfin: multi-horizon comparison and percentile context.
- TIKR: consolidated company financials, filings, transcripts, ownership and news.
- FinChat/Fiscal.ai: ten-year financial and KPI charting, company-centered navigation,
  AI summaries and reduced navigation complexity.
- Morningstar: one research methodology, explicit ratings, thesis, moat, valuation,
  notifications and source-of-truth consistency.

EIOS must not copy their visual identity. It should combine their information density
with EIOS's unique dual-system reasoning, causal audit trail and fail-closed governance.

## 9. Implementation sequence

1. Company cockpit and dual-decision read model.
2. Ten-year annual-report extraction and reconciled financial series.
3. Long-Term Master Dossier view.
4. Current news/event ingestion and relevance classification.
5. Alpha signal/catalyst/expectation view.
6. Evidence-lineage drawer.
7. Monitoring and decision-change history.
8. Cross-company ranking and portfolio views.
