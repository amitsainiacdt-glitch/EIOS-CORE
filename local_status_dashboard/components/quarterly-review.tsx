'use client';
import { useState } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

type Review = { items: { id: string; period: string; basis: string; summary: string;
  figures: Record<string, string>; checks: { code: string; status: string; explanation: string }[];
  plainEnglish: { posture: string; headline: string; summary: string; figure_explanations: string[];
    accounting_note_explanations: { topic: string; meaning: string; review_rationale: string }[];
    profit_bridge: null | { revenue_change_crore: string; pat_change_crore: string; pat_at_prior_margin_crore: string;
      profit_gap_vs_prior_margin_crore: string; other_income_change_crore: string | null; meaning: string; not_yet_attributed: string[] };
    cost_attribution: null | { total_expenses_current_crore:string; total_expenses_prior_crore:string; total_expense_change_crore:string;
      total_expense_change_percent:string; revenue_change_percent:string; pbt_change_crore:string; pbt_change_percent:string;
      pbt_margin_current_percent:string; pbt_margin_prior_percent:string; unallocated_expense_change_crore:string;
      below_pbt_burden_change_crore:string; meaning:string; boundary:string;
      comparable_lines:{metric:string;label:string;current_crore:string;prior_crore:string;change_crore:string;change_percent:string|null;effect:string}[] };
    conclusion: string; limitations: string[] };
  notChecked: string[]; sourceUrl: string | null; sourcePage: number; documentHash: string; assistantUnitReview: boolean;
  queuePath: string; periodEnd: string; reportingNotes: { items: { id: string; topic: string; page: number; passage: string; question: string;
    assistantDraft?: { explanation: string; status: string } | null;
    humanReview?: { decision: string; rationale: string; reviewer: string; reviewed_at: string } | null;
    context: { cues: string[]; dateMentions: string[]; basisMentions: string[] } }[]; invalidCount: number };
  readings: { row_label: string; native_text: string; ocr_text: string; status: string }[] }[];
  invalidPacketCount: number };
const labels: Record<string, string> = { revenue: 'Revenue', other_income: 'Other income', total_income: 'Total income', pat: 'Net profit after tax' };
const noteLabels: Record<string, string> = { LIMITED_REVIEW: 'Audit and review scope', COMPARABILITY: 'Can the periods be compared?', BALANCING_QUARTER: 'How the quarter was calculated', IMPAIRMENT: 'Impairment and exceptional charges', RESTATEMENT_OR_REGROUPING: 'Restatements and regrouping' };

