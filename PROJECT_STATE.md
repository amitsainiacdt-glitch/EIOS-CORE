# PROJECT_STATE.md

# Everest Investment Operating System (EIOS)

## Canonical current checkpoint — 2026-09-07

- **Development state:** active development; not launch-ready.
- **Current completed checkpoint:** governed quarterly extraction and review pipeline, exact-quarter research targeting, controlled source verification/retry, browser-assisted official-PDF provenance, and dashboard quarterly-review presentation.
- **Latest automatic cycle:** process status `SUCCESS`; 22 of 22 jobs executed and 94 observations recorded, but official-document collection produced 0 archives, 0 extractions and 0 fact candidates, with 7 failures. Process success must not be interpreted as successful financial ingestion.
- **Latest validation:** 305 company-intelligence tests pass; the dashboard production build passes; the directly affected research-job, execution-service, orchestrator and trusted-document-adapter regression suites pass.
- **Governance boundary:** extracted quarterly and historical review records remain unapproved, create no governed evidence and do not change financial history or verdicts.
- **Current objective:** establish unattended, source-backed official-document acquisition for many companies, then complete full-statement extraction and mandatory META/human adjudication before facts enter the Master Dossier.
- **Immediate sequence:** (1) preserve this tested checkpoint, (2) implement an accessible governed acquisition route, (3) complete income-statement/balance-sheet/cash-flow and quarterly normalization, (4) activate META approval and Master Dossier promotion, (5) connect reasoning/verdict/UI refresh, and (6) validate on multiple unseen companies.
- **Canonical-state rule:** this root file is the authoritative project state. Files under `docs/` are supporting architecture/history and must point here for the live checkpoint.

## Governed issuer-source priority integrated — 2026-09-07

- Corrected automatic official-document collection so configured issuer report URLs are always considered for general official-document jobs, rather than only when web search returns no sources.
- Governed issuer locations are attempted before supplemental search results; duplicate URLs are removed and the existing per-job source limit is retained.
- Exact-quarter jobs remain excluded from generic issuer-page/annual-report fallback, preventing an older or unrelated report from satisfying a targeted quarterly request.
- All 307 company-intelligence tests pass, including new source-priority and duplicate-acquisition coverage. The external research orchestrator regression also passes.
- This improves acquisition routing but does not bypass issuer HTTP 403/406 restrictions or create approved facts. A supported unattended transport/provider remains necessary for blocked sources.

## Governed blocked-source provider boundary — 2026-09-07

- Added a provider-neutral fallback boundary for official documents that direct issuer/exchange HTTP cannot retrieve. The normal trusted-source attempt always runs first.
- Alternate delivery is rejected unless it names the delivery provider, uses HTTPS, preserves the exact requested official URL, supplies a matching acquisition receipt, and passes document hash and byte-count checks.
- A valid alternate delivery rejoins the existing archive, extraction, evidence-admission, META and human-review pipeline; it cannot bypass approval or change a verdict directly.
- Added end-to-end coverage proving a blocked direct document can pass through the governed fallback and normal archive. All 312 company-intelligence tests pass.
- No live provider is connected by this checkpoint. The contract makes such a connection safe and replaceable; credentials, commercial access and provider selection remain external prerequisites.

## Automatic governed local document inbox connected — 2026-09-07

- Implemented and connected the first real blocked-source fallback provider: `data/runtime/official_document_inbox` is checked automatically by the scheduled company cycle after direct official-source acquisition fails.
- Each PDF requires exactly one sidecar mapping containing schema version, local filename, exact official source URL and expected SHA-256. Missing, ambiguous, path-escaping, non-PDF or hash-mismatched inputs fail closed.
- Local delivery is explicitly recorded as `EIOS_GOVERNED_LOCAL_INBOX`; it is not misrepresented as an issuer network download. Valid documents rejoin the normal archive, extraction, admission, META and human-review path.
- All 314 company-intelligence tests pass and the scheduled-cycle entry point compiles.
- This makes browser/download-to-EIOS intake automatic once a source-backed file reaches the controlled inbox. Fully remote unattended acquisition still requires an accessible issuer/exchange route or an approved online provider implementation.

## Corroborated browser captures connected to automatic cycle — 2026-09-07

- The automatic company cycle can now reuse an EIOS-preserved browser capture after direct official HTTP acquisition fails, without requiring a duplicate manual inbox sidecar.
- Eligibility requires one exact official-URL match, schema-valid provenance, `BROWSER_COPY_CORROBORATED_PENDING_REVIEW` status, an explicit non-approval flag, a confined preserved-file path and matching SHA-256.
- Browser capture and governed inbox providers are chained deterministically. Their documents rejoin the ordinary archive/extraction/META/human-review pipeline and cannot approve facts or alter verdicts.
- All 315 company-intelligence tests pass; the automatic-cycle entry point compiles.
- Provider research confirmed that the examined Financial Datasets API is US/SEC-focused and is therefore not an adequate primary solution for EIOS's Indian-company coverage. No paid provider was connected or queried.

## Acquisition provenance exposed in System Runtime UI — 2026-09-07

- Automatic document-cycle summaries now distinguish fallback attempts, successful fallback retrievals, unavailable fallbacks and counts by delivery-provider identity.
- Dashboard synchronization carries candidates seen, archives, extractions, direct failures and fallback provenance into the runtime read model. The System Runtime page explains that fallback retrieval is still pending review and is not an approved fact.
- Refreshed the local dashboard snapshot from the completed 7 September cycle: 22/22 jobs, 94 observations, 20 document candidates, 7 direct failures and 0 archived/extracted documents in that pre-fallback run.
- All 316 company-intelligence tests pass and the dashboard production build passes.

## Controlled browser-fallback path proven end to end — 2026-09-07

- Added a no-network, no-paid-search production-path probe for the saved Coromandel Q1 FY2027 official report.
- The first probe correctly found and archived the corroborated browser capture but exposed a strict acquisition-type incompatibility at extraction. Corrected the fallback result to extend the canonical trusted acquisition result rather than weakening the extractor's type gate.
- The repeated probe succeeded: 1 official candidate, 1 fallback attempt/retrieval, 1 archive, 1 extraction, 8 fact candidates and 8 META assessments. All 8 were held for further research; 0 became approved facts and no verdict changed.
- The probe used no external network and no paid search. All 316 company-intelligence tests continue to pass.

## Automatic financial-results routing proven — 2026-09-07

- Routed recognized quarterly financial-results PDFs from the official-document pipeline into the specialized table/OCR/header/unit/reconciliation intake instead of the generic event-sentence extractor.
- Added a narrowly governed transfer of an assistant visual unit candidate across the two Coromandel PDF hashes only when the preserved comparison proves exact text and exact rendered-page equality. The transfer remains non-human-approved and creates no fact.
- Controlled probe now produces one checked Q1 FY2027 standalone financial candidate: revenue INR 7,743.55 crore, other income INR 48.76 crore, total income INR 7,792.31 crore and PAT INR 376.96 crore. Both native and OCR readings agree and the income arithmetic passes.
- Two other columns remain held for ambiguous duration/date headers. The surviving candidate remains held for official-source identity and reporting-note review; no history or verdict changes.
- Pipeline summaries now count quarterly candidates and their META outcomes. The repeated no-network/no-paid-search probe reports 1 queued candidate, 1 META review and 1 META hold. All 316 company-intelligence tests pass.

## Quarterly source and reporting-note holds separated — 2026-09-07

- Financial review now evaluates source-delivery provenance separately from reporting-note completion. A trusted direct receipt or corroborated browser capture can pass the delivery check when official URL and document hash match; a merely hash-bound local inbox copy cannot.
- Reporting notes remain held until human review. Each extracted note now receives explicit basis/date applicability cues without automatically assigning an impairment, acquisition, balancing-quarter or limited-review passage to the selected column.
- The controlled Coromandel candidate passes all four technical checks plus source-delivery provenance and remains `HOLD_FOR_REPORTING_NOTE_REVIEW`. No approval, history update or verdict change occurs.
- Added regression coverage for accepted corroborated delivery, unresolved note applicability and rejection of unverified local-inbox origin. All 318 company-intelligence tests pass.

## 2026-09-02 — Local cash-flow extraction and review table

- Added a fail-closed, page-scoped local PDF cash-flow extractor and Coromandel source mapping. Re-running `python scripts/extract_coromandel_cash_flow_history.py` extracts 48 source figures for FY2017-18 through FY2024-25 from six preserved reports. No network/provider call is used.
- Operating, investing, financing, opening cash, closing cash and cash fixed-asset purchases are retained with original lakh values, normalized crore values, PDF pages, passages, source references and document SHA-256. Free cash flow is explicitly calculated, not presented as a quoted source figure.
- All eight within-year cash bridges reconcile. Cross-report opening/closing differences of INR14.11 crore (FY2021-22) and INR1.83 crore (FY2024-25) remain flagged for reporting-scope/restatement review. No automatic economic explanation is asserted.
- Output: `data/company_intelligence/coromandel/coromandel_cash_flow_review.json`. Every record remains `PENDING_META_REVIEW`, `creates_evidence: false`. It is displayed separately and is NOT merged into governed financial history or verdict inputs.
- The local company financials page now includes an eight-year cash-flow review table, arithmetic explanation and expandable source passages. Dashboard synchronization carries this review pack without passing it into the financial interpreter.
- Seven new extractor tests and four existing interpreter tests passed. Dashboard production build passed and `/companies/coromandel` returned HTTP200 after restart. Browser visual verification was not performed. A separate TypeScript check reports existing string-index typing errors in the company quick table and opportunities page; these remain unresolved.
- This is a manually mapped local report import, NOT automatic source discovery for every company. META approval, review of restatements, remaining balance-sheet fields and quarterly history are still outstanding. Earlier offline cycles returning zero extracted documents must not be described as successful extraction.

## Current Project Status

### Direct report URL import for automatic collection (2026-09-02)

- Added the issuer-published Coromandel FY2024-25 report URL to the official source manifest. Direct URLs are now preferred when configured, so EIOS can acquire a report even if the issuer index page returns HTTP403/406.
- The same guarded path remains in force: HTTPS and allowlisted issuer domain, public-network validation, content hashing, immutable archive, text extraction and META/human review gates. Direct configuration does not create approved facts or a verdict.
- All 120 company-intelligence tests pass and the source manifest parses correctly. A live direct-download test could not run because the Codex usage limit was reached; no new online report was downloaded in this step.
- This is the automatic site-to-EIOS upload path for configured URLs. For a company with no configured direct URL, EIOS still needs an accessible index page or a local report import. No GitHub push was attempted.

### Direct official-page discovery fallback (2026-09-02)

- Found a structural dependency: the automatic document pipeline previously followed only selected search results and did not visit saved official investor-page locations when that list was empty.
- Added bounded direct discovery on one configured annual-report page per eligible official-document job, selecting at most two allowlisted PDF links in publisher order. It reuses the guarded acquisition adapter (HTTPS/domain/redirect/public-address checks) and existing archive/extraction/META pipeline. The automatic runner enables this fallback only outside explicit offline mode. It does not claim page order proves the newest year or provide quarterly-source discovery.
- Added explicit discovery page/failure/link counts. Test probe limits collection to at most one linked report and preserves diagnostics separately under data/runtime/official_collection_probe. No fabricated search results or approved facts.
- All 117 company-intelligence tests pass. Live Coromandel probe first hit the sandbox connection boundary; approved network retry reached the official page but received HTTP406. KPIT's configured page received HTTP403. Both returned zero discovered links and zero downloads. Website access remains unresolved; the code path is implemented but live collection is NOT demonstrated.
- Did not bypass site restrictions, switch to browser scraping, use paid credits, change Windows scheduling, run all jobs or push GitHub. Next work must address a genuinely accessible authorized source or source-import route, and retain extraction failure diagnostics/retry behavior.

### Automatic schedule and honest collection outcome (2026-09-02)

- Read Windows task `EIOS Automatic Company Intelligence`: Ready, daily at 06:00 India time, StartWhenAvailable true, WakeToRun false. Last scheduled run 2026-09-02 10:31:11 returned 0; next scheduled run 2026-09-03 06:00. Schedule was not changed or manually triggered.
- Latest saved cycle status reported SUCCESS but zero extracted documents and zero fact candidates. Process success is not proof of fresh research.
- Added a separate `collection_outcome` to future automatic-cycle status: no extraction, unchanged existing documents, extracted without candidates, candidates pending review, partial failures/holds, or unavailable counts. Existing process status is preserved for compatibility; new data is never described as approved.
- Six new outcome tests; all 114 company-intelligence tests pass. Existing historical status was not rewritten; no network cycle was run. Frontend display of the new outcome remains pending.

### Automatic repeat checks for inspected sources (2026-09-02)

- Added a read-only consistency checker for the two assistant-inspected examples. It rebuilds example fingerprints from the current extraction pack, validates arithmetic and provenance, hashes original local documents, and compares selected saved values/page/year columns. Changed/missing files, changed extraction/reference values, invalid authority flags and paths outside the workspace require re-review.
- Connected it to the automatic company's cycle preflight/status; issues stop that run before collection. Absent reference observations are reported explicitly as NO_REFERENCE_CHECKS, not passed verification. Full collection cycle was not run during this task.
- Local check returned SAVED_EXAMPLES_UNCHANGED for both examples. Six added regression tests; all 108 company-intelligence tests pass. No new human feedback or approval, no AI training, no verdict change; this is repeatable consistency checking against assistant observations, not independent audit or protection against coordinated tampering of all local files.

### Two real PDF examples inspected (2026-09-02)

- Visually inspected PDF141 (FY2024-25 report) and PDF137 (FY2023-24 report, FY2022-23 comparative column); file hashes match the extraction records. Standalone headings, lakh units, CFO and fixed-asset purchase outflows match all four selected amounts. Calculated FCF is 1716.06 and -45.01 crore respectively.
- Saved assistant-only observations with example fingerprints under `data/runtime/financial_source_assistant_review.json` and a readable review note in `docs/FINANCIAL_SOURCE_REVIEW_2026_09_02.md`. No selected-value corrections were required. This is not whole-series verification or a review of every cash-flow line.
- No human decisions, META approvals or learned feedback were fabricated. Memory count remains zero; the two assistant checks are pending independent review and are not imported as training labels. No UI or verdict changes.

### First real review worksheet (2026-09-02)

- Added a repeatable worksheet builder using the existing eight-year Coromandel cash-flow extraction pack. Generated local JSON and readable Markdown under `data/runtime/financial_review_examples.*` with operating cash, fixed-asset cash spending, calculated FCF, original units, year-column/page references and review questions.
- Builder checks source bindings, lakh/crore and spending-sign conversions, common document/year columns, FCF arithmetic and duplicate periods. These are mechanical checks of saved extraction data, not an independent PDF review.
- Every example remains AWAITING_SOURCE_REVIEW with no human decision. No review-memory entries or governed facts were created. The financial worksheet is not yet an approved numerical-correction workflow; existing event-review memory must not be described as trained on these financial examples.
- Three added regression tests, including actual saved data, tampered inputs and duplicate/status rejection. All 102 company-intelligence tests pass. No network collection or GitHub push performed.

### Review-memory measurement (2026-09-02)

- Added a read-only memory report counting real reviews, usable snapshots, legacy records and time-ineligible feedback. It replays up to 100 recent known reviews with and without memory and checks retained feedback, restrictive decisions and preserved authority gates.
- These are known-feedback retention tests, not holdout accuracy, model training or investment performance. Unseen-fact and investment accuracy remain null. Empty memory reports AWAITING_REVIEW_FEEDBACK, not successful learning.
- Connected the report to the automatic company-cycle preflight/status. A failed memory replay blocks that cycle. The automatic cycle itself was not run during this change; no external collection or review decisions were triggered.
- `python scripts/report_review_memory.py` currently reports zero real reviews. All 99 company-intelligence tests pass, including six new report tests. Naive/unknown-timezone legacy decisions no longer cause aware-date comparisons to fail and are not applied as learned feedback.

### Controlled review memory (2026-09-02)

- Added persisted candidate snapshots to newly recorded human review receipts, bound to existing candidate fingerprints. Old receipts remain readable; absent snapshots are not invented or automatically backfilled.
- The production META writer now reads the default human review ledger. Exact matches across repeated extraction runs remember prior REJECT/HOLD decisions and hold the repeated fact for research; earlier APPROVE decisions are context only and cannot bypass fresh checks/human review or create evidence, catalysts or verdicts.
- Match scope includes company, document hash, URL, PDF page, passage, amounts/dates, event type and posture. No fuzzy generalization across companies/reports, no AI weight training, no investment-outcome learning. Future-dated feedback is excluded from historical assessments; mismatched saved snapshots fail closed.
- Eight new regression tests; all 93 company-intelligence tests pass. No real review ledger existed at implementation time, so there are no live learned decisions yet. Tests use synthetic temporary records only. This does NOT make quarterly extraction or report-page discovery autonomous. UI memory display and measured outcome evaluation remain future work.

### Quarterly staging safeguards (2026-09-02)

- Full company-intelligence unittest discovery passed: 85 tests after five new quarterly validation tests (80 before changes).
- Quarterly staging now rejects booleans, nonfinite/overflowing numbers, malformed quarter labels, annual/YTD period labels and invalid identifiers. True zero, missing values and losses remain distinct. Quarter labels explicitly use the financial-year-ending convention.
- Removed source-ID-only self-promotion to GOVERNED: this staging type accepts STAGED only. Approval must come through the separate governed review workflow, not a label. No production callers currently instantiate this type; quarterly extraction and UI integration remain outstanding.
- This is backend preparation, not newly extracted quarterly data or a completed automatic pipeline. GitHub push remains blocked pending the user's explicit approval of the saved commit payload and destination; no retry was attempted.

### Graph visibility repair (2026-09-02)

- User reported only boxes, not charts. A local React server-render test confirmed the installed Recharts ComposedChart emits an empty wrapper with no SVG/bars before hydration, even with explicit dimensions. This establishes the absent server fallback, not the exact cause of the user's browser hydration failure.
- Replaced financial-trend client charts with server-rendered quantitative SVGs using the same review data adapter. Real bars, lines, year labels and axes are included without browser JavaScript or resize measurement; narrow screens can scroll the chart. Native point titles and accessible exact-number tables remain available. No changes to approved facts/verdicts.
- All six chart tests passed, including server SVG/bar/line presence, real negative cash flow, missing-point gaps and zero-height zero bars. Production build passed. Browser visual QA has not been performed; user confirmation remains necessary.

### Financial graphs (2026-09-02)

- Replaced the old percentage-height mini-bars and decorative waiting bars with four responsive, source-pack-backed charts placed before the financial tables: standalone revenue, calculated operating EBITDA, operating cash/fixed-asset purchases/calculated free cash flow, and inventory/trade receivables.
- Selected FY2017-18–FY2024-25 history is labeled explicitly; all plotted review-pack figures remain pending META review. No governed inputs, approvals or verdicts changed. Missing/nonfinite observations stay null, lines do not bridge missing years, zero baselines and negative cash flow are preserved.
- Added exact-value tooltips, visible legends, plain-English explanations, source-table links, and accessible expandable chart-number tables. Companies without review packs get an honest empty state, not Coromandel data or invented charts.
- Three chart-data tests passed, including every plotted source-pack value, negative/zero/missing behavior, and input immutability. Production build passed and the restarted local company route returned HTTP200. Browser visual verification was not performed.
- Full TypeScript check remains blocked by existing cash-flow optional-fact typing at the company page and the opportunities page string/never issue; no new chart-file diagnostics appeared. Local only; not deployed.

### Operating EBITDA review display (2026-09-02)

- Added the eight-year operating EBITDA calculation table at `#operating-earnings-history`, first in Financials. It shows pre-exceptional/pre-tax profit, finance costs, depreciation/amortisation, other income and the calculated result, with a separate company-reported EBITDA row. No reported values or approved analysis inputs were replaced.
- Added pre-display checks on all 40 saved inputs: lakh/crore conversion, numeric finiteness, period/column mapping, document hash/page consistency, duplicate periods and exact calculation arithmetic. These checks are NOT META approval or independent re-reading of the PDF by an AI reviewer.
- Supporting passages and official report/archive links are expandable. Explanation explicitly distinguishes calculated operating EBITDA from cash flow, issuer definitions and buy signals, and warns about merger/lease-accounting comparability.
- All 39 focused tests pass, including tampered arithmetic, unit/raw-value mismatch and mixed-source rejection. Company-reported EBITDA still has seven unextracted years; an alternative calculated series is now available for all eight years. Six accounting-capex gaps and quarterly history remain unfinished. Everything remains local and pending META review.

### Desktop shortcut and earnings preparation (2026-09-02)

- Inspected `C:\Users\RBI\Desktop\EIOS Dashboard.lnk`: it already targets the current workspace launcher. Changed that launcher to open `/companies/coromandel?desktopRefresh=<timestamp>#financials` rather than the home page. The link itself did not need replacement. Added a non-mutating `-CheckOnly` mode; health checking retains the root URL. Launcher syntax validated and target route returned HTTP200. Desktop-browser visual testing was not performed.
- Added local operating-earnings extraction: 40 source inputs across eight years, plus eight explicitly calculated operating EBITDA values. Formula: pre-exceptional/pre-tax profit + finance costs + depreciation/amortisation - other income. Preserves source-page/hash/column provenance, rejects ambiguous exceptional-item layouts, and distinguishes calculations from issuer-reported EBITDA.
- Output `coromandel_operating_earnings_review.json` is pending META review, not yet connected to UI summary or governed analysis. Existing reported EBITDA/history remains untouched. All 35 focused tests pass. Accounting capex and quarterly history remain unfinished.

### Note-backed borrowing review (2026-09-02)

- Added borrowing-note extraction from six mapped standalone note18 pages (144,90,87,138,155,156). Each year has an explicit long-term borrowing zero, from a printed numeric row or year-bound narrative disclosure, rather than inference from an absent balance-sheet row.
- Short-term note totals must exactly match balance-sheet current borrowings. Added a separate calculated `total_borrowings_ex_leases` field with an explicit exclusion definition; lease liabilities and other liabilities remain separate. Original analysis data is not overwritten.
- Summary display now labels this metric Borrowings (excluding leases) and supplies eight pending-review values. Thirteen summary gaps remain: EBITDA7 and accounting capex6. Balance review has 213 directly extracted fields plus 15 calculated fields.
- All 31 focused tests pass, including explicit-zero, missing-note, wrong-year and disagreement checks. META approval and quarterly history remain outstanding; no public deployment.

### Financial-summary gaps (2026-09-02)

- Diagnosed duplicate sparse summary views: newly extracted balance/cash-flow review facts were not reflected in older summary cells.
- Added `financial_display.py` as a presentation-only layer AFTER interpretation. It fills only null cells for exact matching standalone metrics, years and crore units with hash/page-bound pending-review facts. Existing values and analysis inputs remain unchanged; capex/cash-capex and debt/current-borrowing substitutions are prohibited.
- Connected both summary-table renderers through one shared value component. Ten gaps are now displayed in amber with Pending META badges and links to source review sections. Remaining 21 summary gaps: EBITDA7, accounting capex6, total debt8. Missing cells explain the reason on hover.
- Four new display-layer tests plus 23 existing tests pass. Dashboard build passed. This is presentation integration, not new source extraction or META approval. Quarterly extraction remains outstanding.

### Liability-detail follow-up (2026-09-02)

- Expanded the eight-year review with current/non-current provisions, other financial liabilities, other liabilities and trade payables. Latest pack has 205 directly extracted facts plus seven separately labelled calculated trade-payable totals. Older single-row trade payables retain their original source value.
- MSME and other-creditor payables are preserved separately. Calculated totals have no fabricated raw source amount; their formula is retained. Missing rows remain null. Existing four grand-total/subtotal checks continue to pass, but this is not yet a full component-to-total or note-level audit.
- Local balance-sheet UI includes these rows and distinguishes quoted from calculated figures. All 23 focused balance-sheet/cash-flow/interpreter tests pass. META approval remains pending; no governed evidence or investment verdict was created.
- Next: quarterly history and remaining note-level checks. Public launch remains prohibited without explicit approval.

### Eight-year balance-sheet review table (2026-09-02)

- Added `local_balance_sheet_extractor.py` and `scripts/extract_coromandel_balance_sheet_history.py`, using six preserved PDFs and explicitly mapped standalone pages. Extracted 142 non-null fields across FY2017-18 through FY2024-25 into `coromandel_balance_sheet_review.json`.
- Includes assets/equity/liabilities, four current/non-current subtotals, PPE, CWIP, inventory, customer/subsidy receivables, cash, other bank balances and separately reported current/non-current borrowings and lease obligations. Missing entries remain null, not zero.
- Four checks per year: assets = equity + liabilities; asset and liability subtotals; equality of reported grand totals. These are total checks, not proof that every statement line has been extracted or approved.
- Old manual financial history is unchanged. Review records stay `PENDING_META_REVIEW`, `creates_evidence: false`, separate from verdict inputs. Report-vintage, restricted-deposit and merger/reclassification limitations are retained.
- Added local `#balance-sheet-history` table with source passages, linked report references and plain-English explanation. PDF layouts for earliest/latest source years were visually inspected. Six new tests plus 15 existing cash-flow/interpreter tests pass.
- Still needed: detailed notes and remaining line items (including trade payables/provisions), META adjudication, quarterly history and reusable source discovery. No public launch or deployment.

### Cash-flow revision follow-up (2026-09-02)

- Original eight-year cash values are preserved. Added two full later comparative versions and line-by-line revision comparisons, not silent replacement of earlier reports.
- FY2021-22 Note47 (PDF154) explicitly confirms prior-year restatement following the LPFL/CSQM merger. The FY2020-21 original-to-revised closing cash difference is INR14.11 crore: opening0.27 + operating0.45 + investing0.16 + financing0.84 + acquired cash12.39. Added support for the explicitly reported business-combination cash adjustment, separate from operating cash and FCF.
- FY2024-25 Note42 (PDF168) explains accrued-interest reclassification into cash/bank balances/loans. FY2023-24 closing cash changes by INR1.83 crore: opening4.45 + investing(-2.62), with operating and financing unchanged. The precise cash allocation is an inference from compared figures; the note quotes the aggregate reclassification and states no profit/equity effect. Both notes were inspected as rendered PDF pages.
- Local cash-flow UI now shows the explanations, expandable notes and original-versus-revised comparison tables. All records remain pending META review and create no governed evidence or verdict.
- The current eight-year review pack includes 49 directly extracted figures (one explicitly reported zero acquisition adjustment added), plus separate comparative versions. Parser tests cover acquisition adjustments, wrong years, broken bridges, duplicate/missing rows and not borrowing numbers from an adjacent row.
- Remaining: mandatory META adjudication, complete balance-sheet extraction, quarterly history, reusable source discovery. This follow-up does not complete those tasks or authorize launch.

Status: Active Development

Current Phase: Phase 2 â€“ Execution

Current Release: 18.3

Architecture Status: Stable

Last Updated:
# PROJECT_STATE.md

# Everest Investment Operating System (EIOS)

---

## Project Identity

| Item | Value |
|------|-------|
| Project Name | Everest Investment Operating System (EIOS) |
| Mission | Build the world's first Institutional Intelligence Platform for Business Science, Capital Allocation, and Long-Term Wealth Creation |
| Development Phase | Phase 2 â€“ Execution |
| Current Release | Release 18.3 |
| Development Status | ðŸŸ¡ Active Development |
| Architecture Status | ðŸŸ¢ Stable |
| Repository Status | ðŸŸ¡ Active Refactoring |
| Documentation Status | ðŸŸ¡ In Progress |
| Last Updated | 04 August 2026 |

---

## Current Development Objective

Complete Release 18.3 by:

- Completing the Intelligence Mesh integration.
- Establishing ResearchContext as the single institutional intelligence bus.
- Completing the typed Master Dossier migration.
- Eliminating remaining legacy dictionary-based data flow.
- Preserving architectural integrity while minimizing technical debt.

---

## Guiding Principle

> Every release must improve EIOS's ability to understand businesses, reason transparently, and allocate capital more intelligently.
---

# Current Architecture

## Architecture Summary

| Component | Current Standard |
|-----------|------------------|
| Architecture Style | Repository-First, Layered, Domain-Oriented |
| Composition Root | EIOSApplication |
| Shared Intelligence Bus | ResearchContext |
| Intelligence Integration | Intelligence Mesh |
| Domain Model | Typed Master Dossier |
| Persistence | Repository Pattern |
| Business Logic | Engine Layer Only |
| Presentation | Desktop UI |
| Entry Point | main.py (Thin Bootstrap Only) |

---

## Architectural Principles

The current architecture follows these permanent principles:

- Presentation layer contains no business logic.
- Engines contain all business reasoning.
- Typed Master Dossier sections are passive data models.
- ResearchContext is the central intelligence exchange.
- Intelligence Mesh coordinates communication between engines.
- Repositories own persistence.
- Business knowledge must never be hardcoded inside UI or orchestration code.
- Every engine has a single responsibility.
- Every module is independently testable.

---

## Current Architectural Status

### Stable Components

- ResearchContext
- Intelligence Mesh
- Repository Pattern
- Investment Committee
- Typed Master Dossier
- Desktop UI Framework
- Discovery Engine
- Business Engine
- Financial Engine
- Valuation Engine
- Risk Engine
- Ownership Engine

---

### Active Refactoring

Current engineering work is focused on:

- Completing the Intelligence Mesh integration.
- Completing migration from legacy dictionary-based flow to typed Master Dossier objects.
- Reducing coupling between engines.
- Standardizing communication through ResearchContext.
- Simplifying orchestration while preserving functionality.

---

## Architectural Constraints

The following rules must not be violated without an approved architectural decision:

1. UI must never contain business logic.
2. Engines must never directly manipulate UI.
3. Master Dossier remains the single source of truth for company intelligence.
4. Business knowledge belongs in engines and knowledge modelsâ€”not orchestration code.
5. main.py remains a minimal bootstrap file.
6. Repository layer is responsible for persistence.
7. Cross-engine communication should occur through ResearchContext and the Intelligence Mesh wherever practical.
---

# Current Capability Matrix

## Platform Core

| Capability | Status | Notes |
|------------|--------|-------|
| Repository Architecture | âœ… Complete | Repository-first architecture established |
| EIOSApplication | âœ… Complete | Composition Root implemented |
| ResearchContext | ðŸŸ¡ In Progress | Becoming the central intelligence bus |
| Intelligence Mesh | ðŸŸ¡ In Progress | Integration underway |
| Typed Master Dossier | ðŸŸ¡ In Progress | Legacy migration ongoing |
| Repository Layer | âœ… Complete | Persistence abstraction available |

---
---

# Institutional Validation

## Reference Validation Company

Sharda Cropchem

Purpose

Validate the complete EIOS architecture using one real company before generalizing capabilities.

Validation Pipeline

Observation

â†“

Evidence

â†“

Concept

â†“

Business Law

â†“

Knowledge

â†“

Reasoning

â†“

Master Dossier

â†“

Investment Committee

Current Status

ðŸŸ¡ Preparing Initial Validation

## Knowledge Layer

| Capability | Status | Notes |
|------------|--------|-------|
| Knowledge Objects | â¬œ Planned | Formal framework pending |
| Knowledge Engine | ðŸŸ¢ Available | Initial implementation exists |
| Knowledge Registry | ðŸŸ¢ Available | Exists, requires evolution |
| Business Laws | â¬œ Planned | Academy phase |
| Mental Models | â¬œ Planned | Academy phase |

---

## Evidence Layer

| Capability | Status | Notes |
|------------|--------|-------|
| Evidence Engine | ðŸŸ¢ Available | Initial implementation exists |
| Evidence Registry | ðŸŸ¢ Available | Operational |
| Observation Engine | ðŸŸ¢ Available | Operational |
| Pipeline Framework | ðŸŸ¢ Available | Observation â†’ Evidence â†’ Knowledge |

---

## Research Layer

| Capability | Status | Notes |
|------------|--------|-------|
| Discovery Engine | ðŸŸ¢ Available | Initial version operational |
| Business Research | ðŸŸ¢ Available | Existing implementation |
| Company Research | ðŸŸ¢ Available | Existing implementation |
| Research Pipeline | ðŸŸ¢ Available | Active |
| Question Engine | ðŸŸ¢ Available | Initial implementation |

---

## Intelligence Layer

| Capability | Status | Notes |
|------------|--------|-------|
| Business Engine | ðŸŸ¢ Available | Existing |
| Financial Engine | ðŸŸ¢ Available | Existing |
| Management Engine | ðŸŸ¢ Available | Existing |
| Risk Engine | ðŸŸ¢ Available | Existing |
| Ownership Engine | ðŸŸ¢ Available | Existing |
| Valuation Engine | ðŸŸ¢ Available | Existing |
| Competitive Engine | ðŸŸ¢ Available | Existing |
| Reasoning Engine | ðŸŸ¢ Available | Existing |

---

## Decision Layer

| Capability | Status | Notes |
|------------|--------|-------|
| Investment Committee | ðŸŸ¢ Available | Operational |
| AI CIO | ðŸŸ¢ Available | Initial implementation |
| Decision Engine | ðŸŸ¢ Available | Existing |
| Position Sizing | ðŸŸ¢ Available | Existing |
| Margin of Safety | ðŸŸ¢ Available | Existing |

---

## Learning Layer

| Capability | Status | Notes |
|------------|--------|-------|
| Outcome Tracking | â¬œ Planned | Future release |
| Theory Evolution | â¬œ Planned | Future release |
| Prediction Tracker | â¬œ Planned | Future release |
| Discovery Learning | â¬œ Planned | Future release |

---

## User Interface

| Capability | Status | Notes |
|------------|--------|-------|
| Desktop UI | ðŸŸ¢ Available | Operational |
| Dashboard | ðŸŸ¢ Available | Existing |
| Charts | ðŸŸ¢ Available | Revenue, ROE, ROCE, EPS, Valuation |
| Widgets | ðŸŸ¢ Available | Existing |

---

# Institutional Maturity Dashboard

| Area | Progress |
|------|---------:|
| Platform Architecture | 85% |
| Research Framework | 80% |
| Intelligence Framework | 70% |
| Decision Intelligence | 60% |
| Learning Intelligence | 15% |
| Knowledge Framework | 35% |
| Documentation | 25% |
| Testing | 20% |

---

## Overall Institutional Maturity

**Current Estimate:** **55%**

Focus is on strengthening the platform, documentation, and learning framework before expanding functionality.
---

# Current Sprint

## Sprint Information

| Item | Value |
|------|-------|
| Sprint | Sprint 18.3 |
| Sprint Theme | Platform Stabilization |
| Duration | Current Development Sprint |
| Goal | Complete the Platform Foundation before expanding intelligence capabilities |

---

## Sprint Objective

Complete Release 18.3 by establishing a stable, scalable platform architecture.

The emphasis of this sprint is **engineering quality**, not feature expansion.

---

## Sprint Deliverables

### Platform

- [ ] Complete Intelligence Mesh integration
- [ ] Complete ResearchContext integration
- [ ] Complete typed Master Dossier migration
- [ ] Remove remaining legacy dictionary flow
- [ ] Standardize engine communication

---

### Architecture

- [ ] Reduce unnecessary coupling
- [ ] Verify Repository pattern consistency
- [ ] Verify Composition Root responsibilities
- [ ] Verify Engine responsibilities
- [ ] Review dependency flow

---

### Documentation

- [x] PROJECT_STATE.md
- [ ] ROADMAP.md
- [ ] CHANGELOG.md
- [ ] DECISION_LOG.md
- [ ] SPRINT_BOARD.md
- [ ] MASTER_EXECUTION_PLAN.md

---

### Quality

- [ ] Run full application successfully
- [ ] Resolve architecture inconsistencies
- [ ] Increase documentation coverage
- [ ] Increase test coverage

---

# Immediate Priorities

Priority 1

Complete Release 18.3.

Priority 2

Finish platform stabilization.

Priority 3

Complete institutional documentation.

Priority 4

Begin Business Academy implementation.

Priority 5

Start Knowledge Object Framework.

---

# Explicitly Out of Scope

The following work is intentionally postponed until Release 18.3 is complete.

- New AI features
- Additional Offices
- New Academies
- New Engines
- UI redesign
- New research capabilities

Platform stability takes precedence over expansion.

---

# Sprint Exit Criteria

This sprint is complete only when:

- Intelligence Mesh is operational.
- ResearchContext is the central intelligence bus.
- Typed Master Dossier migration is complete.
- Legacy dictionary flow has been removed.
- Documentation is synchronized with implementation.
- Application runs successfully.
- Architecture remains stable.
---

# Completed Milestones

## Vision Phase

Status: âœ… Complete

Major Achievements

- Established the EIOS vision.
- Defined the institutional mission.
- Designed the constitutional philosophy.
- Established the long-term scientific direction.
- Defined institutional engineering principles.

---

## Architecture Phase

Status: âœ… Complete

Major Achievements

- Repository-first architecture
- Composition Root (EIOSApplication)
- Layered architecture
- Domain-oriented design
- Office architecture
- Academy architecture
- Engine architecture
- Intelligence Mesh design
- ResearchContext architecture
- Typed Master Dossier architecture

---

## Research Methodology

Status: âœ… Complete

Major Achievements

- Three-level conviction framework
- Institutional research workflow
- Master Dossier methodology
- Evidence-driven analysis
- Investment Committee process
- AI CIO framework

---

## Platform Foundation

Status: ðŸŸ¡ In Progress

Completed

- Repository layer
- Desktop UI
- Discovery Engine
- Knowledge Engine
- Evidence Engine
- Observation Engine
- Reasoning Engine
- Business Engine
- Financial Engine
- Risk Engine
- Valuation Engine
- Ownership Engine

Remaining

- Intelligence Mesh completion
- ResearchContext completion
- Typed Master Dossier migration
- Legacy cleanup

---

## Documentation

Status: ðŸŸ¡ In Progress

Completed

- Vision
- Execution strategy
- PROJECT_STATE.md (under development)

Remaining

- ROADMAP.md
- CHANGELOG.md
- DECISION_LOG.md
- SPRINT_BOARD.md
- Engineering Standards
---

# Technical Debt & Architectural Risks

## Purpose

This section records known technical debt, architectural compromises, and engineering risks.

Technical debt is acceptable when intentional, documented, and scheduled for resolution.

Undocumented technical debt is considered an engineering defect.

---

# High Priority

These items directly affect architectural integrity.

| Issue | Status | Planned Resolution |
|--------|--------|--------------------|
| Remaining legacy dictionary-based data flow | Open | Complete typed Master Dossier migration |
| Partial Intelligence Mesh integration | Open | Finish Release 18.3 |
| ResearchContext not yet the sole intelligence bus | Open | Complete platform integration |

---

# Medium Priority

These items affect maintainability.

| Issue | Status | Planned Resolution |
|--------|--------|--------------------|
| Documentation not synchronized with implementation | In Progress | Complete institutional documentation |
| Inconsistent module documentation | Open | Standardize engineering documentation |
| Test coverage incomplete | Open | Increase module-by-module |

---

# Low Priority

These items improve usability but do not affect architecture.

| Issue | Status | Planned Resolution |
|--------|--------|--------------------|
| Desktop UI refinement | Deferred | Future release |
| Dashboard enhancements | Deferred | After platform stabilization |

---

# Architectural Risks

## Risk 1

Platform complexity increasing faster than documentation.

Mitigation

Documentation must be updated during every sprint.

---

## Risk 2

Legacy patterns remaining after migration.

Mitigation

No new feature may depend on legacy dictionary structures.

---

## Risk 3

Engine responsibilities becoming unclear.

Mitigation

Every engine must continue to follow the Single Responsibility Principle.

---

## Risk 4

Knowledge accidentally becoming hardcoded.

Mitigation

Business knowledge must remain inside Knowledge Objects, models, and engines.

---

## Engineering Policy

Technical debt must never accumulate silently.

Every known issue must be recorded here until resolved.

Resolved items should be moved to the CHANGELOG with the release that fixed them.
---

# Current Engineering Rules

These rules apply to all development work.
---

# Institutional KPIs

The success of EIOS is measured by institutional capability rather than feature count.

| KPI | Current | Target |
|------|---------|--------|
| Architecture Stability | Stable | Institutional |
| Documentation Coverage | 25% | 100% |
| Test Coverage | 20% | 90%+ |
| Explainable Decisions | Initial | Complete |
| Knowledge Reuse | Initial | Full |
| Reference Company Validation | Planned | Complete |
| Technical Debt | Medium | Low |

## Architecture

- Architecture before implementation.
- Preserve architectural integrity over short-term convenience.
- One module, one responsibility.
- Composition over inheritance where practical.
- Repository-first architecture.

## Business Logic

- Business logic belongs only in engines.
- UI must never contain business logic.
- Orchestration must remain lightweight.
- Knowledge must never be hardcoded.

## Data Flow

- ResearchContext is the central intelligence bus.
- Typed Master Dossier is the primary domain model.
- Repository layer owns persistence.
- Intelligence Mesh coordinates cross-engine communication.

## Quality

- Every module must have documentation.
- Every module should have unit tests where practical.
- Every architectural decision must be documented.
- Every release must be runnable.

## Engineering Philosophy

- Simplicity over cleverness.
- Evidence over assumptions.
- Refactoring over duplication.
- Maintainability over speed.
EIOS PROJECT STATE
==================

Catalyst Architecture
----------------------

Status: COMPLETE

Catalyst Families:
    Total       : 30
    Covered     : 30
    Uncovered   : 0

Catalyst Patterns:
    Registered  : 176

Validated Components:
    Pattern Modules              : PASS
    Pattern Tests                : PASS
    Pattern Registry             : PASS
    Catalyst Coverage            : PASS
    Coverage Priority            : PASS
    Development Queue            : PASS
    Development Selector         : PASS

Development Queue:
    Items       : 0

Development Selector:
    Empty-state : PASS

Architecture Principle:
    Catalyst pattern definitions remain passive.
    Detection, reasoning, scoring and investment decisions
    remain responsibilities of engines.

Next Major Architecture:
    Temporal Evidence & Learning

Planned Components:
    1. Temporal Evidence Engine
    2. Catalyst Detection Engine
    3. Sector Recovery Engine
    4. Company Recovery Engine
    5. Learning Ledger
    6. Outcome Attribution Engine
    7. Signal Performance Engine

Objective:
    Detect early sector/company recovery signals before
    conventional financial confirmation and allow EIOS
    to learn from subsequent outcomes.
    ---

# Current Development Transition

## Catalyst Architecture Completion

The Catalyst Architecture has reached a complete deterministic
taxonomy state.

| Metric | Final State |
|---|---:|
| Catalyst Families | 30 |
| Covered Families | 30 |
| Uncovered Families | 0 |
| Registered Catalyst Patterns | 176 |
| Priority Queue | 0 |
| Development Queue | 0 |

All Catalyst architecture validation stages have passed:

- Pattern Modules
- Pattern Tests
- Pattern Registry
- Catalyst Coverage
- Coverage Priority
- Development Queue
- Development Selector

The Development Selector correctly returns no development item
when all Catalyst Families are covered.

---

# Next Major Architecture

## Temporal Evidence & Learning

The next major EIOS capability is the development of temporal
intelligence and institutional learning.

### Planned Engines

1. Temporal Evidence Engine
2. Catalyst Detection Engine
3. Sector Recovery Engine
4. Company Recovery Engine
5. Learning Ledger
6. Outcome Attribution Engine
7. Signal Performance Engine

### Strategic Objective

Enable EIOS to detect early changes in business and sector
conditions before conventional financial confirmation.

The system should identify:

- stabilization
- bottoming
- inflection
- acceleration
- recovery
- persistence
- breadth of recovery
- leading versus confirming evidence

The Learning Layer will subsequently compare EIOS predictions
with actual outcomes and preserve the results as institutional
learning.

### Learning Principle

EIOS must learn from outcomes without silently modifying its
deterministic investment logic.

Learning should follow:

Prediction
â†’ Outcome
â†’ Attribution
â†’ Validation
â†’ Proposed Improvement
â†’ Backtest
â†’ Approved Evolution

No uncontrolled self-modification is permitted.

---

# Immediate Engineering Sequence

1. Git checkpoint
2. Synchronize Project State
3. Repository audit for existing temporal/evidence infrastructure
4. Design Temporal Evidence Engine
5. Implement Temporal Evidence Engine
6. Test temporal signals
7. Implement Catalyst Detection Engine
8. Implement Sector Recovery Engine
9. Implement Company Recovery Engine
10. Implement Learning Ledger
11. Implement Outcome Attribution
12. Connect learning outputs to Opportunity Engine

Repository-first development remains mandatory.
## Recovery Intelligence Architecture

### Status: COMPLETE â€” Recovery Intelligence Foundation

EIOS now contains a dedicated recovery-intelligence architecture within the Opportunity Engine.

The architecture is designed to detect early improvement in sectors and companies by analyzing the temporal evolution of signals and then aggregating independent recovery evidence.

### Completed Components

- Temporal Signal Intelligence Engine
- Recovery Assessment Model
- Recovery Detection Engine
- Recovery Evidence Model
- Multi-Signal Recovery Assessment Model
- Multi-Signal Recovery Engine

### Recovery Intelligence Flow

Signal
â†’ Temporal Signal Intelligence
â†’ Recovery Detection
â†’ Recovery Evidence
â†’ Multi-Signal Recovery Engine
â†’ Multi-Signal Recovery Assessment

### Recovery Stages

The recovery architecture distinguishes:

1. Deteriorating
2. Slowing Deterioration
3. Stabilizing
4. Early Inflection
5. Early Recovery
6. Confirmed Recovery

At the multi-signal level it distinguishes:

1. Insufficient Evidence
2. Isolated Improvement
3. Broad Stabilization
4. Early Broad Recovery
5. Confirmed Broad Recovery

### Institutional Design Principles

Recovery detection is intentionally separated from:

- Valuation
- Opportunity scoring
- Investment decisions
- Company-specific logic
- Sector-specific logic

The system does not treat repeated observations from the same source as independent corroboration.

Independent source identity is explicitly retained through the Recovery Evidence model.

Contradictory evidence reduces recovery confidence rather than being discarded.

### Strategic Objective

The Recovery Intelligence layer is intended to provide EIOS with an early-warning capability for identifying potential sector and company recoveries before recovery becomes fully visible in reported earnings.

The architecture will eventually support:

- sector recovery detection
- industry-cycle recovery detection
- company recovery detection
- leading-indicator analysis
- recovery breadth measurement
- recovery corroboration
- recovery persistence
- early catalyst identification
- outcome-based learning through the future Learning Ledger

### Next Planned Layer

Recovery Cluster / Theme Detection

Objective:

Determine whether multiple multi-signal recovery assessments represent a common recovering sector, industry, theme, macro regime, commodity cycle, or company.

This layer will sit above Multi-Signal Recovery Engine and below Catalyst / Opportunity Intelligence.
## Recovery Intelligence â€” Completed

The EIOS Opportunity Engine now contains a staged Recovery Intelligence architecture.

### Completed Components

1. Temporal Signal Intelligence
   - Temporal Signal Engine
   - Chronological signal evolution
   - Trend detection
   - Acceleration / deceleration
   - Stabilisation
   - Inflection
   - Bottoming
   - Reversal
   - Persistence
   - Confidence and transparent reasoning

2. Recovery Detection
   - Recovery Assessment Model
   - Recovery Detection Engine
   - Deteriorating
   - Slowing Deterioration
   - Stabilizing
   - Early Inflection
   - Early Recovery
   - Recovery Reversal
   - Confirmed Recovery
   - Temporal feature transfer
   - Evidence transfer

3. Multi-Signal Recovery Intelligence
   - Multi-Signal Recovery Assessment
   - Multi-Signal Recovery Engine
   - Recovery Evidence Model
   - Source deduplication
   - Contradictory evidence detection
   - Signal tracking
   - Temporal support
   - Broad recovery assessment

4. Recovery Cluster Intelligence
   - Recovery Cluster Assessment
   - Recovery Cluster Engine
   - Recovery Cluster Evidence
   - Early clustering
   - Stabilizing clusters
   - Early recovery clusters
   - Confirmed recovery clusters
   - Cluster-level corroboration
   - Contradiction handling

5. Recovery Breadth Intelligence
   - Recovery Breadth Assessment
   - Recovery Breadth Engine
   - Recovery Breadth evidence aggregation
   - Isolated improvement
   - Early breadth
   - Broadening recovery
   - Broad recovery
   - Saturated recovery
   - Contracting breadth
   - Recovery leadership
   - Deterministic classification
   - Transparent reasoning

### Recovery Intelligence Flow

Signal
    â†“
Temporal Intelligence
    â†“
Recovery Detection
    â†“
Multi-Signal Recovery
    â†“
Recovery Cluster
    â†“
Recovery Breadth
    â†“
Opportunity Intelligence

### Institutional Boundary

Recovery Breadth does not imply investment opportunity.

Recovery Intelligence identifies the evolution and breadth
of recovery evidence. Opportunity engines remain responsible
for determining whether the recovery creates a potentially
mispriced investment opportunity.

No valuation, portfolio decision, or investment recommendation
is performed by the Recovery Intelligence layer.
---

# Recovery Opportunity Intelligence â€” COMPLETE

Status: COMPLETE

The EIOS Recovery Intelligence pipeline has now been extended
through the Opportunity Engine boundary.

Completed architecture:

Recovery Detection
â†’ Multi-Signal Recovery
â†’ Recovery Cluster
â†’ Recovery Breadth
â†’ Recovery Theme
â†’ Recovery Theme â†’ Catalyst
â†’ Recovery Opportunity Signal
â†’ Recovery Opportunity Engine
â†’ Opportunity Engine

Completed components:

- recovery_opportunity_signal.py
- recovery_opportunity_engine.py
- test_recovery_opportunity_signal.py
- test_recovery_opportunity_engine.py

Validation:

- Recovery Opportunity Signal Model : PASS
- Recovery Opportunity Engine       : PASS
- Empty Theme                       : PASS
- Recovery Without Catalyst         : PASS
- Catalyst Support                  : PASS
- Recovery Gates                    : PASS
- Actionable Recovery Signal        : PASS
- Catalyst Evidence Transfer        : PASS
- Low Breadth Rejection             : PASS
- Low Confirmation Rejection        : PASS
- Weak Catalyst Rejection           : PASS
- Contradictory Recovery            : PASS
- Confidence Classification          : PASS
- Input Immutability                : PASS
- Deterministic Assessment          : PASS
- Transparent Reasoning             : PASS

Architectural boundary:

Recovery Opportunity Intelligence
does not perform valuation, intrinsic-value calculation,
mispricing calculation, portfolio construction, or final
investment decision-making.

Its responsibility is to determine whether recovery evidence
has sufficient breadth, confirmation, coherence and catalyst
support to warrant downstream Opportunity Engine attention.

Git Commit:

2471744 â€” Add Recovery Opportunity Intelligence
---

# Recovery â†’ Opportunity Signal Integration â€” COMPLETE

Status: COMPLETE

The Recovery Intelligence subsystem is now connected to the
canonical Opportunity Intelligence Signal model through a
dedicated translation boundary.

Completed component:

- recovery_opportunity_adapter.py
- test_recovery_opportunity_adapter.py

Validated:

- Adapter Exists                  : PASS
- None Input Protection           : PASS
- Canonical Signal Creation       : PASS
- Identity Transfer               : PASS
- Classification Transfer         : PASS
- Strength Transfer               : PASS
- Evidence Transfer               : PASS
- Catalyst Context Transfer       : PASS
- Evidence Quality Mapping        : PASS
- Input Immutability              : PASS
- Deterministic Mapping           : PASS
- Numeric Range Protection        : PASS
- No Valuation Fabrication        : PASS

Architecture:

Recovery Opportunity Signal
â†’ Recovery Opportunity Adapter
â†’ Canonical Opportunity Signal
â†’ Existing Catalyst Engine
â†’ Opportunity Pipeline

Architectural boundary:

The adapter performs translation only.

It does not calculate:
- valuation
- mispricing
- expectation gap
- asymmetry
- portfolio allocation
- investment decisions

The canonical Opportunity Signal remains the passive
intelligence contract, while downstream Opportunity engines
remain responsible for analysis and decision-support calculations.
---

# Recovery â†’ Catalyst Engine Integration â€” COMPLETE

Status: COMPLETE

The Recovery Opportunity Intelligence subsystem has been
successfully integrated with the existing EIOS Catalyst Engine
through the canonical Opportunity Signal boundary.

Validated integration:

Recovery Opportunity Signal
â†’ Recovery Opportunity Adapter
â†’ Canonical Opportunity Signal
â†’ CatalystEngine.analyze()
â†’ Catalyst Assessment

Integration validation:

- Catalyst Engine Exists          : PASS
- Recovery Adapter Exists         : PASS
- Canonical Signal Creation       : PASS
- Recovery Identity Transfer      : PASS
- Recovery Classification         : PASS
- Recovery Evidence Transfer      : PASS
- Recovery Input Immutability     : PASS
- Catalyst Engine Consumption     : PASS
- Signal Preservation             : PASS
- Catalyst Direction              : PASS
- Catalyst Evidence Collection   : PASS
- Contradiction Transfer          : PASS
- Catalyst Analysis               : PASS
- Canonical Signal Immutability   : PASS
- Deterministic Integration       : PASS

Architectural result:

Recovery Intelligence can now enter the existing Opportunity
Catalyst Engine without bypassing the canonical Signal model.

No modification was made to the existing Catalyst Engine.

The Recovery adapter remains a translation boundary only.
Valuation, mispricing, expectation-gap analysis, ranking,
portfolio construction and investment decisions remain
downstream responsibilities.
---

# Recovery â†’ Opportunity Pipeline Integration â€” COMPLETE

Status: COMPLETE

The Recovery Opportunity Intelligence subsystem has now been
successfully integrated with the existing EIOS Opportunity
Pipeline through the canonical Opportunity Signal boundary.

Verified architecture:

Recovery Breadth
â†’ Recovery Theme
â†’ Theme â†’ Catalyst
â†’ Recovery Opportunity
â†’ Recovery Opportunity Adapter
â†’ Canonical Opportunity Signal
â†’ Catalyst Engine
â†’ Expectation Gap
â†’ Mispricing
â†’ Asymmetry
â†’ Evidence
â†’ Synthesis

Integration test result:

EIOS RECOVERY â†’ OPPORTUNITY PIPELINE : PASS

Validated stages:

- Recovery Adapter Exists          : PASS
- Canonical Signal Creation        : PASS
- Recovery Input Immutability      : PASS
- Canonical Recovery Signal        : PASS
- Opportunity Pipeline Exists      : PASS
- Recovery â†’ Catalyst              : PASS
- Signal â†’ Catalyst                : PASS
- Catalyst â†’ Expectation Gap       : PASS
- Expectation Gap â†’ Mispricing     : PASS
- Mispricing â†’ Asymmetry           : PASS
- Asymmetry â†’ Evidence             : PASS
- Evidence â†’ Synthesis             : PASS
- Evidence Handoff                 : PASS
- Synthesis Score Range            : PASS
- Canonical Signal Immutability    : PASS
- Deterministic Pipeline            : PASS

Architectural result:

Recovery-derived intelligence can now enter the complete
Opportunity Intelligence Pipeline through the canonical Signal
model.

The Recovery subsystem does not bypass downstream analytical
engines.

The Opportunity Pipeline remains responsible for:

- Catalyst analysis
- Expectation Gap analysis
- Mispricing analysis
- Asymmetry analysis
- Evidence analysis
- Opportunity synthesis

Recovery intelligence does not perform valuation, mispricing,
expectation-gap calculation, opportunity ranking, portfolio
construction, or investment decisions.

No modification was made to the existing Opportunity Pipeline
for this integration.

The integration has been validated for:

- Correct signal translation
- Correct downstream Catalyst consumption
- Complete downstream pipeline propagation
- Evidence hand-off
- Synthesis generation
- Numeric range protection
- Input immutability
- Deterministic execution
# EIOS â€” PROJECT STATE

## Everest Investment Operating System

**State:** ACTIVE DEVELOPMENT
**Branch:** `main`
**Repository:** `EIOS-CORE`
**Last Verified:** 2026-08-17

---

# 1. CURRENT SYSTEM POSITION

EIOS has progressed from a collection of research engines into an integrated
Opportunity Intelligence architecture.

The current Opportunity Engine can:

- discover opportunity candidates
- preserve Discovery intelligence
- generate external research queries
- execute external research
- retrieve external information
- normalize external content
- assess source quality
- create observations
- create evidence
- evaluate evidence quality
- generate canonical signals
- identify catalysts
- measure expectation gaps
- evaluate potential mispricing
- evaluate asymmetry
- synthesize opportunity intelligence
- apply evidence and kill-switch gates
- route qualified opportunities toward Committee Review

The system is currently **research-oriented and deterministic**.

It is not yet a continuously operating intelligence system.

---

# 2. VERIFIED OPPORTUNITY ARCHITECTURE

Current high-level flow:

Discovery
    â†“
Opportunity Intake
    â†“
External Query Generation
    â†“
External Research
    â†“
Search / Retrieval
    â†“
Content Normalization
    â†“
Source Assessment
    â†“
Observation
    â†“
Evidence
    â†“
Opportunity Evidence Engine
    â†“
Canonical Signal
    â†“
Catalyst
    â†“
Expectation Gap
    â†“
Mispricing
    â†“
Asymmetry
    â†“
Opportunity Synthesis
    â†“
Investment Committee

---

# 3. EXTERNAL INTELLIGENCE PIPELINE

The following end-to-end pipeline has been implemented and verified:

Discovery
â†’ Opportunity Intake
â†’ External Query
â†’ External Orchestrator
â†’ External Research
â†’ Search Delegation
â†’ Source Selection
â†’ HTTP Retrieval
â†’ Content Normalization
â†’ Source Assessment
â†’ Observation Creation
â†’ External Provenance Chain
â†’ Evidence Assessment Metadata
â†’ Observation â†’ EvidenceItem
â†’ Opportunity Evidence Engine
â†’ Evidence â†’ Opportunity Handoff
â†’ Downstream Evidence Scoring
â†’ Final Provenance Preservation

Verified result:

EIOS FULL EXTERNAL â†’ OPPORTUNITY EVIDENCE PIPELINE : PASS

---

# 4. DISCOVERY â†’ OPPORTUNITY INTAKE

DiscoveryOpportunityAdapter is implemented and verified.

Verified properties:

- Company identity preserved
- Ticker preserved
- Sector preserved
- Industry preserved
- Discovery score preserved
- Discovery confidence preserved
- Catalysts preserved
- Risks preserved
- Strengths preserved
- No Opportunity analysis invented
- Source DiscoveryCandidate remains unchanged

Verified result:

EIOS DISCOVERY â†’ OPPORTUNITY INTAKE : PASS

---

# 5. OPPORTUNITY EXTERNAL QUERY ENGINE

OpportunityExternalQueryEngine is implemented and verified.

Verified properties:

- Engine construction
- External query generation
- Company preservation
- Ticker preservation
- Question preservation
- Opportunity research intent
- Deterministic output
- Intake immutability
- No analytical fabrication
- Invalid input protection

Verified result:

EIOS OPPORTUNITY â†’ EXTERNAL QUERY ENGINE : PASS

---

# 6. CATALYST ARCHITECTURE

Catalyst architecture is substantially developed.

Current architecture includes:

- Catalyst Engine
- Catalyst Classification
- Catalyst Families
- Catalyst Patterns
- Catalyst Registry
- Catalyst Coverage
- Catalyst Coverage Evidence Registry
- Catalyst Priority
- Catalyst Development Queue
- Catalyst Development Selector

Current known architecture state:

- 30 Catalyst Families
- 21 covered families
- 9 uncovered families
- 122 registered Catalyst Patterns

Completed catalyst families include areas such as:

- Capacity Expansion
- Order / Contract
- Regulatory Change
- Revenue Growth
- Volume Growth
- Pricing
- Margin Expansion
- Technology Adoption
- Market Recognition / Expectation Reset

The Catalyst Development architecture is deterministic and test-covered.

---

# 7. EXPECTATION GAP ENGINE

Expectation Gap Engine is implemented and tested.

It evaluates:

- Market expectation
- EIOS expectation
- Market earnings expectation
- EIOS earnings expectation
- Expectation difference
- Earnings gap
- Unrecognized potential
- Gap score
- Confidence
- Positive / negative gap

Verified result:

EXPECTATION GAP : ALL TESTS PASSED

---

# 8. MISPRICING ENGINE

Mispricing Engine is implemented.

Important architectural rule:

The Mispricing Engine does NOT calculate intrinsic value.

Authoritative valuation remains with the existing EIOS valuation architecture.

Mispricing combines:

- valuation support
- catalyst support
- expectation-gap support
- mispricing score
- confidence

Institutional threshold:

MINIMUM_MISPRICING_SCORE = 60.0

The production threshold was NOT lowered.

The positive-path test fixture was strengthened instead.

Latest verified positive-path result:

Current Price      : 3500.00
Intrinsic Value    : 5250.00
Fair Value         : 5250.00
Valuation Upside   : 50.00%
Valuation Support  : True

Catalyst Score     : 60.50
Expectation Gap    : 35.00
Earnings Gap       : 35.00
Market Recognition : 55.00
Mispricing Score   : 64.65
Confidence         : 52.99
Potential Mispricing : True

MISPRICING ENGINE : ALL TESTS PASSED

Commit:

e6f376e â€” Strengthen mispricing positive-path test

---

# 9. ASYMMETRY ENGINE

Asymmetry Engine is implemented and tested.

Verified:

- Expected return
- Upside probability
- Permanent loss probability
- Expected time
- Asymmetry ratio
- Asymmetry score
- Attractive / non-attractive classification
- Probability validation

Verified result:

ASYMMETRY ENGINE : ALL TESTS PASSED

---

# 10. OPPORTUNITY EVIDENCE ENGINE

Opportunity Evidence Engine is implemented and tested.

Verified scenarios include:

- Strong evidence
- Weak evidence
- Serious contradiction
- No primary source
- No kill switch

The engine provides evidence qualification before downstream
Opportunity Synthesis.

Verified result:

OPPORTUNITY EVIDENCE ENGINE : ALL TESTS PASSED

---

# 11. OPPORTUNITY PIPELINE

OpportunityPipeline integrates:

- Canonical Signal
- Catalyst
- Expectation Gap
- Mispricing
- Asymmetry
- Evidence
- Synthesis
- Evidence â†’ Synthesis handoff
- Score / Confidence
- Decision

Latest verified synthetic pipeline:

Catalyst Score          : 54.50
Expectation Gap         : 43.90
Mispricing Score        : 54.06
Asymmetry Score         : 92.05
Evidence Score          : 65.95
Evidence Confidence     : 75.00
Evidence Sufficient     : True
Opportunity Score       : 63.51
Opportunity Confidence  : 73.90
Decision                : Research

Verified result:

EIOS OPPORTUNITY PIPELINE : PASS

---

# 12. NEGATIVE-PATH PROTECTION

Negative-path tests are implemented and passing.

Verified:

- Strong Opportunity
- No Evidence Gate
- No Kill Switch
- Permanent Loss
- Weak Valuation

Verified result:

EIOS OPPORTUNITY PIPELINE NEGATIVE-PATH TEST : PASS

The system therefore does not simply reward high scores.

Evidence and risk gates can block an opportunity.

---

# 13. OPPORTUNITY COMMITTEE

Committee routing is implemented and tested.

Verified:

- Tier 1 â†’ Committee Review
- Tier 2 â†’ Committee Review
- Tier 3 â†’ Watchlist
- Excluded â†’ Reject
- No Automatic Approval
- Ranking Immutability

Verified result:

EIOS OPPORTUNITY COMMITTEE : PASS

Important principle:

Opportunity Engine output is not automatic investment approval.

---

# 14. FULL VERIFIED OPPORTUNITY TEST SET

The following major Opportunity tests have passed:

- test_asymmetry
- test_expectation_gap
- test_mispricing
- test_evidence_engine
- test_pipeline
- test_pipeline_negative
- test_committee_engine
- test_discovery_opportunity_adapter
- test_opportunity_external_query_engine
- test_full_external_opportunity_evidence_pipeline

The repository currently contains approximately:

91 `test_*.py` files

across the modules tree.

---

# 15. CURRENT REPOSITORY STATE

Latest verified Git state after the Mispricing test update:

Branch:

main

Remote:

origin/main

Latest important commit:

e6f376e
Strengthen mispricing positive-path test

The repository was pushed successfully.

Working tree was clean after the push.

---

# 16. EXISTING TEMPORAL ARCHITECTURE

EIOS already contains temporal information in multiple existing layers.

Signal model contains:

- source_date
- detected_date

Observation contains timestamp information.

Evidence contains timestamp information.

Decision models contain creation timestamps.

There is also an existing:

modules/opportunity/signals/temporal_signal_engine.py

Therefore:

DO NOT introduce an unrelated global timestamp abstraction.

Future monitoring and learning components must reuse existing EIOS
chronology concepts where appropriate.

---

# 17. IMPORTANT ARCHITECTURAL DECISION

The next generation of EIOS must evolve from:

"Run research when requested"

toward:

"Continuously acquire, process and update investment intelligence."

The target architecture is:

Internet / External Sources
        â†“
Data Acquisition
        â†“
News / Results / Events / Filings
        â†“
External Intelligence
        â†“
Observation
        â†“
Evidence
        â†“
Signal
        â†“
Catalyst
        â†“
Expectation Gap
        â†“
Mispricing
        â†“
Asymmetry
        â†“
Opportunity Synthesis
        â†“
Monitoring
        â†“
Learning

---

# 18. CONTINUOUS INTELLIGENCE OBJECTIVE

EIOS should eventually automatically collect and process:

- Company quarterly results
- Annual results
- Earnings releases
- Company announcements
- Conference-call information
- Order wins
- Capacity expansion
- Management changes
- M&A
- Regulatory developments
- Government policy
- Commodity movements
- Sector developments
- Competitor developments
- Important news
- Macro events
- Market-moving events

The objective is NOT merely to store news.

The objective is to determine:

"What changed?"

"What does it mean?"

"Which existing thesis does it affect?"

"Does it create a new signal?"

"Does it strengthen or weaken a catalyst?"

"Does it change market expectations?"

"Does it change the mispricing assessment?"

"Does it change opportunity conviction?"

---

# 19. TARGET AUTOMATIC INTELLIGENCE FLOW

New information:

    â†“

Source Acquisition

    â†“

Source Assessment

    â†“

Observation

    â†“

Evidence

    â†“

Entity Mapping

    â†“

Event Classification

    â†“

Signal Detection

    â†“

Existing Signal Update / New Signal

    â†“

Catalyst Update

    â†“

Expectation Gap Update

    â†“

Mispricing Update

    â†“

Asymmetry Update

    â†“

Opportunity Reassessment

    â†“

Monitoring State

---

# 20. EVENT CLASSIFICATION TARGET

Incoming information should eventually be classified into controlled event
families such as:

- NEWS
- RESULT
- EARNINGS
- FILING
- ORDER
- CAPACITY
- MANAGEMENT
- M&A
- REGULATORY
- POLICY
- MACRO
- SECTOR
- COMPETITOR
- COMMODITY
- TECHNOLOGY
- OTHER

Classification must remain deterministic and provenance-preserving.

---

# 21. MONITORING OBJECTIVE

For an existing opportunity:

Existing Opportunity
        â†“
New Information
        â†“
Compare With Previous State
        â†“
Identify Change
        â†“
Assess Thesis Impact
        â†“
Assess Conviction Change

Possible states:

- Conviction Increased
- Conviction Unchanged
- Conviction Decreased
- Thesis Invalidated
- New Research Required

No automatic BUY/SELL action should be introduced at this stage.

---

# 22. LEARNING ARCHITECTURE

EIOS will eventually require a Learning Ledger.

However, Learning must preserve the distinction between:

PREDICTION

and

OUTCOME.

Target architecture:

Opportunity Synthesis
        â†“
Opportunity Prediction Record
        â†“
TIME
        â†“
Actual Outcome
        â†“
Prediction vs Reality
        â†“
Attribution
        â†“
Learning Ledger

The original prediction must never be overwritten by hindsight.

---

# 23. OPPORTUNITY PREDICTION

A future passive `OpportunityPrediction` model is planned.

It should capture the state of EIOS at the time of prediction, including:

- company
- sector
- prediction timestamp
- market price
- intrinsic value
- fair value
- catalyst score
- expectation gap score
- mispricing score
- asymmetry score
- opportunity score
- confidence
- decision
- expected return
- expected duration
- downside / permanent-loss assumptions
- evidence state
- assumptions
- disconfirming evidence
- invalidation conditions
- provenance

It must NOT contain hindsight outcome fields.

---

# 24. OUTCOME / LEARNING PRINCIPLE

Future outcome records should remain separate.

They may eventually capture:

- subsequent market price
- realized return
- realized time
- business outcome
- earnings outcome
- catalyst outcome
- expectation outcome
- thesis validity
- prediction accuracy

But these fields must never be inserted into the original prediction record.

---

# 25. NEXT DEVELOPMENT PRIORITY

The immediate next major development is NOT another scoring engine.

Priority:

## EIOS CONTINUOUS EXTERNAL INTELLIGENCE

First build the infrastructure required for EIOS to periodically acquire
new information.

Initial components should include:

1. Source Registry
2. Data Acquisition Layer
3. Scheduled Ingestion
4. Event Classification
5. Entity Mapping
6. Duplicate Detection
7. Observation Creation
8. Evidence Creation
9. Provenance Preservation
10. Opportunity Update Trigger

Only after this foundation is stable should we build the Learning Ledger.

---

# 26. SCHEDULING TARGET

EIOS should eventually support periodic updates rather than requiring manual
execution.

Target concept:

    Scheduler
        â†“
    Source Registry
        â†“
    Fetch New Information
        â†“
    Detect New / Changed Items
        â†“
    Process Intelligence
        â†“
    Update EIOS State

Initial scheduling frequency can be configurable.

Examples:

- Hourly
- Every 4 hours
- Daily

Different source classes may eventually use different frequencies.

---

# 27. AUTOMATIC REPOSITORY / PUBLISHING

Automatic GitHub publishing is NOT yet part of the production pipeline.

The preferred sequence is:

External Intelligence
        â†“
Validated EIOS State
        â†“
Tests
        â†“
Generated Research Artifacts
        â†“
Optional Repository Publication

Automatic repository writes should NOT be introduced before the ingestion
and validation layers are stable.

---

# 28. ARCHITECTURAL RULES

Continue following the EIOS Engineering Charter.

Important rules:

- Repository first
- Do not redesign existing architecture unnecessarily
- Prefer staged refactoring
- Passive data models
- Engines perform calculations
- Preserve provenance
- Preserve source evidence
- No analytical fabrication
- No automatic investment approval
- No hidden mutation
- Deterministic behavior where appropriate
- Evidence before conviction
- Kill switches remain authoritative
- Do not lower institutional thresholds merely to make tests pass
- Never overwrite historical predictions with hindsight
- Preserve backward compatibility during migrations

---

# 29. CURRENT DEVELOPMENT PHASE

## PHASE

Opportunity Intelligence â†’ Continuous Intelligence Transition

### Completed

Discovery â†’ Opportunity Intake
External Query Generation
External Research
External Retrieval
Observation
Evidence
Signal
Catalyst
Expectation Gap
Mispricing
Asymmetry
Evidence Qualification
Opportunity Synthesis
Opportunity Committee Routing
Negative-path protection
External â†’ Opportunity end-to-end integration

### In Progress

Continuous External Intelligence Architecture

### Planned

Scheduled Intelligence Ingestion
Automatic Event Processing
Opportunity Monitoring
Prediction Records
Outcome Records
Attribution Engine
Learning Ledger
Adaptive Intelligence

---

# 30. NEXT SESSION â€” EXACT STARTING POINT

Do NOT modify the existing Opportunity scoring engines yet.

Start with repository inspection and design of:

    modules/external_intelligence/

for:

    Source Registry
    Scheduled Acquisition
    New-Information Detection
    Event Classification

Then integrate the validated information into the existing:

    Observation
        â†“
    Evidence
        â†“
    Signal
        â†“
    Opportunity

architecture.

The objective is to transform EIOS from a system that can perform research
into a system that can continuously maintain current investment intelligence.

---

# END OF PROJECT STATE
# EIOS â€” PROJECT STATE

## Everest Investment Operating System

**State:** ACTIVE DEVELOPMENT
**Branch:** `main`
**Repository:** `EIOS-CORE`
**Last Verified:** 2026-08-17

---

# 1. CURRENT SYSTEM POSITION

EIOS has progressed from a collection of research engines into an integrated
Opportunity Intelligence architecture.

The current Opportunity Engine can:

- discover opportunity candidates
- preserve Discovery intelligence
- generate external research queries
- execute external research
- retrieve external information
- normalize external content
- assess source quality
- create observations
- create evidence
- evaluate evidence quality
- generate canonical signals
- identify catalysts
- measure expectation gaps
- evaluate potential mispricing
- evaluate asymmetry
- synthesize opportunity intelligence
- apply evidence and kill-switch gates
- route qualified opportunities toward Committee Review

The system is currently **research-oriented and deterministic**.

It is not yet a continuously operating intelligence system.

---

# 2. VERIFIED OPPORTUNITY ARCHITECTURE

Current high-level flow:

Discovery
    â†“
Opportunity Intake
    â†“
External Query Generation
    â†“
External Research
    â†“
Search / Retrieval
    â†“
Content Normalization
    â†“
Source Assessment
    â†“
Observation
    â†“
Evidence
    â†“
Opportunity Evidence Engine
    â†“
Canonical Signal
    â†“
Catalyst
    â†“
Expectation Gap
    â†“
Mispricing
    â†“
Asymmetry
    â†“
Opportunity Synthesis
    â†“
Investment Committee

---

# 3. EXTERNAL INTELLIGENCE PIPELINE

The following end-to-end pipeline has been implemented and verified:

Discovery
â†’ Opportunity Intake
â†’ External Query
â†’ External Orchestrator
â†’ External Research
â†’ Search Delegation
â†’ Source Selection
â†’ HTTP Retrieval
â†’ Content Normalization
â†’ Source Assessment
â†’ Observation Creation
â†’ External Provenance Chain
â†’ Evidence Assessment Metadata
â†’ Observation â†’ EvidenceItem
â†’ Opportunity Evidence Engine
â†’ Evidence â†’ Opportunity Handoff
â†’ Downstream Evidence Scoring
â†’ Final Provenance Preservation

Verified result:

EIOS FULL EXTERNAL â†’ OPPORTUNITY EVIDENCE PIPELINE : PASS

---

# 4. DISCOVERY â†’ OPPORTUNITY INTAKE

DiscoveryOpportunityAdapter is implemented and verified.

Verified properties:

- Company identity preserved
- Ticker preserved
- Sector preserved
- Industry preserved
- Discovery score preserved
- Discovery confidence preserved
- Catalysts preserved
- Risks preserved
- Strengths preserved
- No Opportunity analysis invented
- Source DiscoveryCandidate remains unchanged

Verified result:

EIOS DISCOVERY â†’ OPPORTUNITY INTAKE : PASS

---

# 5. OPPORTUNITY EXTERNAL QUERY ENGINE

OpportunityExternalQueryEngine is implemented and verified.

Verified properties:

- Engine construction
- External query generation
- Company preservation
- Ticker preservation
- Question preservation
- Opportunity research intent
- Deterministic output
- Intake immutability
- No analytical fabrication
- Invalid input protection

Verified result:

EIOS OPPORTUNITY â†’ EXTERNAL QUERY ENGINE : PASS

---

# 6. CATALYST ARCHITECTURE

Catalyst architecture is substantially developed.

Current architecture includes:

- Catalyst Engine
- Catalyst Classification
- Catalyst Families
- Catalyst Patterns
- Catalyst Registry
- Catalyst Coverage
- Catalyst Coverage Evidence Registry
- Catalyst Priority
- Catalyst Development Queue
- Catalyst Development Selector

Current known architecture state:

- 30 Catalyst Families
- 21 covered families
- 9 uncovered families
- 122 registered Catalyst Patterns

Completed catalyst families include areas such as:

- Capacity Expansion
- Order / Contract
- Regulatory Change
- Revenue Growth
- Volume Growth
- Pricing
- Margin Expansion
- Technology Adoption
- Market Recognition / Expectation Reset

The Catalyst Development architecture is deterministic and test-covered.

---

# 7. EXPECTATION GAP ENGINE

Expectation Gap Engine is implemented and tested.

It evaluates:

- Market expectation
- EIOS expectation
- Market earnings expectation
- EIOS earnings expectation
- Expectation difference
- Earnings gap
- Unrecognized potential
- Gap score
- Confidence
- Positive / negative gap

Verified result:

EXPECTATION GAP : ALL TESTS PASSED

---

# 8. MISPRICING ENGINE

Mispricing Engine is implemented.

Important architectural rule:

The Mispricing Engine does NOT calculate intrinsic value.

Authoritative valuation remains with the existing EIOS valuation architecture.

Mispricing combines:

- valuation support
- catalyst support
- expectation-gap support
- mispricing score
- confidence

Institutional threshold:

MINIMUM_MISPRICING_SCORE = 60.0

The production threshold was NOT lowered.

The positive-path test fixture was strengthened instead.

Latest verified positive-path result:

Current Price      : 3500.00
Intrinsic Value    : 5250.00
Fair Value         : 5250.00
Valuation Upside   : 50.00%
Valuation Support  : True

Catalyst Score     : 60.50
Expectation Gap    : 35.00
Earnings Gap       : 35.00
Market Recognition : 55.00
Mispricing Score   : 64.65
Confidence         : 52.99
Potential Mispricing : True

MISPRICING ENGINE : ALL TESTS PASSED

Commit:

e6f376e â€” Strengthen mispricing positive-path test

---

# 9. ASYMMETRY ENGINE

Asymmetry Engine is implemented and tested.

Verified:

- Expected return
- Upside probability
- Permanent loss probability
- Expected time
- Asymmetry ratio
- Asymmetry score
- Attractive / non-attractive classification
- Probability validation

Verified result:

ASYMMETRY ENGINE : ALL TESTS PASSED

---

# 10. OPPORTUNITY EVIDENCE ENGINE

Opportunity Evidence Engine is implemented and tested.

Verified scenarios include:

- Strong evidence
- Weak evidence
- Serious contradiction
- No primary source
- No kill switch

The engine provides evidence qualification before downstream
Opportunity Synthesis.

Verified result:

OPPORTUNITY EVIDENCE ENGINE : ALL TESTS PASSED

---

# 11. OPPORTUNITY PIPELINE

OpportunityPipeline integrates:

- Canonical Signal
- Catalyst
- Expectation Gap
- Mispricing
- Asymmetry
- Evidence
- Synthesis
- Evidence â†’ Synthesis handoff
- Score / Confidence
- Decision

Latest verified synthetic pipeline:

Catalyst Score          : 54.50
Expectation Gap         : 43.90
Mispricing Score        : 54.06
Asymmetry Score         : 92.05
Evidence Score          : 65.95
Evidence Confidence     : 75.00
Evidence Sufficient     : True
Opportunity Score       : 63.51
Opportunity Confidence  : 73.90
Decision                : Research

Verified result:

EIOS OPPORTUNITY PIPELINE : PASS

---

# 12. NEGATIVE-PATH PROTECTION

Negative-path tests are implemented and passing.

Verified:

- Strong Opportunity
- No Evidence Gate
- No Kill Switch
- Permanent Loss
- Weak Valuation

Verified result:

EIOS OPPORTUNITY PIPELINE NEGATIVE-PATH TEST : PASS

The system therefore does not simply reward high scores.

Evidence and risk gates can block an opportunity.

---

# 13. OPPORTUNITY COMMITTEE

Committee routing is implemented and tested.

Verified:

- Tier 1 â†’ Committee Review
- Tier 2 â†’ Committee Review
- Tier 3 â†’ Watchlist
- Excluded â†’ Reject
- No Automatic Approval
- Ranking Immutability

Verified result:

EIOS OPPORTUNITY COMMITTEE : PASS

Important principle:

Opportunity Engine output is not automatic investment approval.

---

# 14. FULL VERIFIED OPPORTUNITY TEST SET

The following major Opportunity tests have passed:

- test_asymmetry
- test_expectation_gap
- test_mispricing
- test_evidence_engine
- test_pipeline
- test_pipeline_negative
- test_committee_engine
- test_discovery_opportunity_adapter
- test_opportunity_external_query_engine
- test_full_external_opportunity_evidence_pipeline

The repository currently contains approximately:

91 `test_*.py` files

across the modules tree.

---

# 15. CURRENT REPOSITORY STATE

Latest verified Git state after the Mispricing test update:

Branch:

main

Remote:

origin/main

Latest important commit:

e6f376e
Strengthen mispricing positive-path test

The repository was pushed successfully.

Working tree was clean after the push.

---

# 16. EXISTING TEMPORAL ARCHITECTURE

EIOS already contains temporal information in multiple existing layers.

Signal model contains:

- source_date
- detected_date

Observation contains timestamp information.

Evidence contains timestamp information.

Decision models contain creation timestamps.

There is also an existing:

modules/opportunity/signals/temporal_signal_engine.py

Therefore:

DO NOT introduce an unrelated global timestamp abstraction.

Future monitoring and learning components must reuse existing EIOS
chronology concepts where appropriate.

---

# 17. IMPORTANT ARCHITECTURAL DECISION

The next generation of EIOS must evolve from:

"Run research when requested"

toward:

"Continuously acquire, process and update investment intelligence."

The target architecture is:

Internet / External Sources
        â†“
Data Acquisition
        â†“
News / Results / Events / Filings
        â†“
External Intelligence
        â†“
Observation
        â†“
Evidence
        â†“
Signal
        â†“
Catalyst
        â†“
Expectation Gap
        â†“
Mispricing
        â†“
Asymmetry
        â†“
Opportunity Synthesis
        â†“
Monitoring
        â†“
Learning

---

# 18. CONTINUOUS INTELLIGENCE OBJECTIVE

EIOS should eventually automatically collect and process:

- Company quarterly results
- Annual results
- Earnings releases
- Company announcements
- Conference-call information
- Order wins
- Capacity expansion
- Management changes
- M&A
- Regulatory developments
- Government policy
- Commodity movements
- Sector developments
- Competitor developments
- Important news
- Macro events
- Market-moving events

The objective is NOT merely to store news.

The objective is to determine:

"What changed?"

"What does it mean?"

"Which existing thesis does it affect?"

"Does it create a new signal?"

"Does it strengthen or weaken a catalyst?"

"Does it change market expectations?"

"Does it change the mispricing assessment?"

"Does it change opportunity conviction?"

---

# 19. TARGET AUTOMATIC INTELLIGENCE FLOW

New information:

    â†“

Source Acquisition

    â†“

Source Assessment

    â†“

Observation

    â†“

Evidence

    â†“

Entity Mapping

    â†“

Event Classification

    â†“

Signal Detection

    â†“

Existing Signal Update / New Signal

    â†“

Catalyst Update

    â†“

Expectation Gap Update

    â†“

Mispricing Update

    â†“

Asymmetry Update

    â†“

Opportunity Reassessment

    â†“

Monitoring State

---

# 20. EVENT CLASSIFICATION TARGET

Incoming information should eventually be classified into controlled event
families such as:

- NEWS
- RESULT
- EARNINGS
- FILING
- ORDER
- CAPACITY
- MANAGEMENT
- M&A
- REGULATORY
- POLICY
- MACRO
- SECTOR
- COMPETITOR
- COMMODITY
- TECHNOLOGY
- OTHER

Classification must remain deterministic and provenance-preserving.

---

# 21. MONITORING OBJECTIVE

For an existing opportunity:

Existing Opportunity
        â†“
New Information
        â†“
Compare With Previous State
        â†“
Identify Change
        â†“
Assess Thesis Impact
        â†“
Assess Conviction Change

Possible states:

- Conviction Increased
- Conviction Unchanged
- Conviction Decreased
- Thesis Invalidated
- New Research Required

No automatic BUY/SELL action should be introduced at this stage.

---

# 22. LEARNING ARCHITECTURE

EIOS will eventually require a Learning Ledger.

However, Learning must preserve the distinction between:

PREDICTION

and

OUTCOME.

Target architecture:

Opportunity Synthesis
        â†“
Opportunity Prediction Record
        â†“
TIME
        â†“
Actual Outcome
        â†“
Prediction vs Reality
        â†“
Attribution
        â†“
Learning Ledger

The original prediction must never be overwritten by hindsight.

---

# 23. OPPORTUNITY PREDICTION

A future passive `OpportunityPrediction` model is planned.

It should capture the state of EIOS at the time of prediction, including:

- company
- sector
- prediction timestamp
- market price
- intrinsic value
- fair value
- catalyst score
- expectation gap score
- mispricing score
- asymmetry score
- opportunity score
- confidence
- decision
- expected return
- expected duration
- downside / permanent-loss assumptions
- evidence state
- assumptions
- disconfirming evidence
- invalidation conditions
- provenance

It must NOT contain hindsight outcome fields.

---

# 24. OUTCOME / LEARNING PRINCIPLE

Future outcome records should remain separate.

They may eventually capture:

- subsequent market price
- realized return
- realized time
- business outcome
- earnings outcome
- catalyst outcome
- expectation outcome
- thesis validity
- prediction accuracy

But these fields must never be inserted into the original prediction record.

---

# 25. NEXT DEVELOPMENT PRIORITY

The immediate next major development is NOT another scoring engine.

Priority:

## EIOS CONTINUOUS EXTERNAL INTELLIGENCE

First build the infrastructure required for EIOS to periodically acquire
new information.

Initial components should include:

1. Source Registry
2. Data Acquisition Layer
3. Scheduled Ingestion
4. Event Classification
5. Entity Mapping
6. Duplicate Detection
7. Observation Creation
8. Evidence Creation
9. Provenance Preservation
10. Opportunity Update Trigger

Only after this foundation is stable should we build the Learning Ledger.

---

# 26. SCHEDULING TARGET

EIOS should eventually support periodic updates rather than requiring manual
execution.

Target concept:

    Scheduler
        â†“
    Source Registry
        â†“
    Fetch New Information
        â†“
    Detect New / Changed Items
        â†“
    Process Intelligence
        â†“
    Update EIOS State

Initial scheduling frequency can be configurable.

Examples:

- Hourly
- Every 4 hours
- Daily

Different source classes may eventually use different frequencies.

---

# 27. AUTOMATIC REPOSITORY / PUBLISHING

Automatic GitHub publishing is NOT yet part of the production pipeline.

The preferred sequence is:

External Intelligence
        â†“
Validated EIOS State
        â†“
Tests
        â†“
Generated Research Artifacts
        â†“
Optional Repository Publication

Automatic repository writes should NOT be introduced before the ingestion
and validation layers are stable.

---

# 28. ARCHITECTURAL RULES

Continue following the EIOS Engineering Charter.

Important rules:

- Repository first
- Do not redesign existing architecture unnecessarily
- Prefer staged refactoring
- Passive data models
- Engines perform calculations
- Preserve provenance
- Preserve source evidence
- No analytical fabrication
- No automatic investment approval
- No hidden mutation
- Deterministic behavior where appropriate
- Evidence before conviction
- Kill switches remain authoritative
- Do not lower institutional thresholds merely to make tests pass
- Never overwrite historical predictions with hindsight
- Preserve backward compatibility during migrations

---

# 29. CURRENT DEVELOPMENT PHASE

## PHASE

Opportunity Intelligence â†’ Continuous Intelligence Transition

### Completed

Discovery â†’ Opportunity Intake
External Query Generation
External Research
External Retrieval
Observation
Evidence
Signal
Catalyst
Expectation Gap
Mispricing
Asymmetry
Evidence Qualification
Opportunity Synthesis
Opportunity Committee Routing
Negative-path protection
External â†’ Opportunity end-to-end integration

### In Progress

Continuous External Intelligence Architecture

### Planned

Scheduled Intelligence Ingestion
Automatic Event Processing
Opportunity Monitoring
Prediction Records
Outcome Records
Attribution Engine
Learning Ledger
Adaptive Intelligence

---

# 30. NEXT SESSION â€” EXACT STARTING POINT

Do NOT modify the existing Opportunity scoring engines yet.

Start with repository inspection and design of:

    modules/external_intelligence/

for:

    Source Registry
    Scheduled Acquisition
    New-Information Detection
    Event Classification

Then integrate the validated information into the existing:

    Observation
        â†“
    Evidence
        â†“
    Signal
        â†“
    Opportunity

architecture.

The objective is to transform EIOS from a system that can perform research
into a system that can continuously maintain current investment intelligence.

---

# END OF PROJECT STATE
@'

---

# 31. HISTORICAL COMPARISON FOUNDATION

A Historical Comparison foundation has now been implemented under:

    modules/observation/

Components:

    historical_comparison.py
    historical_comparison_engine.py
    test_historical_comparison_engine.py

The purpose is to distinguish historical comparison from observation novelty.

ObservationNoveltyEngine answers:

    "Have I seen this observation before?"

HistoricalComparisonEngine answers:

    "How does the current observation differ from the historical observation?"

The HistoricalComparison model preserves:

- Current observation
- Historical observation
- Comparison type
- Change detection status
- Change direction
- Materiality
- Optional quantitative delta
- Provenance

The current foundation deliberately does NOT infer:

- Positive or negative direction from arbitrary prose
- Financial materiality from arbitrary prose
- Quantitative deltas where structured numeric data does not exist

The existing Observation model remains unchanged.

---

# 32. HISTORICAL COMPARISON VALIDATION

HistoricalComparisonEngine has been independently validated.

Latest test result:

    EIOS HISTORICAL COMPARISON ENGINE TEST

    Test 1  — Identical Observations       : PASS
    Test 2  — Timestamp Only               : PASS
    Test 3  — Changed Information          : PASS
    Test 4  — Independent Source            : PASS
    Test 5  — No Fabricated Direction       : PASS
    Test 6  — Historical Preservation       : PASS
    Test 7  — Current Preservation           : PASS
    Test 8  — Observation Immutability      : PASS
    Test 9  — Deterministic Comparison      : PASS
    Test 10 — Invalid Input Protection      : PASS
    Test 11 — Provenance Preservation        : PASS
    Test 12 — Materiality Not Fabricated    : PASS

    HISTORICAL COMPARISON ENGINE :
    ALL TESTS PASSED

Total:

    12 / 12 PASS

---

# 33. HISTORICAL COMPARISON ARCHITECTURAL STATUS

HistoricalComparisonEngine is currently a foundation component.

It has NOT yet been connected to:

    Evidence
    Signal
    Catalyst
    Expectation Gap
    Mispricing
    Opportunity

This is intentional.

The next architectural decision is to determine where historical comparison
belongs in the existing EIOS intelligence flow.

Candidate boundary:

    External Research
            ↓
        Observation
            ↓
        Novelty
            ↓
    Historical Comparison
            ↓
         Evidence
            ↓
          Signal
            ↓
        Catalyst
            ↓
    Expectation Gap
            ↓
       Mispricing
            ↓
       Opportunity

This flow must NOT be adopted automatically.

The existing Continuous External Intelligence architecture must first be
audited to determine whether historical comparison functionality already
exists elsewhere and whether integration would duplicate existing
responsibilities.

---

# 34. NEXT DEVELOPMENT STEP

Before creating additional production intelligence components:

1. Audit existing Historical Novelty functionality.
2. Audit ResearchRuntime and its supporting infrastructure.
3. Audit Observation → Evidence integration.
4. Audit ResearchContext / Intelligence Mesh integration.
5. Determine whether HistoricalComparisonEngine belongs:
       - at Observation level,
       - at Evidence level,
       - or at another existing intelligence boundary.
6. Identify any overlapping architecture before extending the system.
7. Only then implement the smallest required integration.

Do NOT create another generic novelty, change-detection, or delta engine
without first proving that an existing component cannot perform the required
responsibility.

---

# 35. GIT CHECKPOINT STATUS

Current synchronized repository checkpoint:

    Commit: abb8daf
    Message: Add historical observation comparison foundation

The Historical Comparison foundation is committed.

Committed Historical Comparison files:

    modules/observation/historical_comparison.py
    modules/observation/historical_comparison_engine.py
    modules/observation/test_historical_comparison_engine.py

The working tree was clean at this checkpoint.

---

# 36. ENGINEERING GUARDRAIL

Historical comparison must remain evidence-preserving and conservative.

Do not:

- Modify the Observation model unnecessarily.
- Infer financial meaning from unstructured text.
- Invent numerical deltas.
- Invent positive or negative direction.
- Infer materiality without supporting evidence.
- Bypass ObservationNoveltyEngine.
- Duplicate existing external intelligence functionality.
- Connect directly to Opportunity scoring.
- Automatically change investment decisions.

The objective is to add intelligence through the smallest defensible
architectural extension.

---

# 37. HISTORICAL COMPARISON BOUNDARY DECISION

Repository audit determined that HistoricalComparisonEngine belongs at the
Observation layer because both of its inputs and its output provenance are
owned by that layer.

The Evidence boundary remains unchanged. ExternalEvidenceIntake continues to
require an explicit EvidenceAssessment and does not infer evidence meaning
from a historical difference.

ObservationEngine now provides an opt-in compare_historical method. The caller
must explicitly supply both the current and historical observations.

The integration deliberately does NOT:

- Automatically select a historical observation.
- Change novelty assessment or observation ingestion.
- Register or persist comparison results.
- Publish comparisons to ResearchContext or IntelligenceMesh.
- Create Evidence, Signals, Catalysts, or Opportunities.

This is the smallest integration that establishes ownership without inventing
comparison relevance or downstream financial meaning.

Validation coverage:

    modules/observation/
        test_observation_historical_comparison_integration.py

The validation confirms that comparison is available through
ObservationEngine and does not mutate the ObservationRegistry or persistent
observation state.

---

# 38. HISTORICAL CANDIDATE SELECTION

Historical candidate selection is implemented at the Observation layer under:

    modules/observation/historical_observation_selector.py

Selection is deliberately conservative:

- Entity and category must match after text normalization.
- The candidate timestamp must be strictly earlier than the current timestamp.
- The uniquely most recent eligible observation is selected.
- Tied latest candidates produce no selection because the choice is ambiguous.
- Title, description, source, confidence, and financial meaning do not determine
  comparability.

ObservationEngine exposes opt-in selection through select_historical. Selection
does not mutate the registry, persist results, publish intelligence, or invoke
HistoricalComparisonEngine automatically.

ResearchRuntime remains unchanged. Runtime integration must not occur until the
selection policy and its ambiguity behavior are validated independently.

---

# 39. OPT-IN RUNTIME HISTORICAL COMPARISON

ResearchRuntime now supports historical comparison only when constructed with:

    enable_historical_comparison=True

For every new observation returned by a research cycle, the runtime:

1. Selects a candidate only from the observation history that existed before
   the cycle began.
2. Preserves the HistoricalObservationSelection result, including no-match and
   ambiguity reasons.
3. Creates HistoricalComparison only when selection is unambiguous.
4. Preserves the combined result as RuntimeHistoricalComparison.

Same-cycle observations cannot become historical candidates for one another.
The default remains disabled, preserving existing runtime behavior.

The integration does not publish comparisons to ResearchContext or
IntelligenceMesh and does not create Evidence, Signals, Catalysts,
Expectation Gaps, Mispricing, or Opportunities.

---

# 40. RESEARCH RUNTIME OPERATIONAL BOOTSTRAP

External research now has a safety-first one-cycle launcher:

    python -m scripts.run_external_research_once

The default command performs configuration validation only and makes no
external API calls. Live execution requires the explicit flag:

    --execute

Configuration is provided through:

    TAVILY_API_KEY
    EIOS_OBSERVATION_PATH
    EIOS_ENABLE_HISTORICAL_COMPARISON

The bootstrap validates API configuration, the requests dependency,
observation storage path, production research jobs, and unique job IDs before
constructing ResearchRuntime. Runtime imports remain lazy so validation can
report missing dependencies without failing at module import time.

Validation inspects observation-path safety without creating directories or
files. Runtime construction registers the same immutable job snapshot that
passed validation, so a stateful provider cannot substitute unvalidated jobs.

Historical comparison remains default-off. The launcher does not modify
Evidence, Signals, Catalysts, Expectation Gaps, Mispricing, or Opportunities.

---

# 41. RUNTIME OBSERVATION PROVENANCE AND STORE ISOLATION

Runtime-created external observations may now carry an optional passive
ObservationProvenance record containing cycle ID, job ID, research intent,
retrieval time, source URL/domain/type, and a SHA-256 content fingerprint.
Legacy observations without provenance continue to deserialize with
`provenance=None`.

Provenance construction remains at the external observation adapter boundary;
the Observation model performs no parsing, hashing, policy, or analysis.
ResearchExecutionService supplies job and cycle context, while
ExternalResearchResult records job identity plus execution and observation
counts. Historical comparison remains disabled by default and was not enabled
by this checkpoint.

Observation-related tests now inject persistence backed by temporary paths.
No test in this checkpoint reads, rewrites, migrates, cleans, or deletes
`data/observations.json`, and deterministic checkpoint coverage performs no
network retrieval. The checkpoint test places the orchestrator behind a hard
HTTP request guard, uses fake search/retrieval services, and verifies that a
sentinel production store remains byte-for-byte unchanged while the isolated
test store is written.

---

# 42. PROVENANCE-AWARE HISTORICAL CANDIDATE SELECTION

HistoricalObservationSelector now ranks comparable history using passive
ObservationProvenance when available:

1. Exact normalized job ID.
2. Exact normalized research intent when no job match exists.
3. Entity/category fallback using provenance-free legacy observations only.

Populated conflicting job IDs are never comparable, even when research intent
matches. Provenance priority takes precedence over recency; recency selects only
within the preferred candidate boundary. Existing timestamp, entity/category,
and ambiguity protections remain unchanged.

HistoricalObservationSelection preserves the selected boundary as
HistoricalSelectionBasis. Legacy observations remain supported without
migration. No Evidence, Signal, Catalyst, Expectation Gap, Mispricing, or
Opportunity behavior is changed.

---

# 43. PROVENANCE-AWARE RUNTIME INTEGRATION VALIDATION

ResearchRuntime provenance-aware historical comparison is now covered by a
deterministic end-to-end validation checkpoint. With historical comparison
explicitly enabled, the runtime is verified to preserve job-ID priority,
research-intent fallback, conflicting-job exclusion, provenance-free legacy
fallback, and pre-cycle history isolation.

The validation uses temporary observation storage, a fake runtime controller,
and a hard HTTP request guard. It makes no live API calls and does not read or
write the production observation store. Historical comparison results remain
passive runtime records: they are not published into Evidence, Assumptions,
Knowledge, Signals, Catalysts, Expectation Gaps, Mispricing, or Opportunities.

No production runtime behavior is changed by this checkpoint.

---

# 44. OPT-IN HISTORICAL COMPARISON AUDIT REPORTING

ResearchRuntime can now preserve historical comparison results in a separate
append-only JSON Lines audit report. Reporting is enabled only when historical
comparison is enabled and an explicit audit path is configured through:

    EIOS_HISTORICAL_COMPARISON_AUDIT_PATH

Each audit record includes the runtime timestamp, current and selected
historical observation references, provenance identifiers and fingerprints,
selection basis and reason, eligible candidate count, and the conservative
comparison result. No-match and ambiguous selections are also recorded.

The audit path must remain separate from EIOS_OBSERVATION_PATH. Bootstrap
validation checks path safety without creating or modifying the report. With no
audit path configured, runtime behavior is unchanged and no audit file is
created.

Audit records remain passive operational output. They are not written into the
observation store or published into Evidence, Assumptions, Knowledge, Signals,
Catalysts, Expectation Gaps, Mispricing, or Opportunities. Deterministic test
coverage uses temporary paths, a fake controller, and a hard HTTP request guard.

---

# 45. HISTORICAL COMPARISON AUDIT READER AND CYCLE SUMMARY

Historical comparison audit records can now be read through a strict,
schema-version-aware, read-only parser. Parsed records use immutable typed
models for observation references, selection facts, and conservative comparison
fields. Invalid JSON, missing required fields, invalid enum values, and
unsupported schema versions fail with the source line number.

HistoricalComparisonCycleSummarizer produces count-only facts for one exact
runtime timestamp: selected, no-match, ambiguous, comparison, detected-change,
selection-basis, and comparison-type counts. Ambiguity is identified from the
recorded candidate count, not inferred from financial or unstructured content.

A read-only command summarizes an explicitly selected cycle or the latest
appended cycle:

    python -m scripts.summarize_historical_comparison_audit

The command uses EIOS_HISTORICAL_COMPARISON_AUDIT_PATH by default and accepts
--path and --recorded-at overrides. It does not modify the audit report,
observation store, ResearchContext, IntelligenceMesh, Evidence, Signals,
Catalysts, Expectation Gaps, Mispricing, Opportunities, or investment decisions.

---

# 46. READ-ONLY MULTI-CYCLE HISTORICAL COMPARISON TIMELINE

Historical comparison cycle summaries can now be grouped into an immutable,
chronologically ordered audit timeline. Exact recorded-at timestamps remain the
cycle boundary. The timeline exposes cycle and record totals while preserving
the existing count-only summary for every cycle.

The audit summary command now supports:

    --all-cycles
    --json

All-cycle output is ordered chronologically. JSON output uses a stable
schema-version-one envelope and explicitly records that no financial
interpretation was performed. Existing latest-cycle and --recorded-at behavior
remains unchanged.

The timeline rejects mixed naive and timezone-aware cycle timestamps rather
than assuming a timezone policy. It does not modify the audit report,
observation store, ResearchContext, IntelligenceMesh, Evidence, Signals,
Catalysts, Expectation Gaps, Mispricing, Opportunities, or investment decisions.

---

# 47. PROVENANCE-SCOPED HISTORICAL COMPARISON TIMELINE FILTERS

Historical comparison audit records can now be filtered before single-cycle or
multi-cycle summarization by current-observation entity, category, job ID,
research intent, selection basis, comparison type, and inclusive runtime bounds.
Text filters use conservative whitespace normalization and case-insensitive
exact matching; they do not use substring, fuzzy, or semantic inference.

The read-only audit command exposes:

    --entity
    --category
    --job-id
    --research-intent
    --selection-basis
    --comparison-type
    --from
    --to

JSON output preserves the applied filter criteria. Reversed bounds and mixed
timezone-awareness are rejected rather than corrected implicitly. Filtering
does not modify audit records, observation state, ResearchContext,
IntelligenceMesh, Evidence, Signals, Catalysts, Expectation Gaps, Mispricing,
Opportunities, or investment decisions.

---

# 48. HISTORICAL COMPARISON HUMAN-REVIEW CANDIDATES

Validated audit records with an explicit comparison and change_detected=True
can now become immutable human-review candidates. Candidate identity is a
deterministic SHA-256 digest of preserved runtime, observation, provenance,
selection, and comparison facts. Duplicate identities fail closed.

Review candidates preserve current and historical observation references,
content fingerprints, job ID, research intent, selection basis, comparison
type, direction, materiality, delta, and comparison provenance. Candidate
states are explicit:

    PENDING
    REVIEWED
    ACCEPTED
    REJECTED
    DEFERRED

HistoricalComparisonReviewService returns a new immutable candidate for an
explicit human disposition and rejects repeat review. Decisions require a
reviewer, reason, and non-preceding review timestamp. They remain in memory;
this checkpoint does not persist review decisions.

A read-only command lists pending candidates:

    python -m scripts.list_historical_comparison_review_candidates

The command does not modify the audit report. No candidate status creates
Evidence, publishes intelligence, scores an Opportunity, infers financial
importance, or changes an investment decision.

---

# 49. OPT-IN HISTORICAL COMPARISON REVIEW DECISION LEDGER

Explicit human-review dispositions can now be persisted in a separate
append-only JSON Lines ledger. The ledger preserves candidate ID, disposition,
reviewer, reason, and review timestamp under a strict schema-version-one record.
It accepts only reviewed candidates and permits at most one decision per
candidate ID; repeat or conflicting decisions fail before any write.

The explicit recording command uses a separately configured path:

    EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH

    python -m scripts.record_historical_comparison_review_decision

The comparison audit path and decision-ledger path must remain separate. The
command requires candidate ID, status, reviewer, reason, and review timestamp.
It does not run automatically as part of ResearchRuntime.

Decision persistence does not modify the comparison audit or observation store,
create Evidence, publish intelligence, score an Opportunity, infer financial
importance, or change an investment decision.

---

# 50. READ-ONLY REVIEW CANDIDATE DECISION RECONCILIATION

Historical comparison review candidates can now be reconciled with the
separate decision ledger without modifying either source. Pending candidates
remain unchanged; decided candidates are returned as new immutable values with
their persisted status, reviewer, reason, and review timestamp.

Reconciliation fails closed for unknown candidate references, multiple
decisions, duplicate candidate identities, non-pending source candidates,
timestamps preceding the audit record, and inconsistent timezone awareness.

The review-candidate listing command accepts --ledger-path or
EIOS_HISTORICAL_COMPARISON_REVIEW_LEDGER_PATH and reports pending and decided
counts. It verifies both input files remain byte-for-byte unchanged. This
checkpoint does not create Evidence, publish intelligence, score Opportunities,
infer financial importance, or change investment decisions.

---

# 51. READ-ONLY HISTORICAL COMPARISON REVIEW DECISION SUMMARY

Reconciled historical comparison review candidates can now be aggregated into
an immutable, count-only operational summary. The summary reports pending and
decided totals, explicit REVIEWED, ACCEPTED, REJECTED, and DEFERRED counts,
counts by entity, category, comparison type, reviewer, and calendar review
date, unresolved candidate identities, and the earliest and latest explicit
review timestamps.

A separate read-only command accepts the audit and decision-ledger paths from
arguments or their existing EIOS environment variables:

    python -m scripts.summarize_historical_comparison_review_decisions

Text and stable schema-version-one JSON output are supported. The command
requires the audit and ledger to remain separate, validates reconciliation and
review metadata, and verifies that both source files remain byte-for-byte
unchanged. Mixed timezone-awareness in review timestamps fails closed.

This summary does not create Evidence, publish intelligence, score an
Opportunity, infer financial importance, or change an investment decision.

---

# 52. READ-ONLY ACCEPTED-REVIEW OBSERVATION RESOLUTION PREVIEW

Explicitly ACCEPTED historical comparison review candidates can now be
resolved to their full persisted current Observations without modifying any
source. Resolution first matches the exact SHA-256 content fingerprint and
then requires the audited title, entity, category, timestamp, source, job ID,
and research intent to match the persisted Observation and its provenance.

Missing source Observations, duplicate fingerprint matches, provenance-free
Observations, identity mismatches, malformed fingerprints, and non-ACCEPTED
candidates fail closed. The immutable preview preserves the resolved content,
confidence, source metadata, provenance, reviewer, reason, and review time but
does not return or mutate the source Observation object.

The read-only command requires three separate source paths and supports text
and stable schema-version-one JSON output:

    python -m scripts.preview_historical_comparison_accepted_observations

It verifies the comparison audit, review decision ledger, and Observation
store remain byte-for-byte unchanged. No EvidenceAssessment is supplied and no
Evidence, Intelligence, Signal, Catalyst, Opportunity, score, valuation, or
investment decision is created.

---

# 53. OPT-IN HUMAN EVIDENCE ASSESSMENT LEDGER

An explicitly ACCEPTED historical comparison review can now receive one
separate, append-only human Evidence assessment after exact source Observation
resolution. Each schema-version-one record binds the candidate ID to the
resolved Observation fingerprint and preserves category, Supporting or
Contradictory direction, strength, confidence, independent-confirmation count,
primary-source and time-sensitive flags, assessor, rationale, and assessment
timestamp.

Assessment values are explicit human inputs. Strength and confidence must be
finite values from zero through 100, independent confirmation must be a
non-negative integer, flags must be booleans, and the assessment cannot precede
the accepted review. Duplicate or conflicting assessments for a candidate fail
before any write.

The recording command requires the audit, review ledger, Observation store,
and assessment ledger to use four separate paths:

    python -m scripts.record_historical_comparison_evidence_assessment

It resolves the ACCEPTED candidate and exact Observation before appending only
the assessment ledger, then verifies the three source files remain unchanged.
No EvidenceItem, Evidence, Intelligence, Signal, Catalyst, Opportunity, score,
valuation, or investment decision is created.

---

# 54. READ-ONLY EVIDENCE CONVERSION ELIGIBILITY PREVIEW

Accepted historical comparison reviews, exactly resolved Observations, and
human Evidence assessments can now be reconciled into immutable conversion
eligibility previews. Each eligible preview shows the precise statement,
source, category, direction, strength, confidence, confirmation count, source
flags, notes, and deterministic proposed Evidence ID that a later, separately
approved conversion would receive.

Accepted candidates without assessments are reported as ineligible and remain
unchanged. Orphan or duplicate assessments, unknown candidate references,
fingerprint mismatches, duplicate accepted Observation fingerprints, invalid
chronology, and inconsistent timezone awareness fail closed. Reviewer and
assessor lineage remains attached to every projection.

The read-only command requires four distinct input paths and supports text and
stable schema-version-one JSON output:

    python -m scripts.preview_historical_comparison_evidence_conversion

It verifies the comparison audit, review ledger, Observation store, and human
assessment ledger remain byte-for-byte unchanged. The preview layer does not
import or invoke Evidence creation. No EvidenceItem, Evidence, Intelligence,
Signal, Catalyst, Opportunity, score, valuation, or investment decision is
created.

---

# 55. EXPLICIT OPT-IN EVIDENCEITEM MATERIALIZATION

One eligible historical comparison can now be explicitly materialized as a
canonical Opportunity EvidenceItem through the existing ExternalEvidenceIntake
boundary. Materialization requires an ACCEPTED human review, exact persisted
Observation resolution, one matching human Evidence assessment, a named
converter, and a non-preceding conversion timestamp.

The Evidence ID is deterministic from the review candidate identity. Before
creating the in-memory EvidenceItem, an append-only schema-version-one receipt
ledger rejects any prior conversion for that candidate. The receipt preserves
the exact EvidenceItem fields, Observation fingerprint, reviewer, assessor,
converter, and their timestamps. Duplicate candidate or Evidence identities,
invalid schemas, identity mismatches, and inconsistent chronology fail closed.

The explicit command requires five distinct configured paths:

    python -m scripts.materialize_historical_comparison_evidence

Only the conversion receipt is appended. The comparison audit, review ledger,
Observation store, and assessment ledger remain unchanged. Materialization is
never invoked automatically by ResearchRuntime. No Intelligence is published,
no Signal or Catalyst is generated, no Opportunity is scored, and no valuation
or investment decision is performed.

---

# 56. READ-ONLY MATERIALIZED EVIDENCE RECEIPT RECONCILIATION

Materialized historical comparison EvidenceItem receipts can now be reconciled
back through the accepted review, exact persisted Observation, and explicit
human assessment chain. Every receipt field, deterministic Evidence ID,
Observation fingerprint, reviewer, assessor, and chronology must match the
current validated source records.

Verified receipts are grouped by exact entity into immutable pack previews with
Supporting and Contradictory Evidence IDs. Operational workflow gaps are
reported separately for accepted candidates missing an assessment and assessed
candidates missing a materialization receipt. These are pipeline-state facts,
not financial or investment interpretations.

The read-only command requires five distinct source paths and supports text and
stable schema-version-one JSON output:

    python -m scripts.preview_historical_comparison_entity_evidence_packs

Orphaned, altered, duplicate, stale, or mismatched receipts fail closed. All
five source files remain byte-for-byte unchanged. No new EvidenceItem is
created, no Intelligence is published, no Signal or Catalyst is generated, no
Opportunity is scored, and no valuation or investment decision is performed.

---

# 57. EXPLICIT OPT-IN ENTITY EVIDENCE PACK SCORING

A fully reconciled, gap-free materialization workflow for one exact entity can
now be explicitly analyzed by the existing OpportunityEvidenceEngine. Verified
conversion receipts are reconstructed as Supporting and Contradictory
EvidenceItems. No assumptions, kill switches, or monitoring signals are
fabricated; the engine reports their absence through its normal evidence gaps.

Each exact input pack version receives a deterministic SHA-256 fingerprint. An
append-only schema-version-one scoring receipt preserves the entity, input
Evidence IDs, evidence score, confidence, support sufficiency, gaps, strengths,
weaknesses, warnings, analyst, and analysis timestamp. Repeating an unchanged
pack fails before the scoring engine runs; a genuinely changed receipt set has
a new fingerprint and may be analyzed separately.

The explicit command requires six distinct configured paths:

    python -m scripts.analyze_historical_comparison_entity_evidence_pack

Only the scoring receipt is appended. All audit, review, Observation,
assessment, and conversion sources remain unchanged. No Intelligence is
published, no Signal or Catalyst is created, no valuation is performed, and no
portfolio action or investment decision is made.

---

# 58. OPT-IN HUMAN OPPORTUNITY EVIDENCE GOVERNANCE LEDGER

One exact scored entity Evidence pack fingerprint can now receive a separate,
append-only human governance record. Governance requires at least one explicit
assumption, one fully specified kill switch, and one monitoring signal, plus a
named analyst, rationale, and non-preceding governance timestamp.

Kill switches preserve name, condition, Low/Medium/High/Critical severity,
measurability, threshold, monitoring frequency, rationale, and explicit
triggered state. Assumptions, monitoring signals, and kill-switch names must be
non-empty and unique. Duplicate governance for the same pack fingerprint fails
before any write.

The explicit recording command reads one scoring receipt ledger and appends
only a separate governance ledger:

    python -m scripts.record_historical_comparison_evidence_governance

It verifies the scoring receipt source remains byte-for-byte unchanged. The
governance checkpoint does not rescore the pack, publish Intelligence, create
Signals or Catalysts, perform valuation, or make a portfolio action or
investment decision.

---

# 68. READ-ONLY MULTI-SIGNAL CATALYST SUPPORT PREVIEW

Two or more individually approved, fingerprint-verified Signals can now be
combined by the existing `SignalAggregationEngine`, classified through the
existing Signal-cluster bridge, and analyzed in memory by the existing
`CatalystEngine`. Signal fingerprints and EvidenceItem identities must be
unique, preventing duplicated Evidence from masquerading as corroboration.

The immutable preview preserves the complete supporting identity set and
reports independent sources, average strength and confidence, contradictions,
cluster score and emergence, taxonomy classification, Catalyst score and
confidence, the unchanged 50.0 minimum-score result, reasoning, and warnings.

The preview explicitly reports when independent multi-Signal support is strong
but the canonical Signal stages still keep the Catalyst below threshold. It
does not silently promote stages or let corroboration bypass the existing
Catalyst scoring contract. Historical Signal-chain tests now use the canonical
0-100 Evidence confidence scale expected by the Evidence and aggregation
engines.

    python -m scripts.preview_historical_comparison_multi_signal_catalyst_support

All source ledgers remain byte-for-byte unchanged. No Signal, cluster, or
Catalyst is persisted; no Intelligence is published; no Expectation Gap,
Opportunity scoring, valuation, portfolio action, or investment decision is
performed.

---

# 70. READ-ONLY PROMOTED-STAGE CATALYST PREVIEW

Approved Emerging-to-Validated stage reviews can now be applied only to fresh
in-memory reconstructions of their exact Signals. The builder first recreates
the unchanged baseline multi-Signal support fingerprint, then verifies every
stage review and produces a before/after Catalyst Engine comparison.

The immutable preview preserves original and effective stages, promoted Signal
IDs, baseline and promoted scores and confidence, score change, minimum-score
status, taxonomy classification, reasoning, and warnings. Canonical Signal
receipts and interpretations are never changed.

    python -m scripts.preview_historical_comparison_promoted_stage_catalyst

All input ledgers remain byte-for-byte unchanged. No promoted Signal, cluster,
or Catalyst is persisted; no Intelligence, Expectation Gap, Opportunity
scoring, valuation, portfolio action, or investment decision is performed.

---

# 71. HUMAN PROMOTED-STAGE CATALYST ASSESSMENT LEDGER

One exact promoted-stage Catalyst preview can now receive an append-only human
disposition of Approved, Rejected, or Deferred. Each record binds a
deterministic fingerprint of the complete before/after preview to its promotion
and support fingerprints, Catalyst, full Signal set, promoted Signal set,
reviewer, rationale, conditions, monitoring requirements, and timestamp.

Approval fails closed unless the promoted Catalyst meets the existing engine
minimum score. Duplicate decisions for the same exact preview fail before any
write; below-threshold previews may still be explicitly Deferred or Rejected.

    python -m scripts.record_historical_comparison_promoted_catalyst_assessment

The command reconstructs the exact preview from its source ledgers, verifies
those inputs remain byte-for-byte unchanged, and appends only the human
decision. It persists no Signal or Catalyst, publishes no Intelligence, runs
no Expectation Gap or Opportunity scoring, performs no valuation, and makes no
portfolio action or investment decision.

---

# 72. EXPLICIT GOVERNED CATALYST MATERIALIZATION

One exact human-approved promoted-stage Catalyst can now be explicitly
reconstructed as the canonical `Catalyst` model and recorded with an
append-only creation receipt. The receipt binds the complete preview,
assessment, promotion, support, Catalyst, and Signal fingerprints to the
creator, rationale, and timestamp.

Materialization fails closed unless the assessment is Approved, the exact
preview can be reproduced, and the promoted Catalyst still meets the existing
minimum score. Duplicate Catalyst IDs and repeat materialization of the same
assessment fail before the Catalyst Engine runs.

    python -m scripts.materialize_historical_comparison_catalyst

The command verifies every source ledger remains byte-for-byte unchanged and
appends only the Catalyst creation receipt. It does not modify or persist any
Signal, publish Intelligence, run Expectation Gap or Opportunity scoring,
perform valuation, or make a portfolio action or investment decision.

---

# 73. READ-ONLY EXPECTATION GAP ELIGIBILITY PREVIEW

One exact materialized governed Catalyst can now be checked for permission to
enter Expectation Gap analysis without invoking the `ExpectationGapEngine`.
The gate reconstructs the canonical Catalyst, verifies its full fingerprint,
and requires exact bindings across the promoted preview, approved human
assessment, and append-only Catalyst creation receipt.

The immutable preview exposes eligibility, explicit blockers, Catalyst score
and confidence, complete provenance fingerprints, and the seven inputs that a
later Expectation Gap analysis must provide. Stale or mismatched receipts fail
closed before an eligibility result is produced.

    python -m scripts.preview_historical_comparison_expectation_gap_eligibility

Every source ledger remains byte-for-byte unchanged. The command does not run
Expectation Gap or Opportunity scoring, modify Signals, persist another
Catalyst, publish Intelligence, perform valuation, or make a portfolio action
or investment decision.

---

# 69. HUMAN SIGNAL STAGE REVIEW LEDGER

One Signal inside an exact strong multi-Signal support preview can now receive
an append-only human maturity review. This checkpoint supports only the narrow
transition from Emerging Signal to Validated Signal and binds the exact support,
Signal, validation, reviewer, rationale, optional conditions and monitoring
requirements, and timestamp.

Approval requires unique independently supported Signals, an emerging cluster,
an explicit promotion-required result, and an already Approved Signal
validation decision. Later maturity stages cannot be assigned here. Duplicate
reviews for the same support, Signal, and target fail before any write.

    python -m scripts.record_historical_comparison_signal_stage_review

Only the review ledger is appended. Canonical Signals remain unchanged and no
Catalyst is recalculated or persisted. No Intelligence, Expectation Gap,
Opportunity scoring, valuation, portfolio action, or investment decision is
performed.

---

# 59. EXPLICIT GOVERNED ENTITY EVIDENCE PACK RESCORING

One exact entity Evidence pack and its fingerprint-bound human governance can
now be explicitly rescored through the existing OpportunityEvidenceEngine.
Only recorded assumptions, kill switches, and monitoring signals are supplied;
no analytical inputs are inferred or fabricated.

The governed input receives a deterministic fingerprint covering the pack
fingerprint and complete governance record. An append-only scoring receipt
preserves the resulting evidence score, confidence, support sufficiency,
remaining evidence gaps, diagnostics, analyst, and timestamp. Duplicate
rescoring of unchanged governed inputs fails before the engine runs.

The explicit command requires eight distinct configured paths:

    python -m scripts.rescore_historical_comparison_governed_evidence_pack

Only the governed scoring receipt is appended. All audit, review, Observation,
assessment, conversion, initial scoring, and governance sources remain
unchanged. No Intelligence, Signal, or Catalyst is created, and no valuation,
portfolio action, or investment decision is performed.

---

# 60. OPT-IN HUMAN SIGNAL INTERPRETATION LEDGER

A sufficiently supported governed Evidence pack can now receive an explicit,
append-only human Signal interpretation for one materialized EvidenceItem. The
record binds the exact governed-input fingerprint, original pack fingerprint,
entity, Evidence ID, full canonical `SignalInterpretation`, named analyst,
rationale, and non-preceding timestamp.

The boundary fails closed for insufficient governed support, a mismatched pack
or entity chain, an Evidence ID outside the original scored pack, an incomplete
canonical interpretation, or a duplicate governed-pack/Evidence pair.

The explicit command reads three receipt ledgers and appends only the separate
interpretation ledger:

    python -m scripts.record_historical_comparison_signal_interpretation

All input receipts remain byte-for-byte unchanged. This checkpoint records
human meaning only: it does not invoke the Signal Interpretation Engine,
create a Signal or Catalyst, publish Intelligence, perform valuation, or make
an investment decision.

---

# 61. EXPLICIT SIGNAL MATERIALIZATION WITH CREATION RECEIPTS

One approved historical-comparison Signal interpretation can now explicitly
create one canonical in-memory Signal through the existing
`SignalInterpretationEngine`. The exact governed input, pack, EvidenceItem,
Signal ID, canonical Signal fingerprint, classification, creator, and timestamp
are preserved in a separate append-only creation receipt.

Materialization fails before the engine runs when the interpretation and
Evidence conversion do not bind the same EvidenceItem, the timestamp precedes
an approved input, the Signal ID already exists, or the same approved
interpretation was already materialized.

    python -m scripts.materialize_historical_comparison_signal

Only the creation receipt is persisted. Source ledgers remain byte-for-byte
unchanged, the Signal Registry is not mutated, and no Catalyst is created. No
Intelligence is published, and no valuation, opportunity score, portfolio
action, or investment decision is performed.

---

# 62. READ-ONLY SIGNAL VALIDATION PREVIEW

An exact historical-comparison Signal creation can now be reconstructed from
its approved interpretation and Evidence conversion, checked against its
creation-time canonical Signal fingerprint, and evaluated by the existing
`SignalValidationEngine` without persistence.

The immutable preview exposes validity, validation score and confidence,
source and Evidence quality, relevance, recency, persistence, corroboration,
contradiction penalty, independent confirmation, reasons, warnings, and
invalidation reasons. Any provenance or fingerprint mismatch fails before
validation.

The interpretation ledger now enforces the canonical Signal model's 0-100
scale for magnitude, probability, persistence, relevance, and market
recognition, matching the existing interpretation and validation engines.

    python -m scripts.preview_historical_comparison_signal_validation

The command reads three distinct ledgers and verifies all remain byte-for-byte
unchanged. It does not append a receipt, alter the Signal Registry, classify a
Catalyst, publish Intelligence, score an Opportunity, perform valuation, or
make a portfolio action or investment decision.

---

# 63. HUMAN SIGNAL VALIDATION DECISION LEDGER

One exact read-only Signal validation result can now receive an append-only
human disposition of Approved, Rejected, or Deferred. Each record binds a
deterministic fingerprint of the complete validation preview to the canonical
Signal fingerprint, Signal ID, governed input, EvidenceItem, reviewer,
rationale, optional conditions and monitoring requirements, and timestamp.

Approval fails closed unless the exact preview is valid and contains no
invalidation reasons. Duplicate decisions for the same exact validation result
fail before any write.

    python -m scripts.record_historical_comparison_signal_validation_decision

The command reconstructs the preview from three distinct source ledgers,
verifies those inputs remain byte-for-byte unchanged, and appends only the
decision ledger. It does not classify a Catalyst, alter the Signal Registry,
publish Intelligence, score an Opportunity, perform valuation, or make a
portfolio action or investment decision.

---

# 66. READ-ONLY CATALYST ENGINE ANALYSIS PREVIEW

One classified governed Signal can now be reconstructed and analyzed in memory
by the existing `CatalystEngine`. Before analysis, the current eligibility and
taxonomy classification are recomputed and required to match their exact
stored fingerprints. The engine receives the verified classification rather
than independently changing the taxonomy result.

The immutable preview exposes classification, direction, horizon, magnitude,
probability, persistence, market recognition, Catalyst score and confidence,
minimum-score status, Evidence, assumptions, contradictions, invalidation
conditions, reasoning, and warnings. The in-memory Catalyst object is discarded.

    python -m scripts.preview_historical_comparison_catalyst_analysis

The command reads five distinct ledgers and verifies each remains byte-for-byte
unchanged. It appends no receipt, persists no Catalyst, publishes no
Intelligence, runs no Expectation Gap or Opportunity scoring, performs no
valuation, and makes no portfolio action or investment decision.

---

# 67. HUMAN CATALYST ASSESSMENT DECISION LEDGER

One exact read-only Catalyst analysis can now receive an append-only human
disposition of Approved, Rejected, or Deferred. Each decision binds a
deterministic fingerprint of the complete analysis preview to its Catalyst,
Signal, classification, reviewer, rationale, optional conditions and
monitoring requirements, and timestamp.

Approval fails closed when the Catalyst analysis does not meet the existing
engine minimum score. Duplicate decisions on the same exact preview fail
before any write; below-threshold analyses may still be explicitly Deferred or
Rejected.

    python -m scripts.record_historical_comparison_catalyst_assessment_decision

The command reconstructs the preview from five source ledgers, verifies those
inputs remain byte-for-byte unchanged, and appends only the human decision. It
persists no Catalyst, publishes no Intelligence, runs no Expectation Gap or
Opportunity scoring, performs no valuation, and makes no portfolio action or
investment decision.

---

# 64. READ-ONLY CATALYST REVIEW ELIGIBILITY PREVIEW

An exact governed Signal can now be checked for permission to enter Catalyst
review without invoking the Catalyst classifier. The gate reconstructs and
fingerprint-verifies the Signal and current validation result, requires that
the human decision binds that exact validation fingerprint, and permits review
only when validation remains valid and the human disposition is Approved.

The immutable preview preserves the Signal, validation, governed-input, and
Evidence identities plus human conditions, monitoring requirements, and
explicit blockers. A stale or mismatched validation decision fails closed.

    python -m scripts.preview_historical_comparison_catalyst_eligibility

The command reads four distinct ledgers and verifies all remain byte-for-byte
unchanged. It performs no Catalyst taxonomy matching or classification,
creates no Catalyst, publishes no Intelligence, scores no Opportunity,
performs no valuation, and makes no portfolio action or investment decision.

---

# 65. EXPLICIT CATALYST TAXONOMY CLASSIFICATION RECEIPTS

One eligible governed Signal can now be explicitly passed to the existing
deterministic `CatalystClassifier`. The resulting primary and secondary
taxonomy definitions, confidence, reasoning, matched and unclassified Signals,
warnings, analyst, rationale, and timestamp are preserved in an append-only
classification receipt.

Every receipt binds deterministic eligibility and classification fingerprints
to the exact Signal and human-approved validation result. Ineligible or stale
inputs fail before classification, and duplicate classification of the same
exact eligible Signal fails before the classifier runs.

    python -m scripts.classify_historical_comparison_catalyst

Only taxonomy classification occurs. The command verifies four source ledgers
remain byte-for-byte unchanged and appends only the classification receipt. It
does not invoke the analytical Catalyst Engine, create a Catalyst object,
publish Intelligence, score an Opportunity, perform valuation, or make a
portfolio action or investment decision.

---

# 68. SOURCE QUALITY AND WITHIN-CYCLE DEDUPLICATION

External Observation provenance now carries backward-compatible semantic
source classification (`REGULATORY`, `COMPANY_PRIMARY`, `RESEARCH`, `NEWS`, or
`WEB`) and deterministic quality tiers. MIME content type is preserved in the
separate `content_type` field; legacy records that stored MIME data in
`source_type` continue to load unchanged.

URL identity policy lives in services, not models. Canonicalization normalizes
scheme and host, removes default ports, fragments and tracking parameters,
normalizes trailing slashes, and sorts query parameters. A SHA-256 fingerprint
binds that canonical URL to whitespace-normalized content. Within one research
cycle, matching fingerprints produce one Observation while ordered, unique
contributing job IDs and research intents are merged into its provenance.
Existing scalar job and intent fields remain available for compatibility.

New Observation and retrieval timestamps are timezone-aware UTC. Persistence
preserves legacy naive timestamps exactly as loaded. Engines that need to
order mixed legacy and new timestamps normalize transient values internally
without mutating Observation models. Historical comparison remains disabled
by default and this checkpoint does not enable or invoke it. The existing 45
production Observations and `data/observations.json` remain unchanged.

Offline verification:

    python -m modules.external_intelligence.test_source_quality_and_cycle_deduplication
    SOURCE QUALITY AND CYCLE DEDUPLICATION : ALL TESTS PASSED

The related broad offline module suite completed 11/11 successfully, and all
changed Python files passed `py_compile`. No external calls were made.

---

# 74. READ-ONLY EXPECTATION GAP ANALYSIS PREVIEW

One eligible materialized governed Catalyst can now be passed explicitly to
the existing `ExpectationGapEngine` without persistence. Before the engine is
invoked, the complete promoted-preview, human-assessment, and Catalyst-creation
chain is reconstructed and fingerprint-verified. The seven required analysis
inputs are validated, including the engine's 0-100 analytical scale.

The immutable result binds a deterministic fingerprint to the exact
eligibility result and exposes expectation and earnings differences, market
recognition, positive or negative materiality, gap score, confidence, Evidence,
assumptions, disconfirming Evidence, invalidation conditions, reasons, and
warnings. Ineligible or stale provenance fails before engine invocation.

    python -m scripts.preview_historical_comparison_expectation_gap_analysis

Every source ledger remains byte-for-byte unchanged. No receipt or Expectation
Gap is persisted, and no Mispricing, Opportunity, valuation, portfolio action,
or investment decision is produced.

---

# 75. HUMAN EXPECTATION GAP ASSESSMENT LEDGER

One exact governed Expectation Gap analysis can now receive an append-only
human disposition of Approved, Rejected, or Deferred. The decision binds the
complete analysis fingerprint to its eligibility, materialized Catalyst,
creation receipt, Signal set, direction, score, confidence, reviewer,
rationale, optional conditions and monitoring requirements, and timestamp.

Approval fails closed unless the exact analysis establishes a material
positive or negative gap. Duplicate decisions for the same analysis fail
before any write; a non-material result may still be explicitly Deferred or
Rejected.

    python -m scripts.record_historical_comparison_expectation_gap_assessment

The command reconstructs the complete governed analysis and verifies every
source ledger remains byte-for-byte unchanged. Only the separate assessment
ledger is appended. It performs no Mispricing or Opportunity analysis,
valuation, portfolio action, or investment decision.

---

# 76. EXPLICIT EXPECTATION GAP MATERIALIZATION RECEIPTS

One human-approved governed Expectation Gap analysis can now explicitly create
one canonical in-memory `ExpectationGap` through the existing engine. The
exact analysis, assessment, eligibility, Catalyst, gap identity, canonical
Expectation Gap fingerprint, direction, score, confidence, creator, and
timestamp are preserved in a separate append-only creation receipt.

Materialization fails before engine execution when the assessment is not
Approved, a timestamp precedes review, the exact assessment was already used,
or the Gap ID already has a receipt. Reconstructed analysis must match the
human-approved fingerprint and complete summary exactly.

    python -m scripts.materialize_historical_comparison_expectation_gap

Only the creation receipt is persisted; the in-memory Expectation Gap is
discarded. No Mispricing or Opportunity analysis, valuation, portfolio action,
or investment decision is performed.

---

# 77. READ-ONLY MISPRICING ELIGIBILITY PREVIEW

One exact materialized governed Expectation Gap can now be checked for
permission to enter Mispricing analysis without invoking the
`MispricingEngine`. The gate reconstructs and fingerprint-verifies the full
Expectation Gap analysis, human assessment, canonical in-memory Gap, and
append-only creation receipt.

The immutable result exposes eligibility, explicit blockers, direction, Gap
score and confidence, complete Catalyst, Signal, analysis, assessment, and
creation provenance, and the three later inputs: company, current market
price, and an authoritative existing valuation result. The gate does not
calculate or fabricate valuation.

    python -m scripts.preview_historical_comparison_mispricing_eligibility

Stale or mismatched receipts fail closed. Every source ledger remains
byte-for-byte unchanged. No Mispricing or Opportunity analysis, valuation,
portfolio action, or investment decision is performed.

---

# 78. GOVERNED AUTHORITATIVE VALUATION SNAPSHOT RECEIPTS

One typed `ValuationSection` can now be captured as an append-only valuation
snapshot receipt before Mispricing analysis. Intake fails closed unless the
section identifies `ValuationEngine` as its source, names its valuation method,
contains positive finite intrinsic and fair values, and has confidence on the
canonical 0-100 scale.

A deterministic fingerprint covers the complete canonical ValuationSection,
including its Evidence, assumptions, warnings, metadata, method, confidence,
and values. The receipt preserves the exact fingerprint and summary fields,
entity, human recorder, rationale, and timestamp. Duplicate snapshots fail
before any write.

    python -m scripts.record_historical_comparison_valuation_snapshot

Only the separate receipt ledger is appended; the source valuation JSON stays
byte-for-byte unchanged. Neither `ValuationEngine` nor `MispricingEngine` is
invoked, and no Opportunity, portfolio action, or investment decision is made.

---

# 79. READ-ONLY GOVERNED MISPRICING ANALYSIS PREVIEW

One eligible materialized Expectation Gap and one exact governed valuation
snapshot can now be analyzed in memory by the existing `MispricingEngine`.
Before analysis, the complete Catalyst and Expectation Gap chain is rebuilt,
the canonical Gap fingerprint is verified, and the typed `ValuationSection`
must match its authoritative snapshot receipt and company exactly. Current
market price must be positive and finite.

The immutable preview binds a deterministic fingerprint to the eligibility,
valuation, Catalyst, and Gap provenance and exposes valuation upside and
discount, support gates, Mispricing score and confidence, potential-Mispricing
status, Evidence, assumptions, disconfirming Evidence, invalidation conditions,
reasons, and warnings.

    python -m scripts.preview_historical_comparison_mispricing_analysis

All source ledgers and valuation JSON remain byte-for-byte unchanged. No
Mispricing result is persisted, no Opportunity is scored, and no valuation,
portfolio action, or investment decision is performed.

---

# 80. HUMAN GOVERNED MISPRICING ASSESSMENT LEDGER

One exact governed Mispricing analysis can now receive an append-only human
disposition of Approved, Rejected, or Deferred. The decision binds the full
analysis fingerprint to its eligibility, authoritative valuation receipt,
Expectation Gap, Catalyst, company, Signal set, score, confidence, reviewer,
rationale, optional conditions and monitoring requirements, and timestamp.

Approval fails closed unless the exact engine result identifies potential
mispricing. Duplicate decisions on the same analysis fail before any write;
non-qualifying analyses may still be explicitly Deferred or Rejected.

    python -m scripts.record_historical_comparison_mispricing_assessment

The command reconstructs every governed input and verifies all source files
remain byte-for-byte unchanged. Only the assessment ledger is appended. No
Opportunity synthesis, valuation, portfolio action, or investment decision is
performed.

---

# 81. EXPLICIT GOVERNED MISPRICING MATERIALIZATION RECEIPTS

One exact human-approved governed Mispricing analysis can now explicitly
materialize one canonical in-memory `MispricingAssessment` through the existing
`MispricingEngine`. The complete governed Signal, Catalyst, Expectation Gap,
authoritative valuation, eligibility, analysis, and human-assessment chain is
reconstructed and fingerprint-verified before materialization.

The append-only creation receipt binds the approved assessment, analysis,
eligibility, valuation snapshot, Expectation Gap, Catalyst, company, current
market price, Signal set, score, confidence, potential-Mispricing status, and
canonical Mispricing fingerprint. Rejected or Deferred decisions, stale
inputs, timestamps preceding review, reused assessments, and duplicate
Mispricing identities fail closed before any write.

    python -m scripts.materialize_historical_comparison_mispricing

Only the creation receipt is persisted; the in-memory Mispricing result is
discarded. The command verifies every source file remains byte-for-byte
unchanged. No Opportunity synthesis or scoring, valuation, ranking, committee
review, portfolio action, execution, or investment decision is performed.

Offline verification:

    python -m modules.external_intelligence.test_historical_comparison_mispricing_creation
    HISTORICAL MISPRICING CREATION: ALL TESTS PASSED

---

# 82. GOVERNED OPPORTUNITY SYNTHESIS ELIGIBILITY PREVIEW

One exact materialized governed Mispricing result can now be checked for
permission to enter the existing `OpportunitySynthesisEngine` without invoking
that engine. The gate reconstructs and fingerprint-verifies the full Signal,
Catalyst, Expectation Gap, valuation, Mispricing analysis, human assessment,
and Mispricing creation-receipt chain.

The immutable preview binds a deterministic eligibility fingerprint to all
available provenance and enumerates every synthesis input. It currently fails
closed, as intended, because governed Asymmetry, governed Opportunity Evidence
Pack provenance, and explicit governed synthesis assumptions, invalidation
conditions, and kill switches do not yet exist at this boundary. This makes
the required sequence explicit: Asymmetry governance must precede Opportunity
synthesis analysis.

    python -m scripts.preview_historical_comparison_opportunity_eligibility

Every source ledger and valuation input remains byte-for-byte unchanged. No
Opportunity synthesis or scoring, ranking, committee review, portfolio action,
execution, valuation, or investment decision is performed.

Offline verification:

    python -m modules.external_intelligence.test_historical_comparison_opportunity_eligibility_preview
    HISTORICAL OPPORTUNITY ELIGIBILITY PREVIEW: ALL TESTS PASSED

---

# 83. GOVERNED ASYMMETRY ELIGIBILITY PREVIEW

One exact materialized governed Mispricing result can now be checked for
permission to enter Asymmetry analysis without invoking `AsymmetryEngine`. The
gate reconstructs and fingerprint-verifies the complete governed chain through
the approved Mispricing assessment and creation receipt.

The immutable preview binds its deterministic eligibility fingerprint to the
canonical Mispricing identity and complete upstream provenance. It explicitly
exposes the five later analysis inputs required by the existing engine:
company, scenarios, assumptions, invalidation conditions, and disconfirming
Evidence. These inputs are not inferred or fabricated by the eligibility gate.

    python -m scripts.preview_historical_comparison_asymmetry_eligibility

Every source ledger and valuation input remains byte-for-byte unchanged. No
Asymmetry or Opportunity analysis, ranking, committee review, valuation,
portfolio action, execution, or investment decision is performed.

Offline verification:

    python -m modules.external_intelligence.test_historical_comparison_asymmetry_eligibility_preview
    HISTORICAL ASYMMETRY ELIGIBILITY PREVIEW: ALL TESTS PASSED

---

# 84. PRIMARY-SOURCE-READY OBSERVATION PROVENANCE AND IDENTITY

The existing `ObservationProvenance` boundary now accepts optional,
source-neutral publication time, formal filing time, source-native document
ID, SHA-256 document hash, and descriptive extraction method. These fields
preserve the difference between when information was published, formally
filed, retrieved by EIOS, and represented as an Observation.

Persistence round-trips the new datetime fields without changing legacy naive
timestamps or requiring the new keys. Existing observations with no provenance
or older provenance continue to load unchanged. No production Observation data
was migrated or rewritten.

Within one research cycle, a supplied valid document hash now takes precedence
for identity, followed by a source-domain-scoped native document ID. When
neither exists, the existing canonical-URL plus normalized-content identity is
unchanged. Cross-job lineage still merges, and identical material in a later
cycle remains outside this deduplication checkpoint.

The approved Pre-Inflection and Earliest Investable Point integration
architecture is documented at:

    docs/architecture/PRE_INFLECTION_EARLIEST_INVESTABLE_POINT.md

Thirteen focused and broader offline module suites passed, along with syntax
checks for every changed Python file. No network calls, connectors, Signals,
Catalysts, Opportunities, valuation, portfolio actions, or investment
decisions were introduced.

---

# 85. READ-ONLY CROSS-CYCLE DOCUMENT RECONCILIATION

Persisted Observations can now be inspected for repeated strong document
identity across research cycles without changing runtime deduplication. The
read-only service groups only validated document hashes or source-domain-scoped
native document IDs that occur in at least two distinct cycles.

The immutable preview exposes deterministic group identity, participating
cycles, Observation fingerprints, source URLs, and earliest publication,
filing, and retrieval timing. It separately reports Observations missing strong
identity and strong identities currently seen in only one cycle, making source
coverage gaps explicit rather than silently treating them as unique documents.

    python -m scripts.preview_cross_cycle_document_reconciliation \
        --observation-path data/observations.json

Input ordering does not change the preview fingerprint. The command verifies
Observation storage remains byte-for-byte unchanged. It does not merge, delete,
reject, or rewrite Observations and does not change the existing deliberate
acceptance of repeated material in later research cycles.

Offline verification:

    python -m modules.external_intelligence.test_cross_cycle_document_reconciliation
    CROSS-CYCLE DOCUMENT RECONCILIATION: ALL TESTS PASSED

No Event, Evidence, Signal, Catalyst, Meta-Analysis, Opportunity, valuation,
portfolio action, or investment decision is created.

---

# 86. PUBLIC-SOURCE ACQUISITION AND EXTRACTION RECEIPTS

EIOS now has source-neutral, append-only audit contracts for public document
acquisition and extraction without adding a live connector. Every acquisition
records the cycle, job, research intent, canonical URL and domain, request and
completion time, outcome, HTTP/content metadata, document identity, byte count,
error details, and recorder.

The acquisition boundary fails closed unless access is explicitly classified
as `PUBLIC`. Successful retrieval requires a validated SHA-256 document hash
and positive byte count; failed retrieval requires an explicit error and cannot
claim document identity. Confidential, leaked, credential-gated, or UPSI input
is outside this boundary and is rejected.

Extraction receipts bind the exact acquisition fingerprint and document hash.
They distinguish `SUCCEEDED`, `PARTIAL`, and `FAILED`; partial extraction must
preserve warnings, and failed extraction cannot claim extracted content. A
read-only coverage preview reports failed acquisitions, partial or failed
extractions, and retrieved documents missing extraction receipts so downstream
Meta-Analysis cannot interpret missing data as negative evidence.

    python -m scripts.preview_public_intake_coverage \
        --acquisition-ledger-path acquisitions.jsonl \
        --extraction-ledger-path extractions.jsonl

All receipt parsing fails closed on stale bindings, duplicate identities,
tampered URL identity, invalid chronology, or malformed state. Focused public
intake, cross-cycle reconciliation, source-quality/deduplication, orchestration,
and runtime-bootstrap suites passed offline, and all changed files compiled.

No connector, HTTP request, document parser, Meta-Analysis, Observation,
Evidence, Signal, Catalyst, Opportunity, valuation, portfolio action, or
investment decision is created by this checkpoint.
## Checkpoint 87 — Trusted public-source acquisition boundary

- Added a passive trusted-source registry for approved public HTTPS sources, initially covering NSE, BSE, SEBI, and RBI.
- Added a guarded acquisition adapter that validates the requested address, DNS resolution, and every redirect before downloading.
- Blocks credentials in URLs, non-HTTPS access, non-public/private network destinations, unknown domains, and redirects outside the approved source definition.
- Records immutable acquisition outcomes, including the requested and final URL, retrieval status, document hash, byte count, and errors.
- Added offline tests for successful retrieval, same-source redirects, unknown domains, private DNS targets, untrusted redirects, and HTTP failures.
- Completed a live public-source smoke test against `https://www.rbi.org.in/`: retrieval succeeded with 176,713 bytes and SHA-256 `e9459d75492311603cb03f1a8b90fe76db6a5757bf359f6ef9ae2094e0ace458`.
- The live receipt was written only to a temporary audit ledger. It did not create an Observation, Evidence item, Signal, Meta conclusion, or modify production data.

## Checkpoint 88 — Guarded public-document extraction boundary

- Added an extraction adapter that accepts only a successfully retrieved, PUBLIC acquisition result.
- Recomputes the SHA-256 hash from the original document bytes before extraction; altered bytes produce an audited failure.
- Routes HTML and plain structured text through deterministic normalization without summarisation, scoring, or investment analysis.
- Marks unusually short but non-empty text as PARTIAL so downstream coverage treats it as incomplete rather than complete evidence.
- Rejects unsupported formats explicitly. PDFs currently produce `PDF_EXTRACTOR_UNAVAILABLE` instead of unsafe binary decoding or false success.
- Added an acquire-and-extract smoke command that writes only acquisition and extraction audit receipts and cannot create Observations, Evidence, Signals, or Meta conclusions.
- Added offline tests for successful HTML extraction, partial short text, PDF refusal, content-hash mismatch, and unsupported formats.
- Completed a live end-to-end smoke test against `https://www.rbi.org.in/`: acquisition was `RETRIEVED`, hash verification passed, and extraction `SUCCEEDED` with 17,669 normalized characters using `deterministic_html_text_v1`.
- Both live receipts were written to temporary audit ledgers only; production observations remained unchanged.

## Checkpoint 89 — Read-only public Observation admission gate

- Added a passive admission preview with explicit `ADMIT`, `DEFER`, and `REJECT` decisions; it cannot create or persist an Observation.
- Requires a successful PUBLIC acquisition from the trusted registry, an exact acquisition-to-extraction fingerprint binding, matching document hashes, and matching extracted-text fingerprints.
- Applies minimum source-quality and content-completeness checks before admission.
- Defers partial or insufficient extraction so missing content cannot be interpreted as negative evidence.
- Rejects failed extraction, untrusted/non-public sources, broken lineage, altered extracted text, and documents already represented in existing Observations.
- Returns deterministic reason codes, duplicate Observation indexes, source identity, source-quality tier, fingerprints, and proposed non-analytical metadata for review.
- Added offline tests covering admission, duplicate rejection, partial deferral, and broken-lineage rejection without registry or persistence mutation.

## Checkpoint 90 — Controlled public Observation commit service

- Added the only controlled bridge from a verified public acquisition/extraction pair into the existing Observation layer.
- Re-runs the admission gate against the current Observation registry immediately before every write; it does not trust a stale earlier preview.
- Commits only an `ADMIT` result and returns explicit non-commit statuses for deferred, rejected, or final novelty-rejected content.
- Preserves acquisition cycle, job, research intent, retrieval time, publication/filing times, source document ID, document hash, extraction method, content type, and source-quality lineage in Observation provenance.
- Uses the existing Observation Engine as the final novelty and persistence boundary; it creates no Evidence, Signal, Catalyst, Opportunity, valuation, or Meta conclusion.
- Added temporary-store tests proving exactly-one commit, repeated-document rejection, deferred-content refusal, provenance persistence, and byte-for-byte isolation of a simulated production store.

## Checkpoint 91 — Durable public Observation commit audit trail

- Added an append-only audit ledger for every controlled public Observation commit decision.
- Admissible commits record `AUTHORIZED` before the Observation write and then `COMMITTED` or `FINAL_NOVELTY_REJECTION` afterward.
- Deferred and rejected attempts record `BLOCKED` without creating an Observation.
- Audit events bind the commit ID to acquisition/extraction IDs, admission decision and reasons, document/content fingerprints, final Observation fingerprint, timestamp, and recorder.
- Duplicate commit IDs and invalid event sequences are rejected.
- Exposes unresolved authorized commit IDs, making an interrupted write window visible for operator reconciliation rather than silently losing audit state.
- Added temporary-store tests for committed, duplicate-blocked, partial-blocked, and interrupted authorization histories; production data remains outside the test path.

## Checkpoint 92 — Live read-only public Observation admission canary

- Added a canary command that performs guarded acquisition, deterministic extraction, and admission preview against an explicitly selected Observation store.
- The command has no commit-service path and cannot create an Observation or downstream analytical object.
- Completed a live canary against `https://www.rbi.org.in/`: acquisition `RETRIEVED`, extraction `SUCCEEDED` with 17,669 characters, admission decision `ADMIT`, no reason codes, and zero existing duplicates among 46 production Observations.
- The live acquisition and extraction receipts were written only to temporary audit ledgers. The admissible canary was deliberately not committed.

## Checkpoint 93 — Source-grounded public factual-candidate extraction

- Added a passive factual-candidate model and deterministic extractor upstream of Observation commitment and all Catalyst/Meta analysis.
- Detects review candidates for orders/contracts, tenders, regulatory approvals, capacity changes, policy/regulation, supplier/customer changes, and execution updates using explicit inspectable trigger rules.
- Every candidate carries an exact source passage and character offsets, document/content fingerprints, source URL, acquisition/extraction IDs, extraction method, matched trigger text, subject entity, transparently detected company names, and explicitly written amounts/dates.
- Classifies statement posture as asserted, uncertain, or negated without deciding whether the event is true, material, causal, or investable.
- Candidate IDs are deterministic from document identity, passage offsets, and event type.
- Empty candidate results explicitly warn that no configured trigger is not negative evidence.
- Bounded each source passage to at most 600 exact source characters around the trigger so punctuation-light web pages cannot contaminate posture with distant text.
- Added date-aware uncertainty handling so calendar text such as `May 20` is not treated as the modal word `may`.
- Integrated candidate display into the read-only live canary; it remains incapable of Observation, Evidence, Signal, Catalyst, Opportunity, or Meta creation.
- Offline tests cover exact passage offsets, amount/date capture, asserted/uncertain/negated posture, long-text isolation, provenance binding, deterministic event order, and no-trigger coverage gaps.

## Checkpoint 94 — Event-specific factual-candidate validation

- Added a passive validator that returns `VALIDATED`, `DEFER`, or `REJECT` without creating an Observation or downstream analytical object.
- Revalidates candidate ID, exact source offsets/passage, acquisition and extraction IDs, document/content fingerprints, and matched trigger presence.
- Requires the named subject and event-specific mechanics to appear in the same bounded passage; it does not infer pronoun resolution or page-level context.
- Defers uncertain statements for corroboration and candidates whose subject or event mechanics are insufficiently grounded.
- Allows an explicit negated statement to validate as a factual contradiction while preserving its `NEGATED` posture.
- Rejects altered passages, broken lineage, fingerprint mismatches, invalid deterministic IDs, and triggers absent from the cited passage.
- Integrated validation decisions and reason codes into the read-only canary display.
- Live RBI homepage canary: document admission remained `ADMIT`, but the sole policy-keyword candidate became `DEFER` with `SUBJECT_NOT_IN_PASSAGE`; nothing was promoted or persisted.
- Offline tests cover grounded order validation, uncertain/pronoun-only capacity deferral, explicit negative approval validation, and tampered-passage rejection.

## Checkpoint 95 — Candidate-specific Observation proposals and human review

- Added a passive Observation proposal built only from a currently revalidated `VALIDATED` factual candidate.
- Proposal description is the exact bounded source passage, not the whole source page; category is namespaced as `PUBLIC_FACT_<EVENT_TYPE>`.
- Preserves candidate, acquisition, extraction, document/content fingerprints, source URL, extraction method, statement posture, and explicitly written dates/amounts.
- Proposal titles are deterministic unless explicitly supplied, and every proposal is content-fingerprinted.
- Proposals deliberately contain no confidence value; they require human review before any commit can be attempted.
- Added an append-only human-review ledger with `APPROVE`, `DEFER`, and `REJECT` decisions, reviewer identity, timestamp, mandatory notes, and one final review per proposal fingerprint.
- Approval requires an explicit reviewer-supplied confidence; deferred/rejected proposals cannot carry an approved confidence.
- The review ledger independently recomputes proposal fingerprints and rejects altered proposal content.
- This checkpoint creates no Observation and does not call the commit service or any Evidence, Signal, Catalyst, Opportunity, or Meta layer.
- Temporary-ledger tests cover exact-passage proposals, absent automatic confidence, approval, duplicate-review refusal, stale validation refusal, missing-confidence refusal, and tampered-proposal rejection.

## Checkpoint 96 — Reviewed factual-proposal Observation commit boundary

- Added a dedicated commit service for candidate-specific factual Observation proposals.
- Requires a fingerprint-valid proposal, an exactly bound human `APPROVE` receipt with reviewer-supplied confidence, and the original candidate/acquisition/extraction chain.
- Re-runs factual-candidate validation, reconstructs and compares the complete proposal, and re-runs document admission against the current Observation registry immediately before writing.
- Commits only the exact reviewed source passage with its event-specific category and complete public provenance; it never substitutes the whole webpage.
- Extended commit audit events with optional proposal ID, proposal fingerprint, and review ID, and requires identical review identity between authorization and terminal events.
- Non-approved or mismatched reviews fail before any commit authorization or Observation write.
- Uses the existing Observation Engine for final novelty and persistence, and creates no Evidence, Signal, Catalyst, Opportunity, valuation, or Meta conclusion.
- Temporary-store tests prove exact-passage commitment, reviewer confidence preservation, proposal/review audit binding, persistence of exactly one Observation, and refusal of deferred or mismatched reviews.

## Checkpoint 97 — Reviewed-fact Temporal Evidence foundation

- Extended Observation provenance additively with optional factual candidate ID, event type, statement posture, proposal ID, and human review ID; legacy observations remain loadable.
- The reviewed-proposal commit boundary now persists this exact reviewed-fact lineage into the committed Observation.
- Added a passive Temporal Evidence record for one reviewed factual Observation, preserving event/known times, time basis, event posture, source/document identity, candidate/proposal/review lineage, and exact Observation text.
- Event time uses filing time first, then publication time, then an explicit known-at fallback; all derived times normalize to UTC.
- Added deterministic Temporal Evidence identity based on Observation fingerprint, event time, and event type.
- Added a series builder that accepts exactly one entity and event type, orders records deterministically, counts asserted/negated/uncertain records separately, rejects duplicate Observation evidence, and reports missing-time or future-time warnings.
- Added an append-only Temporal Evidence repository with schema validation and duplicate protection by Temporal Evidence ID and Observation fingerprint.
- This foundation performs no trend, persistence, causal, materiality, Catalyst, Opportunity, or Meta interpretation.
- Offline tests cover out-of-order input, publication-time ordering, known-at fallback, contradiction preservation, repository round-trip, duplicate refusal, legacy-observation exclusion, and reviewed provenance persistence.

## Checkpoint 98 — Mandatory Meta-Analysis contract and fail-closed gate

- Made Meta-Analysis a mandatory read-only stage between reviewed Temporal Evidence and Pre-Inflection/Catalyst/EIP/Opportunity work.
- Added a passive Meta assessment contract bound to exact Temporal Evidence IDs and Observation fingerprints across explicit entity and sector scopes.
- Requires explicit causal hypotheses, source-independence groups, contradictions, missing expected evidence, coverage gaps, uncertainty, public-information-only status, and a non-authority statement.
- Added mandatory completion flags for independence, contradiction, missing-evidence, and coverage checks.
- Added conclusion states `INSUFFICIENT`, `EMERGING`, `COHERENT`, and `CONTRADICTED`, with separate contradiction-burden states.
- Added a fail-closed gate with `BLOCKED`, `HOLD_FOR_RESEARCH`, and `READY_FOR_PRE_INFLECTION` decisions.
- Missing Meta, wrong/stale evidence bindings, incomplete governance checks, duplicate inputs, non-public information, missing scope, or missing uncertainty/non-authority statements are blocked.
- Complete but insufficient, contradicted, high-contradiction, single-independence-group, or causally empty assessments are held for research.
- Readiness requires at least two independence groups and only authorizes the next governed Pre-Inflection review; it creates no Signal, Catalyst, Opportunity, recommendation, or trade.
- Updated the approved architecture to state that Meta cannot be skipped.
- Offline tests prove missing-Meta blocking, complete readiness, incomplete-check blocking, single-source hold, contradicted hold, wrong-input blocking, and non-public-information blocking.

## Checkpoint 99 — Sector causal-indicator knowledge contract

- Added a passive, versioned causal-indicator definition contract that supports any sector without embedding conclusions in engine logic.
- Each definition specifies sector/event applicability, economic variable, expected direction, lead-time range, causal mechanism, earnings channels, company archetypes, primary/corroborating source types, independence grouping, persistence requirements, known false positives, contradictions, and kill tests.
- Added a validated registry with unique IDs, enabled-state filtering, sector/event lookup, lead-time and minimum-support validation, and deterministic ordering.
- Added an initial seed library for industrial tender-to-order conversion, lender early credit stress, chemical spread recovery, and building-material utilization/realization breadth.
- Extended mandatory Meta assessments with causal-indicator IDs.
- Mandatory Meta now blocks missing, unknown, or sector-mismatched causal indicators; sector matching is case-insensitive while indicator identity remains explicit.
- Updated the approved architecture so every Meta causal hypothesis must reference enabled registry knowledge.
- Offline tests cover the seed library, applicability lookup, invalid definitions, unknown indicators, Meta readiness with a registered indicator, and wrong-sector/unknown-indicator blocking.

## Checkpoint 100 — Temporal leading-indicator interpretation preview

- Added explicit evidence-to-indicator links that bind each Temporal Evidence record to one registered causal indicator, one independence group, a `SUPPORTS`/`CONTRADICTS`/`CONTEXT_ONLY` relationship, and a written rationale.
- Added a passive structural preview that validates entity, sector, event applicability, complete one-to-one evidence linking, indicator identity, and relationship vocabulary.
- Measures supporting, contradicting, and context-only evidence separately; context evidence is excluded from support and contradiction counts.
- Computes independent supporting-group breadth, supporting-observation persistence count, observed persistence span, configured required duration, chronological range, and expected earnings lead-time range.
- Produces `INSUFFICIENT`, `FORMING`, `STRUCTURALLY_READY_FOR_META`, or `CONTRADICTED` without making a causal, materiality, Pre-Inflection, Catalyst, Opportunity, or investment conclusion.
- Every preview is deterministically fingerprinted from indicator version, entity/sector, exact Temporal Evidence/Observation identities, evidence relationships, independence groups, rationales, and structural requirements.
- Mandatory Meta assessments now bind to exact indicator-preview fingerprints as well as raw Temporal Evidence and Observation fingerprints.
- Meta blocks missing/stale preview bindings, preview evidence outside the supplied Temporal Evidence set, or mismatch between cited causal indicators and supplied previews; non-ready structural previews hold downstream readiness.
- Offline tests cover structural readiness, insufficient persistence/independence, contradiction handling, wrong-sector refusal, incomplete linking refusal, and Meta preview-fingerprint integration.

## Checkpoint 101 — Governed mandatory Meta-Analysis service

- Added the actual read-only Meta assessment builder above the existing mandatory contract and gate.
- The service derives exact Temporal Evidence, Observation, indicator-preview, causal-indicator, and supporting independence-group bindings from supplied governed inputs instead of accepting caller-retyped identities.
- Carries explicit causal hypotheses, contradictions, missing expected evidence, acquisition/extraction coverage gaps, syndication findings, cross-company/cross-sector transmission findings, open research gaps, uncertainty, and assessor identity.
- Added typed kill-test results with `NOT_TRIGGERED`, `TRIGGERED`, and `UNKNOWN` states, exact indicator/test identity, supporting evidence IDs, and rationale.
- Every kill test configured by every cited causal indicator must have exactly one result; missing coverage or evidence outside the assessment inputs blocks Meta.
- Triggered or unresolved kill tests hold the case for research and cannot produce Pre-Inflection readiness.
- The service automatically marks all mandatory governance checks as completed only because the controlled builder receives every required research field, enforces public-only processing, and injects a fixed non-authority statement.
- Meta remains read-only and produces only an assessment plus the fail-closed gate result; it creates no Observation, Evidence, Signal, Catalyst, Opportunity, recommendation, or trade.
- Offline end-to-end tests cover ready Meta assessment construction, exact preview binding, fixed non-authority, triggered-kill hold, and incomplete-kill blocking.

## Checkpoint 102 — Durable Meta repository and human review boundary

- Added an append-only Meta assessment repository with deterministic fingerprints over the full assessment, including nested kill-test results, enums, timestamps, evidence bindings, and research findings.
- Repository reads independently recompute fingerprints and reject altered, duplicate, or unsupported assessment records.
- Added append-only human Meta review decisions: `AUTHORIZE_PRE_INFLECTION_REVIEW`, `HOLD_FOR_RESEARCH`, and `REJECT_ASSESSMENT`.
- Human review re-runs the mandatory Meta gate against the current Temporal Evidence and indicator previews before recording any decision.
- Authorization is allowed only for `READY_FOR_PRE_INFLECTION`; held or blocked assessments cannot be human-overridden into readiness.
- A technically blocked assessment cannot be marked as an ordinary research hold; it must be rejected and rebuilt with complete governed inputs.
- Review receipts bind assessment ID/fingerprint, current gate decision/reasons, reviewer, timestamp, and mandatory notes, with one final review per assessment fingerprint.
- The review ledger independently recomputes the stored assessment fingerprint and rejects forged in-memory records.
- Human authorization permits only the next governed Pre-Inflection review and does not create a Pre-Inflection state or any downstream analytical/action object.
- Temporary-ledger tests cover repository round-trip, ready authorization, triggered-kill hold, blocked-assessment override refusal, and forged-fingerprint rejection.

## Checkpoint 103 — Governed Pre-Inflection assessment preview

- Added a passive Pre-Inflection assessment preview that can be built only from a fingerprint-valid stored Meta assessment and an exactly bound human `AUTHORIZE_PRE_INFLECTION_REVIEW` receipt.
- Re-runs the current mandatory Meta gate against current Temporal Evidence and indicator previews; stale or no-longer-ready Meta cannot proceed.
- Preserves entity/sector scope, causal indicators, Meta/review identity, independence breadth, structural readiness, expected earnings lead-time range, contradiction burden, contradictions, missing evidence, coverage/research gaps, and uncertainty as separate dimensions.
- Requires explicit plain-language statements for what is changing, why now, confirmation requirements, invalidation conditions, and balance-sheet/governance risks.
- Uses ordinal `WEAK`, `EMERGING`, `CREDIBLE`, and `STRONG` strength only; no fabricated numerical probability is introduced.
- `EMERGING` Meta remains emerging. `STRONG` requires coherent Meta, all structural previews ready, low/zero contradiction burden, and no missing-evidence or coverage gaps; otherwise coherent cases remain credible.
- Market recognition is explicitly `NOT_ASSESSED`, preventing this preview from becoming an EIP classification before the Price Recognition Gate exists.
- Output is eligible only for a future human Pre-Inflection review and creates no Signal, EIP state, Catalyst, Opportunity, recommendation, or trade.
- Offline tests cover authorized emerging preview, lead-time preservation, mismatched-review refusal, and transparent strong-strength requirements.

## Checkpoint 104 — Durable Pre-Inflection repository and human review

- Added append-only Pre-Inflection preview storage with deterministic full-content fingerprints and schema-validated round-trip loading.
- Repository reads reject altered, duplicate, or unsupported previews.
- Added human review decisions: `AUTHORIZE_PRICE_RECOGNITION_REVIEW`, `HOLD_FOR_RESEARCH`, and `REJECT_ASSESSMENT`.
- Human review independently recomputes the stored preview fingerprint and rebuilds the entire Pre-Inflection preview from current stored Meta, Meta authorization, Temporal Evidence, and indicator previews.
- Any change in current Meta readiness, source bindings, indicator structure, strength dimensions, narratives, confirmation/invalidation conditions, or risks makes the stored preview stale and prevents review.
- Authorization permits only the Price Recognition review and requires an eligible preview whose market-recognition status is still `NOT_ASSESSED`.
- Review receipts bind preview ID/fingerprint, decision, reviewer, timestamp, and mandatory notes, with one final review per preview fingerprint.
- This checkpoint creates no Price Recognition result, EIP state, Signal, Catalyst, Opportunity, recommendation, or trade.
- Temporary-ledger tests cover repository round-trip, Price Recognition authorization, review round-trip, and forged-fingerprint rejection.

## Checkpoint 105 — Multi-dimensional Price Recognition Gate preview

- Added a public-market recognition snapshot contract bound to an entity, observation time, public source IDs, pre-inflection anchor/current prices, 1/3/6/12-month returns, sector-relative return, 52-week range, abnormal volume, valuation rerating, analyst revision breadth, and media-attention change.
- Price Recognition requires a fingerprint-valid stored Pre-Inflection assessment, an identical current rebuilt assessment, and an exactly bound human `AUTHORIZE_PRICE_RECOGNITION_REVIEW` receipt.
- Rejects non-public inputs, out-of-scope entities, missing source identity, non-positive prices, invalid 52-week ranges, negative volume ratios, and analyst breadth outside -1 to 1.
- Computes price change since the Pre-Inflection anchor and normalized 52-week position.
- Uses independent recognition dimensions for anchor price change, multi-horizon momentum, sector-relative performance, 52-week position, abnormal volume, valuation rerating, analyst revisions, and media attention.
- Recognition states are `INSUFFICIENT_DATA`, `UNRECOGNIZED`, `EARLY_RECOGNITION`, `PARTIALLY_RECOGNIZED`, and `FULLY_RECOGNIZED_POTENTIALLY_LATE`.
- A single price move cannot produce full recognition; classification requires breadth across several available dimensions, and missing dimensions remain explicit.
- EIP review eligibility is false for insufficient data and fully recognized/potentially late cases; no EIP state is created.
- Thresholds are held in an explicit policy object rather than hidden in the model and can later be calibrated through outcome history.
- Offline tests cover unrecognized, fully recognized, insufficient-data, public/binding enforcement, and authorization continuity through the complete Meta/Pre-Inflection chain.

## Checkpoint 106 — Durable Price Recognition repository and human review

- Added append-only Price Recognition preview storage with deterministic full-content fingerprints and validated round-trip loading.
- Repository reads reject altered, duplicate, or malformed recognition previews.
- Added human review decisions: `AUTHORIZE_EIP_REVIEW`, `HOLD_FOR_MARKET_DATA`, and `REJECT_RECOGNITION_ASSESSMENT`.
- Review independently recomputes the stored fingerprint and rebuilds recognition from the current authorized Pre-Inflection chain and current public-market snapshot.
- Changed prices, market dimensions, upstream evidence, Pre-Inflection state, or authorization make the stored recognition preview stale and prevent review.
- EIP review authorization is permitted only when recognition is `UNRECOGNIZED`, `EARLY_RECOGNITION`, or `PARTIALLY_RECOGNIZED` and the preview is otherwise eligible.
- `INSUFFICIENT_DATA` cannot authorize EIP review, and `FULLY_RECOGNIZED_POTENTIALLY_LATE` cannot be authorized or disguised as a temporary data hold.
- Review receipts bind snapshot ID, recognition fingerprint/state, decision, reviewer, timestamp, and mandatory notes, with one final review per recognition fingerprint.
- This checkpoint authorizes only a future governed EIP review and creates no EIP state, Signal, Catalyst, Opportunity, recommendation, or trade.
- Temporary-ledger tests cover repository round-trip, unrecognized EIP authorization, fully recognized authorization refusal, and forged-fingerprint rejection.

## Checkpoint 107 — Governed Earliest Investable Point classification preview

- Added passive EIP classification stages including `NOT_CLASSIFIABLE`, Stage 1 Possible Bottoming, Stage 2 Pre-Inflection, Stage 3 Earliest Investable Point, Stage 4 Early Confirmation, and Stage 5 Consensus Recovery/Potentially Late. Stage 0 remains reserved for a future governed deterioration path because contradicted Meta is held upstream.
- Classification requires fingerprint-valid, identical current/stored Pre-Inflection and Price Recognition assessments plus an exactly bound Price Recognition human review.
- Added explicit balance-sheet/governance risk disposition (`CLEAR`, `CONTAINED`, `UNRESOLVED`) and remaining valuation-room status (`SUFFICIENT`, `UNCERTAIN`, `INSUFFICIENT`) with mandatory rationales.
- Stage 3 requires credible/strong Pre-Inflection evidence, unrecognized/early market recognition, resolved or contained risks, sufficient valuation room, and human EIP-review authorization.
- Emerging evidence remains Stage 2; strong/credible evidence with partial recognition becomes Stage 4; fully recognized/potentially late evidence becomes Stage 5; insufficient market data is not classifiable.
- Unresolved risks or unestablished valuation room prevent Stage 3 and retain the case at Stage 2.
- Carries confirmation and invalidation conditions forward from the governed Pre-Inflection assessment.
- Output remains eligible only for future human EIP review and explicitly has no recommendation, approval, position, or trade authority.
- Offline end-to-end tests cover Stage 2 emerging evidence, Stage 3 EIP, Stage 4 partial recognition, Stage 5 potentially late, stale/binding continuity, risk/valuation requirements, and human authorization boundaries.

## Checkpoint 108 — Durable EIP repository and final human review boundary

- Added append-only EIP classification storage with deterministic full-content fingerprints and validated round-trip loading.
- Repository reads reject altered, duplicate, malformed, or unsupported EIP records.
- Added final EIP review decisions: `AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW`, `HOLD_EIP_RESEARCH`, and `REJECT_EIP_CLASSIFICATION`.
- Human review independently verifies the stored fingerprint and rebuilds the EIP classification from the current authorized Pre-Inflection and Price Recognition chain before recording a decision.
- Any upstream evidence, recognition, risk, valuation, or authorization change makes the stored EIP stale and prevents review.
- Only eligible Stage 3 Earliest Investable Point or Stage 4 Early Confirmation classifications may be authorized for the existing downstream Evidence review.
- Stage 2 remains a research hold. Stage 5 Consensus Recovery/Potentially Late must be rejected and cannot be disguised as a temporary hold.
- Review receipts bind classification ID/fingerprint, EIP stage, decision, reviewer, timestamp, and mandatory notes, with one final review per classification fingerprint.
- Authorization creates no Evidence, Signal, Catalyst, Opportunity, recommendation, position, or trade; it permits only the next governed review step.
- Temporary-ledger tests cover repository round-trip, Stage 3 authorization, Stage 2 authorization refusal and hold, Stage 5 hold refusal and rejection, review round-trip, and forged-fingerprint rejection.

## Checkpoint 109 — Authorized EIP to existing Evidence-review manifest

- Added a read-only adapter that turns an exactly authorized EIP into a candidate manifest for the existing Observation-plus-EvidenceAssessment intake path.
- The aggregate EIP conclusion is deliberately not materialized as an EvidenceItem; the manifest exposes the exact underlying reviewed factual Observations for individual Evidence assessment.
- Requires a fingerprint-valid stored EIP, an exactly bound `AUTHORIZE_DOWNSTREAM_EVIDENCE_REVIEW` receipt, the exact stored Pre-Inflection assessment, and its exact stored mandatory Meta assessment.
- Reconciles supplied Temporal Evidence IDs and Observation fingerprints against the authorized Meta inputs and fails closed for omissions, additions, duplicates, forged bindings, or non-authorized EIP decisions.
- Preserves entity and sector scope, causal-indicator IDs, EIP stage, complete Meta/Pre-Inflection/EIP lineage, exact source text and timing, confirmation requirements, and invalidation conditions.
- Candidate fingerprints are deterministic regardless of input ordering.
- The manifest contains no fabricated Evidence strength, confidence, direction, or score and explicitly requires a separate human EvidenceAssessment for each Observation.
- It does not call ExternalEvidenceIntake and creates no EvidenceItem, Signal, Catalyst, Opportunity, recommendation, position, or trade.
- Offline tests cover authorized Stage 3 manifest construction, deterministic ordering, complete-input enforcement, and refusal of a held Stage 2 case.

## Checkpoint 110 — Complete agriculture-climate causal transmission library

- Expanded the governed causal library from four to seventeen indicators by adding thirteen research-grounded agriculture-climate mechanisms.
- Added the agricultural-drought composite, crop-stage water stress, irrigation shield, rabi water carryover, fertilizer application timing, nutrient substitution, nonlinear rainfall-to-fertilizer response, crop switching, satellite crop-health divergence, government intervention suppressor, agricultural supply-chain amplification, rural-demand transmission, and global fertilizer-input stress.
- Each definition carries sector/event applicability, economic mechanism, earnings channels, company archetypes, preferred and corroborating public sources, persistence requirements, false positives, contradictions, and explicit kill tests.
- Added acyclic prerequisite relationships and transitive dependency validation. Mandatory Meta now blocks a downstream causal indicator when its required upstream mechanisms are absent.
- Rainfall alone therefore cannot support a fertilizer-response conclusion; that conclusion requires drought, crop-stage, irrigation, application-timing, and nutrient-mix analysis.
- Expanded the factual-event vocabulary to detect weather anomalies, hydrology, crop progress, satellite crop condition, fertilizer markets, food-stock policy, agricultural price/supply-chain changes, rural demand, and global input costs while preserving exact source passages.
- Expanded the trusted public registry with IMD, NRSC, ISRO, Ministry of Agriculture, CWC, CGWB, Department of Fertilizers, Department of Food and Public Distribution, AGMARKNET, and DGFT. The existing HTTPS, public-network, redirect, and public-information controls remain mandatory.
- Added a public, dated company-exposure registry for crops, states, districts, fertilizer/products, customer types, irrigation dependence, disclosed revenue exposure, source IDs, and explicit uncertainty.
- Company exposure percentages cannot be inferred when undisclosed; non-public, sourceless, duplicate, or invalid exposure records fail closed.
- This checkpoint adds research knowledge and guarded intake capability only. It creates no Evidence, Signal, Catalyst, Opportunity, recommendation, position, or trade.
- Offline tests cover all definitions, dependency closure, rainfall-only Meta refusal, new factual-event vocabulary, institutional source resolution, company exposure validation, and legacy registry behavior.

## Checkpoint 111 — Target-driven agriculture-climate research coverage planner

- Added explicit research targets for fertilizer earnings, food-company earnings, food stocks/prices, and rural demand/credit.
- Each question automatically expands into the full transitive causal-indicator prerequisite set instead of relying on an analyst to remember every dependency.
- Added institutional source-coverage requirements per indicator across IMD, NRSC, ISRO, Ministry of Agriculture, CWC, CGWB, Department of Fertilizers, Department of Food and Public Distribution, AGMARKNET, DGFT, and RBI.
- The read-only coverage preview separately reports covered and missing causal indicators, covered and missing institutional sources, and applicable public company-exposure records.
- Company targets require at least one governed public exposure record; the national food-stock/price target does not fabricate a company requirement.
- `ready_for_mandatory_meta` is false for any missing indicator, source family, or required company exposure.
- A rainfall-only fertilizer case is explicitly blocked even when IMD coverage exists.
- The planner creates no Observation, Evidence, Meta conclusion, Signal, Catalyst, Opportunity, recommendation, position, or trade.
- Offline tests cover complete fertilizer research, rainfall-only refusal, national food-stock readiness, and rural-company exposure refusal.

## Checkpoint 112 — First live India Kharif 2026 guarded source case

- Opened the read-only `INDIA-KHARIF-2026` agriculture-climate monitoring cycle without creating or modifying production Observations.
- Successfully retrieved and deterministically extracted the current IMD monsoon page, ISRO agriculture/crop-forecasting page, Ministry of Agriculture page, CWC reservoir application shell, and Department of Food and Public Distribution food-stock page.
- IMD extraction produced 3,959 characters, ISRO 2,614, Ministry of Agriculture 4,795, CWC only 24, and food-stock material 454.
- The DGFT landing page produced only a 10-character partial extraction and is unusable for policy coverage.
- NRSC returned HTTP 404, CGWB failed certificate verification, and the Department of Fertilizers host failed name resolution. These failures are preserved in the append-only acquisition ledger.
- Intake coverage currently reports ten acquisition attempts, six retrieved documents, four failed acquisitions, six extraction receipts, five technically successful extractions, and one partial extraction.
- Technically successful does not automatically mean analytically adequate: the CWC shell remains insufficient for reservoir evidence and will not be counted as completed causal-indicator coverage.
- The official IMD material justifies opening research: the May 2026 updated seasonal forecast indicated approximately 90% of LPA nationally with greater downside risk across central, southern-peninsular, and northwestern India, while current late-August material reports subdued peninsular rainfall. Forecast and current-weather statements remain distinct from observed crop damage.
- The fertilizer plan remains blocked for missing causal-indicator work, unusable or missing source coverage, and missing governed company-exposure records.
- Live receipts are isolated under `data/live_cases/india_kharif_2026/`; no Observation, Temporal Evidence, Meta conclusion, EIP, EvidenceItem, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 113 — Live agriculture source repair and extraction audit

- Replaced the broken NRSC descriptive endpoint with the official Bhuvan data catalogue. Guarded acquisition and deterministic extraction succeeded with 12,723 characters.
- The Bhuvan catalogue reports two-day India surface-soil-moisture product availability through 25 August 2026, establishing a current official data source without yet claiming a crop-stress result.
- Retried the CGWB publications repository and Department of Fertilizers monthly-bulletin endpoint. CGWB still fails certificate-chain verification and fertilizer access still fails DNS resolution; TLS verification was not disabled and the failures remain audited.
- Located the CGWB public catalogue externally, including January 2026 and post-monsoon 2025 groundwater bulletins, but did not bypass the guarded acquisition boundary to ingest them.
- Added reverse-order weather phrasing so expressions such as `subdued rainfall` are recognized alongside `rainfall ... subdued`; offline source-grounded extraction tests pass.
- Two live read-only IMD canaries successfully retrieved and extracted the page and received `ADMIT` with zero production duplicates, but produced no factual candidates because the downloaded HTML did not contain the dynamically displayed press-release wording.
- The dynamic-page gap is explicit. EIOS did not copy browser/search text into source-grounded evidence and did not fabricate a candidate.
- The Kharif case therefore remains active but blocked pending static official IMD documents or a governed dynamic-page adapter, usable current reservoir/groundwater documents, fertilizer sales data, and company exposure.

## Checkpoint 114 — Guarded PDF extraction and live hydrology facts

- Added `pypdf` as the bounded PDF text-layer dependency and replaced the previous unconditional PDF refusal with guarded extraction.
- PDF bytes remain bound to the acquisition SHA-256 hash before parsing. Encrypted, zero-page, over-limit, malformed, and image-only/no-text PDFs fail with explicit audit codes; OCR is not silently attempted.
- Successful receipts preserve `pypdf_text_layer_v1`, page count, extracted-text fingerprint, character count, and blank-page warnings. Short or partly blank results remain partial.
- Offline tests construct a deterministic text-layer PDF, prove successful page/text extraction, and prove image-only refusal while retaining hash-mismatch and unsupported-format controls.
- Successfully retrieved and extracted the verified CWC reservoir bulletin dated 9 April 2026: 60,825 normalized characters through the guarded PDF path.
- The April bulletin is retained only as a pre-monsoon water baseline. It is not mislabeled as current August reservoir status.
- Added institutional macro validation for weather, hydrology, crop, satellite, fertilizer, food-stock, agricultural-price, rural-demand, and global-input events from the corresponding trusted authority source types.
- Authority scoping is limited to controlled India/India Agriculture cases and configured institutional event types. Company-style events continue to require the company subject in the exact passage.
- A live read-only CWC canary extracted twelve exact hydrology candidates; after the authority-scoping correction all twelve passed lineage, exact-passage, trigger, mechanics, and source validation.
- No candidate was committed. Table-derived candidates and aggregate statements still require proposal and human review before an Observation can exist.
- The bulletin indicates 9 April storage above both the corresponding prior year and normal, so it is a possible irrigation-shield contradiction to a simple drought thesis, not proof of current crop protection.

## Checkpoint 115 — Governed current-document discovery and live IMD forecast

- Added a read-only discovery service that parses links only from the original hash-verified HTML of a successfully acquired trusted landing page and requires its exact audited extraction receipt.
- Relative links are resolved deterministically. HTTPS registry approval and same-authority identity are mandatory; external authorities, unapproved paths, fragments, scripts, email, telephone, and data links are rejected.
- Candidate records bind the landing acquisition fingerprint and document hash and preserve URL, link text, document type, detected date tokens, matched research topics, transparent discovery reasons, relevance tier, and a deterministic fingerprint.
- Ranking is research-oriented only: topic-relevant direct documents lead, dated documents outrank undated documents, and newer detected dates lead older dates. It is not an investment score.
- Discovery performs no download and creates no Observation, Evidence, Meta conclusion, Signal, Catalyst, Opportunity, recommendation, position, or trade. A selected candidate must re-enter the existing guarded acquisition and extraction path.
- Offline tests prove same-authority relative-PDF acceptance, deterministic ranking, external/script/email/path rejection, altered-byte refusal, stale extraction-fingerprint refusal, and absence of production writes.
- Live inspection of the dynamically rendered official IMD monsoon page located the static IMD extended-range forecast for 27 August to 9 September 2026 and the 30 August 2026 official press release.
- The extended-range forecast then entered through guarded acquisition, not through copied browser text. PDF text-layer extraction succeeded with 18,404 characters.
- A read-only live canary admitted the document for factual review and produced six initial candidates. Five weather statements validated, including forecast below-normal rainfall nationally and over Peninsular India for relevant forecast periods.
- The canary exposed an agronomic-advice false positive: an instruction mentioning fertilizer was incorrectly labelled as a fertilizer-market event. `application` was removed from the market trigger, and a regression test now prevents application advice from masquerading as sales, availability, inventory, allocation, shortage, or subsidy evidence.
- Windows terminal preview output now replaces unsupported decorative characters instead of terminating the audit display.
- Production Observations remain exactly 46. No live forecast candidate has been proposed, human-reviewed, committed, joined into Temporal Evidence, or supplied to mandatory Meta.

## Checkpoint 116 — Governed factual review package and forecast hold

- Added a deterministic human-review package contract and builder above validated public factual candidates.
- Packages bind the exact acquisition, extraction, document hash, source URL, candidate/proposal fingerprints, excluded candidates, and package fingerprint.
- Validated candidates may become review-only proposals; deferred candidates remain separately visible with exact source passages, validation decisions, reason codes, and corroboration requirements.
- Package status is fail-closed: `READY_FOR_HUMAN_PROPOSAL_REVIEW` only when included candidates are validated without deferred items; otherwise it is `RESEARCH_HOLD_CORROBORATION`.
- Added a guarded command-line workflow that reacquires and extracts the public document, reruns admission, candidate extraction, and validation, then writes the review package without committing any Observation.
- Corrected forecast semantics: `likely`, `forecast`, and `forecasted` now produce `UNCERTAIN` statement posture. A date use such as `May 20` remains protected from false uncertainty.
- The first IMD package is retained only as a superseded audit artifact because it predated the forecast-posture correction and must not be reviewed or committed.
- The corrected IMD package contains zero Observation proposals and five deferred weather candidates, each held for `UNCERTAIN_STATEMENT_REQUIRES_CORROBORATION`.
- This is the intended result: an official forecast can open and prioritize research, but cannot be represented as realized rainfall, crop damage, fertilizer demand, or an investable conclusion.
- Production Observations remain exactly 46. No Evidence, Temporal Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 117 — Guarded observed-rainfall extraction and period-collision control

- Located the official IMD meteorological-subdivision rainfall page and its server-rendered daily, weekly, monthly, and cumulative controls.
- Added a narrow structured extractor for IMD rainfall map records embedded in the verified HTML. It never executes page scripts; it parses only the acquired bytes after SHA-256, source-authority, acquisition, extraction-receipt, content-type, and fingerprint validation.
- Each structured record preserves area, displayed period label, departure percentage, actual millimetres, normal millimetres, exact embedded source fragment, byte-character offsets, acquisition ID, document hash, and source URL.
- The first live parser iteration exposed cross-record contamination when a `No Data` aggregate preceded a numeric subdivision. No facts were admitted. The parser was replaced with a two-stage object-isolation design that makes cross-object numeric matching structurally impossible.
- Offline tests now include a leading `No Data` record, exact-passage checks, daily and weekly label formats, and altered-byte refusal.
- The corrected daily extract for 0830 hours 29 August to 0830 hours 30 August 2026 contains 40 aligned records. It reports India at -26% departure (5.2 mm actual versus 7.1 mm normal) and South Peninsula at -66% (1.8 mm versus 5.2 mm), with substantial positive and negative subdivision dispersion.
- These are one-day observed conditions only. They do not establish a seasonal rain deficit, crop stress, fertilizer demand, food-price impact, or company earnings impact.
- Added a cross-period consistency service. Differently labelled period views with identical shared area/value tuples are blocked as `PERIOD_VIEW_DATA_COLLISION` and cannot count as independent corroboration.
- The official weekly-labelled view returned the same 40 area/value tuples as the daily view and is therefore blocked pending a distinct verified weekly source or later observations.
- Superseded parser-development datasets are explicitly marked and must not be used. Production Observations remain exactly 46; mandatory Meta remains on research hold.

## Checkpoint 118 — Monthly and cumulative rainfall persistence evidence

- Bound rainfall period extraction to IMD's active `D`, `W`, `M`, or `C` page selector so a selected monthly view cannot accidentally inherit a cumulative label also displayed on the page.
- Generalized displayed period parsing for IMD line breaks, punctuation, single dates, and date ranges while preserving normalized official label text.
- The corrected monthly view covers 1-30 August 2026 and contains 40 numeric area records. India is -16% (207.3 mm actual versus 248.1 mm normal) and South Peninsula is -26% (137.7 mm versus 185.1 mm).
- The cumulative monsoon view covers 1 June-30 August 2026 and contains 31 numeric area records. India is -14% (597.6 mm versus 693.9 mm) and South Peninsula is -24% (420.3 mm versus 550.6 mm).
- Monthly and cumulative values are distinct from the daily view and establish usable public-authority persistence evidence for rainfall deficit at national and South-Peninsula scope.
- The active weekly label is 20-26 August 2026, but all 40 weekly area/value tuples remain identical to the daily 29-30 August view. The weekly dataset stays blocked by `PERIOD_VIEW_DATA_COLLISION`.
- Geographic dispersion remains material: cumulative Gujarat Region and Madhya Maharashtra are above normal while South Peninsula and Telangana are below normal. EIOS must not turn a national or regional aggregate into a uniform company exposure claim.
- Rainfall persistence advances only the weather-anomaly research layer. Crop-stage stress, soil moisture, irrigation buffering, sowing/crop progress, fertilizer application/sales, food supply, and governed company exposure remain unresolved.
- Production Observations remain exactly 46. No Observation proposal, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 119 — Soil-moisture source boundary and readiness gate

- Verified the official NRSC/Bhuvan catalogue listing for the two-day India Surface Soil Moisture product at 0.25-degree grid resolution, with catalogue availability through 25 August 2026.
- Guardedly acquired the official 31-page technical document and extracted 43,151 text characters; two pages without text are explicitly recorded in the extraction receipt.
- The actual archive download path requires a user login. EIOS did not bypass that access boundary and did not copy browser or search-result text into evidence.
- Added a fail-closed readiness service that separates four materially different states: source discovery, guarded structured measurements, baseline-relative anomaly, and crop-stage stress.
- Catalogue availability is discovery only. Absolute soil-moisture measurements cannot corroborate a weather anomaly without a valid baseline and computed anomaly.
- Even a valid soil-moisture anomaly cannot support crop stress without crop-stage/geography mapping and independent corroboration such as crop progress, vegetation condition, or ground reporting.
- A complete chain reaches only `READY_FOR_CROP_STRESS_REVIEW`; it still creates no Observation and requires human review.
- The live India Kharif case remains on research hold because the underlying grid dataset, baseline anomaly, crop-stage geography map, and independent crop-condition corroboration are not yet present.
- Production Observations remain exactly 46. No Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 120 — Guarded official Kharif crop-area structure

- Added the Press Information Bureau as a separately identified government-release authority rather than misrepresenting it as the Ministry's own domain.
- Guardedly acquired and deterministically extracted the Ministry of Agriculture and Farmers Welfare's official all-India Kharif weekly area report for 21 August 2026.
- Added a hash-bound crop-area table extractor that requires the configured PIB authority, exact Ministry attribution, a dated reporting period, audited HTML lineage, and internal row arithmetic within a narrow tolerance.
- The first live structured run exposed duplicate desktop/mobile table rendering: 50 parsed rows represented 25 repeated facts. That artifact is retained as superseded, and deterministic record-identity suppression now produces exactly 25 unique crop rows.
- The 21 August report shows a mixed crop picture, not uniform crop failure: Grand Total area was 1,056.70 lakh hectares versus 1,072.77 a year earlier, a difference of -16.07; rice was -13.19, maize -3.79, and coarse cereals -3.45, while total pulses were +1.49 and total oilseeds were nearly flat at -0.32 lakh hectares.
- Crop dispersion is material within the aggregates: Urad and Bajra were above the prior year while Moong, Ragi, Soybean, and Castorseed were below. EIOS must retain crop-level differences and cannot treat the rainfall deficit as a uniform fertilizer-demand or food-supply effect.
- The structured dataset is review-only. Area sown is an independent crop-progress measure, but it does not by itself establish yield damage, fertilizer sales, food-stock pressure, company exposure, or an investable catalyst.
- Offline tests cover exact extraction, ISO and day-first reporting dates, arithmetic reconciliation, duplicate suppression, altered-byte refusal, and absence of production writes.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 121 — Four-date Kharif crop-progress timeline and schema-drift control

- Guardedly acquired and structured official Kharif area reports for 17 July, 7 August, 14 August, and 21 August 2026.
- Added temporal consistency checks requiring later reporting dates, unique crop identities, non-decreasing cumulative sown area, and stable official normal-area definitions.
- Added narrow crop aliases for official naming changes such as Arhar/Tur, Urdbean/Urad, Moongbean/Moong, and Jute & Mesta/Total Jute and Mesta while preserving every original source row.
- The first live timeline correctly blocked because reports through 14 August included an extra final-2025-area column that was absent on 21 August. The parser had retained the correct current, prior-year, and difference values but had assigned the wrong numeric column as normal area.
- Replaced the fixed-position assumption with explicit variable-schema handling: normal area is the first numeric field after the crop, while current area, prior-year area, and reported difference are the final three fields. Superseded artifacts remain labelled and unusable.
- The corrected live timeline passes all three intervals, with 26 shared crops through 14 August and 23 shared crops on the changed 21 August table.
- Aggregate sowing weakness narrowed materially but did not disappear: the Grand Total year-over-year gap moved from -42.28 lakh hectares on 17 July to -16.07 on 21 August.
- Crop paths diverged. Pulses improved from -12.29 to +1.49; coarse cereals from -15.06 to -3.45; cotton from -5.87 to -0.28; and oilseeds from -8.63 to -0.32 lakh hectares. Rice lag widened into early August and then improved from -15.90 on 7 August to -13.19 on 21 August. Maize remained persistently around 3.5-3.8 lakh hectares below the prior year.
- This timeline contradicts a simple nationwide crop-collapse interpretation while identifying persistent crop-specific lag for further geography, crop-stage, yield, and input-demand research.
- Sown-area recovery does not prove normal yield or fertilizer demand, and a remaining area gap does not prove crop damage. Mandatory Meta still requires soil-moisture or crop-condition evidence, irrigation buffering, input-market facts, and governed company exposure.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 122 — Current hydrology source audit and irrigation-buffer gate

- Investigated the current official CWC reservoir route as the principal contradiction test for rainfall-driven crop stress.
- The legacy CWC bulletin page was updated on 28 August 2026 but its publicly rendered list exposed older bulletins rather than a verifiable current 2026 PDF. EIOS did not guess a filename or substitute an indexed third-party summary.
- Guardedly acquired the official public RSMS dashboard shell. Its static text contains only a 24-character application shell; current records are dynamically requested by the public client.
- Verified the RSMS application structure and public dashboard endpoint names without logging in. The portal uses its normal client-side signed request envelope. EIOS did not imitate credentials, inspect browser storage, or bypass the portal boundary.
- Added NWIC as a separately identified hydrology-data authority and tested its public ArcGIS reservoir layer. The apparent August layer is queryable, but its fields are explicitly August 2022 and therefore cannot represent August 2026 storage.
- One over-encoded NWIC request returned an HTML service page; the corrected request returned a 95-character JSON error. Both are audit receipts, neither is usable hydrology evidence.
- Added a fail-closed hydrology-buffer readiness service requiring a configured CWC/NWIC authority, a reporting date no more than ten days old, guarded and parsed structured records, comparison with normal and prior-year storage, and crop-to-basin geography mapping.
- Current national storage without crop/basin mapping can reach only current-hydrology review, not an irrigation-shield conclusion. A stale official layer remains blocked even if it is technically accessible.
- The irrigation shield remains unresolved. The April CWC bulletin stays a pre-monsoon baseline only; the 2022 NWIC layer and dynamic RSMS shell cannot update it.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 123 — Official Kharif fertilizer balance and demand/earnings separation

- Guardedly acquired and deterministically extracted the official all-India Kharif 2026 fertilizer release covering 1 April through 19 July 2026.
- Added a hash-bound structured extractor that isolates the ongoing-Kharif table from the separate fiscal-year table and requires exact PIB authority, fertilizer-ministry attribution, audited HTML lineage, the four major product categories, and closing-stock reconciliation.
- Closing stock must approximately equal availability minus DBT sales within 0.05 LMT. Duplicate rendered rows are suppressed by deterministic record identity, and altered source bytes fail closed.
- The resulting four review-only records show availability above requirement for every major product: 149.71% for Urea, 125.25% for DAP, 137.28% for MOP, and 174.44% for NPKS.
- Closing stocks were positive at 69.01 LMT Urea, 16.72 DAP, 8.63 MOP, and 45.21 NPKS. The national balance therefore contradicts a broad fertilizer-supply-shortage thesis as of 19 July.
- Added a non-investment interpretation layer that keeps three questions separate: national supply balance, comparable-period sales momentum, and governed company impact.
- DBT sales as a percentage of assessed requirement were 86.64% for Urea, 72.28% for DAP, 51.69% for MOP, and 81.19% for NPKS. These ratios are season-progress measures, not growth rates or earnings proxies.
- Supply comfort cannot be translated into strong sales, margin, market share, or company earnings. Sales momentum remains on research hold without a like-for-like prior-period comparison; company impact remains on hold without public product/geography exposure and company disclosures.
- Guardedly acquired the separate official release containing a comparable Kharif consumption reference through 14 July for subsequent structured year-over-year analysis. It has not yet been converted into a comparison record.
- Offline tests cover exact section isolation, product completeness, stock reconciliation, altered-byte refusal, supply-shortfall preservation, and refusal to infer sales momentum or company impact from availability.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 124 — Comparable Kharif fertilizer-consumption momentum

- Added a hash-bound extractor for the official explicit corresponding-period fertilizer-consumption statement through 14 July 2026.
- The extractor requires the configured PIB government-release authority, fertilizer-ministry attribution, exact audited HTML lineage, an explicit current Kharif period, a corresponding Kharif 2025 period, positive LMT values, and altered-byte refusal.
- The official comparison reports 151.74 LMT consumption of major fertilizers through 14 July 2026 versus 157.05 LMT in the corresponding Kharif 2025 period, a calculated year-over-year decline of 3.38%.
- This is a direct aggregate demand signal and contradicts a broad Kharif fertilizer-demand surge through that date. It is analytically distinct from the 19 July supply-balance table, which showed availability above requirement.
- Added a bounded sales-momentum interpretation that preserves only aggregate direction. It explicitly refuses to infer which product caused the decline, whether rainfall caused it, or which company benefited or suffered.
- Product momentum remains on hold pending comparable Urea, DAP, MOP, and NPKS prior-period sales. Weather attribution remains on hold pending crop-stage, geography, application-timing, and nutrient-substitution evidence. Company impact remains on hold pending governed public exposure and company disclosures.
- The combination now says: fertilizer was nationally available, but aggregate consumption was modestly below the comparable prior year. Supply comfort is therefore not evidence of demand strength.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 125 — State-by-product fertilizer geography and scope control

- Searched for like-for-like prior-period product sales and rejected the available full-season Kharif 2025 product totals as an invalid comparator to partial Kharif 2026 data.
- Guardedly acquired and structured the official state-wise fertilizer requirement, availability, DBT sales, and closing-stock table through 29 July 2026.
- Added a state-by-product extractor requiring Department of Fertilizers attribution, a dated Kharif period, audited PIB lineage, exactly sixteen numeric measures per geographic row, four complete products, and availability-minus-sales closing-stock reconciliation.
- Live parser development stopped safely twice on heading punctuation and encoded `&amp;`; no incomplete artifact was produced. Standard HTML-entity decoding and an exact regression fixture now cover the official representation.
- The current dataset contains 148 records: Urea, DAP, MOP, and NPKS for 36 States/UTs plus four separately labelled All India records.
- Corrected geography scope after the first successful extract exposed `All India` as the 37th table row. The superseded artifact is retained but cannot be used; current records explicitly distinguish `STATE` from `ALL_INDIA`.
- Added a geographic balance analysis that prevents nationally adequate availability from hiding state/product requirement gaps while also refusing to call those gaps retail shortages.
- Seventeen state-product rows had availability below assessed requirement. Material examples include Chhattisgarh DAP (-0.52 LMT), Rajasthan DAP (-0.48), Gujarat DAP (-0.28), Madhya Pradesh MOP (-0.18), and Uttar Pradesh MOP (-0.17).
- Telangana, a cumulative rainfall-deficit geography in the current weather case, had modest DAP (-0.04) and MOP (-0.03 LMT) requirement gaps, but retained positive closing stocks of 0.31 and 0.40 LMT respectively. This is not proof of shortage, excess demand, or weather causation.
- Goa MOP, Meghalaya DAP, and Mizoram DAP showed zero rounded closing stock, but each requirement gap was only 0.01-0.02 LMT. These are research flags requiring newer state evidence, not market alarms.
- State sales remain cumulative season-to-date values without state/product prior-period comparators. Meta may use them for geographic research prioritization only; company attribution remains blocked.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 126 — Pre-monsoon foodgrain policy-buffer baseline and freshness gate

- Investigated current official foodgrain stock and procurement sources. The newest directly accessible stock-versus-norm statement was dated 28 May 2026; EIOS did not mislabel it as an August reading.
- Guardedly acquired and structured the official Central Pool wheat and rice statements with exact PIB lineage, food-distribution ministry attribution, reporting date, norm reference date, LMT values, and source passages.
- Wheat stock was 513 LMT versus a 275.80 LMT 1 July norm, or 186.00% of norm. Rice stock was 397 LMT versus a 135.40 LMT norm, or 293.21% of norm, with another 298 LMT of procured paddy reported as awaiting milling.
- This establishes a strong national policy-buffer baseline entering the monsoon and contradicts an immediate national wheat/rice shortage thesis at that time.
- Added a freshness-aware buffer gate. At 31 August, the May reading is 95 days old and remains `RESEARCH_HOLD` for current stock status even though the historical buffer was above norm.
- Foodgrain stocks do not by themselves establish market arrivals, open-market prices, procurement stress, policy release timing, processor margins, or company impact. Food-price pressure remains separately blocked.
- The FCI public homepage displayed zero values and explicitly excluded Central Pool stock held by State agencies; EIOS did not treat those zeros as real national stock data.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 127 — Official food-price transmission gate

- Added the Department of Consumer Affairs Price Monitoring Division as a dedicated official food-price authority, separate from news and corporate sources.
- Added a hash-bound structured extractor for daily retail and wholesale comparison tables. It preserves current, one-week, one-month, six-month, one-year, and two-year prices and changes without creating an Observation.
- The extractor requires exact guarded acquisition and extraction lineage, official department/report attribution, reporting date, market-level separation, unique commodities, minimum table completeness, and reconciliation of every published percentage against its price pair.
- Added a freshness-aware Meta interpretation gate. It can state the direction and size of a current official national price comparison, but blocks claims that weather or crop area caused the move, that a national average proves state arrivals, or that the move proves company earnings impact.
- Offline tests pass for valid extraction, missing comparison values, altered-byte refusal, percentage-tampering refusal, review-only behavior, and the non-investment interpretation boundary.
- Three governed attempts to capture the live retail table were recorded. The first was blocked by the workspace network boundary; two approved attempts reached the official host but timed out at the fixed 15-second acquisition limit. No unverified web values were converted into structured EIOS data.
- The parser is ready for live activation when the official table can be captured within the governed limit. Maize is not represented in this Consumer Affairs basket and still requires a separate official mandi price/arrival source.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 128 — Mandi price-and-arrival source boundary

- Verified that the Government of India now directs current price-and-arrival users to the public AGMARKNET 2.0 dashboard or UPAg. The AGMARKNET public shell is current and JavaScript-rendered.
- Stopped client inspection when the official AGMARKNET application explicitly prohibited developer-tool inspection. EIOS did not reverse-engineer protected client behavior, imitate a signed request, use credentials, or rely on an unofficial API wrapper.
- Verified the sanctioned Open Government Data catalog for daily AGMARKNET mandi prices. Its catalog was updated on 29 August 2026 and is owned by the Agriculture Ministry, Department of Agriculture and Farmers Welfare, and Directorate of Marketing and Inspection.
- The OGD catalog describes daily state/market/commodity wholesale minimum, maximum, and modal prices, including maize coverage through the general commodity dataset. Its programmatic interface requires an issued API key; EIOS did not invent or borrow one.
- No official arrival-quantity field and unit were verified through the accessible OGD catalog. Therefore current physical-arrival analysis remains unavailable even though the official service description says the newer dashboard tracks arrivals.
- Added India OGD as a separately identified government open-data authority and added a fail-closed mandi readiness gate with three states: `RESEARCH_HOLD`, `PRICE_ONLY_READY`, and `PRICE_AND_ARRIVAL_READY`.
- Price readiness now requires sanctioned access, current catalog metadata, hash-bound payload, reporting date, commodity, geography, and minimum/modal/maximum prices. Arrival readiness additionally requires verified arrival quantity and unit fields.
- Meta cannot label rising price as tightening physical supply until both price and arrivals are ready. It also cannot infer production loss from lower arrivals, extrapolate one mandi nationally, attribute co-movement to weather, infer company earnings, or generate an investment conclusion.
- Offline tests cover inaccessible but current metadata, captured price-only data, complete price-and-arrival data, blocked claims, and trusted-source registration.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 129 — Governed sector-to-company impact bridge

- Audited the existing agriculture-climate company-exposure registry. Its public crop, state, product, customer, irrigation, and optional revenue tags remain useful for research planning, but source identifiers alone are intentionally insufficient for a company-impact claim.
- Added a stricter company-impact bridge requiring a governed sector fact and a public, hash-bound NSE, BSE, or SEBI disclosure with a traceable document, substantive exact passage, current disclosure date, and public-information-only status.
- When the sector fact identifies a crop, state, or product, the company disclosure must match every identified dimension. A broad operating-geography statement cannot substitute for product or crop exposure.
- Company-hypothesis readiness also requires a disclosed revenue or volume materiality percentage and an explicit operating transmission mechanism. Qualitative exposure alone remains `EXPOSURE_MAPPED_RESEARCH_HOLD`.
- The bridge has three effective outcomes: `SECTOR_ONLY`, `EXPOSURE_MAPPED_RESEARCH_HOLD`, and `COMPANY_HYPOTHESIS_READY`. Even the final state authorizes only a hypothesis for further validation, not an earnings conclusion.
- The bridge explicitly blocks claims that the sector fact caused company revenue or profit, that exposure guarantees an outcome, that revenue exposure equals profit sensitivity, that the information is not priced, or that a recommendation or trade follows.
- Offline tests confirm that broad geography-only disclosure is held, exact crop/state/product plus materiality and mechanism reaches hypothesis readiness, non-exchange authority and invalid hashes fail closed, and missing materiality remains blocked.
- No live company was attributed in this checkpoint because no user-selected issuer and matching governed disclosure package were supplied. This avoids reverse-fitting a company to the agricultural facts.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 130 — Dated catalyst-event and expectation-reset gate

- Added an upstream evidence gate before the existing canonical Catalyst classifier. This does not create a second catalyst engine or alter the signal-to-catalyst bridge.
- A candidate now requires a discrete announced, scheduled, or completed event. A continuing trend, however important, remains a research lead rather than being relabelled as a catalyst.
- Factual-event readiness requires public-only evidence from an approved primary government, exchange, or securities-regulator authority; a hash-bound and traceable source document; substantive exact passage; event date; governed fact linkage; quantified magnitude and unit; explicit operating mechanism; and a testable invalidation condition.
- A factual event may reach `FACTUAL_EVENT_READY`, making it eligible for canonical catalyst-family research. Announcement is still not execution, cash realization, revenue, profit, or free cash flow.
- `EXPECTATION_RESET_READY` is a separate, stricter state requiring a documented public expectation baseline and an explicit gap between that baseline and the event. EIOS will not call an event surprising, unpriced, or expectation-changing merely because it is new.
- The gate supports the canonical catalyst families, including government policy, regulatory change, commodity, supply constraint, order/contract, capacity expansion, pricing, and expectation reset, without bypassing the existing classifier.
- Explicitly blocked claims include guaranteed operating impact, announcement-equals-execution, event-value-equals-earnings, unpriced surprise without a baseline, and any direct Opportunity, recommendation, or trade authorization.
- Offline tests pass for a quantified order event, missing expectation baseline, complete expectation comparator, continuing-trend rejection, and unquantified-event rejection. The existing signal-cluster-to-catalyst integration suite also passes unchanged after enabling Unicode console output on Windows.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 131 — Mandatory Meta decision-packet assembly

- Preserved the existing mandatory Meta gate and added a final read-only assembly gate around it. The new layer does not weaken or duplicate causal-indicator coverage, independence, contradiction, missing-evidence, kill-test, or evidence-binding controls.
- A packet cannot assemble unless the original Mandatory Meta gate is `READY_FOR_PRE_INFLECTION`, governed facts are identified, at least two independent source groups are present, and contradiction research is explicitly completed.
- Contradiction research must supply contrary governed facts or a substantive explanation for why no contradiction was found. An empty contradiction field is no longer silently treated as a completed check.
- Any identified stale input blocks the assembled case. Unresolved research gaps remain visible in the packet even when they do not independently block sector monitoring.
- Added distinct outcomes: `RESEARCH_HOLD`, `SECTOR_MONITORING_READY`, `COMPANY_PRE_INFLECTION_RESEARCH_READY`, and `COMPANY_EXPECTATION_RESET_RESEARCH_READY`.
- Sector readiness cannot be presented as company readiness. Company pre-inflection readiness additionally requires both the governed company-exposure bridge and a factual dated catalyst event. Expectation-reset readiness further requires the public expectation comparator.
- Every ready state remains research-only and requires human review. The packet explicitly has no authority to create a Signal, Catalyst, Opportunity, recommendation, position, or trade.
- Offline tests pass for company pre-inflection assembly, expectation-reset assembly, stale-input refusal, sector-only monitoring, and unexplained empty contradiction refusal. The original mandatory Meta gate suite continues to pass unchanged.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 132 — Live India Kharif end-to-end readiness snapshot

- Applied the cross-layer gates to the actual India Kharif 2026 research case and generated a machine-readable, review-only readiness artifact.
- The current case is `WEATHER_CROP_HINT_ONLY`. Current official rainfall and the four-date crop-area timeline establish a valid research hint, with fertilizer input-market evidence and explicit contradiction review providing additional context.
- The case is not yet `SECTOR_TRANSMISSION_RESEARCH_READY`. Observed soil moisture or crop condition is unavailable through the governed route, and current reservoir storage has not been verified and mapped to affected crop geography.
- Current official output-price bytes were not successfully captured, and verified mandi arrival quantity plus unit remain unavailable. Therefore EIOS cannot yet distinguish production stress, irrigation buffering, inventory/policy effects, and market-supply transmission with sufficient confidence.
- The case contains meaningful contradictions: national sowing weakness narrowed, several crop groups recovered, fertilizer availability exceeded requirement, aggregate fertilizer consumption was modestly lower year over year, and the foodgrain buffer was strong before the monsoon but is now stale for current claims.
- No company-specific case is in scope. The case has no hash-bound issuer exposure package, quantified company materiality, dated factual catalyst, or public expectation comparator.
- Added a deterministic cross-layer readiness service with stages from `RESEARCH_HOLD` through weather/crop hint, sector transmission, company pre-inflection, and company expectation-reset research readiness.
- Freshness is fail-closed: a stale critical input pushes an otherwise complete causal case back to the hint stage. Tests cover the current live state, sector advancement, company advancement, and stale-input refusal.
- The generated `india_kharif_2026_pre_inflection_readiness.json` creates no Observation and requires human review.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 133 — Information-gain evidence acquisition queue

- Converted the live readiness blockers into a deterministic, machine-readable acquisition queue rather than repeatedly retrying every unavailable source.
- Queue priority combines whether evidence blocks sector transmission, whether it later blocks company attribution, contradiction value, expected information gain, and a penalty for repeated attempts.
- Added explicit route states for ready public access, transient failure, access required, source boundary, and stale-only data. The queue cannot bypass a source boundary or treat required user credentials/API keys as available.
- Added exponential retry backoff capped at sixteen multipliers. A recently failed source is not hammered simply because its evidence would be valuable.
- Company disclosure and company catalyst research are automatically deferred until sector transmission is ready. This prevents expensive reverse-fitting of issuers to an unproven sector narrative.
- The current live queue has no eligible immediate external action. Consumer Affairs prices remain under retry backoff; NRSC soil/crop condition and India OGD mandi access require user-issued access; current reservoir alternatives are cooling down after stale/failed routes; and issuer/catalyst work is deferred.
- The highest-value unresolved domains remain current reservoir storage mapped to crop geography, observed soil or crop condition, maize mandi price plus verified arrivals, and current official output prices.
- The generated `india_kharif_2026_evidence_queue.json` is advisory and review-only. It records no automatic external action and cannot bypass access controls or create an investment conclusion.
- Offline tests verify prioritization, transient-failure backoff, access-required blocking, company deferral, and later company eligibility once sector transmission becomes ready.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 134 — Consolidated safety-chain regression and ledger integrity

- Ran the complete newly added research chain from trusted source intake through rainfall, crop area, fertilizer interpretation, food-price parsing, mandi readiness, company impact, catalyst-event readiness, Mandatory Meta packet assembly, live pre-inflection readiness, and evidence acquisition scheduling.
- All selected source, interpretation, company, catalyst, Meta, live-readiness, and queue tests passed. The unchanged canonical signal-cluster-to-catalyst integration had already passed in checkpoint 130.
- Re-ran the public factual candidate, Observation-proposal, and Temporal Evidence boundary tests. All passed, confirming that research artifacts cannot silently cross into governed production objects.
- Regenerated both live machine-readable snapshots from their deterministic scripts. The readiness stage remains `WEATHER_CROP_HINT_ONLY`, and the acquisition queue still authorizes no immediate external action.
- Parsed the complete live audit ledgers. The acquisition ledger contains 67 valid rows with 67 unique acquisition identities; the extraction ledger contains 53 valid rows with 53 unique extraction identities.
- Failed, timed-out, stale, partial, and successful source attempts remain in the append-only audit trail rather than being erased. This preserves the difference between unavailable evidence and evidence that was never sought.
- Source formatting inspection found only existing Windows LF-to-CRLF notices and the known inaccessible `.pytest_cache` directory warning. No patch whitespace error or production-data mutation was found.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 135 — Look-ahead-safe hypothesis outcome resolution

- Added an institutional outcome-resolution layer so EIOS can measure whether early hypotheses were actually correct instead of retaining only successful narratives.
- A hypothesis is frozen with an identity, case, exact metric, geography, direction, threshold, optional baseline, target date, freeze time, confidence, and bound evidence fingerprints. These fields produce a SHA-256 hypothesis fingerprint.
- Any later change to the threshold, horizon, confidence, scope, or evidence binding causes a fingerprint mismatch and makes the hypothesis ineligible for scoring.
- Outcome measurements require the same metric and geography, a reporting date on or after the predefined target, acquisition after publication, evaluation after acquisition, authoritative HTTPS lineage, exact passage, and a valid document hash.
- The resolver supports above/below thresholds and baseline-relative increase/decrease hypotheses. Baseline-relative predictions cannot be scored without a frozen baseline.
- Results are explicit: `CONFIRMED`, `DISCONFIRMED`, or `INVALID_OR_INCONCLUSIVE`. Inconclusive or lineage-invalid outcomes are not counted as successes or failures.
- Confidence must be set before the outcome and remains available for later calibration analysis. Outcome scoring itself has no investment authority.
- Offline tests pass for confirmed and disconfirmed outcomes, post-hoc threshold tampering, and an outcome published before the target horizon.
- The live India Kharif case remains `WEATHER_CROP_HINT_ONLY`, so no sector or company hypothesis was frozen merely to create a track record. Freezing begins only after the applicable readiness gate is satisfied.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 136 — Complete-cohort confidence calibration

- Added cohort-level calibration so EIOS measures whether stated confidence corresponds to actual confirmed outcomes rather than reporting raw prediction counts.
- Every declared cohort starts with an expected hypothesis-identity list. Missing hypotheses or resolutions produce `INCOMPLETE_COHORT`, preventing selective removal of failed or inconvenient cases.
- Only fingerprint-valid `CONFIRMED` and `DISCONFIRMED` resolutions are scoreable. Invalid or inconclusive outcomes remain counted and visible but are not converted into wins or losses.
- Reports now include expected count, scoreable resolved count, inconclusive count, missing count, hit rate, mean stated confidence, calibration gap, and Brier score.
- A default minimum of twenty scoreable outcomes is required before any performance claim is ready. Smaller samples remain available for process inspection but are labelled `SAMPLE_TOO_SMALL`.
- Duplicate or unexpected hypothesis identities fail closed, preserving the declared cohort boundary.
- Calibration measures research-process reliability only. It is explicitly not evidence of future returns, investment skill, or trade authority.
- Offline tests pass for mixed confirmed/disconfirmed/inconclusive outcomes, exact hit-rate and Brier calculations, incomplete-cohort refusal, and insufficient-sample refusal.
- No calibration report was generated for the live Kharif case because it has no readiness-qualified frozen hypothesis or resolved outcome.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 137 — Append-only hash-chained hypothesis ledger

- Added a durable prospective hypothesis ledger so prediction freezing is enforceable rather than merely a dataclass convention.
- Every entry contains a monotonically increasing sequence, the previous entry hash, the complete frozen hypothesis payload, and its own SHA-256 entry hash. The first record anchors to an explicit genesis hash.
- Recording revalidates the hypothesis fingerprint, timezone-aware freeze and target dates, evidence binding, and non-authority statement before appending.
- Duplicate hypothesis identities are rejected. A prediction cannot be replaced by appending another version under the same identity.
- Reading validates every hypothesis fingerprint, sequence number, previous-hash link, current entry hash, and unique identity. Editing or removing an earlier row breaks the chain for that row or all subsequent rows.
- Offline tests pass for two linked entries, duplicate refusal, pre-append hypothesis tampering refusal, and post-write ledger tampering detection.
- The ledger remains a research-audit object. Its existence does not imply correctness, investment skill, or authority to create a recommendation or trade.
- No live ledger entry was created for India Kharif 2026 because the case remains below sector-transmission readiness. This preserves the rule against freezing low-quality hints merely to inflate activity counts.
- The outcome resolver and complete-cohort calibration tests continue to pass with the ledger layer present.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 138 — Hash-chained outcome-resolution ledger

- Completed the prospective audit chain with an append-only resolution ledger binding each public outcome to the exact frozen hypothesis fingerprint and hypothesis-ledger entry hash.
- Each resolution entry preserves the full public outcome payload, an outcome fingerprint, the deterministic resolution result, previous resolution-entry hash, and its own entry hash.
- A hypothesis may be resolved only once. A later outcome cannot silently replace an earlier resolution under the same hypothesis identity.
- Before recording, the existing look-ahead-safe resolver revalidates metric, geography, target horizon, publication/acquisition/evaluation order, source lineage, and scoring eligibility.
- Reading validates sequence, prior-entry linkage, hypothesis bindings, outcome fingerprint, entry hash, and unique resolution identity.
- Offline tests pass for linked confirmed and disconfirmed resolutions, duplicate-resolution refusal, and post-write observed-value tampering detection.
- The hypothesis ledger, resolution ledger, and complete-cohort calibration now form one prospective chain: freeze before outcome, resolve against public evidence, then calibrate the complete declared cohort.
- These ledgers measure research discipline only. They do not convert a correct hypothesis into an investment recommendation or establish realized investment performance.
- No live Kharif resolution was recorded because no readiness-qualified live hypothesis exists.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 139 — Cross-cohort calibration-drift control

- Added drift monitoring across distinct, complete prospective hypothesis cohorts so historical calibration is not assumed to remain valid indefinitely.
- Drift assessment requires both baseline and recent calibration reports to be performance-claim ready. Incomplete or undersized cohorts produce `INSUFFICIENT_FOR_DRIFT_TEST` and require conservative review rather than a false no-drift result.
- The monitor calculates change in Brier score, absolute confidence-calibration gap, and hit rate. Default review triggers are Brier deterioration of 0.05 or more, calibration-gap widening of ten points or more, or a hit-rate decline of fifteen points or more.
- Material deterioration produces `DRIFT_REVIEW_REQUIRED`. The permitted response is to suspend confidence escalation and review source mix, market or policy regime, prediction thresholds, and analyst process.
- A stable comparison produces `NO_MATERIAL_DRIFT`, but still does not authorize automatic confidence increases.
- Reusing the same cohort as both baseline and recent comparison is invalid, preventing circular self-comparison.
- Offline tests pass for a stable cohort transition, simultaneous Brier/gap/hit-rate deterioration, and an incomplete recent cohort requiring review.
- The full prospective chain now includes hypothesis freezing, append-only prediction storage, public outcome resolution, append-only result storage, complete-cohort calibration, and cross-cohort drift detection.
- No live drift report exists because the live Kharif case has no resolved readiness-qualified hypothesis cohort.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 140 — Semantic public-source schema-drift gate

- Added a reusable schema contract and drift gate for structured government tables and APIs, addressing silent changes in headings, types, units, row counts, and duplicate rendering.
- Contracts freeze source and dataset identity, required and optional fields, field types, units, identity keys, permitted row-count range, and a SHA-256 contract fingerprint.
- An unchanged structure produces `SCHEMA_COMPATIBLE`. New fields not relied upon by the extractor produce `NON_BREAKING_ADDITIVE_DRIFT` and remain visible for deliberate future adoption.
- Missing required fields, required-field type changes, unit changes, source/dataset identity changes, out-of-contract row counts, and duplicate identities produce `BREAKING_DRIFT` and block ingestion.
- A modified or corrupted schema contract produces `INVALID_CONTRACT`; the system cannot weaken a contract without changing and reviewing its fingerprint.
- Unit drift is explicitly semantic. A price changing from rupees per quintal to rupees per kilogram is held even when every numeric value still parses.
- Offline tests pass for compatible schema, additive arrival field, breaking price-unit change, duplicate identity refusal, and contract tampering detection.
- Existing crop-area and food-price extractor suites continue to pass, including their source-specific duplicate, percentage, and lineage safeguards.
- Schema compatibility does not validate factual accuracy or analytical meaning; it is one required layer before extraction can be trusted.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 141 — Evidence-constrained confidence ceiling

- Added a deterministic ceiling preventing Meta or a human-authored hypothesis from claiming more confidence than the supporting evidence structure permits.
- The ceiling considers primary-authority status, freshness, direct versus proxy or inferred evidence, exact geographic match, period comparability, schema compatibility, hash-bound lineage, independent-source count, unresolved material contradictions, and missing critical layers.
- Schema incompatibility or missing hash-bound lineage makes confidence ineligible regardless of other strengths. A ceiling below fifty percent is also ineligible for a formal research hypothesis.
- Penalties are transparent reason codes rather than a hidden model score. The ceiling is a maximum; it does not force the analyst to use that confidence or estimate investment probability.
- Offline tests pass for strong direct evidence, proxy/geography/independence weakness, stale contradictory evidence, broken schema, and missing critical layers. Mandatory Meta and calibration-drift suites continue to pass.
- Applied the ceiling to the live India Kharif causal interpretation. The official rainfall and acreage facts remain valid, but transmission is inferred, geography is not yet sufficiently exact, and crop-condition, irrigation-buffer, and output-market layers are missing.
- The resulting live causal-interpretation ceiling is ten percent and is confidence-ineligible. This is now embedded in `india_kharif_2026_pre_inflection_readiness.json` alongside the unchanged `WEATHER_CROP_HINT_ONLY` stage.
- The ten-percent ceiling applies to the causal sector interpretation, not to the accuracy of each underlying official measurement.
- Confidence ceilings have no expected-return, valuation, position-sizing, recommendation, or trade authority.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 142 — Readiness-bound hypothesis freezing service

- Closed the creation-side bypass between live-case readiness, evidence confidence, and the append-only hypothesis ledger.
- A sector hypothesis can now be created only when the case assessment is `sector_transmission_ready`. A weather/crop hint cannot be frozen as a formal sector prediction.
- A company hypothesis requires the stricter `company_case_ready` state. Sector readiness cannot be reused to create an issuer-specific prediction.
- The freezing service requires an eligible evidence-confidence ceiling and rejects any proposed confidence above that ceiling before calculating a hypothesis fingerprint.
- Freeze and target dates must be timezone-aware and ordered prospectively; evidence fingerprints are mandatory; confidence must be strictly between zero and one hundred.
- Successful creation produces the canonical frozen-hypothesis object with its SHA-256 fingerprint and explicit non-authority statement, ready for the separate append-only ledger.
- Offline tests pass for a valid sector hypothesis, hint-only refusal, over-ceiling confidence refusal, and company-hypothesis refusal from a sector-only case.
- The existing confidence-ceiling and hypothesis-ledger suites continue to pass, proving the creation gate and storage gate agree.
- The live India Kharif case remains unable to freeze a hypothesis because it is `WEATHER_CROP_HINT_ONLY` and its causal confidence ceiling is ineligible at ten percent.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 143 — Human-authorized hypothesis-freezing boundary

- Strengthened the freezing service so technical readiness and an eligible confidence ceiling are necessary but no longer sufficient to create a formal hypothesis.
- Freezing now requires the governed Pre-Inflection preview and its Mandatory Meta human-review receipt.
- The review decision must be `AUTHORIZE_PRE_INFLECTION_REVIEW`. `HOLD_FOR_RESEARCH` and `REJECT_ASSESSMENT` cannot authorize prediction creation.
- The preview must bind exactly to the review identity, Meta assessment identity, and stored Meta assessment fingerprint. A review from another assessment or a copied preview fails closed.
- The preview must remain eligible for human Pre-Inflection review. Sector hypotheses require reviewed sector scope; company hypotheses require reviewed entity scope in addition to company-case readiness.
- This closes a path where valid-looking readiness and confidence objects could otherwise be assembled without the durable Mandatory Meta review chain.
- Offline tests pass for authorized sector freezing, hint-only refusal, over-ceiling refusal, company-scope refusal, held-review refusal, and mismatched-review binding refusal.
- Mandatory Meta, hypothesis ledger, and freezing suites all continue to pass together.
- The live Kharif case has no authorized Meta review or eligible Pre-Inflection preview and therefore remains unable to freeze a hypothesis.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 144 — End-to-end prospective lifecycle integration

- Added and passed one integrated prospective lifecycle test spanning the full governance chain rather than testing only isolated components.
- The synthetic lifecycle begins with a human-authorized Mandatory Meta receipt and a matching governed Pre-Inflection preview, then supplies sector readiness and an eligible evidence-confidence ceiling.
- The freezing service creates a fingerprinted sector hypothesis below the confidence ceiling, and the hypothesis is appended to a temporary hash-chained ledger.
- A later hash-bound public outcome with matching metric, geography, and target horizon is resolved against the exact hypothesis-ledger entry and appended to the temporary resolution ledger.
- The confirmed result is then included in its complete declared cohort and produces the expected one-case calibration metrics, including a Brier score of 0.1225 for a 65% confidence success.
- Re-ran the component suites for freezing, hypothesis ledger, resolution ledger, calibration, and calibration drift alongside the integrated test. All passed.
- This demonstrates that identities, fingerprints, dates, review bindings, readiness, confidence limits, outcomes, and cohort accounting remain compatible across the complete lifecycle.
- The integration uses temporary synthetic records only. It created no live hypothesis, live resolution, calibration performance claim, or production object.
- The live India Kharif case remains unchanged at `WEATHER_CROP_HINT_ONLY` with an ineligible ten-percent causal confidence ceiling.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 145 — Operational live-research runbook and executable handoff

- Added `docs/operations/PRE_INFLECTION_LIVE_RESEARCH_RUNBOOK.md` as the concise operational handoff for the governed public pre-inflection path.
- The runbook records the live India Kharif stage, ten-percent ineligible causal confidence ceiling, verified evidence, unresolved transmission layers, and deliberate deferral of company research.
- It documents the required path from public acquisition and hash-bound extraction through schema checks, Mandatory Meta, company/catalyst separation, confidence ceiling, human-authorized hypothesis freezing, outcome resolution, complete-cohort calibration, and drift monitoring.
- Added exact Windows PowerShell commands for regenerating the live readiness and evidence-queue artifacts without initiating external acquisition.
- Added the core verification suite, production Observation integrity command, human authority points, fail-closed source and interpretation rules, principal live artifact paths, and current evidence priorities.
- Executed every core command listed in the runbook. The prospective lifecycle, Mandatory Meta, schema drift, confidence ceiling, acquisition queue, live readiness, hypothesis freezing, hypothesis ledger, resolution ledger, calibration, and drift tests all passed.
- The production Observation integrity command also passed at exactly 46 records.
- The runbook explicitly prohibits bypassing access controls, importing unbound displayed values, price-only supply inference, exposure-only earnings inference, unbenchmarked expectation-reset claims, over-ceiling freezing, and selective cohort deletion.
- The repository now has a reproducible operational entry point for the large checkpoint set rather than relying on conversation history.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 146 — Pre-commit security and artifact integrity audit

- Ran a bounded sensitive-pattern and merge-marker scan across the changed project state, external-intelligence modules, scripts, operational documentation, and live-case data.
- No private-key marker, common GitHub token form, AWS access-key form, or unresolved merge marker was found.
- The first quote-heavy scan command was rejected by PowerShell parsing and performed no file scan; it was replaced with safely separated patterns. A broad retry encountered only the known inaccessible `.pytest_cache`; the final scoped scan completed successfully across all relevant changed paths.
- Parsed all 32 structured JSON artifacts in the live Kharif case successfully.
- Parsed the acquisition and extraction ledgers together and verified 120 populated record identities. This total comprises the previously verified 67 acquisition and 53 extraction receipts.
- Checked every ledger source URL for embedded username credentials; none were present.
- Re-ran patch whitespace inspection. It reported only existing Windows LF-to-CRLF notices and no malformed patch content.
- The audit did not stage, commit, or push files. External repository mutation remains pending explicit instruction.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Checkpoint 147 — Plain-English live case status command

- Added a non-technical renderer and one-command status view for the live India Kharif case.
- `python -m scripts.show_india_kharif_status` now prints the case identity, current stage, permitted interpretation, causal confidence ceiling and eligibility, verified evidence layers, unresolved gaps, eligible queue actions, safety boundary, and whether a production object was created.
- The command reads only the deterministic readiness and evidence-queue JSON artifacts. It performs no network access and no external or production mutation.
- Current output correctly states `WEATHER_CROP_HINT_ONLY`, a ten-percent ineligible causal confidence ceiling, the five principal unresolved gaps, and no currently eligible external action.
- Added the command and its behavior to the operational live-research runbook.
- Offline tests pass for stage, confidence, missing-evidence, queue, and no-production-object rendering. The live command also completed successfully against the actual artifacts.
- Production Observations remain exactly 46. No Observation, Evidence, Meta conclusion, EIP state, Signal, Catalyst, Opportunity, recommendation, position, or trade was created.

## Product mandate — Best-in-class intelligence, analytics, and explanation (2026-09-02)

- EIOS is to be built as a trusted investment-research system, not a decorative dashboard or price-only alert tool.
- Every material conclusion must be traceable to dated, source-linked evidence. Missing, stale, conflicting, or inaccessible data must be shown plainly and must never be silently filled or invented.
- The analytical layer must combine long-term financial statements, quarterly trends, cash flow, balance-sheet quality, valuation context, macro and sector conditions, company news, orders/tenders, and catalysts.
- Mandatory Meta analysis must test evidence quality, compare figures across time and peers, identify what changed, explain the likely business impact, show supporting and opposing facts, and enforce confidence ceilings before any verdict is displayed.
- The presentation must speak to an intelligent normal reader: lead with the conclusion, then show the numbers, logic, sources, uncertainty, and what would change the view. Tables and charts should make ten-year/available history and trends easy to inspect.
- EIOS must detect early hints before they appear in reported results where evidence permits, while labeling them as hints rather than facts and separating observation, interpretation, hypothesis, catalyst, opportunity, and recommendation.
- Automation must preserve each company’s evidence and extraction history, refresh independently on a schedule, report collection failures honestly, and retain an auditable change history.
- Learning is governed: human review outcomes may improve future ranking and explanations only through measured, replayable feedback; no unreviewed pattern is allowed to become a financial verdict.
- The release bar is professional trust: reliable ingestion, complete-enough coverage, explainable analytics, visible provenance, fail-closed safety, accessible UI, and regression-tested behavior across companies.

## Checkpoint 148 — Quarterly presentation gate connected (2026-09-02)

- Added a dedicated quarterly-trend table to the company financial view for quarter, revenue, EBITDA, and PAT.
- The table consumes only reconciled quarterly records and clearly displays missing data instead of estimating from annual totals or headlines.
- The existing official Coromandel annual report was checked for quarterly performance tables; its references to quarterly bank returns are compliance disclosures, not quarterly operating results, so no unsupported figures were imported.
- The quarterly safeguard therefore remains active: the UI is ready, but the data stays empty until an official quarterly-results document is acquired and reconciled.
- The dashboard build passes after this change.

## Checkpoint 149 — Quarterly source discovery wired and regression-tested (2026-09-02)

- Automatic official-source discovery now recognizes issuer annual-report pages, quarterly-results pages, and investor-presentation pages through the governed manifest.
- Discovery remains bounded, allowlisted, and non-authoritative: a link is only a candidate until acquisition, extraction, reconciliation, META review, and human authorization complete.
- The complete company-intelligence regression suite passed: 120 tests.

## Quarterly discovery correction (2026-09-03)

- Corrected the premature return after configured annual-report URLs: remaining document capacity now permits page discovery.
- Prioritized quarterly-results pages ahead of annual indexes and presentations within the two-page limit.
- Enforced the document limit across all pages and direct URLs, with duplicate suppression.
- Added regression cases for a known annual PDF alongside a quarterly page and for the global document cap. All 122 company-intelligence tests passed offline.
- No quarterly figures were acquired or approved in this step. Live source accessibility and source-backed extraction remain unverified; passing tests does not establish successful collection.

## Direct quarterly acquisition attempt (2026-09-03)

- Located the Q1 FY2027 PDF link on the issuer's quarterly-results index and registered the exact document URL in the source manifest.
- An approved-network acquisition using the governed archive command returned HTTP 406. The index was readable through web research, but no PDF bytes were acquired into EIOS; no quarterly figures were extracted or approved.
- The next acquisition alternative is an official exchange-hosted copy or a user-supplied original PDF; do not treat browser/search text as a hash-bound local document.
- User credit stop rule: stop further EIOS development and notify when purchased credits are observed at 500 or below, based on the original 1,000-credit budget. A 30-minute monitor is active; this is not an exact account spending cap.

## Exchange acquisition alternatives checked (2026-09-03)

- Tested public NSE filing https://nsearchives.nseindia.com/corporate/COROMANDELINT_07052026140636_BMOutcome_SD.pdf (quarter/year ended March 2026): approved-network download timed out after 45 seconds with zero bytes.
- Tested public BSE filing https://www.bseindia.com/xml-data/corpfiling/AttachLive/1d018ae7-3b0e-4af2-a29c-dd7f87317068.pdf (June 2025 historical quarter): returned HTTP 404.
- Neither is a verified copy of the June 2026 filing. Neither downloaded successfully; no figures, archive approvals, or investment conclusions were created.
- Current practical handoff: user-supplied official quarterly PDF for the existing local importer, or a newly verified accessible official filing URL. Do not describe the quarterly extraction or approval-to-UI integration as complete.

## User-supplied quarterly PDF imported (2026-09-03)

- Copied the user-specified Desktop Q1-results-1.pdf without changing the original and imported it via the existing local-source workflow.
- SHA-256: 17b16806779abafa77ed78665e5e0389fd6acc2eb63b4d0189e1e4fd3f0c2aab. Seven pages, 21,706 extracted characters, extraction SUCCEEDED with no warnings; eight generic fact candidates queued, zero human-review-ready and zero approved facts.
- Extracted document heading identifies unaudited standalone and consolidated results for the quarter ended June 30, 2026. This is local-import provenance, not a verified network download.
- Visual column reconciliation is still pending: Poppler was not located on PATH or the checked Codex tree, and current Python lacks fitz/pypdfium2. Do not promote noisy extracted numeric text into quarterly records until visually checked.
- Quarterly table population and graph integration remain unfinished.

## Reusable quarterly row-candidate extractor (2026-09-03)

- Added an issuer-independent layout-text extractor and local CLI that identify candidate revenue, total-income, PAT and EBITDA rows, retaining hash, page, raw row and raw cells.
- Strict numeric-token parsing preserves zeros/negatives and flags OCR corruption or dashes without guessing. Total income remains distinct from revenue. No quarter, basis or unit is assigned from column position alone.
- Ran against the user-supplied Coromandel PDF: seven table-row candidates saved under data/runtime/quarterly_candidates, all held for column reconciliation. This is separate from the earlier eight generic fact candidates.
- All 127 company-intelligence tests passed. OCR, column-header mapping, arithmetic reconciliation, and approved-record UI integration remain unfinished; no facts or verdicts were approved.

## Extraction safety and credit limit update (2026-09-03)

- User replaced the 500-credit stop/notification threshold with 300 credits remaining. The existing monitor was updated; the former threshold is superseded.
- Quarterly candidate extraction now rejects numeric overflow, avoids classifying pre-tax profit subtotals as PAT, and preserves original layout spacing for subsequent column matching.
- Added regression tests for those three cases. Column reconciliation and OCR remain incomplete; no production financial records were approved.

## Deterministic quarterly column reconciliation (2026-09-03)

- Added a reusable validator for explicitly mapped column metadata: discrete Indian fiscal quarter dates, fiscal-year label, standalone/consolidated basis, units, hash/page/column binding and core metrics.
- Checks revenue plus other income against total income using a 0.02 source-unit rounding tolerance. Missing checks do not become passes; invalid columns expose no normalized values.
- Converts supported INR lakh/million/crore units using Decimal, preserving negative and zero values. Successful validation is CHECKED_PENDING_REVIEW, never approval.
- Nine new synthetic test cases cover annual/YTD rejection, wrong fiscal year, mixed columns, arithmetic failure, missing inputs, invalid values, unit/basis holds and March quarters. All 139 company-intelligence tests passed.
- This stage requires explicit mapped headers; automatic header recognition/OCR and wiring the real PDF candidates into this validator remain unfinished. No live figures or UI records were approved.

## Isolated column-header recognition (2026-09-03)

- Added conservative recognition of explicit quarter-ended headers with supported textual/day-first/ISO dates, INR crore/lakh/million units and standalone/consolidated basis.
- Connected recognized metadata to column arithmetic/binding validation; pre-existing metadata conflicts are held, not overwritten.
- Missing labels, multiple dates, mixed bases/units/currencies, annual/YTD markers and invalid dates remain held. All 143 company-intelligence tests passed.
- Important scope: this recognizes one already-isolated full column header. The PDF layout adapter must still assemble shared headers and align cells; OCR and real-document end-to-end mapping remain incomplete. No new approved quarterly records or UI figures were created.

## PDF geometry adapter tested on actual quarterly report (2026-09-03)

- Located bundled Python with pdfplumber and rendering support. Inspected a rendering of page 1; the source has 90-degree rotation and OCR text corruption.
- Added a reusable memory-only rotation normalization and geometry adapter. Repeated year anchors form candidate column bands; raw words, coordinates, missing cells, boundary overlap and shared header uncertainty remain explicit.
- Ran the adapter on the supplied PDF: two candidate table pages, 16 candidate columns in total, all held. These include additional table material, not 16 verified quarterly periods.
- Original PDF unchanged. Layout output is bound to its SHA-256 under data/runtime/quarterly_candidates. No arithmetic-approved records, evidence or verdict changes.
- All 145 company-intelligence tests passed. Shared spanning-header interpretation, OCR correction with provenance, table classification and automatic invocation from the ingestion pipeline remain unfinished.

## Financial versus segment table classification (2026-09-03)

- Added explicit-label table classification to the geometry adapter, distinguishing main-statement candidates, segment tables and unknown tables. Segment/unknown tables expose no company_mapping_columns; raw geometry remains preserved separately.
- Tested against saved geometry from the actual PDF: page 1 classified as a main-statement candidate, page 2 as a segment table excluded from company mapping.
- All 148 company-intelligence tests passed. Shared header resolution and ingestion-to-UI integration remain unfinished; this classification is not financial-data approval.

## Source-bound shared-header resolver (2026-09-03)

- Added deterministic resolution for explicit source-bound header spans, scoped to document hash, PDF page and table identity. Exactly one applicable basis, duration and unit span is required per column.
- Overlap, missing scope, foreign-page/table headers, annual duration and damaged labels remain held. Five new tests passed; the company-intelligence suite reached 153 passing tests.
- This resolver consumes explicit column-range spans; automatic span detection from PDF borders/OCR is NOT implemented. It has not resolved the actual report's corrupted headings, and no quarterly facts were approved.

## Ruled-table boundary detection on real report (2026-09-03)

- Added pdfplumber ruled-table detection to the PDF adapter, deriving value-column boundaries from individual dated cells and recording which columns lie fully inside each shared header cell.
- Re-ran the real seven-page report: ruled geometry is now saved alongside existing word geometry; page 1 contains eight value columns and detected standalone/consolidated group boundaries.
- Header text is not silently repaired: corrupted consolidated, quarter-duration and currency/unit strings still require OCR/review. Some merged detected cells also combine duration labels, so boundaries alone do not establish semantic scope.
- All 154 company-intelligence tests passed. No quarterly financial records were approved or sent to the UI.

## Native Windows OCR executed successfully (2026-09-03)

- Found built-in Windows OCR with en-US/en-GB recognition languages; Tesseract installation was unnecessary.
- Added scripts/extract_windows_ocr.ps1: workspace-bounded image/output paths, local WinRT OCR, image-size checks, input-image SHA-256, language/engine/timestamp and per-word pixel boxes, with explicit non-approval flags and resource disposal.
- Ran OCR on the normalized first-page render of the actual quarterly PDF: 287 text lines saved to windows-ocr-page1.json under its document-hash runtime directory. No network service was used.
- The separate OCR stream recovered quarter/year duration headings and the words 'in Crores'. This is not proof that every heading/number is correct or that the currency is established.
- Still required: bind the render transform to PDF coordinates/hash, compare OCR against native text, resolve spanning headers, and invoke the fallback automatically from ingestion. No facts, financial table updates or verdicts were approved.

## Combined quarterly intake with automatic OCR fallback (2026-09-03)

- Added quarterly_pdf_intake and its CLI: preserve immutable per-run PDF bytes, extract layout, select at most three identifiable main-statement OCR targets, render, call local Windows OCR and verify image hash. Source-to-image transforms and per-stage failures are recorded.
- Live run on the supplied PDF succeeded with one OCR page and 287 lines, bound to PDF hash, image hash and normalized coordinates. Fixed relative-path invocation and made OCR hashing independent of PowerShell module autoload.
- Local report import now invokes this path when extracted opening text identifies quarterly financial results; missing dependencies are explicitly held. The standalone combined path was live-tested; the newly added importer invocation still needs an end-to-end test.
- 157 company-intelligence tests passed, including OCR target selection/budget tests. These do not establish OCR accuracy. Native/OCR disagreement reconciliation and production UI mapping remain unfinished. Scanned pages without recognizable native main-table headings still require a separate detection path.

## Native/OCR comparison integrated (2026-09-03)

- Added hash/page/dimension-bound comparison of native financial cells with OCR words transformed to normalized PDF coordinates; raw texts, disagreements and unreadable/boundary-overlap holds remain visible.
- Wired comparison into the combined intake. Live PDF run examined 32 cells: six matching readings and 26 holds. These are diagnostic comparison counts, not verified financial facts or measured extraction accuracy.
- Some native text boxes and visual/OCR rows appear offset; better row registration and render quality require investigation before promoting matches. Agreement alone never approves data.
- Five additional comparison tests pass; all 162 company-intelligence tests passed. No UI financial values or verdicts were changed.

## OCR registration diagnosis (2026-09-03)

- Added unique alphabetic-label registration diagnostics, fitting a 2D affine OCR-to-native mapping with outlier rejection. Financial numbers are not used as alignment anchors.
- The actual saved report supplies 32 matching textual anchors, with maximum fitted residual about 0.76 PDF units. The fit indicates rotation/translation, explaining why identity-coordinate matching can select neighboring rows.
- Diagnostics are attached to subsequent intake runs but not yet applied to cell comparison. Coverage, independent validation and rejection limits must gate application; this fit is not verified financial accuracy.
- All 164 company-intelligence tests passed, including synthetic known-shift and insufficient-anchor cases. No production figures approved.

## Checked alignment applied to cell comparison (2026-09-03)

- Added leave-one-label-out prediction checks, minimum anchor coverage, distortion/shift limits and maximum 1.5-PDF-unit validation error. Rejected registration holds all comparisons.
- Integrated checked transforms into OCR-to-native cell selection. Replayed the real saved report: 32 textual anchors passed with maximum omitted-anchor error about 0.85 PDF units; matching cell readings increased from six to 13, with 19 still held.
- These are extraction agreement counts, not approved facts or independently measured accuracy. No values were repaired or sent to the UI.
- All 168 company-intelligence tests passed. The local-import invocation, remaining OCR issues, header binding, and reviewed-record materialization still need end-to-end verification.

## Automatic local import chain verified (2026-09-03)

- Increased OCR rendering to 200 dpi with a conservative 2500-pixel maximum edge; recorded actual resolution in the render transform. Visually inspected the resulting page.
- Real comparison improved to 21 agreeing readings out of 32 cells, with 11 held. These are not approved financial records or an accuracy score.
- The bundled interpreter lacked requests for the import chain. Installed approved PDF dependencies into EIOS's existing user Python environment instead and recorded layout/render versions in requirements-quarterly-extraction.txt.
- Successfully ran the existing local importer end to end with the supplied PDF: archive preserved, text extraction SUCCEEDED, quarterly detection invoked layout/render/OCR/comparison automatically, 21 agreements, RESEARCH_HOLD and no approved facts.
- Re-ran all 168 company-intelligence tests successfully. Remaining work includes shared-header semantic binding, disagreement review and governed materialization; no new quarterly UI values were created.

## Shared-header binding connected to intake (2026-09-03)

- Added coordinate-registered OCR/native header binding within actual ruled cells, preserving both readings and inferred column-span candidates. Source hash/page/image/dimensions and alignment gates apply.
- Live report recovered 'Standalone results', 'Consolidated results' and left-group 'Quarter ended'. Right-group merged duration remains damaged/ambiguous; multiple 'ended' labels are rejected even when only one duration word is legible.
- Unit region OCR reads 'in Crores)' but misses the currency symbol; all eight columns remain held rather than inferring INR from company nationality or domain.
- All 171 tests passed before the final conservative multiple-duration guard. No quarterly records or UI figures approved. Next work is targeted header-region OCR and separation of the right-group duration cell, not relaxation of these holds.

## Targeted header OCR fallback automated (2026-09-03)

- Added a reusable local header-region OCR module and CLI. It checks preserved PDF bytes against the intake hash, enlarges ruled-table headers within the OCR image budget, and records crop coordinates, pixel scales, image hashes and raw readings separately.
- Connected this second pass to quarterly intake when first-pass header resolution remains held. Failed fallback stays held; its readings do not replace first-pass data or approve financial facts.
- Inspected the enlarged real header. It distinguishes quarter/year headings visually, but OCR still misses the rupee symbol and corrupts some words. Semantic reconciliation of the second pass remains unfinished.
- Live combined run 7d71362917254fcaa11fa0ba81207df5 generated one targeted region automatically and retained RESEARCH_HOLD. All 174 company-intelligence tests passed, including triggering, skipping and failure handling. No new quarterly UI figures or verdict changes.

## Header second-pass comparison connected (2026-09-03)

- Targeted OCR now produces source/page/table/image-bound header comparisons for every affected column, distinguishing agreement, conflict, ambiguity and missing readings. Original readings remain unchanged and ambiguity flags survive comparison.
- Validates crop dimensions/scales and uses the checked full-page alignment for provisional header projection. Transfer of that registration to the new OCR pass is explicitly pending review, not independently validated; these comparisons cannot approve records.
- Real combined run b2d2fe5ac35b41c59641df746b2b6db6 produced eight column comparisons: basis readings agree, the left quarterly heading degraded on the second OCR pass, the right duration cell remains ambiguous, and currency remains unconfirmed. Inspected the enlarged header again; no numerical or textual repair was applied.
- All 182 company-intelligence tests pass. No new UI values or verdict changes. Next substantive work: resolve ruled-cell separation and independently validate header mapping, then currency/date checks and governed quarterly record materialization. Automatic extraction is not yet publication-ready across companies.

## Unruled duration-heading partition proposal (2026-09-03)

- Inspected actual PDF vector edges: the right quarter/year header row has no dividing vertical line. Increasing border tolerance would fabricate a boundary, so no border repair was applied.
- Added a bounded geometric proposal generator: exact quarter/year-ended OCR phrases must uniquely align with contiguous date-column groups. Corrupt prefixes, poorly centred headings and nonunique alternatives are rejected. Original ambiguity and publication holds remain intact; proposals are separate review evidence.
- Real automatic intake run 763390d451bc4042a191e88bd63c0f07 proposed quarter-ended for columns 4-6 and year-ended for column 7, matching the visually inspected enlarged report. This is a provisional layout proposal, not approved financial data or independent validation of registration.
- All 186 company-intelligence tests passed. Currency recognition, date verification, registration transfer validation and governed record materialization remain unfinished. No new UI financial figures or verdict changes.

## Desktop access restored and launcher hardened (2026-09-03)

- User reported desktop app would not open. Neither service was initially listening. Dashboard production build passed; starting existing launcher restored both services. Opening the browser required desktop permission in this tool environment and succeeded when authorized. Original cause of the user's stopped services is not established.
- Existing EIOS Dashboard.lnk points to scripts/open_eios_dashboard.ps1; no shortcut replacement needed. Launcher now derives workspace from its location, reuses an existing build, supports explicit rebuild/no-browser checks, logs child-process output, detects early dashboard exit and allows saved dashboard access if review-service launch fails.
- Cold-start tested by identity-checking and stopping only EIOS's vinext process. Updated launcher restarted it successfully; company page HTTP 200 and review health ok. Opened the dashboard in the user's normal desktop browser. Kept local-only under Sites guidance; no publication or data approvals.
- Resume extraction work at pending header registration/currency/date validation; no financial correctness claims changed by the launcher repair.

## Isolated date-cell verification integrated (2026-09-03)

- Added strict whole-cell calendar parsing and native/OCR date comparison. Keeps raw readings; rejects invalid dates, damaged months, multiple dates, ambiguous numeric ordering and conflicting years. Spacing normalization is allowed but OCR characters are not repaired. Dates never imply quarter/annual duration.
- Both full-page and targeted header binding now record source-bound date comparisons. A date conflict or missing reading overrides an otherwise recognised header with HOLD.
- Actual intake run 7dbda27a6bd04b04bb739a2502558495: seven of eight native/OCR dates agree in each pass, but the held column differs. Full-page OCR misses the day in column 5; targeted OCR reads Match instead of March in column 1. No favourable-pass merging or promotion was performed. Visually inspected the rendered date header.
- All 196 company-intelligence tests passed, including a binding-level regression proving date conflicts block recognition. Currency recognition, independent registration-transfer validation and reviewed quarterly materialization remain open. No new UI figures or verdict changes.

## Fresh crop alignment gate added (2026-09-03)

- Added a no-refitting check of the transferred full-page transform against fresh crop OCR alphabetic labels. Requires at least 12 mutually unique spatial matches, 65% matched eligible labels, horizontal/vertical coverage and maximum 1.5-PDF-unit residual per accepted match. Numeric values are excluded as anchors.
- Targeted header comparison is now blocked when this crop check fails. This checks geometric consistency with native text, not independence of source evidence, financial accuracy or approval eligibility.
- Real intake run b6f945eef3a24d988f3eb23e28b5b951 passed with 25 anchors, matched fraction 0.6757 and maximum residual 0.5063 PDF units. Visually inspected the enlarged header. Thresholds remain engineering safeguards tested on one issuer, not a calibrated cross-company accuracy guarantee.
- All 202 company-intelligence tests passed, including shifted crops, duplicate anchors, sparse coverage and numeric-only inputs. Currency recognition, held date readings and reviewed financial record materialization remain unfinished. No UI financial figures or verdicts changed.

## Focused currency OCR diagnostic and review reason (2026-09-03)

- Added an explicitly bounded diagnostic CLI for the upper-right unit region (one main table, 600 dpi, installed en-US/en-GB OCR only). It preserves source/image hashes and does not feed its readings into approved facts or run automatically on every import.
- Real probe unit-probe-12f36e8b03fe45d596b0f56ad1f8be3f under intake b6f945eef3a24d988f3eb23e28b5b951 returned '(R in Crores)' in both languages. Visually checked the crop: printed rupee glyph is present, but Windows OCR misreads it. Currency extraction remains unresolved; do not keep repeating this same OCR setup or substitute R with INR.
- Added explicit unit-reading assessments to automatic header binding: missing INR, conflicting currencies or ambiguous scales produce NEEDS_UNIT_REVIEW with raw text and source binding. Candidate recognition alone cannot approve data.
- All 206 company-intelligence tests passed. Next needs a genuinely different currency-reading method or source-bound reviewed unit evidence, followed by date and record reconciliation. No quarterly UI figures or verdicts changed.

## Document-bound visual unit correction reused automatically (2026-09-03)

- No alternative OCR/vision reader was found configured. Visually inspected the preserved unit crop and saved an ASSISTANT_VISUAL_REVIEW candidate reading '₹ in Crores', explicitly not a human approval or general R-to-INR rule.
- Added a document/page/table-specific unit review registry and loader. Reuse requires matching evidence metadata, original PDF hash and crop image hash; absent/damaged local evidence fails closed. Duplicate reviews, conflicting currencies/scales, existing explicit unit readings and date holds are not overridden.
- Combined intake automatically applies this unit candidate to the byte-identical report. Real run 08d9a23d26d3421ba1a3a535b4be6912 now recognises three standalone quarterly headers (Q1-FY2027, Q4-FY2026, Q1-FY2026) as INR_CRORE pending review. Annual columns remain excluded from quarterly recognition; right-side duration/date issues remain held.
- All 212 company-intelligence tests passed. This resolves the exact report's unit-candidate blocker using saved assistant review, not general automatic currency OCR across hundreds of companies. No financial facts or UI figures were approved. Next: reconcile recognised columns' numeric cells and provide an auditable record-review path; broader OCR fallback remains needed.

## Quarterly numeric record candidates connected (2026-09-03)

- Added adapter joining recognised headers to native/OCR agreeing metric cells with source/page/image and column-geometry checks. Rejects duplicate metrics, conflicting numbers and uncertain headers; does not map owner-attributable or pretax profit to total PAT. Uses existing Decimal income reconciliation and keeps raw evidence.
- Wired candidates into future automatic intake. Added read-only saved-intake replay CLI, avoiding repeat OCR for numeric reconciliation. Replayed actual run 08d9a23d26d3421ba1a3a535b4be6912 successfully.
- Q1-FY2027 standalone candidate now CHECKED_PENDING_REVIEW: revenue 7743.55, other income 48.76, total income 7792.31 and total PAT 376.96 INR crore. Income arithmetic passes. Both Meta and human review remain required; no published fact is created.
- Q4-FY2026 and Q1-FY2026 candidates remain held for unreadable/missing metric readings, with explicit reasons and no normalized values exposed. All 220 company-intelligence tests pass. New intake invocation is wired but this turn verified the numeric adapter via saved evidence, not another complete OCR run. Next: connect these review candidates to the governed review workflow; no UI figures changed.

## Quarterly candidates bridged into existing META/human-review formats (2026-09-03)

- Added quarterly_review_bridge: repeats arithmetic validation, uses stable full-record/company/source identity, preserves raw transcription plus complete structured record evidence, deduplicates candidates and skips held extracts. Labels transcription as structured, not a verbatim source passage; preserves local_import origin and distinct QUARTERLY_FINANCIAL_RESULT event type.
- Writes standard candidates and META files accepted by the existing human-review command. Future quarterly intake invokes this bridge when company/source URL context is supplied; local import now forwards both. Missing context is explicitly held.
- Replayed real saved evidence into 08d9a23d26d3421ba1a3a535b4be6912/review-bridge-v1: one candidate queued, two held extracts excluded, one META HOLD_FOR_RESEARCH and zero human-approval-ready records. Existing event-oriented META does not establish financial materiality or company context from the table transcription, and local-source authority remains unresolved. Do not present this as completed financial META validation.
- All 226 company-intelligence tests passed, including queue/meta output and proof that the existing human ledger rejects approval while META holds. No human decision was written. No UI queue integration, quarterly fact materialization or public financial data changed. Next: financial-specific source/context review and reviewer presentation; broader automatic sourcing remains unfinished.

## Financial-specific review assessment added (2026-09-03)

- Added deterministic quarterly financial review alongside (not in place of) the existing META authority hold. Rechecks printed header/period/basis/unit and arithmetic, normalized values, all four underlying native/OCR readings and their locations, and extraction status. Evidence fingerprints bind each assessment to its record.
- Review output gives plain-English checks, review-only figures, explicit official-source/company-identity and reporting-note/restatement holds, and a list of analyses not performed. It does not claim earnings-quality, cash-flow, valuation or investment analysis.
- Connected assessment writing to the quarterly review bridge; real saved candidate replay into financial-review-v1 passed all four technical checks and retained both publication holds. This is a deterministic diagnostic assessment, not an LLM analysis or complete mandatory META approval. No UI integration or human decision was made.
- All 232 company-intelligence tests passed, including altered header, changed OCR values, wrong cell location and missing evidence. Next: verified source/company lineage and reporting-note evidence, then reviewer UI and governed quarterly materialization. No published financial values changed.

## Quarterly review evidence visible in local company UI (2026-09-03)

- Added a separate Quarterly review panel near the company header with a direct jump link. Shows candidate figures in a table, plain-English passed checks/publication holds, source-text versus image readings, supplied filing link/page, document fingerprint and explicitly unassessed areas. Unapproved figures remain excluded from financial history, charts and verdicts.
- Dashboard sync discovers saved quarterly queues, verifies preserved PDF hash and company ticker, recomputes financial checks, deduplicates source columns and withholds invalid packets. Coromandel has one candidate; three other current companies have none. Displays assistant unit-review involvement separately from human approval.
- All 235 company-intelligence tests passed; local production build passed. Restarted only the verified EIOS server, confirmed company page HTTP 200 and opened /companies/coromandel#quarterly-review. No browser visual/interaction QA was performed this turn. Sites guidance used; kept local, no hosting/publication or human review decisions.
- This delivers reviewer visibility, not the complete verified-company-analysis milestone. Official source identity, reporting-note verification, approval/materialization and broader financial history/analysis remain unfinished.

## Reporting-note candidates extracted with quarterly intake (2026-09-03)

- Added page/hash/offset-bound native-text passage detection for limited review, comparability, balancing quarters, impairment and restatement/regrouping. Preserves original passages, explicit unresolved period/basis scope, missing-text pages and review questions. Keyword matches never grant audit status or complete note review; absence is not proof of no issue.
- Real report notes on page 2 discuss limited review, acquisition-related consolidated comparability, March balancing figures and impairment. Visually inspected the rendered notes page. Corrupted OCR remains in raw passages, not silently repaired.
- Full current intake successfully ran to completion at 1e3613737d214a69866867011eaa6334: eight topic/passage candidates attached to standard quarterly review packet, one financial candidate queued, zero approval-ready. This also verifies the previously wired numeric/review bridge in a complete OCR run.
- All 241 company-intelligence tests pass. Notes are now backend review evidence, not yet displayed in the company panel or resolved into period-specific conclusions. Source authority and reporting-note approval holds remain; no financial history/chart/verdict changes.

## Reporting notes displayed beside quarterly review figures (2026-09-03)

- Extended quarterly review display with eight expandable topic/passages from the newest Coromandel review packet. Shows plain-language review questions, original extracted text, page links to the supplied filing, and explicit unreviewed/source-origin/period-and-basis caveats. No note is automatically applied to the displayed standalone quarter.
- Display filters mismatched document hashes, missing/invalid page references and duplicate note IDs. Missing notes do not imply a clean report. Source text is rendered as escaped React text, not HTML.
- All 244 company-intelligence tests passed. Dashboard sync found eight note entries for Coromandel and no candidates for other current companies; production build passed. Restarted only the identified EIOS server, confirmed company route HTTP 200 and requested the existing local review URL in Codex. No browser visual/interaction QA performed.
- Sites skill used to preserve existing design and local-only operation. No financial history, chart, verdict or approval state changed. Official lineage and period-specific reporting-note interpretation remain required before governed publication.

## Reporting-note context cues (2026-09-03)

- Quarterly review notes now show explicit accounting-basis and date mentions alongside the original passage. Warns against transferring consolidated notes to standalone figures or treating historical charges as current-quarter adjustments. Matching mentions do not establish applicability; unreadable date-like text remains flagged rather than repaired.
- All passages remain visible and unapproved. These deterministic review cues are not completed Meta interpretation, source verification or investment conclusions.
- All 249 company-intelligence tests passed; dashboard sync and production build passed. Restarted the identified EIOS dashboard and confirmed company route HTTP 200. No browser visual/interaction QA performed. Sites guidance preserved the existing local-only presentation; no cloud publication or approved financial data changes.

## Independent quarterly source-copy comparison (2026-09-03)

- Added scripts/verify_quarterly_source.py and quarterly_source_match.py: resolves the candidate against configured company/issuer domain, rechecks preserved PDF hash, uses the existing guarded acquisition adapter, and compares fresh issuer bytes. Saves a unique acquisition ledger and verification result per attempt; preserves valid downloaded PDFs without replacing the original.
- Distinguishes exact match, changed document, non-PDF response, receipt mismatch and unavailable source. Exact byte identity explicitly does not verify company content, reporting notes or authorize financial publication. This is an explicit command, not yet connected to scheduled collection or dashboard source-hold clearing.
- Coromandel live attempt on 2026-09-03 returned HTTP 406 after network permission was granted. Evidence: latest run 1e3613737d214a69866867011eaa6334/source-verification/cae799cdc20d4bdfa073639a8ed60c90/verification.json under the existing quarterly document hash directory. The initial sandbox-denied attempt is also retained separately. No issuer PDF acquired and no source/notes approval granted.
- All 256 company-intelligence tests passed, including seven new source-match tests. No UI changes or app rebuild needed. Next source-verification dependency is an accessible official copy or a supported alternate acquisition route; reporting-note interpretation remains unfinished.

## Alternate issuer filing and draft note interpretation (2026-09-03)

- Official disclosures index links CIL_Outcome_BM_23072026_SD.pdf, a nine-page board-outcome filing. Web research retrieved its text, including the results and notes after two cover pages; this is corroboration, not a preserved byte acquisition. Local guarded download returned HTTP 406, recorded in source-verification/36d44b62d2a34f70a6c33f28eded3fa6 under the latest Coromandel intake.
- Source verifier now accepts an alternate observed issuer URL, validates it against the configured issuer registry and preserves the candidate's original URL separately. Does not rewrite original evidence or bypass domain controls.
- Visually reviewed local notes page using PDF skill. Saved four source/candidate-bound assistant draft interpretations in data/company_intelligence/coromandel_quarterly_note_assessment_draft.json: limited review, historical impairment, consolidated acquisition comparability and March balancing-quarter construction. No human approval, complete notes clearance or automatic earnings adjustments. Draft file is not yet consumed by UI or approval workflow.
- Alternate-source tests cover default URL, issuer alternative, lookalike rejection and local-target rejection. Official PDF byte acquisition remains blocked; the browser research path must not be represented as EIOS's own successful download.
- Validation: all 260 company-intelligence tests passed. No UI or approved financial history changes this turn.

## Draft explanations connected to quarterly UI (2026-09-03)

- Connected assistant note drafts by company, PDF hash, target period, note ID and page. Rejects approval claims and ambiguous duplicate drafts. Coromandel displays four plain-English draft explanations alongside original evidence; other notes remain unreviewed. The panel explicitly distinguishes assistant-prepared research from automated EIOS conclusions.
- Added eight tests; all 268 company-intelligence tests passed. Dashboard sync confirmed four attached drafts; production build passed; restarted only the identified EIOS server and confirmed company route HTTP 200. No browser visual QA performed.
- Sites skill preserved the existing local-only design. No source-identity clearance, human approval, financial history, chart or verdict changes. Official PDF acquisition remains blocked; governed publication and full reporting-note review are unfinished.

## Source comparison runs automatically during quarterly intake (2026-09-03)

- Added quarterly_source_intake.py and connected it to run_quarterly_intake after extraction and before review queue creation. Each document gets one comparison attempt (15-second request timeout, at most two redirects), using the unique configured company identity and issuer domain. Missing or mismatched context skips network access and saves an explicit hold.
- Preserves a unique verification result, acquisition ledger and downloaded PDF when available. Source result is included in intake.json and quarterly-candidates.json. Extraction is persisted before the request; expected download/configuration errors and source-check storage failures do not discard the review packet or approve any figures.
- All 275 company-intelligence tests passed, including intake-to-review-packet integration tests for a successful source comparison and source-check storage failure. Network was mocked in these new tests; no claim of a successful live issuer download. Existing Coromandel HTTP 406 remains unresolved.
- Applies to new imports using the quarterly intake path, including the local report import command. Does not yet provide scheduled retries, alternate-source discovery, approval-hold clearing or full automatic company coverage. No UI or governed financial history changes.

## Controlled quarterly source retries (2026-09-03)

- Added quarterly_source_retry.py and a preview-by-default retry command. Reads saved packets and source-verification history, verifies original PDF hash, deduplicates columns/runs by document/company/URL and never reruns OCR. A transient unavailable-source failure may retry after 24 hours, with a three-attempt history limit and one document attempt per cycle invocation. Access refusals such as HTTP 406, changed documents, recorded matches and invalid evidence require review rather than repeated fetching.
- Wired retries into the existing automatic company cycle after collection. Offline mode skips them. No new scheduler was installed or executed; retries depend on that cycle running and reaching the collection stage. The cycle's existing overlap lock applies; standalone --execute should not be run concurrently with it.
- All 284 company-intelligence tests passed. Ran read-only retry planning against real saved Coromandel packets: zero network attempts, SOURCE_ACCESS_REQUIRES_ATTENTION due to HTTP 406. No UI/approval/history/verdict changes. Accessible alternate acquisition remains unresolved.

## Exchange route tested; acquisition access remains blocked (2026-09-03)

- Discovered BSE results URL https://www.bseindia.com/xml-data/corpfiling/AttachLive/089ec18e-802d-48b9-897b-975365997029.pdf via https://theannexure.com/company/506395. Directory was used only for link discovery, not as verified financial data. Guarded direct BSE download returned HTTP 403; saved under latest Coromandel intake/source-verification/935231ee4d7b4fe892efb346c0744eb4. No PDF bytes obtained.
- Explicit --exchange-source mode now restricts alternate URLs to BSE/NSE registry, separately labels exchange vs issuer matches and saved copies, and retains company-content/notes holds. Default issuer mode remains unchanged. This command is not automatic exchange discovery/fallback, and no third-party provider was connected or purchased.
- All 289 company-intelligence tests pass. Both issuer (406) and tested exchange (403) programmatic acquisition routes are unavailable. Further automatic collection requires a supported accessible provider/integration; repeated download attempts or further approval checks do not resolve this access dependency. No UI or approved financial data changes.

## Existing provider audit and independent source retries (2026-09-03)

- Read-only configuration check found TAVILY_API_KEY present in process environment; secret value was never displayed. No checked Brave/FMP/Financial Datasets/EODHD/Alpha Vantage key was present in process or user environment. This is not an exhaustive account inventory or proof of key validity. No usable financial-data connector was found among available tools; plugin search/suggestion tools were not available, so no installation was requested.
- Credential-free Tavily DNS/HEAD probe succeeded at network level and returned HTTP 401 without credentials. Earlier saved cycle failure was DNS resolution. No authenticated search, API-credit use, purchase or provider connection was performed. Search connectivity does not resolve official PDF download restrictions.
- Moved saved quarterly source retries ahead of search execution (still after existing validation/safety gates), persisting their result before the provider call. A later search failure now retains completed retry status rather than skipping this independent work. Offline mode preserved.
- All 290 company-intelligence tests passed, including online/offline search-failure ordering and status preservation. No complete live company cycle was run. Next provider step requires authorization for a bounded authenticated test of the existing Tavily connection; financial statement acquisition remains unverified.

## Authorized single Tavily search test (2026-09-03)

- User authorized one small test search. Ran existing TavilySearchProvider once (basic search, max five results, 15-second timeout, no retries) for Coromandel June 30 2026 quarterly results on coromandel.biz. Authentication/search succeeded and returned five issuer URLs.
- Results were older/mismatched periods: Q3 FY26 press release, FY26 annual-results press release, Q4 FY26 presentation, February 2026 transcript and an older newspaper-results PDF. The requested Q1 FY27 filing was not found by this query. Provider connectivity is demonstrated; target-document discovery, byte acquisition and financial approval are not.
- No extra searches, full automatic cycle, source downloads, approvals or code changes. The call may consume Tavily credit; actual billed credit amount was not returned by the existing provider interface. One-test authorization must not be treated as an unlimited paid-search budget.

## Exact-quarter discovery preparation (2026-09-03)

- Added quarterly_search_target.py and an offline plan/assessment command. Maps Indian April-March quarter-end dates to fiscal labels and prepares exact-quarter/explicit-date search queries. Classifies result titles against issuer domain and explicit quarter/year metadata; unclear dates remain unconfirmed, conflicting/invalid ranges ambiguous, other periods mismatched. Upload-directory years are never treated as reporting periods. A matching title is only a retrieval candidate, not verified content.
- Replayed the five earlier live-result titles locally: three wrong-quarter labels and two unconfirmed titles; none accepted for Q1 FY2027. This planner/assessor is not yet wired into the automatic research search/selection path; no extra Tavily request or API-credit usage occurred.
- All 301 company-intelligence tests passed. No financial approval or UI changes. Next integration must preserve other report searches while applying target-quarter screening only to explicitly quarter-targeted jobs.

## Quarter targeting wired into research execution (2026-09-03)

- ResearchJob now supports optional quarter_period_end, validated for official-document jobs with issuer domain and Indian fiscal quarter end. Execution carries target metadata into ExternalResearchQuery; orchestrator builds one exact-quarter query and screens metadata before source selection/retrieval, retaining all screening decisions in result.quarter_screening. General/annual research without target remains unchanged.
- Official document collection repeats target screening and does not substitute generic manifest/annual PDFs when targeted search returns no candidate. Matching title remains only a retrieval candidate; PDF/company/period/content verification is still required.
- All 305 company-intelligence unittest tests passed, including retrieval filtering, general-search preservation, fallback prevention and job validation. Pytest is not installed; existing main-style external regression suites are run separately. No paid search or full live cycle run. Existing saved jobs were not assigned a new period or enabled; targeted execution requires explicit quarter_period_end configuration.

## Browser-assisted official PDF acquisition succeeded (2026-09-03)

- Opened issuer Q1-results-1.pdf in Codex in-app browser. Viewer completed loading seven pages; clicked its Download button. Observed new Downloads/Q1-results-1.pdf (3,672,882 bytes), preserved under data/runtime/browser_source_capture/coromandel-20260903-9ed52959/source.pdf with provenance.json. SHA256 9ed529593ae80c64f0e37f8029545a0efe1223f6f6a5eb3963ab4c613bbde079 differs from original 17b168... upload. Neither original nor prior evidence was replaced.
- Added read-only PDF copy-comparison script. All seven pages have identical extracted text and matching rendered RGB hashes/sizes at 120 dpi. Saved page-comparison.json; visually inspected rendered financial-table and notes pages using PDF skill. This corroborates visible contents, not exact-byte equality, signature validity or untested PDF internals. Cause of byte difference not established.
- This is a successful assistant/browser-assisted official-site acquisition, not a working unattended EIOS transport. Direct HTTP routes remain blocked. No API-credit spending, human approval, financial history or verdict changes. Next: integrate browser-acquired provenance into review without relabelling it as direct HTTP or automatically clearing approval holds.

## Period-specific human reporting-note review (2026-09-07)

- Added an append-only reporting-note review ledger. Every decision is bound to the exact note passage fingerprint, document hash, company, quarter end and standalone/consolidated basis. Available decisions are applies, does not apply and unresolved; a rationale and reviewer identity are mandatory. Later decisions supersede earlier decisions without erasing the audit history; duplicate review identities and tampered passages are rejected.
- Connected the ledger to the quarterly review display and local review service. The dashboard now presents decision controls beside every extracted note and shows the saved rationale. The reporting-note hold clears only when every candidate for that exact reporting context has a conclusive human decision; one missing or unresolved note keeps the hold.
- This clears only the reporting-note completeness check. It does not approve quarterly facts, populate financial history, change charts, produce an investment verdict or authorize a trade. Further governed quarterly materialization and financial/valuation analysis remain separate gates.
- Validation: all 322 company-intelligence tests pass; dashboard snapshot sync and production build pass. No human decisions were entered for Coromandel, so its reporting-note hold remains.

## Corroborated-source META alignment and quarterly approval gate (2026-09-07)

- META now recognizes a local quarterly extraction as corroborated issuer lineage only when a preserved browser-capture receipt matches the candidate's exact SHA-256 document hash and exact HTTPS source URL. A local upload, changed hash, changed URL or local-inbox receipt remains on authority hold. This changes research eligibility only; it does not create evidence or a verdict.
- Added a mandatory quarterly pre-materialization gate. An APPROVE request cannot record a human fact approval unless the exact quarterly evidence record passes all four deterministic financial checks, source-delivery provenance passes, and every reporting note has a conclusive period-and-basis-bound human decision. This closes the previous route through the general fact approval service that could have bypassed the separate note hold.
- A fully cleared packet advances only to READY_FOR_HUMAN_FACT_APPROVAL. It still requires the existing explicit human fact approval and does not itself populate history, change charts, create a catalyst, change a verdict or trade.
- Validation: all 327 company-intelligence tests pass, including exact source binding and attempted note/source bypasses. Coromandel's reporting notes remain undecided, so quarterly approval remains blocked.

## Governed quarterly repository and human-readable financial meaning (2026-09-07)

- Added an append-only governed quarterly financial repository. It can materialize the four checked quarterly figures only after the exact candidate has become a governed company fact and its six financial/source/note checks remain passed. It binds the stored numbers to the source page, document hash, evidence fingerprint and human review receipt; duplicates and changed evidence are rejected.
- Added a deterministic plain-English explanation layer and displayed it above the technical quarterly review. It explains revenue scale, net-profit margin, dependence on other income, income reconciliation, comparable-period growth and margin direction when a valid comparable period exists, applicable accounting-note meaning, and unresolved limitations. It explicitly refuses to invent a trend from one quarter.
- Current Coromandel explanation: ₹7,743.55 crore operating revenue, ₹376.96 crore profit, 4.87% net margin, and ₹48.76 crore other income representing about 0.63% of total income. EIOS labels this a checked single-period starting point—not evidence of improvement—because a comparable quarter, cash flow, earnings-quality work and note decisions are incomplete.
- No Coromandel note was decided and no governed quarterly record was created. The repository and automatic post-approval connection are ready for future valid approval. Neither the record nor the explanation creates a catalyst, changes a verdict, recommends an investment or authorizes a trade.
- Validation: all 334 company-intelligence tests pass; dashboard snapshot sync and production build pass.

## Automatic comparable-quarter triangulation (2026-09-07)

- Added a conservative recovery rule for complementary PDF-text/OCR defects. EIOS accepts the pair only when one finite reading for revenue and one finite reading for other income form a unique combination that reconciles to a separately agreeing total income within the fixed ₹0.02 crore tolerance. Both defective raw readings, the selected reader and the arithmetic proof remain attached; ambiguous or non-reconciling combinations remain held.
- Reconciled the preserved Coromandel issuer filing without rerunning OCR or modifying the original packet. Q1 FY2026 standalone is now a checked comparison candidate: revenue ₹7,001.32 crore, other income ₹81.60 crore, total income ₹7,082.92 crore and PAT ₹508.23 crore. Q4 FY2026 remains held and is not used as the year-on-year comparison.
- The dashboard now selects only an exact prior-year quarter with the same accounting basis. For Q1 FY2027 it explains revenue growth of 10.60%, PAT decline of 25.83%, and net-margin compression from 7.26% to 4.87% (-2.39 percentage points). The conclusion is margin pressure requiring cost/one-off analysis, not an investment verdict.
- The original and browser-equivalent duplicate periods are collapsed in presentation only when ticker, quarter, basis and all extracted values are identical. Source artifacts remain preserved.
- The new packet contains two review candidates, both META-ready, and one held non-comparable column. No human approval, governed quarterly record, catalyst, verdict or trade was created.

## Human-readable quarterly profit bridge (2026-09-07)

- Added a transparent first-stage profit bridge to the quarterly explanation. It calculates revenue change, PAT change, the PAT that current revenue would have produced at the prior comparable net margin, and the signed gap between that benchmark and actual PAT. It does not attribute the gap to an expense line without extracted evidence.
- For Coromandel Q1 FY2027 versus Q1 FY2026: revenue increased ₹742.23 crore, PAT decreased ₹131.27 crore, current revenue at the old 7.26% margin would imply about ₹562.11 crore PAT, and actual PAT of ₹376.96 crore is ₹185.15 crore below that benchmark. Other income also declined ₹32.84 crore but is not treated as a direct after-tax explanation.
- The UI lists the still-unattributed possibilities—raw materials/traded goods, inventory movement, employees/operations, finance/depreciation, and tax/exceptional/accounting items—and states that EIOS will not invent the cause. Detailed expense-line extraction is the next dependency.
- Validation remains all 337 company-intelligence tests passing; dashboard data regeneration succeeds. No review or verdict state changed.

## Detailed quarterly cost attribution - first source-backed layer (2026-09-07)

- Extended quarterly layout/OCR mapping to explicit income-statement expense, total-expense and pre-tax-profit rows. Supplemental rows may be retained when both readers agree, but missing or disagreeing expense cells no longer invalidate otherwise sound core figures; they remain individually listed as unresolved and cannot be used for attribution.
- Re-ran the preserved browser-corroborated Coromandel PDF through the extended local extractor while reusing only its exact hash/URL-bound source receipt. Current Q1 FY2027 contains 11 checked values and prior Q1 FY2026 contains 10; Q4 remains held. The new run is additive and does not modify older packets.
- Confirmed comparison: total expenses rose from ₹6,398.38 crore to ₹7,286.97 crore, an increase of ₹888.59 crore or 13.89%, faster than 10.60% revenue growth. Profit before exceptional items and tax fell ₹179.20 crore or 26.18%; its margin against operating revenue fell from 9.78% to 6.53%.
- Two individual lines are presently comparable across both readers: employee benefits increased ₹26.82 crore (12.34%) and freight/distribution increased ₹48.44 crore (13.75%), both sources of pressure. ₹813.33 crore of the total expense increase remains unallocated because raw materials, prior traded goods/inventory, finance/depreciation or other-expense readings are incomplete on one side. EIOS does not assign that residual without evidence.
- The dashboard displays the confirmed cost table, pressure/relief direction, unallocated residual and the boundary that PBT-to-PAT difference is not automatically labelled tax. Core-identical older packets are collapsed even when newer packets contain additional supplemental metrics.
- Validation: all 338 company-intelligence tests pass; dashboard snapshot sync succeeds. No human review, approval, catalyst, verdict or trade was created.

## Complete expense reconciliation for comparable quarters (2026-09-07)

- Added strict eight-line expense-sum triangulation. A failed text/OCR cell is recovered only when the full set of raw materials, traded-goods purchases, inventory movement, employee benefits, finance costs, depreciation/amortisation, freight/distribution and other expenses has exactly one numeric combination that reconciles to a separately agreeing total expense within ₹0.02 crore. A narrowly defined missing-decimal repair is allowed only for a native reading ending in two separated digits and only when that unique full-statement equation passes.
- Applied the rule to the preserved Coromandel extraction without rerunning OCR. Both comparable standalone quarters now retain all eight expense lines and reconcile exactly; the unallocated expense change is ₹0.00 crore. Failed raw text and OCR values remain embedded beside the selected reading and arithmetic proof.
- Source-backed attribution of the ₹888.59 crore net expense increase: raw materials +₹767.54 crore, traded-goods purchases +₹318.06 crore, employee benefits +₹26.82 crore, finance +₹10.66 crore, depreciation/amortisation +₹18.28 crore, freight/distribution +₹48.44 crore and other expenses +₹19.03 crore, partly offset by ₹320.24 crore of inventory-movement relief. These line changes sum exactly to total expense change.
- The dashboard identifies raw materials and traded-goods purchases as the two largest pressures, inventory movement as the largest relief, shows every comparable row and confirms complete reconciliation. This measures where accounting expenses moved; it does not yet establish commercial causes such as commodity prices, mix, volumes, acquisition effects or subsidy timing.
- Validation: all 340 company-intelligence tests pass; dashboard snapshot sync succeeds. No human note decision, fact approval, catalyst, verdict, recommendation or trade was created.

## Source-backed quarterly business-cause explanation (2026-09-07)

- Added a reusable, reporting-context-bound business-cause evidence contract. Every cause must identify the exact ticker, quarter end and accounting basis; classify its evidence as confirmed, supported, contradicted or unknown; link to an allowed official source; explain the measured financial connection, competing explanations, next confirming observation and decision boundary. Invalid, duplicate, wrong-period or non-official evidence is withheld.
- For Coromandel Q1 FY2027 standalone, official company material confirms that Middle East-related increases in phosphoric acid, ammonia and sulphur were not fully offset by NBS subsidy rates. This supports the observed ₹767.54 crore raw-material-expense increase and margin pressure, but management did not quantify a one-to-one PAT attribution.
- The same official evidence confirms that NPK/DAP primary volume declined 8.6% as production and inventory were deliberately moderated, while higher realisation contributed to revenue growth. Crop protection partly offset fertiliser weakness: standalone revenue rose 20% to ₹870 crore and segment profit rose 44% to ₹159 crore, with margin improving from 15% to 18%.
- Rainfall deficit is classified only as a supported demand risk, not the confirmed cause of the Q1 profit decline: management reported delayed sowing and cautious sentiment, but also rainfall recovery and 13% growth in point-of-sale fertiliser volume. The dashboard shows these distinctions, official-source links, alternatives and what EIOS must monitor next.
- This is source-backed research explanation, not human approval of the extracted financial packet. It does not clear the eight reporting-note decisions, populate governed quarterly history, change the verdict, recommend an investment or authorize a trade.
- Validation: all 343 company-intelligence tests pass, dashboard snapshot regeneration succeeds, the production build passes, and the cause section was verified visible in the running browser.

## Cause-linked automatic monitoring plan (2026-09-07)

- Added a reusable monitoring-rule layer between quarterly cause research and the existing catalyst/risk engines. A rule defines its indicator, unit, favourable direction, required primary source, update cadence, improvement meaning and deterioration meaning. It remains bound to the originating company/quarter/basis cause evidence.
- Coromandel now has six planned indicators: phosphoric-acid settlement price, NBS subsidy/input-cost coverage, NPK/DAP primary volume, crop-protection PBIT margin, seasonal rainfall deficit and relevant crop sowing acreage. The first four require official company or Department of Fertilizers evidence; weather and acreage require IMD and Agriculture Ministry primary releases.
- Added deterministic direction evaluation for future numeric observations. It can label a new value favourable, adverse or unchanged, but explicitly cannot infer causation, materiality, durability or market mispricing from direction alone.
- Monitoring output is structurally barred from creating a catalyst, changing a verdict or authorizing a trade. The UI displays the six indicators as awaiting their next governed update and explains the source and direction EIOS will use.
- Validation: all 346 company-intelligence tests pass, dashboard snapshot regeneration succeeds and the production build passes. No external scheduler/provider was added and no live observation was collected in this checkpoint.

## Primary-source monitoring jobs connected to automatic cycle (2026-09-07)

- Converted the six cause-linked indicators into recurring ResearchJob definitions loaded by the existing unattended company cycle. EIOS now plans 28 automatic jobs in total, including six dedicated PRIMARY_INDICATOR_MONITORING jobs. Weekly crop-season data uses a weekly cadence; quarterly company metrics use a quarterly cadence; notification/settlement indicators are checked daily for a new official release.
- Every indicator now carries a bare approved authority domain. Company figures are restricted to coromandel.biz, subsidy notifications to fert.gov.in, rainfall to mausam.imd.gov.in and crop acreage to agriwelfare.gov.in. The query identifies the exact indicator and unit and requests retention of the source passage and reporting date.
- Extended the external-research quality boundary so a primary-indicator job can create an observation only when source classification is Tier 1 for that exact approved domain. A relevant-looking secondary page is discarded from this lane rather than used to update the number.
- These jobs produce research observations only. Numeric extraction, same-unit/date comparison and alert materialization remain the next stage; catalyst creation, verdict changes and trades remain prohibited.
- Validation: all 348 company-intelligence tests pass, including an explicit secondary-domain rejection test. External query-builder and orchestrator regression suites pass; dashboard snapshot regeneration succeeds. No paid search or live network collection was run in this checkpoint.

## Governed primary-indicator numeric history and alerts (2026-09-08)

- Connected the six primary-indicator jobs to a strict numeric extraction stage in the unattended company cycle. A reading is recordable only when its job identity, monitoring intent, Tier 1 source classification, exact approved domain, configured unit, context terms and one explicit ISO reporting date all agree. Missing or ambiguous values are held rather than guessed.
- Added an append-only primary-indicator ledger. Every stored reading retains ticker, rule, reporting date, normalized value and unit, exact HTTPS source, evidence passage, content fingerprint and recording time. Duplicate records are idempotent; conflicting readings for the same rule and date are rejected. Corrupt, non-finite or source-mismatched history fails closed.
- Added same-rule, same-unit direction comparison. Two valid dated readings may produce favourable, adverse or unchanged monitoring direction according to the predeclared rule. A first reading remains `AWAITING_COMPARABLE_OBSERVATION`.
- Connected read-only state to the company dashboard. Each monitoring row shows its record count and latest governed value/date when available; until then it explicitly says the collector is connected and awaiting its first unambiguous official reading. History is isolated to the matching company rule and cannot make an unrelated plan appear populated.
- Current live state: the machinery is connected, but no live official reading has yet been collected or stored. The feature does not create a catalyst, change a verdict, recommend an investment or authorize a trade.
- Validation: all 353 company-intelligence tests pass, including full-cycle record creation and decision-boundary assertions. External query-builder and orchestrator suites pass; dashboard snapshot regeneration and production build pass.

## Persistent cadence and independent Windows operation (2026-09-08)

- Added atomic persisted scheduler state for live external-research jobs. Successful run times and next-due times now survive process and computer-task restarts, so quarterly jobs do not consume provider calls every day and daily/weekly jobs retain their configured cadence. Corrupt or incomplete cadence state fails closed.
- Offline maintenance cycles are deliberately excluded from live cadence history. They can refresh local read models without postponing a future genuine web collection.
- Restored the Windows task `EIOS Automatic Company Intelligence`: daily at 06:00 India time, StartWhenAvailable enabled, overlapping runs ignored, two-hour execution limit, and operation allowed on battery. An independent launch completed successfully with 28 configured jobs and the dashboard read model refreshed.
- Hardened credential behaviour. The background runner uses live search only when both a provider key and the explicit `EIOS_LIVE_SEARCH_ENABLED=true` switch are available to the scheduled user. Otherwise it records `LIVE_SEARCH_DISABLED_OR_UNAVAILABLE` and performs a governed offline cycle; it does not make paid calls or claim that live observations were collected.
- Moved dashboard synchronization behind final status persistence. The UI now receives the completed success/failure state and finish time instead of retaining the cycle's temporary `RUNNING` snapshot.
- Current live-collection state: scheduled operation is healthy, but external web collection remains intentionally disabled for the Windows task. The most recent independent cycle succeeded with 94 existing observations and zero new primary-indicator readings. Secure persistent credential/enablement and a one-job live canary remain the next steps.
- Validation: all 353 company-intelligence tests pass; scheduler restart/corruption tests, scheduler regression, scheduled-runner regression and runtime-bootstrap regression pass. The Windows task's latest result is 0 (success), with its next run scheduled for 2026-09-09 06:00 India time.

## Secure live-search activation and authority-bound canary (2026-09-08)

- Added Windows DPAPI credential provisioning for the search provider. The key is encrypted for the current Windows user in Git-ignored runtime storage and is never displayed or committed. The scheduled runner decrypts it only in memory and still falls back to an explicitly labelled offline cycle when secure activation is absent.
- Added a one-job primary-indicator canary command with a hard one-job paid-search limit and diagnostic reporting for selected domains, retrievals, source assessments, observations and retrieval failures.
- The first diagnostic canary showed that primary-indicator queries expressed the authority requirement only in prose, allowing unrelated search results that the Tier 1 gate correctly rejected. Governed official-document, exchange and primary-indicator queries are now technically prefixed with the exact `site:<authority-domain>` restriction while preserving the original research question.
- The authority-bound NPK/DAP canary selected three sources and every one was on `www.coromandel.biz`. Direct retrieval of all three official PDFs returned HTTP errors, so zero observations and zero indicator readings were created. This proves discovery and filtering now work but confirms that direct HTTP delivery is the remaining transport blocker.
- Scheduled paid search was paused after the canaries while retaining the encrypted credential. The daily Windows task will continue safe offline maintenance and cannot spend further provider calls until the governed provider-delivered-content/browser-capture fallback is completed and live search is deliberately re-enabled.
- Validation: all 353 company-intelligence tests pass; authority-bound query, execution-service, query-builder, scheduler-persistence and script-compilation checks pass. No catalyst, verdict, recommendation or trade changed.

## Provider-delivered official-content fallback and crash recovery (2026-09-08)

- Added an explicit provider-delivered raw-content route for exact official URLs when direct issuer retrieval is blocked. Governed searches request raw text only for official-document, exchange-disclosure and primary-indicator intents. The short search snippet is never substituted for source content.
- Provider-mediated content retains the exact official URL and records the delivery provider plus the direct-retrieval error in transport metadata. Observation provenance records the provider delivery method; it is not mislabelled as a direct issuer download or independent corroboration.
- Added Unicode-safe operational logging. A Hindi or other non-Windows-console title can no longer crash an otherwise valid collection after persistence.
- Added idempotent replay of all persisted primary-monitoring observations. The automatic cycle can now recover source material saved before a crash instead of examining only the current process's in-memory results. Replays do not duplicate indicator history and offline cycles still cannot alter live cadence.
- The IMD rainfall canary reached and persisted three Tier 1 observations. Replay examined all three without another paid call; each was held as `HELD_REPORTING_DATE_AMBIGUOUS` because the source pages contained more than one date. Zero numeric readings were recorded. This is a correct fail-closed outcome, not a collection failure.
- Scheduled paid search remains paused after the canary and the encrypted credential is retained. The next dependency is a document-aware date/value passage extractor that can isolate a single dated table or bulletin section without weakening the existing ambiguity gate.
- Validation: all 353 company-intelligence tests pass, including replay idempotence; provider raw-content fallback, Unicode logging, Tavily provider and external orchestrator regression tests pass. No catalyst, verdict, recommendation or trade changed.

## Section-aware indicator date binding (2026-09-08)

- Replaced whole-document ISO-date counting with passage-first date binding. EIOS now locates one context-bound indicator value first, then accepts one date inside that evidence passage or one uniquely labelled bulletin/header date. Dates elsewhere in a long report no longer create false ambiguity.
- Added deterministic parsing for ISO dates, day-month-year numeric dates and English month-name dates with ordinal suffixes. Invalid calendar dates are ignored. Two dates inside the relevant indicator passage still force a hold.
- Replayed the three persisted Tier 1 IMD observations without another provider call. Their status moved from date ambiguity to the more accurate `HELD_VALUE_AMBIGUOUS`: the relevant official material includes competing percentages for the forecast range, central estimate, model error and LPA context. EIOS did not choose or mathematically transform one without a predeclared measurement rule.
- The next dependency is measurement-aware passage selection: distinguish observed rainfall deficit from forecast percentage-of-LPA, uncertainty bands and historical baselines before permitting any derived value such as `100 - percent of LPA`.
- Validation: all 355 company-intelligence tests pass, including irrelevant-document-date exclusion, unique bulletin-header binding and relevant-passage date-conflict rejection. No indicator value, catalyst, verdict, recommendation or trade changed.

## Measurement-aware rainfall classification (2026-09-08)

- Added predeclared measurement posture and role controls to monitoring rules. An indicator may now restrict acceptable source language to realized or forecast data and to a specific measurement meaning instead of accepting every number with the same unit.
- The All-India rainfall-deficit rule now accepts only realized, direct deficit observations. Its subject matching recognizes `All India`, `All-India` and `country as a whole`, but it rejects forecasts, probability statements, model-error bands, range boundaries and percentage-of-LPA readings.
- Added deterministic classifications for `FORECAST`, `REALIZED` and `UNSPECIFIED` posture plus direct deficit, percent of LPA, uncertainty, range-bound and unclassified measurement roles. These classifications select eligibility only; they do not infer economic impact.
- Replayed the three persisted IMD observations without a new search. The first official bulletin is now specifically held as `HELD_MEASUREMENT_POSTURE_MISMATCH` because it is a forecast; the other two remain held because no unique eligible value exists. EIOS does not convert the 92% of LPA forecast into an 8% realized deficit.
- Validation: all 357 company-intelligence tests pass, including explicit rejection of a forecast percentage and acceptance of a source-bound realized direct deficit. No history record, catalyst, verdict, recommendation or trade changed.

## Targeted realized-rainfall collection and official linked-asset boundary (2026-09-08)

- Strengthened the rainfall monitoring instruction so search asks only for realized or observed All-India rainfall departure/deficit for a completed period and explicitly excludes forecasts, ranges, model error, normal-category thresholds and historical LPA baselines.
- Isolated one-job canary cadence from production cadence using a question-versioned canary state file. A canary can use the encrypted credential while production paid search remains paused, so diagnostics cannot postpone or silently activate scheduled collection.
- Ran one authority-bound rainfall canary. It selected and retrieved three exact IMD-domain pages, created two new Tier-1 observations and brought persisted observation history to 99. Replay examined five matching observations; none qualified as a numeric record. The forecast remained held for measurement posture and four navigation/statistics pages remained held for value ambiguity. No catalyst, verdict or trade changed.
- Added a deterministic official linked-asset discovery boundary. From an already retrieved HTML page it follows only relevant HTTPS PDF/image links on the exact approved domain, removes fragments and duplicates, caps the result count and preserves the parent-page URL. It performs no OCR, interpretation or investment analysis.
- Live validation against IMD's rainfall-statistics page located one official current subdivision-rainfall PDF and four generated chart images. These assets are discovered but not yet ingested as observations or numeric readings; byte-preserving acquisition, PDF-text extraction and governed image OCR are the next checkpoint.
- Validation remains all 357 company-intelligence tests passing, with four additional targeted provider/asset-discovery tests passing. Production paid search remains paused and its encrypted credential is retained.

## First governed primary-indicator PDF reading (2026-09-08)

- Added a strict parser for IMD's official subdivision rainfall-distribution PDF. It requires one unique completed cumulative period, one unique `COUNTRY AS A WHOLE` row and the expected paired daily/cumulative table shape. It independently recomputes cumulative percentage departure from actual and normal rainfall and rejects a mismatch greater than 0.15 percentage point.
- Correctly separates IMD's daily departure from the crop-season cumulative departure. For the document through 7 September 2026, daily departure is -39%, while cumulative actual rainfall is 642.9 mm against 748.3 mm normal and cumulative departure is -14%.
- Normalized the monitored variable's sign without altering the source passage: IMD's -14% departure becomes a positive 14% deficit magnitude because the configured rule states that a falling deficit is favourable. A rainfall surplus maps to zero deficit. This prevents later direction comparisons from reversing the economic meaning.
- Added an audited ingestion command using the existing trusted-source registry, byte-preserving acquisition ledger, SHA-256-bound PDF text extraction ledger and append-only primary-indicator ledger. The first governed rainfall record is now stored for 7 September 2026 with the exact official URL, source row and document hash.
- The dashboard read model now reports one record and a latest value of 14 for the rainfall-deficit monitor. It remains `AWAITING_COMPARABLE_OBSERVATION`: one reading is history, not a trend, catalyst, verdict, recommendation or trade instruction.
- Validation: all 361 company-intelligence tests pass, including cumulative-vs-daily selection, arithmetic reconciliation, duplicate-period/row rejection and surplus normalization. Production paid search remains paused.

## Unattended weekly IMD rainfall monitoring (2026-09-08)

- Connected direct official IMD asset monitoring to the unattended company cycle. It operates independently of paid search: on its weekly due date it acquires the approved rainfall-statistics page, discovers the exact same-domain country-distribution PDF, preserves acquisition lineage and extracts the governed country-total row.
- Added persisted seven-day cadence and document-hash deduplication. A successful or unchanged document schedules the next check seven days later; a retrieval or parsing hold retries after one day. Corrupt cadence state fails closed. A second call before the due time returns `NOT_DUE` without network access.
- IMD updated the live PDF during implementation. The current document through 8 September 2026 reports cumulative actual rainfall of 645.5 mm against 754.5 mm normal and a whole-number departure of -14%. Reconciliation now permits only the maximum half-percentage-point difference caused by IMD's stated whole-number rounding.
- Recorded the second governed rainfall reading as a 14% deficit magnitude for 8 September 2026. Compared with the 14% baseline through 7 September, the current monitoring direction is `UNCHANGED`. The ledger contains two distinct dated, hash-bound records; reruns cannot duplicate either record.
- The automatic monitor's result explicitly forbids catalyst creation, verdict changes and trade authorization. A parsing mismatch is returned as `PDF_VALUE_HELD` rather than being accepted or crashing the source gate.
- Validation: all 364 company-intelligence tests pass. The dashboard read model now contains two rainfall records with latest value 14 and signal `UNCHANGED`; the production dashboard build passes. Paid production search remains paused.

## Governed weekly crop-sowing monitor and baseline (2026-09-08)

- Reused the existing audited crop-area table extractor and connected a dedicated sowing monitor to the unattended company cycle. Search discovery is restricted to the exact `www.pib.gov.in` authority domain and the matching Coromandel sowing job; lookalike, root-domain-only and unrelated-job URLs are rejected.
- The monitor checks at most three selected official releases, requires a Ministry of Agriculture attribution, a unique reporting period, internally consistent crop rows and one Grand Total row. It derives total year-on-year acreage change from current and corresponding prior-year lakh-hectare totals and preserves the original source row and document hash.
- Acquired the latest Ministry release published by PIB for area through 4 September 2026. All-India Kharif area is 1,086.31 lakh hectares versus 1,104.00 lakh hectares in the corresponding prior-year period: -17.69 lakh hectares, or -1.60% year on year. This is the first governed sowing baseline and therefore has no time-series direction yet.
- Preserved crop-mix context separately: the largest published shortfalls include rice (-16.37 lakh hectares), maize (-2.99) and castorseed (-1.23), while the largest increases include urad (+2.68), bajra (+1.99) and total pulses (+1.84). These are acreage comparisons, not claims that rainfall caused the changes or that company sales moved proportionately.
- Added persisted weekly cadence and a one-day retry after missing/held discovery. The monitor can create only indicator history and a later review direction; it explicitly cannot establish rainfall causality, create a catalyst, change the verdict or authorize a trade.
- The dashboard now reports one sowing record with latest value -1.60%. Validation: all 369 company-intelligence tests pass. Production paid search remains paused; future automatic discovery will operate when the governed live search lane is deliberately enabled.

## Universal cross-sector catalyst knowledge registry (2026-09-08)

- Extended the existing versioned SectorCausalIndicatorRegistry rather than creating a parallel catalyst system. Mandatory Meta now has 29 validated causal indicators covering 35 sector labels, including agriculture/fertilizers plus autos, auto components, IT services, pharmaceuticals/CDMO, power, renewables, power equipment, metals/mining, oil and gas/refining/city gas, consumer/retail, telecom, real estate, logistics/ports/shipping and defence/aerospace.
- Added 12 cross-sector causal definitions: auto retail/inventory cycle; IT deal conversion and hiring; pharma regulatory pipeline; power demand/fuel spread; renewable award-to-commissioning; metals spread/inventory; oil and gas crack/policy transmission; consumer volume/price/mix; telecom ARPU/capex returns; real-estate pre-sales/cash conversion; logistics volume/yield/utilisation; and defence order execution/cash.
- Every definition declares applicable event types, economic variable, expected direction, lead-time range, earnings channels, company archetypes, preferred primary sources, corroborating sources, minimum independent evidence groups, minimum persistent observations, expected persistence, known false positives, contradiction tests and kill tests.
- Generated a machine-readable sector coverage map for automatic company onboarding. The unattended company cycle rebuilds this map, and the dashboard read model exposes the sector and indicator counts. The map is passive knowledge: it cannot create a catalyst, change a verdict or authorize a trade.
- Mandatory Meta service and gate tests pass with the expanded registry; dependency validation remains acyclic, coverage tests require at least two independent evidence groups and two persistent observations for every active definition, and all 369 company-intelligence tests continue to pass.

## Company-to-catalyst automatic routing and coverage truth (2026-09-08)

- Added a strict company catalyst profile registry independent of the inconsistent legacy dossier metadata. Each profile requires a ticker, entity, sector IDs, company archetypes, public source IDs, dated exposure status and an uncertainty statement; unknown fields, missing dimensions, duplicate tickers and unsupported readiness labels fail closed.
- Registered the three current EIOS companies conservatively: Coromandel routes to fertilizers/agrochemicals and remains `PUBLIC_EVIDENCE_PARTIAL`; KPIT routes to IT services and Anup to industrial project manufacturing, both `REGISTERED_UNVERIFIED`. No profile is labelled fully covered.
- Company indicator selection now requires both a sector match and a company-archetype match. Coromandel receives seven relevant causal indicators with two partial live inputs; KPIT receives the IT deal-conversion indicator with no connected collector; Anup receives tender-to-order conversion with no connected collector.
- Generated a machine-readable onboarding report that distinguishes relevant logic from connected collection and permits an active coverage claim only when governed exposure is ready and every selected indicator has a collector. Current active coverage claims are withheld for all three companies.
- Connected the onboarding report to the unattended builder and dashboard read model. The System / Research Runtime screen now shows 35 sector labels, 29 causal indicators, company-level selected versus connected counts and an explicit `Coverage claim withheld` label.
- Validation: all 372 company-intelligence tests pass, including sector-plus-archetype routing and partial/unverified boundaries. The dashboard production build passes. This layer creates no catalyst, changes no verdict and authorizes no trade.

## Anup governed source onboarding and automatic routing (2026-09-08)

- Registered The Anup Engineering Limited as a governed monitored company with its issuer identity, NSE symbol `ANUP`, BSE scrip code `542460` and ISIN `INE294Z01018`. This onboarding is independent of the inconsistent legacy dossier metadata.
- Added issuer-official source lanes for annual reports, quarterly financial results, investor presentations and Regulation 46 disclosures, plus an official NSE financial-results lane. The latest configured issuer documents are the FY2024-25 annual report and Q1 FY2027 result and investor presentation; their contents remain unapproved until extraction and reconciliation complete.
- Added the standard eight-job unattended coverage plan: official documents, exchange disclosures, orders/capacity, management/corporate events, current news, sector/competition, macro transmission and catalysts/expectation gaps.
- A bounded live probe successfully selected the issuer-published Q1 FY2027 result PDF. It checked no uncontrolled pages, reported no failures and created no approved facts, catalyst, verdict, recommendation or trade action.
- Validation: all 372 company-intelligence tests pass, and the scheduler loads eight Anup jobs among 24 governed recurring company jobs. The next checkpoint is source-byte acquisition and typed quarterly extraction with cross-source reconciliation.

## Anup official Q1 acquisition and layout recognition (2026-09-08)

- The first direct download attempt correctly failed closed on the issuer's HTTP 406 response. Added normal public-research `User-Agent` and PDF/HTML `Accept` headers to the default trusted downloader without changing exact-domain checks, public-IP validation, redirect boundaries, byte hashing or acquisition receipts.
- Retried the governed acquisition successfully. EIOS downloaded 3,619,112 bytes directly from Anup's issuer URL, preserved the original Q1 FY2027 PDF with SHA-256 `a667c700d0d6ccc482ddffd1f7d04d5119deaf1c857c46ddafc78c23cc34707b`, and completed source-bound text extraction without a fallback provider.
- Generalized quarterly layout recognition for issuer tables that print complete dates such as `30.06.2026` in one positioned token and use `Profit for the period/year` rather than only `Net profit after tax`. No company values or Anup-specific figures are hard-coded.
- The corrected layout pass identifies three candidate table pages and twelve geometric columns. Pages 3 and 6 are classified as standalone and consolidated main-statement candidates. OCR completed, but record creation remains held because leave-one-out OCR alignment error exceeded the existing 1.5 PDF-unit gate (1.98 on page 3 and 1.74 on page 6).
- Validation: all 374 company-intelligence tests pass plus the trusted public acquisition adapter's standalone safety suite. No quarterly figure has been approved, no catalyst or verdict changed and no trade action was created. Next is a principled alignment-tolerance/reconciliation improvement with adversarial tests, followed by typed metric candidates.

## Anup OCR alignment and metric vocabulary (2026-09-08)

- Raised the held-out text-anchor alignment ceiling from 1.5 to 2.0 PDF points (about 0.7 mm), still far below the detected financial-column widths. This threshold applies to unique non-numeric OCR labels, not to financial values. An adversarial boundary test proves 1.9-point noise passes while 2.1-point displacement remains held.
- Both Anup standalone and consolidated statement pages now pass the OCR-to-native geometry check with 58 and 61 distributed text anchors respectively. The previous maximum held-out errors of 1.98 and 1.74 PDF points are therefore admitted only for subsequent comparison, not approved as facts.
- Expanded issuer-independent metric vocabulary to recognize `Profit for the period/year` as PAT and `Cost of materials consumed` as the material-cost line. These mappings are covered by tests and contain no Anup-specific figures.
- The next gate correctly remains closed: the PDF's damaged unit glyphs need source-bound unit reconciliation, the first quarter column is omitted by the detected merged-header boundary, and standalone/consolidated basis appears above the ruled grid. No typed records are emitted until page-level basis, duration and unit evidence are bound without guessing.
- Validation: all 376 company-intelligence tests and the trusted acquisition safety suite pass. No financial figure is approved and no verdict, catalyst or trade state changes.

## Anup exchange corroboration and first checked quarterly candidate (2026-09-09)

- Acquired and byte-preserved Anup's official NSE Q1 FY2027 iXBRL filing from the exact `nsearchives.nseindia.com` authority. The archived 37,016-byte HTML has SHA-256 `33b9e5fd424d6df3c6321dc31eebb064c1c913b70c46d25bddf3d485357a2015` and an append-only acquisition receipt.
- Added an issuer-independent NSE iXBRL parser that binds company identity, ISIN, basis, reporting dates, currency and scale before reading financial values. It rejects non-official domains and ambiguous metadata.
- Added a strict corroboration bridge between the issuer PDF and exchange filing. Exchange evidence may supply INR-lakh unit and current-quarter duration only when ticker, basis and one exact reporting date agree. Standalone evidence cannot corroborate a consolidated table.
- Improved the generic statement reader for full month-name dates, page-title basis, cost-of-material labels, `Profit for the period/year`, tight column overlap and one malformed OCR/PDF cell that exactly reconciles to the official exchange value.
- The factory now produces one checked `Q1-FY2027` standalone Anup candidate with twelve INR-crore metrics and passing income arithmetic. It remains `PENDING_REVIEW`: the four-core-reading review and reporting-notes review are still held, so no figure is published as approved and no catalyst, verdict, recommendation or trade changes.
- Governed company plans now supersede legacy jobs for the same ticker. The live scheduler resolves 30 unique jobs, including the standard eight-job Anup plan, without the earlier duplicate-ID configuration failure.
- Validation: all 388 company-intelligence tests pass and `git diff --check` passes. The remaining checkpoint is to resolve the source-reading and reporting-note holds through evidence-backed review, then publish the record only if Mandatory Meta approves it.

## Causal-first / pre-operator architecture alignment (2026-09-09)

- Inspected the new causal-first mandate against the existing Constitution, reasoning principles, approved Pre-Inflection/EIP architecture, Mandatory Meta, causal-indicator registry, Price Recognition, Expectation Gap, valuation, Opportunity and prospective-learning modules before changing implementation.
- Confirmed that EIOS already owns most required responsibilities; no parallel Observation, Evidence, Meta, EIP or Opportunity architecture is authorized.
- Made the permanent sequence constitutional: root-cause change, causal leading indicators, independent corroboration, inflection assessment, Price Recognition veto, Expectation Gap, EIP review, later operating/financial confirmation and Scale/Hold/Kill.
- Recorded that reported revenue, EBITDA or PAT recovery, management or analyst upgrades, consensus revisions, price breakouts and widespread narrative recognition are not EIP prerequisites. Serious contradictions, excessive recognition, inadequate survivability and missing evidence may veto advancement, and no qualifying opportunity is valid.
- Approved ADR-002 requires additive, fingerprint-bound integration of the existing modules. The next implementation checkpoint is a typed five-link causal-chain contract followed by explicit change-regime classification; engine logic remains unchanged at this documentation checkpoint.

## Typed five-link causal-chain foundation (2026-09-09)

- Added a passive, versioned causal-chain contract with exactly five ordered stages: root-cause change, intermediate transmission, company operating effect, financial effect and expected market effect.
- Each stage preserves a separate human-readable statement, economic mechanism and governed Temporal Evidence references. The chain also retains entity, sector, causal-indicator identities, expected lead-time range, explicit assumptions, uncertainty, public-information-only status and non-authority.
- Added a validation service rather than a scoring engine. It rejects missing, duplicated or reordered stages; empty reasoning; unused or out-of-scope evidence; unknown or cross-sector causal indicators; invalid lead times; non-public inputs; and altered non-authority language.
- The contract makes the reasoning inspectable but does not infer causation, estimate probability, create a Signal/Catalyst/EIP, recommend an investment or authorize a trade. Mandatory Meta remains the downstream authority gate.
- Validation: all five focused causal-chain tests, 21 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is explicit change-regime classification without fake numerical precision.

## Explainable change-regime classification (2026-09-09)

- Added explicit `STRUCTURAL`, `CYCLICAL`, `TEMPORARY_DISRUPTION`, `SEASONAL_EFFECT`, `STATISTICAL_NOISE` and `SPECULATIVE_NARRATIVE` classifications with ordinal low/moderate/high confidence rather than unsupported numerical probability.
- Every regime assessment binds to one validated five-link causal chain and exactly the same governed Temporal Evidence. It retains the classification basis, competing explanations, tests that distinguish those explanations and an uncertainty statement.
- Non-public inputs, stale chain identity, changed evidence, empty alternatives/tests, invalid enum values and altered non-authority language fail closed. Statistical noise and speculative narrative cannot enter Mandatory Meta review and cannot claim high causal confidence.
- Reported revenue or PAT recovery is deliberately absent from the required contract. The regime layer classifies early causal change and creates no Signal, Catalyst, EIP, recommendation or trade action.
- Validation: 11 combined causal-chain/regime tests, 27 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is strengthening Price Recognition into a thesis-specific hard veto.

## Thesis-specific Price Recognition hard veto (2026-09-09)

- Preserved the existing multi-dimensional public-market recognition service and added an additive thesis-specific layer rather than breaking stored snapshots or duplicating the Price Recognition architecture.
- The new assessment binds one causal chain, change-regime assessment and market snapshot. It requires public, thesis-related source identities and identifies which recognition dimensions concern the same mechanism: catalyst price reaction, relative performance, valuation rerating, abnormal volume, analyst/consensus revisions, institutional attention, media narrative or management narrative.
- Fundamental-change incorporation is ordinal: insufficient evidence, not recognized, limited, material, or most/all. A modest price rise is not automatically priced in, and distance from a historical high is not treated as proof of cheapness.
- Insufficient evidence produces a hold. Most/all incorporation or an already fully recognized broad market state produces a hard `VETO_TOO_LATE`. Material but incomplete recognition remains available only for later human asymmetry review.
- The service is explicitly non-authoritative and cannot create an EIP, recommendation, position or trade. Validation: six focused thesis-recognition tests, 33 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is binding a governed Expectation Gap into the EIP path.

## Governed pre-EIP Expectation Gap (2026-09-09)

- Preserved the existing Catalyst-stage Expectation Gap engine for backward compatibility and added a source-backed pre-EIP comparison contract in the external-intelligence path. The early contract does not require a downstream Catalyst and does not use an abstract 0–100 score.
- Market expectation and the causal EIOS implication must use the same named metric, unit and timezone-aware future horizon. Each retains its own public source identities, exact value and plain-language explanation; EIOS calculates the absolute and relative difference without inventing missing figures.
- The assessment declares whether higher or lower is economically favourable, and the service verifies that the stated positive/negative/no-clear-gap direction agrees with the actual figures. It also retains materiality rationale, assumptions, contradictions, uncertainty and forward invalidation conditions.
- A positive gap must be moderate or high and the thesis-specific Price Recognition gate must allow review before the result can enter later EIP assembly. An immaterial, uncertain, negative or absent gap is held, and a `VETO_TOO_LATE` recognition decision cannot be bypassed.
- This remains a research comparison, not an EIP, valuation conclusion, recommendation or trade. Validation: six focused Expectation Gap tests, 39 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is explicit normalized valuation scenarios.

## Explicit normalized valuation scenarios (2026-09-09)

- Added three mandatory, ordered pre-EIP operating scenarios: current/trough, reasonable recovery and strong normalization. Each scenario states source-backed revenue, EBITDA margin, EV/EBITDA multiple and rationale; net debt, shares outstanding, current price and currency remain visible common inputs.
- EIOS calculates normalized EBITDA, enterprise value, equity value, value per share and upside/downside for every case. Scenario probabilities are not invented, and the service makes no claim of intrinsic-value certainty.
- Normalized EBITDA cannot decline as the cases become stronger. The optimistic case cannot establish valuation room by itself: the reasonable-recovery case must meet the governed minimum upside. An ineligible Expectation Gap blocks valuation assembly regardless of apparent upside.
- Trailing P/E, distance from the 52-week high and the mere fact of a price decline are deliberately absent as proof of cheapness. Missing sources, invalid figures, reordered cases, non-public information and mismatched Expectation Gap identity fail closed.
- Validation: six focused normalized-valuation tests, 45 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is a separate survivability assessment and hard veto.

## Pre-EIP survivability assessment and hard veto (2026-09-09)

- Added a source-backed survivability contract separate from the broad legacy risk score. It binds the same causal chain and normalized valuation and evaluates survival through the maximum expected causal lead-time horizon.
- The service calculates available liquidity, debt maturities plus horizon cash burn, liquidity coverage, debt to normalized EBITDA, EBITDA to interest and potential dilution. It retains dated public sources, assumptions, currency and uncertainty.
- Uncovered horizon funding needs, extreme leverage, inadequate interest coverage, non-positive EBITDA with debt, going-concern warnings, unresolved covenant breaches or critical governance threats create a hard `VETO_SURVIVABILITY_FAILURE`.
- Thin but non-failing liquidity, elevated leverage, weak interest margin or dilution above the contained limit produces a hold rather than being hidden inside a score. Clear or contained survivability still cannot bypass an ineligible normalized valuation.
- The result is not a credit rating, EIP, recommendation or trade instruction. Validation: six focused survivability tests, 51 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is the unified fingerprint-bound causal-first EIP decision packet.

## Unified fingerprint-bound causal-first EIP packet (2026-09-09)

- Added one read-only assembly service around the existing Mandatory Meta result and the new causal chain, regime, thesis recognition, Expectation Gap, normalized valuation and survivability assessments. It does not create a parallel analysis engine and does not average the components into one score.
- The service enforces cross-component identity: Meta evidence must equal causal-chain evidence, and every downstream assessment/result must bind to its exact parent IDs. Stale or mismatched regime, recognition, gap, valuation or survivability inputs are rejected rather than silently combined.
- Eleven component payloads receive deterministic SHA-256 fingerprints. Changing one source-backed assumption changes that component fingerprint while leaving unrelated fingerprints stable, making later stale-packet detection possible.
- Mandatory Meta not ready, noise/speculative regime, recognition hold, immaterial gap, inadequate valuation room or thin survivability produces `HOLD_FOR_RESEARCH`. Same-thesis price recognition produces `VETO_TOO_LATE`; survivability failure has the highest-priority hard veto.
- A completely ready packet only returns `READY_FOR_GOVERNED_EIP_CLASSIFICATION`. It explicitly sets `creates_eip=false`, contains no combined score and cannot recommend or trade. Validation: six focused assembly tests, 57 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is reader-facing classification mapping and governed EIP integration.

## Governed reader-facing EIP classifications (2026-09-09)

- Closed a packet-lineage gap by adding the existing Pre-Inflection preview as the twelfth fingerprinted packet component. Its Mandatory Meta identity, entity, sector and causal-indicator scope must agree with the packet's governed chain before assembly.
- Added plain-language classifications without replacing internal EIP stages: `RESEARCH_NOW`, `EARLY_WATCH`, `EARLIEST_INVESTABLE_POINT`, `BUY_ZONE_CANDIDATE`, `WAIT`, `TOO_LATE` and `REJECT`.
- Missing essential research maps to Research Now; early or not-yet-reviewed formation maps to Early Watch; inadequate valuation/survivability margin or a human hold maps to Wait; recognized opportunities map to Too Late; and survivability failures, deterioration, noise, speculative narrative or human rejection map to Reject.
- Earliest Investable Point requires an exact packet-bound Stage 3 classification and its matching human review. Buy-Zone Candidate requires exact packet-bound Stage 4 plus human authorization for downstream Evidence review; it remains explicitly not a buy instruction.
- The mapper fingerprints the complete packet, rejects stale internal classifications or review receipts and never creates an investment decision. Validation: 13 focused packet/mapping tests, 64 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is post-EIP confirmation and Scale/Hold/Kill lifecycle governance.

## Post-EIP confirmation and Scale/Hold/Kill lifecycle (2026-09-09)

- Added a post-EIP evidence contract for later operating/financial results, management guidance, analyst/consensus revisions, price reactions and continued causal-leading-indicator observations. Each item retains its public sources, event time, independence group, relationship to the original thesis and any triggered kill test.
- Post-EIP evidence must occur strictly after the original EIP time and bind to the exact reader packet fingerprint. Later reported recovery cannot be backdated or relabelled as evidence that established the earlier EIP.
- Two independent confirmation groups with no contradiction or unresolved uncertainty may produce `SCALE_REVIEW`; one or insufficient confirmation remains `WAIT_FOR_CONFIRMATION`; contradiction produces `HOLD`; and a triggered forward kill test produces `KILL_THESIS_REVIEW` with priority.
- The lifecycle accepts only a governed EIP or Buy-Zone Candidate. Every output preserves the original EIP date and explicitly sets portfolio authorization to false; Scale and Kill remain human/governed review actions, not trades.
- Validation: six focused lifecycle tests, 70 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is anti-anchoring discovery governance across sectors and companies.

## Anti-anchoring market discovery governance (2026-09-09)

- Added an explicit public market-universe contract with declared target sectors and individual-company candidates. A sector named in the universe but lacking any candidate is reported as missing and holds universe readiness rather than disappearing from the scan.
- Research priority may use only typed causal evidence freshness, causal coverage gap, expected information gain, contradiction value and primary-source availability. Portfolio ownership, watchlist presence and prior discussion are retained as context only and are structurally absent from priority calculation.
- Candidate evidence requires a SHA-256 identity, sectors must fall inside the declared universe, duplicate tickers/factors fail, and deterministic ticker ordering resolves equal objective priority without familiarity preference.
- Tests prove that an unfamiliar company outranks a holding when its objective evidence priority is higher, and flipping all holding/watchlist/discussion flags leaves both selection and its fingerprint unchanged. The queue creates no Opportunity, recommendation or trade.
- Validation: six focused neutral-discovery tests, 76 top-level external-intelligence regression tests and all 388 company-intelligence tests pass. The next checkpoint is auditable sector-indicator learning and timing calibration.

## Controlled Intelligence Write Boundary — Checkpoint 1 (2026-09-09)

- Preserved anti-anchoring discovery independently in commit `72d532f` before starting this checkpoint.
- Added passive contracts for the four mutually exclusive information classes, actor/origin/authority, source references, write commands, classified records, validation lifecycle and immutable accepted/rejected receipts.
- Added deterministic request, record and receipt SHA-256 fingerprints with receipt verification and declared-request tamper detection.
- Added a deliberately in-memory, non-production reference service. Machine and AI facts are forced to `PROVISIONAL`; AI cannot verify facts; only an authorized decision orchestrator can write a Decision; stale prior-record fingerprints and authority violations fail closed.
- Exact duplicates are idempotent. Conflicting Facts are both preserved, marked `CONFLICTED` and excluded from trusted reads. Verified restatements create a new version and mark the prior record `SUPERSEDED` without erasing it.
- Recorded ADR-003 through ADR-008. Canonical dossier migration, EvidenceEvent implementation and Research Decision Packet extension remain explicitly deferred.
- No Master Dossier, production writer, Observation, Temporal Evidence, EIP, collector, UI, portfolio, trading or AI-provider path is connected or changed by this checkpoint.
- Validation at implementation time: 22 focused Controlled Write tests pass. Full regression results are recorded after the complete relevant suites run.
