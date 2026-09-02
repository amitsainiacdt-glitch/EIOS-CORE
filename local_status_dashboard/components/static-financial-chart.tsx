type Row = { period: string; [key: string]: number | string | null };
type Series = { key: string; label: string; color: string; kind: 'bar' | 'line' };
const format = (value: number) => value.toLocaleString('en-IN', { maximumFractionDigits: 2 });

// Server-rendered quantitative SVG: charts remain present without hydration or ResizeObserver.
export function StaticFinancialChart({ data, series, title }: { data: Row[]; series: readonly Series[]; title: string }) {
  const values = data.flatMap(row => series.map(s => row[s.key])).filter((v): v is number => typeof v === 'number' && Number.isFinite(v));
  if (!values.length) return <p>No source figures available.</p>;
  const width = 640, height = 310, left = 76, right = 20, top = 24, bottom = 48;
  const low = Math.min(0, ...values), high = Math.max(0, ...values);
  const span = high - low || 1;
  const min = low < 0 ? low - span * 0.05 : 0;
  const max = high > 0 ? high + span * 0.08 : (low < 0 ? 0 : 1);
  const plotWidth = width - left - right, plotHeight = height - top - bottom;
  const step = plotWidth / Math.max(data.length, 1);
  const x = (index: number) => left + step * (index + 0.5);
  const y = (value: number) => top + (max - value) / (max - min) * plotHeight;
  const barCount = series.filter(s => s.kind === 'bar').length;
  const barWidth = Math.min(28, step * 0.65 / Math.max(1, barCount));
  const ticks = Array.from({ length: 5 }, (_, i) => min + (max - min) * i / 4);
  return <div className="mt-4 overflow-x-auto" tabIndex={0} role="region" aria-label={`${title}. Scroll horizontally on small screens.`}>
    <svg data-financial-chart="server-rendered" viewBox={`0 0 ${width} ${height}`} width={width} height={height} style={{ display: 'block', width: '100%', minWidth: 520, height: 'auto' }} role="img" aria-label={`${title}. Values in rupees crore. Exact numbers in the table below.`}>
      <title>{title}</title><desc>Annual standalone financial history. Pending META review. Missing values are gaps; zero values are not inflated.</desc>
      {ticks.map((tick, i) => <g key={i}><line x1={left} x2={width - right} y1={y(tick)} y2={y(tick)} stroke="#29434a" strokeDasharray="3 3" /><text x={left - 9} y={y(tick) + 4} textAnchor="end" fill="#cbd5e1" fontSize={12}>{format(Math.round(tick))}</text></g>)}
      <line x1={left} x2={width - right} y1={y(0)} y2={y(0)} stroke="#94a3b8" />
      {data.map((row, index) => <text key={row.period} x={x(index)} y={height - 20} textAnchor="middle" fill="#cbd5e1" fontSize={12}>{row.period.replace('FY20', '')}</text>)}
      {series.map(s => {
        const barIndex = series.filter(item => item.kind === 'bar').findIndex(item => item.key === s.key);
        let connected = false;
        const path = data.map((row, i) => {
          const value = row[s.key];
          if (typeof value !== 'number' || !Number.isFinite(value)) { connected = false; return ''; }
          const command = `${connected ? 'L' : 'M'}${x(i)},${y(value)}`;
          connected = true;
          return command;
        }).join(' ');
        return <g key={s.key} data-series={s.key}>
          {s.kind === 'line' && <path d={path} fill="none" stroke={s.color} strokeWidth={2.5} />}
          {data.map((row, i) => {
            const value = row[s.key];
            if (typeof value !== 'number' || !Number.isFinite(value)) return null;
            const label = `${row.period} · ${s.label}: ₹${format(value)} crore`;
            return s.kind === 'bar'
              ? <rect key={row.period} x={x(i) - barCount * barWidth / 2 + barIndex * barWidth} y={Math.min(y(0), y(value))} width={barWidth - 2} height={Math.abs(y(value) - y(0))} fill={s.color}><title>{label}</title></rect>
              : <circle key={row.period} cx={x(i)} cy={y(value)} r={3.5} fill={s.color}><title>{label}</title></circle>;
          })}
        </g>;
      })}
    </svg>
  </div>;
}
