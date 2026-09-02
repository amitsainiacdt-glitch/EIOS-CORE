export type DisplayCell = { value: number | null; status: string; reason: string; section?: string | null; source?: { pdf_page: number; report_year?: string } | null };
export function FinancialSummaryValue({ period, metric }: { period: { values: Record<string, number | null>; displayCells?: Record<string, DisplayCell> }; metric: string }) {
  const cell = period.displayCells?.[metric];
  const value = cell ? cell.value : period.values[metric];
  if (value == null) return <span className="text-slate-400" title={cell?.reason ?? 'Not yet extracted'}>Missing</span>;
  if (cell?.status === 'PENDING_META_REVIEW') return <a href={`#${cell.section}`} className="text-amber-200 underline decoration-amber-200/40 underline-offset-4" title={`${cell.reason} Report ${cell.source?.report_year}, PDF page ${cell.source?.pdf_page}`}>
    {value.toLocaleString('en-IN')}<span className="block text-[0.6rem]">Pending META</span>
  </a>;
  return <span>{value.toLocaleString('en-IN')}</span>;
}
