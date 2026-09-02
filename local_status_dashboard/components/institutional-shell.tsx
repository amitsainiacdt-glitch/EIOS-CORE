import Link from 'next/link';
import { Activity, Bell, BookOpenText, Bot, Boxes, BriefcaseBusiness, Building2, ChevronDown, CircleGauge, Database, FileText, FlaskConical, GraduationCap, LayoutDashboard, Radar, Search, Settings, ShieldCheck, Target } from 'lucide-react';

const primary = [
  { href: '/', label: 'Intelligence Home', icon: LayoutDashboard },
  { href: '/opportunities', label: 'Opportunity Watch', icon: Target },
  { href: '/companies', label: 'Companies', icon: Building2 },
  { href: '/sectors', label: 'Sectors', icon: Boxes, future: true },
  { href: '/watchlists', label: 'Watchlists', icon: Radar, future: true },
  { href: '/portfolio', label: 'Portfolio', icon: BriefcaseBusiness, future: true },
  { href: '/research', label: 'Research', icon: BookOpenText, future: true },
  { href: '/intelligence', label: 'Intelligence', icon: Activity, future: true },
  { href: '/documents', label: 'Documents', icon: FileText, future: true },
];
const system = [
  { href: '/system/runtime', label: 'Research Runtime', icon: CircleGauge },
  { href: '/system/learning', label: 'Learning Ledger', icon: GraduationCap, future: true },
  { href: '/settings', label: 'Settings', icon: Settings, future: true },
];

export function InstitutionalShell({ active, generatedAt, children }: { active: string; generatedAt: string; children: React.ReactNode }) {
  const updated = generatedAt ? new Date(generatedAt).toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : 'Unknown';
  return <div className="min-h-screen bg-background text-foreground lg:grid lg:grid-cols-[15.5rem_minmax(0,1fr)]">
    <aside className="hidden min-h-screen border-r border-white/[0.07] bg-[#071013] lg:sticky lg:top-0 lg:flex lg:h-screen lg:flex-col">
      <div className="flex h-[4.6rem] items-center gap-3 border-b border-white/[0.07] px-5"><span className="grid h-9 w-9 place-items-center rounded-lg border border-emerald-300/15 bg-emerald-300/[0.07] text-emerald-200"><Database size={18} /></span><div><p className="text-sm font-semibold tracking-[0.2em] text-white">EIOS</p><p className="text-[0.62rem] uppercase tracking-[0.12em] text-slate-600">Equity Intelligence</p></div></div>
      <nav aria-label="Primary" className="flex-1 overflow-y-auto px-3 py-4"><NavGroup items={primary} active={active} /><div className="my-4 border-t border-white/[0.06]" /><div title="Workspace reserved for future backend connection" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs text-slate-700"><FlaskConical size={16} /><span>Commodity EIOS</span><span className="ml-auto text-[0.55rem] uppercase tracking-wider">Reserved</span></div><div className="my-4 border-t border-white/[0.06]" /><p className="px-3 pb-2 text-[0.58rem] font-semibold uppercase tracking-[0.16em] text-slate-700">System</p><NavGroup items={system} active={active} /></nav>
      <div className="border-t border-white/[0.07] p-4"><div className="flex items-center gap-2 rounded-lg border border-emerald-300/10 bg-emerald-300/[0.035] px-3 py-2 text-[0.68rem] text-emerald-200"><ShieldCheck size={14} />Local · governed · review required</div></div>
    </aside>
    <div className="min-w-0">
      <header className="sticky top-0 z-40 flex h-[4.6rem] items-center gap-3 border-b border-white/[0.07] bg-[#081316]/95 px-4 backdrop-blur-xl sm:px-6 xl:px-8"><div className="flex items-center gap-2 lg:hidden"><Database className="text-emerald-200" size={18} /><span className="text-sm font-semibold tracking-[0.16em]">EIOS</span></div><label className="relative hidden max-w-xl flex-1 sm:block" title="Universal search will activate after the governed query API is connected"><span className="sr-only">Universal search is not yet connected</span><Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-700" size={16} /><input disabled aria-label="Universal search is not yet connected" placeholder="Universal search · backend connection pending" className="h-10 w-full cursor-not-allowed rounded-lg border border-white/[0.06] bg-white/[0.015] pl-10 pr-4 text-xs text-slate-700 outline-none placeholder:text-slate-700" /></label><div className="ml-auto flex items-center gap-2"><div className="hidden text-right xl:block"><p className="text-[0.58rem] uppercase tracking-[0.12em] text-slate-600">Latest intelligence</p><p className="mt-0.5 text-[0.68rem] text-slate-400">{updated}</p></div><span className="hidden h-7 w-px bg-white/[0.07] xl:block" /><span className="inline-flex items-center gap-2 rounded-lg border border-emerald-300/12 bg-emerald-300/[0.04] px-2.5 py-2 text-[0.65rem] font-medium text-emerald-200"><span className="h-1.5 w-1.5 rounded-full bg-emerald-300" />Runtime connected</span><button disabled title="Alert service not connected" aria-label="Alerts are not yet connected" className="grid h-9 w-9 cursor-not-allowed place-items-center rounded-lg border border-white/[0.05] text-slate-700"><Bell size={15} /></button><button disabled title="AI research query service not connected" aria-label="AI research assistant is not yet connected" className="grid h-9 w-9 cursor-not-allowed place-items-center rounded-lg border border-white/[0.05] text-slate-700"><Bot size={15} /></button><button className="hidden items-center gap-1.5 rounded-lg border border-white/[0.07] px-2.5 py-2 text-[0.68rem] text-slate-400 sm:flex">Local user <ChevronDown size={12} /></button></div></header>
      <div className="border-b border-white/[0.06] bg-[#071114] px-4 py-2 lg:hidden"><div className="flex gap-1 overflow-x-auto"><MobileLink href="/" label="Home" active={active === 'home'} /><MobileLink href="/opportunities" label="Opportunities" active={active === 'opportunity-watch'} /><MobileLink href="/companies" label="Companies" active={active === 'companies'} /><MobileLink href="/system/runtime" label="Runtime" active={active === 'research-runtime'} /></div></div>
      <main className="mx-auto max-w-[108rem] px-4 py-6 sm:px-6 xl:px-8 xl:py-8">{children}</main>
    </div>
  </div>;
}

function NavGroup({ items, active }: { items: typeof primary; active: string }) {
  return <div className="space-y-0.5">{items.map(({ href, label, icon: Icon, future }) => future ? <div key={href} title="Workspace reserved for a future backend connection" className="flex cursor-not-allowed items-center gap-3 rounded-lg px-3 py-2.5 text-xs text-slate-700"><Icon size={16} /><span>{label}</span></div> : <Link key={href} href={href} className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs transition ${active === label.toLocaleLowerCase().replaceAll(' ', '-') || (active === 'home' && href === '/') ? 'border border-emerald-300/10 bg-emerald-300/[0.065] text-emerald-100' : 'text-slate-500 hover:bg-white/[0.03] hover:text-slate-200'}`}><Icon size={16} /><span>{label}</span></Link>)}</div>;
}
function MobileLink({ href, label, active }: { href: string; label: string; active: boolean }) { return <Link href={href} className={`shrink-0 rounded-md px-3 py-1.5 text-[0.68rem] ${active ? 'bg-emerald-300/10 text-emerald-200' : 'text-slate-500'}`}>{label}</Link>; }
