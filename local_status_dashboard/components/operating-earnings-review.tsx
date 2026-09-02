import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

type Fact = { value: number; source_passage: string; raw_value: string; pdf_page: number; source_url: string; url_kind: string; document_hash: string; report_year: string };
export type OperatingEarningsReview = { periods: { period: string; facts: Record<string, Fact>; calculated_operating_ebitda: number; limitation: string; arithmetic_status: string }[] };
const rows = [
  ['profit_before_exceptional_and_tax', 'Profit before exceptional items and tax'],
  ['finance_costs', '+ Finance costs'], ['depreciation_amortisation', '+ Depreciation and amortisation'],
  ['other_income', '− Other income'],
];
const number = (value: number) => value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export function OperatingEarningsTable({ review, reported }: { review?: OperatingEarningsReview | null; reported: { period: string; values: Record<string, number | null> }[] }) {
  if (!review?.periods.length) return null;
  const latest = review.periods[review.periods.length - 1];
  return <article id="operating-earnings-history" className="scroll-mt-32 rounded-xl border border-amber-300/20 bg-[#0a171a] p-5">
    <h3 className="text-lg font-semibold text-white">Eight-year operating EBITDA calculation</h3>
    <p className="mt-2 text-sm leading-6 text-slate-300">Standalone · ₹ crore · {review.periods[0].period} to {latest.period}. Read down each column to follow the calculation.</p>
    <p className="my-3 rounded-lg bg-amber-300/5 p-3 text-sm leading-6 text-amber-100">Calculated from report figures, not quoted company EBITDA. Source-input arithmetic checked; META review remains pending. The existing company-reported figures are preserved separately.</p>
    <Table className="min-w-[74rem] tabular-nums"><TableHeader><TableRow><TableHead className="sticky left-0 bg-[#0a171a] text-slate-300">Calculation / comparison</TableHead>{review.periods.map(p => <TableHead key={p.period} className="text-right text-slate-300">{p.period}</TableHead>)}</TableRow></TableHeader>
      <TableBody>{rows.map(([key, label]) => <TableRow key={key} className="border-white/10"><TableHead scope="row" className="sticky left-0 bg-[#0a171a] text-slate-200">{label}</TableHead>{review.periods.map(p => <TableCell key={p.period} className="text-right text-slate-100">{number(p.facts[key].value)}</TableCell>)}</TableRow>)}
        <TableRow className="border-white/10"><TableHead scope="row" className="sticky left-0 bg-[#0a171a] text-amber-200">= Calculated operating EBITDA</TableHead>{review.periods.map(p => <TableCell key={p.period} className="text-right font-semibold text-amber-100">{number(p.calculated_operating_ebitda)}</TableCell>)}</TableRow>
        <TableRow><TableHead scope="row" className="sticky left-0 bg-[#0a171a] text-slate-300">Company-reported EBITDA (existing history)</TableHead>{review.periods.map(p => { const value = reported.find(r => r.period === p.period)?.values.ebitda; return <TableCell key={p.period} className="text-right text-slate-300">{value == null ? 'Not extracted' : number(value)}</TableCell>; })}</TableRow>
      </TableBody>
    </Table>
    <div className="mt-5 space-y-3 text-sm leading-6 text-slate-300">
      <p><strong className="text-white">What this tells you:</strong> This calculation separates operating earnings from exceptional items and other income, before finance costs, depreciation and amortisation. In {latest.period}, the calculation is {number(latest.facts.profit_before_exceptional_and_tax.value)} + {number(latest.facts.finance_costs.value)} + {number(latest.facts.depreciation_amortisation.value)} − {number(latest.facts.other_income.value)} = ₹{number(latest.calculated_operating_ebitda)} crore.</p>
      <p>It is not cash flow or money available for shareholders: taxes, working capital, capital spending and debt payments still matter. A higher number alone is not a buy signal.</p>
      <p className="text-amber-100">{latest.limitation} Merger restatements and lease-accounting changes can affect comparisons across years. A match after rounding does not prove that the company uses the same EBITDA definition.</p>
    </div>
    <details className="mt-5 border-t border-white/10 pt-3"><summary className="cursor-pointer text-sm font-medium text-sky-200">Inspect the calculation inputs and report sources</summary>
      {review.periods.map(p => <section key={p.period} className="mt-4 text-sm leading-6 text-slate-300"><h4 className="font-semibold text-white">{p.period}</h4>{rows.map(([key, label]) => { const f = p.facts[key]; return <div key={key} className="mt-3"><p><strong>{label}</strong> · Original {f.raw_value} lakh · Report {f.report_year} · PDF page {f.pdf_page}</p><p>{f.source_passage}</p><a className="text-sky-200 underline" href={f.url_kind === 'DIRECT_OFFICIAL_PDF' ? `${f.source_url}#page=${f.pdf_page}` : f.source_url} target="_blank" rel="noreferrer">{f.url_kind === 'DIRECT_OFFICIAL_PDF' ? 'Open official report' : 'Open official archive; select report year'}</a></div>; })}<p className="mt-3 break-all text-xs text-slate-400">Source SHA-256: {p.facts.revenue.document_hash}</p></section>)}
    </details>
  </article>;
}