export function QuarterlyReview({ review }: { review: Review }) {
  const [editing, setEditing] = useState<{ itemId: string; noteId: string; queuePath: string; decision: string } | null>(null);
  const [rationale, setRationale] = useState('');
  const [busy, setBusy] = useState(false);
  const [feedback, setFeedback] = useState<Record<string,string>>({});
  async function submit() {
    if (!editing || rationale.trim().length < 10) return;
    setBusy(true);
    try {
      const response = await fetch('http://127.0.0.1:3001/quarterly-note-review', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ queuePath: editing.queuePath, quarterlyCandidateId: editing.itemId, noteId: editing.noteId, decision: editing.decision, rationale: rationale.trim(), reviewer: 'EIOS_LOCAL_USER' }) });
      const body = await response.json() as { error?: string }; if (!response.ok) throw new Error(body.error || 'Review failed');
      setFeedback(current => ({...current, [editing.noteId]: `${editing.decision.replaceAll('_',' ')} recorded — refresh to recompute the hold`})); setEditing(null); setRationale('');
    } catch (error) { setFeedback(current => ({...current, [editing.noteId]: error instanceof Error ? error.message : 'Review service unavailable'})); }
    finally { setBusy(false); }
  }
  return <section id="quarterly-review" className="scroll-mt-32 rounded-xl border border-amber-300/20 bg-[#0a171a] p-5 mt-6 text-base text-slate-200">
    <h2 className="text-xl font-semibold text-white">Quarterly review</h2>
    <p className="mt-2 text-amber-200">Unapproved research · Not included in financial history, charts or the investment verdict.</p>
    {!review.items.length && <p className="mt-4">No quarterly review candidate is available for this company.</p>}
    {review.invalidPacketCount > 0 && <p className="mt-3 text-amber-200">Some saved review evidence could not be validated and has been withheld.</p>}
    {review.items.map(item => <article key={item.id} className="mt-5 border-t border-white/10 pt-5">
      <h3 className="text-lg font-semibold">{item.period} · {item.basis === 'STANDALONE' ? 'Standalone accounts' : 'Consolidated accounts'}</h3>
      <p className="mt-2 leading-7">{item.summary}</p>
      <section className="mt-4 rounded-xl border border-sky-300/15 bg-sky-300/[0.035] p-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-sky-200">What these figures are saying</p>
        <h4 className="mt-2 text-lg font-semibold text-white">{item.plainEnglish.headline}</h4>
        <p className="mt-2 leading-7 text-slate-200">{item.plainEnglish.summary}</p>
        <ul className="mt-4 space-y-2">{item.plainEnglish.figure_explanations.map(text => <li key={text} className="flex gap-2 leading-7 text-slate-300"><span className="text-sky-300">•</span><span>{text}</span></li>)}</ul>
        {item.plainEnglish.profit_bridge && <div className="mt-4 border-t border-white/10 pt-4"><p className="font-medium text-violet-200">Where the missing profit went — first bridge</p><div className="mt-3 grid gap-2 sm:grid-cols-2 xl:grid-cols-4"><Bridge label="Revenue change" value={item.plainEnglish.profit_bridge.revenue_change_crore} signed /><Bridge label="Profit change" value={item.plainEnglish.profit_bridge.pat_change_crore} signed /><Bridge label="Profit at old margin" value={item.plainEnglish.profit_bridge.pat_at_prior_margin_crore} /><Bridge label="Profit gap vs old margin" value={item.plainEnglish.profit_bridge.profit_gap_vs_prior_margin_crore} signed /></div><p className="mt-3 leading-7 text-slate-300">{item.plainEnglish.profit_bridge.meaning}</p><p className="mt-2 text-sm leading-6 text-amber-100">Not yet attributed: {item.plainEnglish.profit_bridge.not_yet_attributed.join('; ')}. EIOS will not invent the cause.</p></div>}
        {item.plainEnglish.cost_attribution && <div className="mt-4 border-t border-white/10 pt-4"><p className="font-medium text-violet-200">Confirmed cost attribution</p><p className="mt-2 leading-7 text-slate-300">{item.plainEnglish.cost_attribution.meaning}</p><div className="mt-3 overflow-x-auto"><Table><TableHeader><TableRow><TableHead>Comparable cost</TableHead><TableHead className="text-right">Earlier</TableHead><TableHead className="text-right">Current</TableHead><TableHead className="text-right">Change</TableHead><TableHead>Effect</TableHead></TableRow></TableHeader><TableBody>{item.plainEnglish.cost_attribution.comparable_lines.map(line=><TableRow key={line.metric}><TableCell>{line.label}</TableCell><TableCell className="text-right">{Number(line.prior_crore).toLocaleString('en-IN')}</TableCell><TableCell className="text-right">{Number(line.current_crore).toLocaleString('en-IN')}</TableCell><TableCell className="text-right">{Number(line.change_crore)>=0?'+':''}{Number(line.change_crore).toLocaleString('en-IN')}</TableCell><TableCell className={line.effect==='PRESSURE'?'text-rose-200':'text-emerald-200'}>{line.effect.toLowerCase()}</TableCell></TableRow>)}</TableBody></Table></div><p className="mt-3 text-sm text-amber-100">₹{Number(item.plainEnglish.cost_attribution.unallocated_expense_change_crore).toLocaleString('en-IN')} crore of the expense increase remains unallocated because one or both source readings are incomplete.</p><p className="mt-2 text-xs leading-5 text-slate-500">{item.plainEnglish.cost_attribution.boundary}</p></div>}
        {!!item.plainEnglish.accounting_note_explanations.length && <div className="mt-4 border-t border-white/10 pt-4"><p className="font-medium text-amber-200">Accounting notes translated</p>{item.plainEnglish.accounting_note_explanations.map((note,index) => <div key={`${note.topic}-${index}`} className="mt-2"><p className="leading-7 text-slate-300">{note.meaning}</p>{note.review_rationale && <p className="text-sm text-slate-500">Reviewer’s reason: {note.review_rationale}</p>}</div>)}</div>}
        <p className="mt-4 rounded-lg border border-white/10 bg-black/15 p-3 font-medium leading-7 text-white">EIOS conclusion: {item.plainEnglish.conclusion}</p>
      </section>
      <div className="mt-4 grid gap-6 xl:grid-cols-2">
        <div><h4 className="mb-2 font-medium">Figures awaiting review — ₹ crore</h4>
          {Object.keys(item.figures).length ? <Table className="text-base"><TableHeader><TableRow><TableHead>Metric</TableHead><TableHead className="text-right">Candidate value</TableHead></TableRow></TableHeader><TableBody>
            {Object.entries(item.figures).map(([key,value]) => <TableRow key={key}><TableCell>{labels[key] ?? key}</TableCell><TableCell className="text-right tabular-nums">{Number(value).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell></TableRow>)}
          </TableBody></Table> : <p>Figures withheld because extraction checks did not pass.</p>}
          <p className="mt-3 text-sm leading-6 text-slate-400">Matching readings and a correct total do not establish business quality or make this an investment recommendation.</p>
        </div>
        <div><h4 className="font-medium">Why it is not published yet</h4><ul className="mt-3 space-y-3">{item.checks.map(check => <li key={check.code} className="leading-6"><span className={check.status === 'PASS' ? 'text-emerald-300' : 'text-amber-200'}>{check.status === 'PASS' ? 'Passed check' : 'Still required'}: </span>{check.explanation}</li>)}</ul></div>
      </div>
      <div className="mt-6 border-t border-white/10 pt-5">
        <h4 className="text-lg font-semibold">What the reporting notes mean</h4>
        <p className="mt-2 leading-7 text-slate-300">These passages come from the same document, but may concern another quarter or consolidated accounts. Their relevance to the figures above has not yet been confirmed. Finding a passage does not complete its review.</p>
        {!item.reportingNotes.items.length && <p className="mt-3 text-slate-400">No reporting-note passages are available here. This does not mean the report has no qualifications or adjustments.</p>}
        {item.reportingNotes.invalidCount > 0 && <p className="mt-3 text-amber-200">Some note references were withheld because their source details were incomplete.</p>}
        <div className="mt-4 grid gap-3 lg:grid-cols-2">{item.reportingNotes.items.map(note => <details key={note.id} className="min-w-0 rounded-lg border border-white/10 bg-black/10 p-4">
          <summary className="cursor-pointer font-medium text-sky-200">{noteLabels[note.topic] ?? 'Reporting note'} · Page {note.page}<span className={`mt-1 block text-sm ${note.humanReview ? 'text-emerald-200' : 'text-amber-200'}`}>{feedback[note.id] || (note.humanReview ? `Human decision: ${note.humanReview.decision.replaceAll('_',' ')}` : note.assistantDraft ? 'Draft explanation available — awaiting review' : 'Unreviewed passage')}</span></summary>
          {note.assistantDraft && <div className="mt-4 rounded-md border border-amber-300/20 bg-amber-300/5 p-4">
            <p className="font-medium text-amber-200">In plain English — assistant research draft</p>
            <p className="mt-2 leading-7">{note.assistantDraft.explanation}</p>
            <p className="mt-2 text-sm leading-6 text-slate-300">Prepared with assistant review, not an automatic EIOS conclusion. Source verification and human approval remain incomplete; this does not change earnings or the investment verdict.</p>
          </div>}
          <p className="mt-3 leading-7">{note.question}</p>
          <div className="mt-3 rounded-md border border-sky-300/15 bg-sky-300/5 p-3">
            <p className="font-medium text-sky-200">How this may relate to the figures above</p>
            <ul className="mt-2 list-disc space-y-2 pl-5 leading-7">{note.context.cues.map(cue => <li key={cue}>{cue}</li>)}</ul>
            {note.context.dateMentions.length > 0 && <p className="mt-2 text-sm text-slate-400">Dates found in the passage: {note.context.dateMentions.join(', ')}. These are mentions, not verified reporting periods.</p>}
          </div>
          <p className="mt-3 text-sm text-slate-400">Extracted source text — may contain reading errors:</p>
          <blockquote className="mt-2 max-h-80 overflow-auto whitespace-pre-wrap break-words border-l-2 border-slate-500 pl-3 text-base leading-7 text-slate-300">{note.passage}</blockquote>
          {note.humanReview ? <div className="mt-3 rounded-md border border-emerald-300/15 bg-emerald-300/5 p-3"><p className="font-medium text-emerald-200">Reviewed: {note.humanReview.decision.replaceAll('_',' ')}</p><p className="mt-1 text-sm text-slate-300">{note.humanReview.rationale}</p></div> : <div className="mt-3"><p className="mb-2 text-sm text-slate-400">Does this note apply to the {item.basis.toLowerCase()} quarter ending {item.periodEnd}?</p><div className="flex flex-wrap gap-2">{[['APPLIES','Applies'],['DOES_NOT_APPLY','Does not apply'],['UNRESOLVED','Still uncertain']].map(([decision,label]) => <button key={decision} onClick={() => {setEditing({itemId:item.id,noteId:note.id,queuePath:item.queuePath,decision});setRationale('')}} className="rounded-md border border-white/10 px-3 py-2 text-sm text-slate-200">{label}</button>)}</div>{editing?.noteId === note.id && <div className="mt-3"><textarea rows={3} value={rationale} onChange={event => setRationale(event.target.value)} placeholder="Explain what you checked and why…" className="w-full rounded-md border border-white/10 bg-black/20 p-3 text-sm text-white"/><button disabled={busy || rationale.trim().length < 10} onClick={submit} className="mt-2 rounded-md bg-emerald-300 px-3 py-2 text-sm font-semibold text-[#071114] disabled:opacity-40">{busy ? 'Recording…' : 'Confirm decision'}</button></div>}</div>}
          {item.sourceUrl && <a className="mt-3 inline-block text-sm text-sky-300 underline" href={`${item.sourceUrl.split('#')[0]}#page=${note.page}`} target="_blank" rel="noreferrer">Open supplied filing at page {note.page} — origin unverified</a>}
        </details>)}</div>
      </div>
      <details className="mt-5 rounded-lg border border-white/10 p-4"><summary className="cursor-pointer font-medium">Inspect source readings and limits</summary>
        <p className="my-3 text-sm text-slate-400">Locally imported report, page {item.sourcePage}. {item.assistantUnitReview && 'Currency includes a saved assistant visual correction. '}This panel does not grant human approval.</p>
        {item.sourceUrl && <a className="text-sky-300 underline" href={`${item.sourceUrl.split('#')[0]}#page=${item.sourcePage}`} target="_blank" rel="noreferrer">Open supplied filing link — origin not yet verified</a>}
        <Table className="mt-3 text-sm"><TableHeader><TableRow><TableHead>Source row</TableHead><TableHead>PDF text</TableHead><TableHead>Image reading</TableHead></TableRow></TableHeader><TableBody>{item.readings.map((row,i) => <TableRow key={i}><TableCell>{row.row_label}</TableCell><TableCell>{row.native_text}</TableCell><TableCell>{row.ocr_text || 'Missing'}</TableCell></TableRow>)}</TableBody></Table>
        <p className="mt-4 leading-7">Not assessed here: {item.notChecked.join('; ')}.</p>
        <p className="mt-3 break-all text-sm text-slate-400">Document fingerprint: {item.documentHash}</p>
      </details>
    </article>)}
  </section>;
}
function Bridge({label,value,signed=false}:{label:string;value:string;signed?:boolean}) { const number=Number(value); return <div className="rounded-lg border border-white/10 bg-black/15 p-3"><p className="text-xs text-slate-500">{label}</p><p className={`mt-1 font-semibold tabular-nums ${number < 0 ? 'text-rose-200':'text-emerald-200'}`}>{signed && number >= 0 ? '+' : ''}{number.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2})} cr</p></div> }
