'use client';

import { useMemo, useRef, useState } from 'react';
import { ArrowRight, BookOpen, BookOpenCheck, Building2, CheckCircle2, ExternalLink, FileSearch, Inbox, Newspaper, Search, ShieldAlert, Sparkles, Target, TrendingUp } from 'lucide-react';

type Evidence = { title: string; category: string; confidence: number | null };
type Discovery = { title: string; sourceUrl: string; discoveredAt: string | null; researchIntent: string; sourceQualityTier: string; reviewStatus: string; verdictImpact: string };
type ExtractedFact = { factId: string; kind: string; statement: string; period: string | null; sourcePage: string | null };
type ReviewInboxItem = {
  candidateId: string;
  queuePath: string;
  metaPath: string;
  eventType: string;
  statementPosture: string;
  sourcePassage: string;
  explicitAmounts: string[];
  explicitDates: string[];
  pdfPage: number | null;
  sourceUrl: string;
  reviewStatus: string;
  meta: null | {
    decision: string;
    authorityStatus: string;
    relevanceStatus: string;
    materialityStatus: string;
    causalityStatus: string;
    contradictionStatus: string;
    verdictImpact: string;
    reasonCodes: string[];
    uncertaintyStatement: string;
  };
};
type ReviewInbox = { total: number; ready: number; held: number; approved: number; items: ReviewInboxItem[] };
type AnnualReport = {
  financialYear: string;
  title: string;
  officialUrl: string;
  access: 'DIRECT_OFFICIAL_PDF' | 'OFFICIAL_ARCHIVE';
  status: 'EXTRACTED_PENDING_HUMAN_REVIEW' | 'AVAILABLE_NOT_EXTRACTED';
  extractedFactCount: number;
  highlights: string[];
};
type AnnualReportStudy = {
  status: string;
  extractionCoveragePercent: number;
  availableYears: number;
  extractedYears: number;
  reviewedYears: number;
  metaStatus: string;
  metaPermittedConclusion: string;
  verdictStatus: string;
  findings: { findingId: string; category: string; headline: string; interpretation: string; confidencePercent: number; status: string }[];
  missingWork: string[];
};
type IntelligenceSnapshot = {
  generatedAt: string;
  verdictStatus: string;
  verdict: string | null;
  confidencePercent: number | null;
  verdictReasons: string[];
  unresolvedGaps: string[];
  requiresHumanReview: boolean;
  layers: { name: string; status: string; summary: string; coveragePercent: number }[];
  longTerm: { status: string; permittedConclusion: string; coveragePercent: number };
  alpha: { status: string; permittedConclusion: string; coveragePercent: number };
  news: { status: string; items: unknown[]; statement: string };
};
type Company = {
  name: string;
  ticker: string;
  sector: string;
  evidenceCount: number;
  averageEvidenceConfidence: number | null;
  latestEvidenceAt: string | null;
  recentEvidence: Evidence[];
  recentDiscoveries: Discovery[];
  reviewInbox: ReviewInbox;
  officialSourceCount: number;
  officialSourceTypes: string[];
  sourceDiscoveryStatus: string;
  extractedFactCount: number;
  extractedFacts: ExtractedFact[];
  extractionStatus: string;
  annualReportArchiveUrl: string | null;
  annualReportGovernanceNote: string | null;
  annualReports: AnnualReport[];
  annualReportStudy: AnnualReportStudy | null;
  intelligenceSnapshot: IntelligenceSnapshot | null;
  researchLink: { relevance: string; company_bridge_ready: boolean; reason: string; permitted_claim: string } | null;
  companyBridgeReady: boolean;
  datedCatalystReady: boolean;
  readiness: string;
  readinessLabel: string;
};

const decisionSpine = [
  { step: '01', title: 'Decision now', detail: 'Long-Term + Alpha' },
  { step: '02', title: 'What changed', detail: 'Material deltas' },
  { step: '03', title: '10-year story', detail: 'Business evolution' },
  { step: '04', title: 'Financial path', detail: 'Quality + returns' },
  { step: '05', title: 'Current intelligence', detail: 'News + events' },
  { step: '06', title: 'Catalysts', detail: 'Expectations + timing' },
  { step: '07', title: 'Value + risk', detail: 'Contradictions' },
  { step: '08', title: 'Evidence audit', detail: 'Sources + monitoring' },
] as const;

