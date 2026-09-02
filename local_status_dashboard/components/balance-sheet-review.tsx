import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

type Fact = { value: number; source_passage: string; raw_value: string | null; pdf_page: number; source_url: string; url_kind: string; document_hash: string; report_year: string };
export type BalanceSheetReview = { periods: { period: string; facts: Record<string, Fact | null> }[]; extracted_fact_count: number; limitations: string[] };
const rows = [
  ['total_assets', 'Total assets'], ['total_equity', 'Shareholders’ equity'], ['total_liabilities', 'Total liabilities'],
  ['current_assets', 'Current assets'], ['non_current_assets', 'Non-current assets'],
  ['current_liabilities', 'Current liabilities'], ['non_current_liabilities', 'Non-current liabilities'],
  ['property_plant_equipment', 'Property, plant and equipment'], ['capital_work_in_progress', 'Projects under construction'],
  ['inventory', 'Inventory'], ['trade_receivables', 'Money due from customers'], ['subsidies_receivable', 'Government subsidies receivable'],
  ['cash_equivalents', 'Cash and cash equivalents'], ['other_bank_balances', 'Other bank balances'],
  ['current_liabilities_borrowings', 'Current borrowings'], ['non_current_liabilities_borrowings', 'Non-current borrowings'],
  ['current_liabilities_lease_liabilities', 'Current lease liabilities'], ['non_current_liabilities_lease_liabilities', 'Non-current lease liabilities'],
  ['trade_payables_total', 'Trade payables (reported or summed)'], ['trade_payables_msme', 'Trade payables — MSMEs'], ['trade_payables_other', 'Trade payables — other creditors'],
  ['current_liabilities_provisions', 'Current provisions'], ['non_current_liabilities_provisions', 'Non-current provisions'],
  ['current_liabilities_other_financial_liabilities', 'Other current financial liabilities'], ['non_current_liabilities_other_financial_liabilities', 'Other non-current financial liabilities'],
  ['current_liabilities_other_liabilities', 'Other current liabilities'], ['non_current_liabilities_other_liabilities', 'Other non-current liabilities'],
];
const format = (v: number) => v.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export function BalanceSheetReviewTable({ review }: { review?: BalanceSheetReview | null }) {
  if (!review?.periods.length) return null;
  const latest = review.periods[review.periods.length - 1];
  const value = (key: string) => latest.facts[key] ? format(latest.facts[key]!.value) : 'not available';
  return <article id="balance-sheet-history" className="scroll-mt-32 rounded-xl border border-amber-300/20 bg-[#0a171a] p-5">
    <h3 className="text-lg font-semibold text-white">Eight-year balance-sheet table</h3>
    <p className="mt-2 text-sm leading-6 text-slate-300">{review.periods[0].period} to {latest.period} · Standalone · ₹ crore · {review.extracted_fact_count} extracted figures.</p>
    <p className="my-3 rounded-lg bg-amber-300/5 p-3 text-sm leading-6 text-amber-100">Pending META review. Four checks on reported totals pass for each year. This is not full statement approval. A dash means not separately reported or extracted—not zero. Select a number to reach its source details below.</p>
    <Table className="min-w-[72rem] tabular-nums"><TableHeader><TableRow><TableHead className="sticky left-0 bg-[#0a171a] text-slate-300">Balance-sheet measure</TableHead>{review.periods.map(p => <TableHead key={p.period} className="text-right text-slate-300">{p.period}</TableHead>)}</TableRow></TableHeader>
      <TableBody>{rows.map(([key, label]) => <TableRow key={key} className="border-white/10"><TableHead scope="row" className="sticky left-0 bg-[#0a171a] text-slate-200">{label}</TableHead>{review.periods.map(p => <TableCell key={p.period} className="text-right text-slate-100">{p.facts[key] ? <a href={`#balance-source-${p.period}`} className="underline decoration-slate-600 underline-offset-4">{format(p.facts[key]!.value)}</a> : '—'}</TableCell>)}</TableRow>)}</TableBody>
    </Table>
    <div className="mt-5 space-y-3 text-sm leading-6 text-slate-300">
      <p><strong className="text-white">How to read this:</strong> In {latest.period}, reported assets of ₹{value('total_assets')} crore equal liabilities of ₹{value('total_liabilities')} crore plus shareholders’ equity of ₹{value('total_equity')} crore. Assets are not the company’s market value; liabilities include more than borrowings.</p>
      <p>Cash and cash equivalents are ₹{value('cash_equivalents')} crore, while other bank balances are ₹{value('other_bank_balances')} crore. Do not treat every bank deposit as spendable cash: maturity and restrictions must be checked in the notes.</p>
      <p>Receivables and inventory are not cash already collected. Subsidy payments, customer collections and inventory movement need separate analysis before drawing a conclusion.</p>
      {review.limitations.map(l => <p key={l} className="text-amber-100">{l}</p>)}
    </div>
    <div className="mt-5 space-y-3">{review.periods.map(p => <section id={`balance-source-${p.period}`} key={p.period} className="scroll-mt-32 border-t border-white/10 pt-3">
      <details><summary className="cursor-pointer text-sm font-medium text-sky-200">{p.period} — inspect the original source figures</summary>
        {rows.map(([key, label]) => { const f = p.facts[key]; return f && <div key={key} className="mt-3 text-sm leading-6 text-slate-300"><p><strong>{label}</strong> · {f.raw_value ? `Original ${f.raw_value} lakh` : 'Calculated from the two source rows'} · Report {f.report_year} · PDF page {f.pdf_page}</p><p>{f.source_passage}</p><a className="text-sky-200 underline" href={f.url_kind === 'DIRECT_OFFICIAL_PDF' ? `${f.source_url}#page=${f.pdf_page}` : f.source_url} target="_blank" rel="noreferrer">{f.url_kind === 'DIRECT_OFFICIAL_PDF' ? 'Open official report' : 'Open official archive; select report year'}</a></div>; })}
        <p className="mt-3 break-all text-xs text-slate-400">Document SHA-256: {p.facts.total_assets?.document_hash}</p>
      </details>
    </section>)}</div>
  </article>;
}
