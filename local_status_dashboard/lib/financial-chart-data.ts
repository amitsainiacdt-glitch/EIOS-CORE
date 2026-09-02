type ReviewPeriod = {
  period: string;
  facts: Record<string, { value: number } | null>;
  calculated_operating_ebitda?: number;
  derived?: { free_cash_flow: number };
};
type Review = { periods: ReviewPeriod[] } | null;
export type ChartReviews = { operatingEarningsReview?: Review; cashFlowReview?: Review; balanceSheetReviewData?: Review };
const finite = (value: unknown): number | null => typeof value === 'number' && Number.isFinite(value) ? value : null;

// Display-only: never backfill governed facts or treat missing observations as zero.
export function buildFinancialChartData(history: ChartReviews, periods: string[]) {
  const earnings = new Map(history.operatingEarningsReview?.periods.map(p => [p.period, p]));
  const cash = new Map(history.cashFlowReview?.periods.map(p => [p.period, p]));
  const balance = new Map(history.balanceSheetReviewData?.periods.map(p => [p.period, p]));
  return [...new Set(periods)].sort().map(period => ({
    period,
    revenue: finite(earnings.get(period)?.facts.revenue?.value),
    operatingEbitda: finite(earnings.get(period)?.calculated_operating_ebitda),
    operatingCash: finite(cash.get(period)?.facts.operating_cash_flow?.value),
    cashCapex: finite(cash.get(period)?.facts.cash_capex?.value),
    freeCash: finite(cash.get(period)?.derived?.free_cash_flow),
    inventory: finite(balance.get(period)?.facts.inventory?.value),
    receivables: finite(balance.get(period)?.facts.trade_receivables?.value),
  }));
}
