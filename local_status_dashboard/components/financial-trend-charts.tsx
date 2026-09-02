import { StaticFinancialChart } from '@/components/static-financial-chart';
import { buildFinancialChartData, type ChartReviews } from '@/lib/financial-chart-data';

const panels = [
  { title: 'Sales — how much business is being done?', note: 'Revenue from the standalone reports. Higher sales do not necessarily mean higher profit.', href: '#operating-earnings-history', series: [{ key: 'revenue', label: 'Revenue', color: '#7dd3fc', kind: 'bar' }] },
  { title: 'Operating earnings — is the business earning more?', note: 'Calculated operating EBITDA, not company-reported EBITDA or net profit. See the calculation below.', href: '#operating-earnings-history', series: [{ key: 'operatingEbitda', label: 'Calculated operating EBITDA', color: '#c4b5fd', kind: 'line' }] },
  { title: 'Cash — what remains after fixed-asset spending?', note: 'Calculated free cash flow = operating cash flow minus cash fixed-asset purchases. Excludes separate acquisition and leasehold-land spending; a negative value means these purchases exceeded operating cash.', href: '#cash-flow-history', series: [{ key: 'operatingCash', label: 'Cash from operations', color: '#6ee7b7', kind: 'bar' }, { key: 'cashCapex', label: 'Cash fixed-asset purchases', color: '#fcd34d', kind: 'bar' }, { key: 'freeCash', label: 'Calculated free cash flow', color: '#7dd3fc', kind: 'line' }] },
  { title: 'Working capital — where is money tied up?', note: 'Inventory is unsold stock; trade receivables are money due from customers. Increases need to be judged against sales and collection periods, not treated as automatic red flags.', href: '#balance-sheet-history', series: [{ key: 'inventory', label: 'Inventory', color: '#c4b5fd', kind: 'line' }, { key: 'receivables', label: 'Trade receivables', color: '#fcd34d', kind: 'line' }] },
] as const;
const format = (value: number) => value.toLocaleString('en-IN', { maximumFractionDigits: 2 });

export function FinancialTrendCharts({ history, periods }: { history: ChartReviews; periods: string[] }) {
  const data = buildFinancialChartData(history, periods);
  return <section id="financial-trends" className="scroll-mt-32 space-y-4" aria-labelledby="financial-trends-title">
    <div><h3 id="financial-trends-title" className="text-xl font-semibold text-white">Financial trends at a glance</h3>
      <p className="mt-2 text-sm leading-6 text-slate-300">Selected annual history: {data[0]?.period ?? 'not available'} to {data.at(-1)?.period ?? 'not available'} · Standalone · ₹ crore. Hover over a point for the exact figure, or open the accessible numbers below each graph.</p>
      <p className="mt-2 text-sm text-amber-200">Awaiting META review — these charts do not change the investment verdict. Reporting changes and merger restatements can affect year-to-year comparisons. Gaps mean missing data, not zero.</p></div>
    <div className="grid min-w-0 gap-4 xl:grid-cols-2">{panels.map(panel => {
      const available = data.some(row => panel.series.some(series => row[series.key] !== null));
      return <article key={panel.title} className="min-w-0 rounded-xl border border-white/10 bg-[#0a171a] p-4 sm:p-5">
        <h4 className="text-base font-semibold text-white">{panel.title}</h4><p className="mt-2 text-xs text-slate-300">₹ crore · Source figures / calculations awaiting review</p>
        {available ? <StaticFinancialChart data={data} series={panel.series} title={panel.title} /> : <p className="my-6 rounded-lg border border-dashed border-slate-600 p-6 text-sm text-slate-300">No source-linked review figures available for this chart yet.</p>}
        <ul className="mt-3 flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-200">{panel.series.map(series => <li key={series.key} className="flex items-center gap-2"><span aria-hidden="true" className="h-2 w-4 rounded-sm" style={{ background: series.color }} />{series.label}</li>)}</ul>
        <p className="mt-4 text-sm leading-6 text-slate-300">{panel.note}</p>
        <a href={panel.href} className="mt-2 inline-block text-sm text-sky-200 underline underline-offset-4">Read the calculation and report sources</a>
        <details className="mt-3 text-sm text-slate-300"><summary className="cursor-pointer text-sky-200">View exact chart numbers</summary><div className="mt-2 overflow-x-auto"><table className="w-full text-right tabular-nums"><caption className="sr-only">{panel.title} — ₹ crore, pending META review</caption><thead><tr><th scope="col" className="p-2 text-left">Year</th>{panel.series.map(series => <th scope="col" key={series.key} className="p-2">{series.label}</th>)}</tr></thead><tbody>{data.map(row => <tr key={row.period} className="border-t border-white/10"><th scope="row" className="p-2 text-left font-normal">{row.period}</th>{panel.series.map(series => <td key={series.key} className="p-2">{row[series.key] === null ? 'Missing' : format(row[series.key]!)}</td>)}</tr>)}</tbody></table></div></details>
      </article>;
    })}</div>
  </section>;
}
