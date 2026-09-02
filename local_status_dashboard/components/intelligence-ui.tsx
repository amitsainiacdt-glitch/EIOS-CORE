import { AlertCircle, CircleDashed, ShieldCheck } from 'lucide-react';

export function PageHeader({ eyebrow, title, description, action }: { eyebrow: string; title: string; description: string; action?: React.ReactNode }) {
  return <header className="flex flex-col gap-4 border-b border-white/[0.08] pb-6 md:flex-row md:items-end md:justify-between"><div><p className="terminal-label">{eyebrow}</p><h1 className="mt-2 font-heading text-3xl font-medium tracking-[-0.025em] text-white">{title}</h1><p className="mt-2.5 max-w-3xl text-sm leading-6 text-slate-500">{description}</p></div>{action}</header>;
}

export function TrustBadge({ state }: { state: string }) {
  const normalized = state.toUpperCase();
  const positive = ['READY', 'CONFIRMED', 'GOVERNED_FACT', 'SUCCESS', 'ACTIVE'].some((value) => normalized === value || normalized.includes(value));
  const warning = ['PARTIAL', 'HOLD', 'PENDING', 'PROVISIONAL', 'DISCOVERED', 'INCOMPLETE'].some((value) => normalized.includes(value));
  const negative = ['CONFLICTING', 'FAILED', 'ERROR', 'UNAVAILABLE'].some((value) => normalized.includes(value));
  const stale = normalized.includes('STALE');
  const label = normalized.includes('UNKNOWN') ? 'UNKNOWN' : normalized.replaceAll('_', ' ');
  const classes = positive ? 'border-emerald-300/15 bg-emerald-300/[0.055] text-emerald-200' : negative ? 'border-rose-300/15 bg-rose-300/[0.055] text-rose-200' : warning ? 'border-amber-300/15 bg-amber-300/[0.055] text-amber-200' : stale ? 'border-violet-300/15 bg-violet-300/[0.055] text-violet-200' : 'border-white/[0.08] bg-white/[0.025] text-slate-500';
  return <span className={`inline-flex items-center gap-1.5 rounded-md border px-2 py-1 text-[0.58rem] font-semibold uppercase tracking-[0.08em] ${classes}`}>{positive ? <ShieldCheck size={11} /> : warning || negative ? <AlertCircle size={11} /> : <CircleDashed size={11} />}{label}</span>;
}

export function EmptyState({ title, detail }: { title: string; detail: string }) {
  return <div className="rounded-xl border border-dashed border-white/[0.1] bg-white/[0.015] px-5 py-10 text-center"><CircleDashed className="mx-auto text-slate-700" size={21} /><p className="mt-3 text-sm text-slate-300">{title}</p><p className="mx-auto mt-1 max-w-xl text-xs leading-5 text-slate-600">{detail}</p></div>;
}

export function CoverageBar({ value }: { value: number }) {
  return <div className="h-1.5 overflow-hidden rounded-full bg-white/[0.05]"><div className={`h-full rounded-full ${value === 100 ? 'bg-emerald-300' : value > 0 ? 'bg-amber-300' : 'bg-slate-700'}`} style={{ width: `${value}%` }} /></div>;
}
