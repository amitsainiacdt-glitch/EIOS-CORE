const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { buildFinancialChartData } = require('./financial-chart-data.ts');

test('missing observations remain null, true zero and negative values survive', () => {
  const data = buildFinancialChartData({ cashFlowReview: { periods: [{ period: 'FY2022-23', facts: { operating_cash_flow: { value: 0 }, cash_capex: { value: 45.01 } }, derived: { free_cash_flow: -45.01 } }] } }, ['FY2023-24', 'FY2022-23', 'FY2022-23']);
  assert.equal(data.length, 2);
  assert.equal(data[0].operatingCash, 0);
  assert.equal(data[0].freeCash, -45.01);
  assert.equal(data[1].operatingCash, null);
  assert.equal(data[0].revenue, null);
});
test('nonfinite numbers are not graphed and no company data is manufactured', () => {
  assert.equal(buildFinancialChartData({}, ['FY2024-25'])[0].revenue, null);
  const data = buildFinancialChartData({ operatingEarningsReview: { periods: [{ period: 'FY2024-25', facts: { revenue: { value: Infinity } }, calculated_operating_ebitda: NaN }] } }, ['FY2024-25']);
  assert.equal(data[0].revenue, null);
  assert.equal(data[0].operatingEbitda, null);
});
test('eight-year source packs map exactly without modifying review data', () => {
  const read = name => JSON.parse(fs.readFileSync(path.join(__dirname, '../../data/company_intelligence/coromandel', name), 'utf8'));
  const history = { operatingEarningsReview: read('coromandel_operating_earnings_review.json'), cashFlowReview: read('coromandel_cash_flow_review.json'), balanceSheetReviewData: read('coromandel_balance_sheet_review.json') };
  const before = JSON.stringify(history);
  const data = buildFinancialChartData(history, history.cashFlowReview.periods.map(p => p.period));
  assert.equal(data.length, 8);
  for (const row of data) {
    const earnings = history.operatingEarningsReview.periods.find(p => p.period === row.period);
    const cash = history.cashFlowReview.periods.find(p => p.period === row.period);
    const balance = history.balanceSheetReviewData.periods.find(p => p.period === row.period);
    assert.equal(row.revenue, earnings.facts.revenue.value);
    assert.equal(row.operatingEbitda, earnings.calculated_operating_ebitda);
    assert.equal(row.operatingCash, cash.facts.operating_cash_flow.value);
    assert.equal(row.cashCapex, cash.facts.cash_capex.value);
    assert.equal(row.freeCash, cash.derived.free_cash_flow);
    assert.equal(row.inventory, balance.facts.inventory.value);
    assert.equal(row.receivables, balance.facts.trade_receivables.value);
  }
  assert.equal(data.find(p => p.period === 'FY2022-23').freeCash, -45.01);
  assert.equal(JSON.stringify(history), before);
});
