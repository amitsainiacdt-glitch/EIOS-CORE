'use client';

import { Check, Copy, Share2 } from 'lucide-react';
import { useState } from 'react';

export function ReferralCard() {
  const [copied, setCopied] = useState(false);
  const copyLink = async () => {
    const link = `${window.location.origin}/?ref=eios-friend`;
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  };
  return <section className="mt-7"><div className="flex items-center gap-3"><h2 className="shrink-0 text-[0.65rem] font-semibold uppercase tracking-[0.16em] text-slate-400">Share the research standard</h2><span className="h-px flex-1 bg-white/[0.07]" /></div><article className="mt-3 flex flex-col gap-4 rounded-xl border border-sky-300/12 bg-sky-300/[0.022] p-5 lg:flex-row lg:items-center lg:justify-between"><div className="flex gap-3"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-sky-300/[0.08] text-sky-200"><Share2 size={16} /></span><div><p className="text-sm font-medium text-white">Know someone who values evidence over noise?</p><p className="mt-1 max-w-2xl text-xs leading-5 text-slate-500">Invite them to explore EIOS. The referral link is ready to share; account attribution and referral rewards will activate when the identity service is connected.</p></div></div><button type="button" onClick={copyLink} className="inline-flex shrink-0 items-center justify-center gap-2 rounded-lg border border-sky-300/15 bg-sky-300/[0.07] px-3.5 py-2.5 text-xs font-medium text-sky-100 transition hover:bg-sky-300/[0.12]">{copied ? <Check size={14} /> : <Copy size={14} />}{copied ? 'Referral link copied' : 'Copy referral link'}</button></article></section>;
}
