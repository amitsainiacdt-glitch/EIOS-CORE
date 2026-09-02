import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

type Fact = { value: number; source_url: string; url_kind: string; pdf_page: number; source_passage: string; raw_value: string; document_hash: string; report_year: string };
type ReportingNote = Omit<Fact, 'value' | 'raw_value'> & { reason: string; explanation: string };
export type CashFlowReview = {
  periods: { period: string; facts: Record<string, Fact>; derived: { free_cash_flow: number; free_cash_flow_definition: string } }[];
  extracted_fact_count: number;
  continuity_warnings: { period: string; difference_crore: number; meaning: string; reason?: string; note?: ReportingNote }[];
  revision_reviews?: { period: string; deltas_crore: Record<string, number>; original: { facts: Record<string, Fact> }; revised: { facts: Record<string, Fact> }; note: ReportingNote }[];
};
const rows = [
  ['operating_cash_flow', 'Cash from operations'],
  ['investing_cash_flow', 'Investing cash flow'],
  ['financing_cash_flow', 'Financing cash flow'],
  ['cash_capex', 'Cash spent on fixed assets'],
  ['opening_cash', 'Opening cash'],
  ['closing_cash', 'Closing cash'],
];
const number = (value: number) => value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export function CashFlowReviewTable({ review }: { review?: CashFlowReview | null }) {
  if (!review?.periods.length) return null;
  const latest = review.periods[review.periods.length - 1];
  return <article id="cash-flow-history" className="scroll-mt-32 rounded-xl border border-amber-300/20 bg-[#0a171a] p-5">
    <h3 className="text-lg font-semibold text-white">Eight-year cash-flow table</h3>
    <p className="mt-2 text-sm leading-6 text-slate-300">{review.periods[0].period} to {latest.period} · Standalone · ₹ crore. {review.extracted_fact_count} figures extracted from saved reports. Negative numbers mean cash went out.</p>
    <p className="my-3 rounded-lg bg-amber-300/5 p-3 text-sm leading-6 text-amber-100">Pending META review. Each year’s cash bridge reconciles, but these figures are not approved verdict inputs. This table is separate from the existing financial-history view.</p>
    <Table className="min-w-[68rem] tabular-nums">
      <TableHeader><TableRow className="border-white/10"><TableHead className="sticky left-0 bg-[#0a171a] text-slate-300">Cash-flow measure</TableHead>{review.periods.map(p => <TableHead key={p.period} className="text-right text-slate-300">{p.period}</TableHead>)}</TableRow></TableHeader>
      <TableBody>{rows.map(([key, label]) => <TableRow key={key} className="border-white/10">
        <TableHead scope="row" className="sticky left-0 bg-[#0a171a] text-slate-200">{label}</TableHead>
        {review.periods.map(p => <TableCell key={p.period} className="text-right text-slate-100">{p.facts[key] ? number(p.facts[key].value) : '—'}</TableCell>)}
      </TableRow>)}
        <TableRow className="border-white/10"><TableHead scope="row" className="sticky left-0 bg-[#0a171a] text-emerald-200">Free cash flow (calculated)</TableHead>{review.periods.map(p => <TableCell key={p.period} className="text-right text-emerald-100">{number(p.derived.free_cash_flow)}</TableCell>)}</TableRow>
      </TableBody>
    </Table>
    <div className="mt-5 space-y-3 text-sm leading-6 text-slate-300">
      <p><strong className="text-white">What this means:</strong> In {latest.period}, operations generated ₹{number(latest.facts.operating_cash_flow.value)} crore. Cash purchases of fixed assets used ₹{number(latest.facts.cash_capex.value)} crore, leaving ₹{number(latest.derived.free_cash_flow)} crore on this free-cash-flow definition. This is a calculation, not a buy recommendation.</p>
      <p>{latest.derived.free_cash_flow_definition} Free cash flow is not the change in the bank balance: investments, borrowings and dividends also move cash.</p>
      {review.continuity_warnings.map(w => <div key={w.period} className="rounded-lg border border-amber-300/15 p-3 text-amber-100">
        <p className="font-semibold">{w.reason ?? 'Reporting difference'} · {w.period} · ₹{number(w.difference_crore)} crore</p>
        <p className="mt-2">{w.meaning}</p><p className="mt-2 text-xs">Both source versions are preserved. META review is still pending.</p>
        {w.note && <details className="mt-3"><summary className="cursor-pointer text-sky-200">Read the reporting note · PDF page {w.note.pdf_page}</summary>
          <p className="mt-2 whitespace-pre-line text-slate-300">{w.note.source_passage}</p>
          <a className="text-sky-200 underline" href={w.note.url_kind === 'DIRECT_OFFICIAL_PDF' ? `${w.note.source_url}#page=${w.note.pdf_page}` : w.note.source_url} target="_blank" rel="noreferrer">{w.note.url_kind === 'DIRECT_OFFICIAL_PDF' ? 'Open official report' : `Open official archive · select ${w.note.report_year}`}</a>
        </details>}
      </div>)}
      {!!review.revision_reviews?.length && <details className="border-t border-white/10 pt-3"><summary className="cursor-pointer font-medium text-sky-200">Compare original and revised cash figures</summary>
        {review.revision_reviews.map(r => <section key={r.period} className="mt-4">
          <h4 className="mb-2 font-semibold text-white">{r.period} · original versus later comparative</h4>
          <Table className="min-w-[36rem] tabular-nums"><TableHeader><TableRow><TableHead>₹ crore</TableHead><TableHead className="text-right">Original</TableHead><TableHead className="text-right">Revised</TableHead><TableHead className="text-right">Difference</TableHead></TableRow></TableHeader>
            <TableBody>{[...rows.filter(([key]) => key !== 'cash_capex'), ['business_combination_cash', 'Acquired cash adjustment']].map(([key, label]) => <TableRow key={key}>
              <TableHead scope="row">{label}</TableHead><TableCell className="text-right">{r.original.facts[key] ? number(r.original.facts[key].value) : 'Not reported'}</TableCell><TableCell className="text-right">{r.revised.facts[key] ? number(r.revised.facts[key].value) : 'Not reported'}</TableCell><TableCell className="text-right">{number(r.deltas_crore[key])}</TableCell>
            </TableRow>)}</TableBody>
          </Table>
          <p className="mt-2 text-xs">Comparison arithmetic treats an absent acquisition-adjustment line as zero; no source value is invented. Opening cash + operating + investing + financing + acquired cash = closing cash in each version.</p>
        </section>)}
      </details>}
    </div>
    <details className="mt-5 border-t border-white/10 pt-4"><summary className="cursor-pointer text-sm font-medium text-sky-200">Check the source passages, pages and original figures</summary>
      <div className="mt-4 space-y-4">{review.periods.map(p => <section key={p.period}>
        <h4 className="font-semibold text-white">{p.period}</h4>
        {rows.map(([key, label]) => { const f = p.facts[key]; if (!f) return null; return <div key={key} className="mt-2 rounded-md bg-white/[0.025] p-3 text-sm leading-6 text-slate-300">
          <p><strong>{label}</strong> · Report {f.report_year} · PDF page {f.pdf_page} · Original value {f.raw_value} lakh</p>
          <p className="mt-1">{f.source_passage}</p>
          <a className="text-sky-200 underline" href={f.url_kind === 'DIRECT_OFFICIAL_PDF' ? `${f.source_url}#page=${f.pdf_page}` : f.source_url} target="_blank" rel="noreferrer">{f.url_kind === 'DIRECT_OFFICIAL_PDF' ? 'Open official report' : 'Open official report archive (select report year)'}</a>
          <p className="mt-1 break-all text-xs text-slate-400">Preserved document SHA-256: {f.document_hash}</p>
        </div>; })}
      </section>)}</div>
    </details>
  </article>;
}
