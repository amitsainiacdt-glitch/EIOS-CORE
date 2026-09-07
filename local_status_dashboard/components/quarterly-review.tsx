import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

type Review = { items: { id: string; period: string; basis: string; summary: string;
  figures: Record<string, string>; checks: { code: string; status: string; explanation: string }[];
  notChecked: string[]; sourceUrl: string | null; sourcePage: number; documentHash: string; assistantUnitReview: boolean;
  reportingNotes: { items: { id: string; topic: string; page: number; passage: string; question: string;
    assistantDraft?: { explanation: string; status: string } | null;
    context: { cues: string[]; dateMentions: string[]; basisMentions: string[] } }[]; invalidCount: number };
  readings: { row_label: string; native_text: string; ocr_text: string; status: string }[] }[];
  invalidPacketCount: number };
const labels: Record<string, string> = { revenue: 'Revenue', other_income: 'Other income', total_income: 'Total income', pat: 'Net profit after tax' };
const noteLabels: Record<string, string> = { LIMITED_REVIEW: 'Audit and review scope', COMPARABILITY: 'Can the periods be compared?', BALANCING_QUARTER: 'How the quarter was calculated', IMPAIRMENT: 'Impairment and exceptional charges', RESTATEMENT_OR_REGROUPING: 'Restatements and regrouping' };

export function QuarterlyReview({ review }: { review: Review }) {
  return <section id="quarterly-review" className="scroll-mt-32 rounded-xl border border-amber-300/20 bg-[#0a171a] p-5 mt-6 text-base text-slate-200">
    <h2 className="text-xl font-semibold text-white">Quarterly review</h2>
    <p className="mt-2 text-amber-200">Unapproved research · Not included in financial history, charts or the investment verdict.</p>
    {!review.items.length && <p className="mt-4">No quarterly review candidate is available for this company.</p>}
    {review.invalidPacketCount > 0 && <p className="mt-3 text-amber-200">Some saved review evidence could not be validated and has been withheld.</p>}
    {review.items.map(item => <article key={item.id} className="mt-5 border-t border-white/10 pt-5">
      <h3 className="text-lg font-semibold">{item.period} · {item.basis === 'STANDALONE' ? 'Standalone accounts' : 'Consolidated accounts'}</h3>
      <p className="mt-2 leading-7">{item.summary}</p>
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
          <summary className="cursor-pointer font-medium text-sky-200">{noteLabels[note.topic] ?? 'Reporting note'} · Page {note.page}<span className="mt-1 block text-sm text-amber-200">{note.assistantDraft ? 'Draft explanation available — awaiting review' : 'Unreviewed passage'}</span></summary>
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
