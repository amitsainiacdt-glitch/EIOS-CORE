'use client';

import { useState } from 'react';
import { ExternalLink, ShieldCheck } from 'lucide-react';

type Item = { candidateId: string; queuePath: string; metaPath: string; eventType: string; statementPosture: string; sourcePassage: string; explicitAmounts: string[]; explicitDates: string[]; pdfPage: number | null; sourceUrl: string; reviewStatus: string; meta: null | { decision: string; uncertaintyStatement: string } };

export function GovernedReviewInbox({ items }: { items: Item[] }) {
  const [reviewing, setReviewing] = useState<{ item: Item; decision: 'APPROVE' | 'HOLD' | 'REJECT' } | null>(null);
  const [rationale, setRationale] = useState('');
  const [confidence, setConfidence] = useState(70);
  const [feedback, setFeedback] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);
  async function submit() {
    if (!reviewing || rationale.trim().length < 10) return;
    setBusy(true);
    try {
      const response = await fetch('http://127.0.0.1:3001/review', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ candidateId: reviewing.item.candidateId, queuePath: reviewing.item.queuePath, metaPath: reviewing.item.metaPath, decision: reviewing.decision, rationale: rationale.trim(), approvedConfidence: reviewing.decision === 'APPROVE' ? confidence : undefined, reviewer: 'EIOS_LOCAL_USER' }) });
      const result = await response.json() as { ok: boolean; error?: string };
      if (!response.ok || !result.ok) throw new Error(result.error || 'Decision could not be recorded.');
      setFeedback((current) => ({ ...current, [reviewing.item.candidateId]: `${reviewing.decision} recorded` })); setReviewing(null); setRationale('');
    } catch (error) { setFeedback((current) => ({ ...current, [reviewing.item.candidateId]: error instanceof Error ? error.message : 'Review service unavailable.' })); }
    finally { setBusy(false); }
  }
  if (!items.length) return <div className="rounded-xl border border-dashed border-white/[0.1] px-5 py-8 text-center"><ShieldCheck className="mx-auto text-slate-700" size={20} /><p className="mt-3 text-sm text-slate-300">No official facts are waiting for review.</p><p className="mt-1 text-xs text-slate-600">New page-linked passages will appear here automatically.</p></div>;
  return <div className="space-y-3">{items.map((item) => <article key={item.candidateId} className="rounded-xl border border-white/[0.07] bg-black/10 p-4"><div className="flex flex-wrap items-center gap-2"><span className="text-[0.6rem] font-semibold uppercase tracking-wider text-sky-200">{item.eventType.replaceAll('_', ' ')}</span><span className="ml-auto text-[0.6rem] uppercase text-amber-200">{feedback[item.candidateId] || item.reviewStatus.replaceAll('_', ' ')}</span></div><blockquote className="mt-3 border-l-2 border-emerald-300/25 pl-3 text-sm leading-6 text-slate-200">{item.sourcePassage}</blockquote><div className="mt-3 flex flex-wrap gap-3 text-xs text-slate-600">{item.pdfPage !== null && <span>PDF page {item.pdfPage}</span>}<a href={item.sourceUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-sky-300">Official source <ExternalLink size={11} /></a></div>{!feedback[item.candidateId] && <div className="mt-3 flex gap-2"><Action label="Approve" disabled={item.meta?.decision !== 'READY_FOR_HUMAN_REVIEW'} onClick={() => setReviewing({ item, decision: 'APPROVE' })} /><Action label="Hold" onClick={() => setReviewing({ item, decision: 'HOLD' })} /><Action label="Reject" onClick={() => setReviewing({ item, decision: 'REJECT' })} /></div>}{reviewing?.item.candidateId === item.candidateId && <div className="mt-3 rounded-lg border border-white/[0.08] p-3"><textarea value={rationale} onChange={(event) => setRationale(event.target.value)} rows={3} placeholder="Required rationale…" className="w-full rounded-lg border border-white/[0.08] bg-black/20 p-3 text-xs text-white outline-none" />{reviewing.decision === 'APPROVE' && <label className="mt-2 block text-xs text-slate-500">Confidence {confidence}%<input type="range" min="0" max="100" value={confidence} onChange={(event) => setConfidence(Number(event.target.value))} className="mt-1 block w-full accent-emerald-300" /></label>}<div className="mt-3 flex gap-2"><button disabled={busy || rationale.trim().length < 10} onClick={submit} className="rounded-md bg-emerald-300 px-3 py-2 text-xs font-semibold text-[#071114] disabled:opacity-40">{busy ? 'Recording…' : 'Confirm'}</button><button onClick={() => setReviewing(null)} className="rounded-md border border-white/[0.08] px-3 py-2 text-xs text-slate-400">Cancel</button></div></div>}</article>)}</div>;
}
function Action({ label, disabled = false, onClick }: { label: string; disabled?: boolean; onClick: () => void }) { return <button disabled={disabled} onClick={onClick} className="rounded-md border border-white/[0.09] px-3 py-1.5 text-xs text-slate-300 disabled:cursor-not-allowed disabled:opacity-25">{label}</button>; }