export function CompanySearch({ companies }: { companies: Company[] }) {
  const [query, setQuery] = useState('');
  const [selectedTicker, setSelectedTicker] = useState(companies.find((company) => company.intelligenceSnapshot)?.ticker ?? companies[0]?.ticker ?? '');
  const [activeLens, setActiveLens] = useState<'longTerm' | 'alpha'>('longTerm');
  const [reviewing, setReviewing] = useState<{ item: ReviewInboxItem; decision: 'APPROVE' | 'HOLD' | 'REJECT' } | null>(null);
  const [reviewRationale, setReviewRationale] = useState('');
  const [reviewConfidence, setReviewConfidence] = useState('70');
  const [reviewFeedback, setReviewFeedback] = useState<Record<string, string>>({});
  const [submittingReview, setSubmittingReview] = useState(false);
  const detailRef = useRef<HTMLElement>(null);
  const normalizedQuery = query.trim().toLocaleLowerCase();
  const matches = useMemo(() => companies.filter((company) =>
    !normalizedQuery || [company.name, company.ticker, company.sector].some((value) => value.toLocaleLowerCase().includes(normalizedQuery))
  ), [companies, normalizedQuery]);
  const selected = matches.find((company) => company.ticker === selectedTicker) ?? matches[0];

  function openCompany(ticker: string) {
    setSelectedTicker(ticker);
    window.setTimeout(() => detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 0);
  }

  async function submitReview() {
    if (!reviewing || reviewRationale.trim().length < 10) return;
    setSubmittingReview(true);
    try {
      const response = await fetch('http://127.0.0.1:3001/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          candidateId: reviewing.item.candidateId,
          queuePath: reviewing.item.queuePath,
          metaPath: reviewing.item.metaPath,
          decision: reviewing.decision,
          rationale: reviewRationale.trim(),
          approvedConfidence: reviewing.decision === 'APPROVE' ? Number(reviewConfidence) : undefined,
          reviewer: 'EIOS_LOCAL_USER',
        }),
      });
      const result = await response.json() as { ok: boolean; error?: string };
      if (!response.ok || !result.ok) throw new Error(result.error || 'Review could not be recorded.');
      setReviewFeedback((current) => ({ ...current, [reviewing.item.candidateId]: reviewing.decision }));
      setReviewing(null);
      setReviewRationale('');
    } catch (error) {
      setReviewFeedback((current) => ({ ...current, [reviewing.item.candidateId]: error instanceof Error ? error.message : 'Review service is unavailable.' }));
    } finally {
      setSubmittingReview(false);
    }
  }

  return (
    <section className="panel mt-6 rounded-3xl border border-white/8 p-6 sm:p-7" id="company-search">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div><p className="eyebrow">Company intelligence</p><h2 className="mt-1 text-xl font-semibold text-white">Search companies known to EIOS</h2><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">Results come only from governed production observations. Evidence is not automatically treated as a catalyst or investment case.</p></div>
        <label className="relative block w-full lg:max-w-md"><span className="sr-only">Search by company, ticker or sector</span><Search aria-hidden="true" className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search company, ticker or sector" className="h-12 w-full rounded-2xl border border-white/10 bg-[#081619] pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-emerald-400/45 focus:ring-2 focus:ring-emerald-400/10" /></label>
      </div>

      {selected ? <div className="mt-6 grid gap-5 lg:grid-cols-[0.72fr_1.28fr]">
        <div className="space-y-3">
          {matches.map((company) => <button key={company.ticker} type="button" aria-pressed={selected.ticker === company.ticker} onClick={() => openCompany(company.ticker)} className={`group w-full rounded-2xl border p-4 text-left transition ${selected.ticker === company.ticker ? 'border-emerald-400/30 bg-emerald-400/[0.07]' : 'border-white/7 bg-white/[0.02] hover:border-white/15'}`}>
            <div className="flex items-start justify-between gap-3"><div className="flex gap-3"><span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-white/5 text-slate-300"><Building2 aria-hidden="true" size={18} /></span><div><p className="font-medium text-white">{company.name}</p><p className="mt-1 text-xs text-slate-500">{company.ticker} · {company.sector}</p></div></div><span className="rounded-full bg-sky-400/10 px-2.5 py-1 text-xs text-sky-200">{company.evidenceCount} items</span></div>
            <div className="mt-4 flex items-center justify-end gap-1.5 text-xs font-medium text-emerald-300">Open company <ArrowRight aria-hidden="true" className="transition-transform group-hover:translate-x-0.5" size={14} /></div>
          </button>)}
        </div>

        <article ref={detailRef} tabIndex={-1} className="scroll-mt-5 rounded-2xl border border-white/7 bg-black/10 p-5 outline-none sm:p-6">
          <div className="flex flex-col gap-4 border-b border-white/7 pb-5 sm:flex-row sm:items-start sm:justify-between"><div><p className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-300">{selected.ticker}</p><h3 className="mt-1 text-2xl font-semibold text-white">{selected.name}</h3><p className="mt-1 text-sm text-slate-500">{selected.sector}</p></div><span className="inline-flex items-center gap-2 self-start rounded-full border border-amber-300/18 bg-amber-300/[0.07] px-3 py-1.5 text-xs text-amber-200"><ShieldAlert aria-hidden="true" size={14} />{selected.readinessLabel}</span></div>
          <nav aria-label={`${selected.name} research sections`} className="-mx-1 mt-4 flex gap-1 overflow-x-auto px-1 pb-1"><SectionLink href="#decision-now" label="Decision Now" /><SectionLink href="#what-changed" label="What Changed" /><SectionLink href="#review-inbox" label="Review Inbox" /><SectionLink href="#ten-year-story" label="10-Year Story" /><SectionLink href="#report-library" label="Reports" /><SectionLink href="#evidence-audit" label="Evidence" /></nav>
          <div className="mt-5 grid gap-3 sm:grid-cols-5"><Metric label="Evidence" value={`${selected.evidenceCount}`} /><Metric label="Official sources" value={`${selected.officialSourceCount}`} /><Metric label="Extracted facts" value={`${selected.extractedFactCount}`} /><Metric label="Average confidence" value={selected.averageEvidenceConfidence === null ? 'Not scored' : `${selected.averageEvidenceConfidence}%`} /><Metric label="Dated catalyst" value={selected.datedCatalystReady ? 'Verified' : 'Not verified'} warning={!selected.datedCatalystReady} /></div>
          {selected.intelligenceSnapshot && <section id="decision-now" className="mt-5 scroll-mt-24 overflow-hidden rounded-2xl border border-white/9 bg-[#071316]">
            <div className="border-b border-white/8 p-4 sm:p-5">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between"><div><p className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-300">Decision cockpit</p><h4 className="mt-1 text-xl font-semibold text-white">Why EIOS is holding its verdict</h4><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">A verdict is shown only when every mandatory evidence layer is complete. Analysis coverage and confidence remain separate.</p></div><div className="rounded-xl border border-amber-300/18 bg-amber-300/[0.07] px-4 py-3"><p className="text-[0.62rem] font-semibold uppercase tracking-[0.13em] text-amber-300">Current verdict</p><p className="mt-1 text-base font-semibold text-amber-100">{selected.intelligenceSnapshot.verdictStatus.replaceAll('_', ' ')}</p><p className="mt-1 text-xs text-amber-200/60">Human review required</p></div></div>
              <div className="mt-5 grid gap-3 md:grid-cols-2">
                <LensButton icon={TrendingUp} title="Long-Term Compounder" subtitle="Business quality · management · valuation" active={activeLens === 'longTerm'} status={selected.intelligenceSnapshot.longTerm.status} coverage={selected.intelligenceSnapshot.longTerm.coveragePercent} onClick={() => setActiveLens('longTerm')} />
                <LensButton icon={Target} title="Alpha / Change" subtitle="Signals · catalysts · expectation gap" active={activeLens === 'alpha'} status={selected.intelligenceSnapshot.alpha.status} coverage={selected.intelligenceSnapshot.alpha.coveragePercent} onClick={() => setActiveLens('alpha')} />
              </div>
              <div className="mt-5 border-t border-white/7 pt-4"><div className="flex items-center justify-between gap-3"><div><p className="text-[0.62rem] font-semibold uppercase tracking-[0.15em] text-slate-500">EIOS Decision Spine</p><p className="mt-1 text-xs text-slate-500">One causal route from conclusion to source evidence</p></div><span className="rounded-full bg-violet-300/8 px-2.5 py-1 text-[0.6rem] font-semibold uppercase tracking-[0.1em] text-violet-200">EIOS signature sequence</span></div><div className="mt-3 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">{decisionSpine.map((item, index) => <div key={item.step} className={`relative rounded-xl border p-3 ${index === 0 ? 'border-emerald-300/22 bg-emerald-300/[0.055]' : 'border-white/7 bg-white/[0.02]'}`}><div className="flex items-center gap-2"><span className={`text-[0.62rem] font-semibold ${index === 0 ? 'text-emerald-300' : 'text-slate-600'}`}>{item.step}</span><p className="text-xs font-medium text-slate-200">{item.title}</p></div><p className="mt-1 pl-6 text-[0.65rem] text-slate-600">{item.detail}</p></div>)}</div></div>
            </div>
            <div className="p-4 sm:p-5">
              <div className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
                <div><p className="text-[0.65rem] font-semibold uppercase tracking-[0.13em] text-slate-500">Permitted conclusion</p><p className="mt-2 text-sm leading-6 text-slate-200">{selected.intelligenceSnapshot[activeLens].permittedConclusion}</p><div className="mt-4 grid gap-2 sm:grid-cols-2">{selected.intelligenceSnapshot.layers.filter((layer) => activeLens === 'longTerm' ? ['financials','management','competition','risks_and_contradictions','valuation','master_dossier'].includes(layer.name) : ['macro','sector','micro','news_and_filings','company_events','meta_causality','catalysts','expectations'].includes(layer.name)).map((layer) => <div key={layer.name} className="rounded-xl border border-white/7 bg-white/[0.025] p-3"><div className="flex items-center justify-between gap-2"><span className="text-[0.65rem] font-semibold uppercase tracking-[0.08em] text-slate-400">{layer.name.replaceAll('_', ' ')}</span><span className={`text-[0.62rem] ${layer.status === 'READY' ? 'text-emerald-300' : layer.status === 'NOT_STARTED' ? 'text-slate-600' : 'text-amber-300'}`}>{layer.status.replaceAll('_', ' ')}</span></div><div className="mt-2 h-1.5 overflow-hidden rounded-full bg-white/5"><div className={`h-full rounded-full ${layer.status === 'READY' ? 'bg-emerald-300' : 'bg-amber-300'}`} style={{ width: `${layer.coveragePercent}%` }} /></div></div>)}</div></div>
                <aside className="rounded-xl border border-rose-300/12 bg-rose-300/[0.035] p-4"><div className="flex items-center gap-2"><ShieldAlert aria-hidden="true" className="text-rose-300" size={16} /><p className="text-xs font-semibold uppercase tracking-[0.12em] text-rose-200">What blocks the verdict</p></div><ul className="mt-3 space-y-2">{selected.intelligenceSnapshot.unresolvedGaps.slice(0, 6).map((gap) => <li key={gap} className="flex gap-2 text-xs leading-5 text-slate-400"><span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-rose-300" />{gap.replaceAll('_', ' ')}</li>)}</ul><p className="mt-3 text-[0.65rem] text-slate-600">+ {Math.max(0, selected.intelligenceSnapshot.unresolvedGaps.length - 6)} additional mandatory gaps</p></aside>
              </div>
              <div className="mt-4 flex gap-3 rounded-xl border border-sky-300/12 bg-sky-300/[0.035] p-4"><Newspaper aria-hidden="true" className="mt-0.5 shrink-0 text-sky-300" size={17} /><div><p className="text-xs font-semibold uppercase tracking-[0.12em] text-sky-200">Current news basis</p><p className="mt-1 text-xs leading-5 text-slate-400">{selected.intelligenceSnapshot.news.statement}</p></div></div>
            </div>
          </section>}
          {selected.recentDiscoveries.length > 0 && <section id="what-changed" className="mt-5 scroll-mt-24 rounded-2xl border border-white/8 bg-white/[0.018] p-4 sm:p-5"><div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div><p className="text-xs font-semibold uppercase tracking-[0.15em] text-sky-200">02 · What changed</p><h4 className="mt-1 text-base font-medium text-white">Automatic discoveries awaiting judgment</h4><p className="mt-1 text-xs leading-5 text-slate-500">Collected items are not evidence. EIOS first tests relevance and source authority; verdict impact remains locked.</p></div><span className="self-start rounded-full border border-sky-300/12 bg-sky-300/[0.05] px-3 py-1.5 text-xs text-sky-200">{selected.recentDiscoveries.length} recent discoveries</span></div><div className="mt-4 space-y-2">{selected.recentDiscoveries.map((item, index) => <article key={`${item.title}-${index}`} className="grid gap-3 rounded-xl border border-white/7 bg-black/10 p-3.5 sm:grid-cols-[1fr_auto]"><div><div className="flex flex-wrap items-center gap-2"><span className="rounded-full bg-white/5 px-2 py-1 text-[0.58rem] font-semibold uppercase tracking-[0.08em] text-slate-500">{item.researchIntent.replaceAll('_', ' ')}</span><span className="text-[0.62rem] text-slate-600">{item.sourceQualityTier.replaceAll('_', ' ')}</span></div><a href={item.sourceUrl} target="_blank" rel="noreferrer" className="mt-2 inline-flex items-start gap-1.5 text-sm leading-5 text-slate-200 transition hover:text-sky-200">{item.title}<ExternalLink aria-hidden="true" className="mt-0.5 shrink-0" size={12} /></a></div><div className="flex flex-row items-center gap-2 sm:flex-col sm:items-end sm:justify-center"><span className={`rounded-full px-2 py-1 text-[0.58rem] font-semibold uppercase tracking-[0.08em] ${item.reviewStatus === 'PENDING_HUMAN_REVIEW' ? 'bg-amber-300/10 text-amber-200' : 'bg-rose-300/8 text-rose-200'}`}>{item.reviewStatus.replaceAll('_', ' ')}</span><span className="text-[0.6rem] uppercase tracking-[0.08em] text-slate-600">Verdict impact: {item.verdictImpact}</span></div></article>)}</div></section>}
          <section id="review-inbox" className="mt-5 scroll-mt-24 rounded-2xl border border-emerald-300/12 bg-emerald-300/[0.025] p-4 sm:p-5">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div className="flex gap-3"><span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-emerald-300/10 text-emerald-200"><Inbox aria-hidden="true" size={18} /></span><div><p className="text-xs font-semibold uppercase tracking-[0.15em] text-emerald-200">Governed fact review</p><h4 className="mt-1 text-base font-medium text-white">Read the source passage before it enters EIOS</h4><p className="mt-1 max-w-xl text-xs leading-5 text-slate-500">META checks authority, relevance, materiality, causality and contradictions. Nothing here changes a verdict without a recorded human decision.</p></div></div><div className="flex gap-2 text-[0.65rem]"><span className="rounded-full bg-emerald-300/8 px-2.5 py-1 text-emerald-200">{selected.reviewInbox.ready} ready</span><span className="rounded-full bg-amber-300/8 px-2.5 py-1 text-amber-200">{selected.reviewInbox.held} held</span></div></div>
            {selected.reviewInbox.items.length === 0 ? <div className="mt-4 rounded-xl border border-dashed border-white/10 bg-black/10 px-5 py-7 text-center"><p className="text-sm text-slate-300">No extracted official facts are waiting for review.</p><p className="mx-auto mt-1 max-w-xl text-xs leading-5 text-slate-600">This is an honest empty state. When EIOS archives a new or changed official document, its page-linked passages and META assessment will appear here automatically.</p></div> : <div className="mt-4 space-y-3">{selected.reviewInbox.items.map((item) => { const recorded = reviewFeedback[item.candidateId]; const actionable = !['APPROVE', 'REJECT', 'HOLD', 'GOVERNED_FACT'].includes(item.reviewStatus) && !['APPROVE', 'REJECT', 'HOLD'].includes(recorded); return <article key={item.candidateId} className="rounded-xl border border-white/8 bg-black/10 p-4"><div className="flex flex-wrap items-center gap-2"><span className="rounded-full bg-sky-300/8 px-2 py-1 text-[0.6rem] font-semibold uppercase tracking-[0.08em] text-sky-200">{item.eventType.replaceAll('_', ' ')}</span><span className="rounded-full bg-white/5 px-2 py-1 text-[0.6rem] text-slate-400">{item.statementPosture.replaceAll('_', ' ')}</span><span className="ml-auto rounded-full bg-amber-300/8 px-2 py-1 text-[0.6rem] font-semibold uppercase text-amber-200">{(['APPROVE', 'REJECT', 'HOLD'].includes(recorded) ? recorded : item.reviewStatus).replaceAll('_', ' ')}</span></div><blockquote className="mt-3 border-l-2 border-emerald-300/30 pl-3 text-sm leading-6 text-slate-200">{item.sourcePassage}</blockquote><div className="mt-3 flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-500">{item.pdfPage !== null && <span>PDF page {item.pdfPage}</span>}{item.explicitAmounts.length > 0 && <span>Amounts: {item.explicitAmounts.join(', ')}</span>}{item.explicitDates.length > 0 && <span>Dates: {item.explicitDates.join(', ')}</span>}<a href={item.sourceUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-sky-200">Open official source <ExternalLink aria-hidden="true" size={11} /></a></div>{item.meta && <details className="mt-3 rounded-lg border border-violet-300/10 bg-violet-300/[0.025] p-3"><summary className="cursor-pointer text-xs font-medium text-violet-200">See META assessment</summary><div className="mt-3 grid gap-2 text-[0.68rem] sm:grid-cols-2"><MetaCheck label="Authority" value={item.meta.authorityStatus} /><MetaCheck label="Relevance" value={item.meta.relevanceStatus} /><MetaCheck label="Materiality" value={item.meta.materialityStatus} /><MetaCheck label="Causality" value={item.meta.causalityStatus} /><MetaCheck label="Contradictions" value={item.meta.contradictionStatus} /><MetaCheck label="Verdict impact" value={item.meta.verdictImpact} /></div><p className="mt-3 text-xs leading-5 text-slate-500">{item.meta.uncertaintyStatement}</p>{item.meta.reasonCodes.length > 0 && <p className="mt-2 text-[0.65rem] text-slate-600">Reasons: {item.meta.reasonCodes.map((reason) => reason.replaceAll('_', ' ').toLocaleLowerCase()).join(' · ')}</p>}</details>}{actionable && <div className="mt-3 flex flex-wrap gap-2"><ReviewButton label="Approve" tone="approve" disabled={item.meta?.decision !== 'READY_FOR_HUMAN_REVIEW'} onClick={() => setReviewing({ item, decision: 'APPROVE' })} /><ReviewButton label="Hold" tone="hold" onClick={() => setReviewing({ item, decision: 'HOLD' })} /><ReviewButton label="Reject" tone="reject" onClick={() => setReviewing({ item, decision: 'REJECT' })} /></div>}{recorded && !['APPROVE', 'REJECT', 'HOLD'].includes(recorded) && <p className="mt-3 text-xs text-rose-200">{recorded}</p>}{reviewing?.item.candidateId === item.candidateId && <div className="mt-3 rounded-xl border border-white/10 bg-[#071316] p-4"><p className="text-sm font-medium text-white">Record {reviewing.decision.toLocaleLowerCase()} decision</p><label className="mt-3 block text-xs text-slate-400">Rationale<textarea value={reviewRationale} onChange={(event) => setReviewRationale(event.target.value)} rows={3} placeholder="Explain why this fact should be approved, held or rejected…" className="mt-1.5 w-full rounded-xl border border-white/10 bg-black/20 p-3 text-sm text-white outline-none focus:border-emerald-300/30" /></label>{reviewing.decision === 'APPROVE' && <label className="mt-3 block text-xs text-slate-400">Approved confidence: {reviewConfidence}%<input type="range" min="0" max="100" value={reviewConfidence} onChange={(event) => setReviewConfidence(event.target.value)} className="mt-2 w-full accent-emerald-300" /></label>}<div className="mt-3 flex gap-2"><button type="button" disabled={submittingReview || reviewRationale.trim().length < 10} onClick={submitReview} className="rounded-lg bg-emerald-300 px-3 py-2 text-xs font-semibold text-[#061113] disabled:cursor-not-allowed disabled:opacity-40">{submittingReview ? 'Recording…' : 'Confirm decision'}</button><button type="button" onClick={() => setReviewing(null)} className="rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-300">Cancel</button></div><p className="mt-2 text-[0.65rem] text-slate-600">This creates an irreversible audit entry. It does not create a catalyst, verdict or trade.</p></div>}</article>; })}</div>}
          </section>
          {selected.officialSourceCount > 0 && <div className="mt-4 rounded-xl border border-sky-300/10 bg-sky-300/[0.04] p-4"><p className="text-xs font-semibold uppercase tracking-[0.13em] text-sky-200">Official intake queue</p><p className="mt-2 text-sm leading-6 text-slate-400">{selected.officialSourceTypes.map((type) => type.replaceAll('_', ' ').toLocaleLowerCase()).join(' · ')}</p><p className="mt-1 text-xs text-slate-600">{selected.extractedFactCount > 0 ? `${selected.extractedFactCount} facts extracted into the review layer; approval is still pending.` : 'Sources discovered; documents and facts are not yet extracted or approved.'}</p></div>}
          {selected.researchLink && <div className="mt-4 rounded-xl border border-amber-300/14 bg-amber-300/[0.045] p-4"><p className="text-xs font-semibold uppercase tracking-[0.13em] text-amber-200">Rainfall-to-company bridge</p><p className="mt-2 text-sm leading-6 text-slate-300">{selected.researchLink.permitted_claim}</p><p className="mt-2 text-xs leading-5 text-slate-500">Hold: {selected.researchLink.reason}</p></div>}
          {selected.annualReportStudy && <section id="ten-year-story" className="mt-6 scroll-mt-24 overflow-hidden rounded-2xl border border-violet-300/15 bg-violet-300/[0.035]">
            <div className="border-b border-white/7 p-4 sm:p-5"><div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div className="flex gap-3"><span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-violet-300/10 text-violet-200"><Sparkles aria-hidden="true" size={19} /></span><div><p className="text-xs font-semibold uppercase tracking-[0.14em] text-violet-200">EIOS annual-report study</p><h4 className="mt-1 text-base font-medium text-white">What the reports currently tell us</h4><p className="mt-1 text-xs leading-5 text-slate-500">Every conclusion below is calculated from extracted facts and remains auditable.</p></div></div><span className="self-start rounded-full border border-amber-300/15 bg-amber-300/[0.07] px-3 py-1.5 text-xs font-medium text-amber-200">Verdict: research hold</span></div>
              <div className="mt-4 grid gap-3 sm:grid-cols-[1fr_auto]"><div><div className="flex items-center justify-between text-xs"><span className="text-slate-400">Ten-year extraction</span><span className="font-medium text-white">{selected.annualReportStudy.extractedYears} of {selected.annualReportStudy.availableYears} reports</span></div><div className="mt-2 h-2 overflow-hidden rounded-full bg-white/5"><div className="h-full rounded-full bg-gradient-to-r from-violet-400 to-sky-300" style={{ width: `${selected.annualReportStudy.extractionCoveragePercent}%` }} /></div></div><div className="grid grid-cols-2 gap-2 sm:min-w-48"><Metric label="Extracted" value={`${selected.annualReportStudy.extractedYears}`} /><Metric label="Reviewed" value={`${selected.annualReportStudy.reviewedYears}`} warning={selected.annualReportStudy.reviewedYears === 0} /></div></div>
            </div>
            <div className="p-4 sm:p-5"><p className="text-xs font-semibold uppercase tracking-[0.13em] text-slate-500">Preliminary analytical findings</p><div className="mt-3 grid gap-3 lg:grid-cols-2">{selected.annualReportStudy.findings.map((finding) => <article key={finding.findingId} className="rounded-xl border border-white/7 bg-black/10 p-4"><div className="flex items-center justify-between gap-3"><span className="rounded-full bg-violet-300/8 px-2 py-1 text-[0.6rem] font-semibold uppercase tracking-[0.09em] text-violet-200">{finding.category.replaceAll('_', ' ')}</span><span className="text-xs text-slate-600">{finding.confidencePercent}% source confidence</span></div><h5 className="mt-3 text-sm font-medium leading-5 text-white">{finding.headline}</h5><p className="mt-2 text-xs leading-5 text-slate-400">{finding.interpretation}</p></article>)}</div>
              <div className="mt-4 rounded-xl border border-sky-300/12 bg-sky-300/[0.035] p-4"><p className="text-xs font-semibold uppercase tracking-[0.13em] text-sky-200">Meta — permitted conclusion</p><p className="mt-2 text-sm leading-6 text-slate-300">{selected.annualReportStudy.metaPermittedConclusion}</p><p className="mt-2 text-[0.65rem] uppercase tracking-[0.1em] text-slate-600">{selected.annualReportStudy.metaStatus.replaceAll('_', ' ')}</p></div>
              <details className="mt-3 rounded-xl border border-white/7 bg-black/10 p-4"><summary className="cursor-pointer text-xs font-medium text-slate-300">Why EIOS has not issued a verdict</summary><ul className="mt-3 space-y-2">{selected.annualReportStudy.missingWork.map((item) => <li key={item} className="flex gap-2 text-xs leading-5 text-slate-500"><span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-amber-300" />{item}</li>)}</ul></details>
            </div>
          </section>}
          {selected.annualReports.length > 0 && <section id="report-library" className="mt-6 scroll-mt-24 rounded-2xl border border-sky-300/12 bg-sky-300/[0.025] p-4 sm:p-5">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div className="flex gap-3"><span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-sky-300/10 text-sky-200"><BookOpen aria-hidden="true" size={19} /></span><div><p className="text-xs font-semibold uppercase tracking-[0.14em] text-sky-200">10-year annual report library</p><h4 className="mt-1 text-base font-medium text-white">Read the source. See what EIOS has understood.</h4><p className="mt-1 max-w-xl text-xs leading-5 text-slate-500">Reports are ordered newest first. A green card means facts were extracted with page references; it does not mean they are approved evidence.</p></div></div>
              {selected.annualReportArchiveUrl && <a href={selected.annualReportArchiveUrl} target="_blank" rel="noreferrer" className="inline-flex shrink-0 items-center gap-1.5 self-start rounded-xl border border-white/10 bg-white/[0.035] px-3 py-2 text-xs font-medium text-slate-300 transition hover:border-sky-300/30 hover:text-white">Official archive <ExternalLink aria-hidden="true" size={13} /></a>}
            </div>
            <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-5">
              {selected.annualReports.map((report) => {
                const extracted = report.status === 'EXTRACTED_PENDING_HUMAN_REVIEW';
                return <div key={report.financialYear} className={`flex min-h-40 flex-col rounded-xl border p-3.5 ${extracted ? 'border-emerald-300/25 bg-emerald-300/[0.065]' : 'border-white/7 bg-black/10'}`}>
                  <div className="flex items-start justify-between gap-2"><div><p className={`text-lg font-semibold ${extracted ? 'text-emerald-100' : 'text-white'}`}>FY {report.financialYear}</p><p className="mt-1 text-[0.68rem] leading-4 text-slate-500">{report.access === 'DIRECT_OFFICIAL_PDF' ? 'Direct official PDF' : 'Available in official archive'}</p></div>{extracted ? <CheckCircle2 aria-label="Extracted" className="shrink-0 text-emerald-300" size={17} /> : <BookOpen aria-label="Available" className="shrink-0 text-slate-600" size={16} />}</div>
                  <div className="mt-3"><span className={`rounded-full px-2 py-1 text-[0.6rem] font-semibold uppercase tracking-[0.08em] ${extracted ? 'bg-emerald-300/12 text-emerald-200' : 'bg-white/5 text-slate-500'}`}>{extracted ? `${report.extractedFactCount} facts · review pending` : 'Not yet extracted'}</span></div>
                  <a href={report.officialUrl} target="_blank" rel="noreferrer" className="mt-auto inline-flex items-center gap-1.5 pt-4 text-xs font-medium text-sky-200 transition hover:text-sky-100">{report.access === 'DIRECT_OFFICIAL_PDF' ? 'Read report' : 'Find in archive'} <ExternalLink aria-hidden="true" size={12} /></a>
                </div>;
              })}
            </div>
            {selected.annualReports.some((report) => report.highlights.length > 0) && <div className="mt-4 rounded-xl border border-emerald-300/12 bg-emerald-300/[0.035] p-4"><div className="flex flex-wrap items-center justify-between gap-2"><p className="text-xs font-semibold uppercase tracking-[0.13em] text-emerald-200">Latest extracted report at a glance</p><span className="text-xs text-slate-500">FY {selected.annualReports.find((report) => report.highlights.length > 0)?.financialYear}</span></div><div className="mt-3 grid gap-2 sm:grid-cols-2">{selected.annualReports.find((report) => report.highlights.length > 0)?.highlights.map((highlight) => <div key={highlight} className="flex gap-2 rounded-lg bg-black/10 px-3 py-2.5"><span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-300" /><p className="text-xs leading-5 text-slate-300">{highlight}</p></div>)}</div></div>}
            {selected.annualReportGovernanceNote && <p className="mt-3 text-[0.68rem] leading-5 text-slate-600">{selected.annualReportGovernanceNote}</p>}
          </section>}
          {selected.extractedFacts.length > 0 && <div id="evidence-audit" className="mt-6 scroll-mt-24"><div className="mb-3 flex items-center justify-between gap-3"><div className="flex items-center gap-2"><BookOpenCheck aria-hidden="true" className="text-sky-300" size={17} /><h4 className="text-sm font-medium text-white">Extracted company facts</h4></div><span className="rounded-full bg-sky-400/10 px-2.5 py-1 text-[0.65rem] font-medium uppercase tracking-[0.1em] text-sky-200">Review pending</span></div><div className="max-h-[32rem] space-y-2 overflow-y-auto pr-1">{selected.extractedFacts.map((fact) => <div key={fact.factId} className="rounded-xl border border-white/7 bg-white/[0.025] p-4"><div className="mb-2 flex flex-wrap items-center gap-2"><span className="rounded-full bg-white/5 px-2 py-1 text-[0.62rem] font-semibold uppercase tracking-[0.1em] text-slate-400">{fact.kind.replaceAll('_', ' ')}</span>{fact.period && <span className="text-xs text-slate-500">{fact.period}</span>}</div><p className="text-sm leading-6 text-slate-200">{fact.statement}</p>{fact.sourcePage && <p className="mt-2 text-xs text-slate-600">Official annual report · printed pages {fact.sourcePage}</p>}</div>)}</div></div>}
          <div className="mt-6"><div className="mb-3 flex items-center gap-2"><FileSearch aria-hidden="true" className="text-emerald-300" size={17} /><h4 className="text-sm font-medium text-white">Most recent governed evidence</h4></div>{selected.recentEvidence.length > 0 ? <div className="space-y-2">{selected.recentEvidence.map((item, index) => <div key={`${item.title}-${index}`} className="flex items-start justify-between gap-4 rounded-xl border border-white/6 bg-white/[0.02] px-4 py-3"><div><p className="text-sm leading-5 text-slate-200">{item.title}</p><p className="mt-1 text-xs text-slate-500">{item.category}</p></div><span className="shrink-0 text-xs text-slate-500">{item.confidence == null ? 'Unscored' : `${item.confidence}%`}</span></div>)}</div> : <div className="rounded-xl border border-dashed border-white/10 px-4 py-7 text-center"><p className="text-sm text-slate-400">No governed production evidence is attached yet.</p><p className="mt-1 text-xs text-slate-600">The company is searchable, but EIOS will not infer a case from its name or sector.</p></div>}</div>
          <div className="mt-5 flex gap-3 rounded-xl border border-violet-300/10 bg-violet-300/[0.04] p-4"><Sparkles aria-hidden="true" className="mt-0.5 shrink-0 text-violet-300" size={17} /><p className="text-xs leading-5 text-slate-400">Meta will analyse these clues later, but the company bridge and dated catalyst must be independently verified before EIOS can advance this company.</p></div>
        </article>
      </div> : <div className="mt-6 rounded-2xl border border-dashed border-white/10 py-12 text-center"><Search aria-hidden="true" className="mx-auto text-slate-600" size={24} /><p className="mt-3 text-sm text-slate-400">No governed company matches “{query}”.</p><p className="mt-1 text-xs text-slate-600">This does not mean the company does not exist—only that it is not yet in this trusted local index.</p></div>}
    </section>
  );
}

function Metric({ label, value, warning = false }: { label: string; value: string; warning?: boolean }) {
  return <div className="rounded-xl border border-white/6 bg-white/[0.025] p-3"><p className="text-[0.65rem] font-semibold uppercase tracking-[0.13em] text-slate-500">{label}</p><p className={`mt-1.5 text-sm font-medium ${warning ? 'text-amber-200' : 'text-slate-200'}`}>{value}</p></div>;
}

function LensButton({ icon: Icon, title, subtitle, active, status, coverage, onClick }: { icon: typeof TrendingUp; title: string; subtitle: string; active: boolean; status: string; coverage: number; onClick: () => void }) {
  return <button type="button" aria-pressed={active} onClick={onClick} className={`rounded-xl border p-4 text-left transition ${active ? 'border-emerald-300/25 bg-emerald-300/[0.065]' : 'border-white/7 bg-white/[0.02] hover:border-white/15'}`}><div className="flex items-start justify-between gap-3"><div className="flex gap-3"><span className={`grid h-9 w-9 shrink-0 place-items-center rounded-xl ${active ? 'bg-emerald-300/12 text-emerald-200' : 'bg-white/5 text-slate-500'}`}><Icon aria-hidden="true" size={17} /></span><div><p className="text-sm font-medium text-white">{title}</p><p className="mt-1 text-xs text-slate-500">{subtitle}</p></div></div><span className="text-xs font-medium text-slate-400">{coverage}%</span></div><div className="mt-3 flex items-center justify-between"><span className="text-[0.62rem] font-semibold uppercase tracking-[0.1em] text-amber-200">{status.replaceAll('_', ' ')}</span><span className="text-[0.62rem] text-slate-600">Open lens</span></div></button>;
}

function SectionLink({ href, label }: { href: string; label: string }) {
  return <a href={href} className="shrink-0 rounded-lg border border-white/7 bg-white/[0.025] px-3 py-2 text-xs font-medium text-slate-400 transition hover:border-emerald-300/20 hover:text-white">{label}</a>;
}

function MetaCheck({ label, value }: { label: string; value: string }) {
  return <div className="rounded-lg bg-black/10 px-3 py-2"><p className="font-semibold uppercase tracking-[0.09em] text-slate-600">{label}</p><p className="mt-1 leading-4 text-slate-300">{value.replaceAll('_', ' ').toLocaleLowerCase()}</p></div>;
}

function ReviewButton({ label, tone, disabled = false, onClick }: { label: string; tone: 'approve' | 'hold' | 'reject'; disabled?: boolean; onClick: () => void }) {
  const colors = tone === 'approve' ? 'border-emerald-300/20 text-emerald-200 hover:bg-emerald-300/8' : tone === 'hold' ? 'border-amber-300/20 text-amber-200 hover:bg-amber-300/8' : 'border-rose-300/20 text-rose-200 hover:bg-rose-300/8';
  return <button type="button" disabled={disabled} onClick={onClick} title={disabled ? 'Approval is locked because META has not marked this fact ready.' : undefined} className={`rounded-lg border px-3 py-2 text-xs font-medium transition disabled:cursor-not-allowed disabled:opacity-30 ${colors}`}>{label}</button>;
}
