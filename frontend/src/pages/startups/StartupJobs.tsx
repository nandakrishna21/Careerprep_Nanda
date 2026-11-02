import { Fragment, useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import {
  Building2,
  ChevronDown,
  ExternalLink,
  MapPin,
  RefreshCw,
  Search,
  ShieldCheck,
  Trophy,
} from 'lucide-react';
import { Badge, Button, Card, EmptyState } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { errorMessage, get, invalidateCache, post } from '../../lib/api';
import { type Job, type Paged } from '../../lib/types';
import { useAuth } from '../../stores/auth';
import {
  RESEARCH_NOTES,
  RESEARCH_SESSION,
  STARTUP_JOBS,
  TOP_TEN,
  type StartupJob,
  type VerificationStatus,
} from '../../lib/startupJobs';

const VERIFICATION_COLOR: Record<VerificationStatus, 'green' | 'amber' | 'rose'> = {
  Verified: 'green',
  Partial: 'amber',
  Unverified: 'rose',
};

const CITY_FILTERS = ['All', 'Hyderabad', 'Bengaluru'] as const;
type CityFilter = (typeof CITY_FILTERS)[number];

interface BoardSyncStatus {
  last_synced_at: string | null;
  token_configured?: boolean;
}

function normName(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]/g, '');
}

// Search needles for a research company: the main name plus aliases hidden in
// parentheses ("Fairground (formerly Orbital)" also matches "Orbital").
function needlesFor(company: string): string[] {
  const needles = new Set<string>();
  const add = (raw: string) => {
    const n = normName(raw);
    if (n.length >= 4) needles.add(n);
  };
  let primary = company;
  for (const group of company.match(/\(([^)]+)\)/g) ?? []) {
    const inner = group.slice(1, -1);
    primary = primary.replace(group, ' ');
    add(inner.replace(/^(formerly|operated by)\s+/i, ''));
  }
  add(primary);
  return [...needles];
}

// Bidirectional contains match so "Eli Lilly and Company" hits job boards that
// list "Eli Lilly" (and vice versa). Very short names are skipped to avoid
// accidental substring hits.
function jobMatchesCompany(jobCompany: string, needles: string[]): boolean {
  const j = normName(jobCompany);
  if (j.length < 4) return false;
  return needles.some((needle) => j.includes(needle) || needle.includes(j));
}

function timeAgo(iso: string | null): string | null {
  if (!iso) return null;
  const mins = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

const HEADERS = [
  'Company',
  'City',
  'Industry',
  'Company Website',
  'Company Size',
  'Tech Stack',
  'Funding',
  'Job Role',
  'Experience',
  'Salary',
  'Job Link',
  'Recruiter',
  'Verification Status',
];

export default function StartupJobs() {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin' || user?.role === 'superadmin';
  const [city, setCity] = useState<CityFilter>('All');
  const [query, setQuery] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);
  const [live, setLive] = useState<Record<number, Job[]> | null>(null);
  const [syncStatus, setSyncStatus] = useState<BoardSyncStatus | null>(null);
  const [syncing, setSyncing] = useState(false);

  const needlesByRank = useMemo(
    () => new Map(STARTUP_JOBS.map((s) => [s.rank, needlesFor(s.company)])),
    [],
  );

  const loadLive = async () => {
    try {
      const recent: Job[] = [];
      for (let page = 1; page <= 4; page++) {
        const data = await get<Paged<Job>>('/jobs', {
          type: 'it',
          page,
          page_size: 100,
          sort: 'newest',
        });
        recent.push(...data.items);
        if (data.items.length === 0 || recent.length >= data.total) break;
      }
      const matches: Record<number, Job[]> = {};
      for (const startup of STARTUP_JOBS) {
        const needles = needlesByRank.get(startup.rank) ?? [];
        const hits = recent.filter((job) => jobMatchesCompany(job.company, needles));
        if (hits.length) matches[startup.rank] = hits;
      }
      setLive(matches);
    } catch {
      setLive({});
    }
  };

  const loadStatus = async () => {
    try {
      setSyncStatus(
        isAdmin
          ? await get<BoardSyncStatus>('/admin/jobs/sync/status')
          : await get<BoardSyncStatus>('/jobs/sync/status'),
      );
    } catch {
      setSyncStatus(null);
    }
  };

  useEffect(() => {
    void loadLive();
    void loadStatus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAdmin]);

  const pollForFreshSync = async (before: string | null) => {
    const t0 = Date.now();
    for (let i = 0; i < 150; i++) {
      await new Promise((resolve) => setTimeout(resolve, 5000));
      const elapsed = Math.round((Date.now() - t0) / 1000);
      const label = `${Math.floor(elapsed / 60)}:${String(elapsed % 60).padStart(2, '0')}`;
      let status: BoardSyncStatus | null = null;
      try {
        status = await get<BoardSyncStatus>('/admin/jobs/sync/status');
        setSyncStatus(status);
      } catch {
        /* keep polling through blips */
      }
      if (status?.last_synced_at && status.last_synced_at !== before) return true;
      toast.loading(`Crawling live boards… ${label} elapsed — safe to keep browsing, it finishes on its own.`, {
        id: 'startup-sync',
      });
    }
    return false;
  };

  const runSync = async () => {
    if (syncing) return;
    if (syncStatus && syncStatus.token_configured === false) {
      toast.error('Live refresh is unavailable — the crawler API key has not been configured on the server.');
      return;
    }
    setSyncing(true);
    const before = syncStatus?.last_synced_at ?? null;
    toast.loading('Crawling live boards with Apify — usually 3–8 minutes…', { id: 'startup-sync' });
    try {
      await post<{ started: boolean }>('/admin/jobs/sync?track=it&background=true');
      const fresh = await pollForFreshSync(before);
      invalidateCache('/jobs');
      await Promise.all([loadLive(), loadStatus()]);
      if (fresh) {
        toast.success('Openings refreshed — live matches updated below.', {
          id: 'startup-sync',
          duration: 6000,
        });
      } else {
        toast('Still crawling — live matches will catch up shortly.', {
          id: 'startup-sync',
          duration: 8000,
        });
      }
    } catch (err) {
      toast.error(errorMessage(err), { id: 'startup-sync', duration: 8000 });
    } finally {
      setSyncing(false);
    }
  };

  const items = useMemo(() => {
    const q = query.trim().toLowerCase();
    return STARTUP_JOBS.filter((job) => {
      if (city !== 'All' && job.city !== city) return false;
      if (!q) return true;
      return (
        job.company.toLowerCase().includes(q) ||
        job.role.toLowerCase().includes(q) ||
        job.industry.toLowerCase().includes(q) ||
        job.skills.toLowerCase().includes(q) ||
        job.techStack.toLowerCase().includes(q)
      );
    });
  }, [city, query]);

  const liveMatches = useMemo<{ startup: StartupJob; jobs: Job[] }[]>(
    () =>
      live
        ? items
            .map((startup) => ({ startup, jobs: live[startup.rank] ?? [] }))
            .filter((row) => row.jobs.length > 0)
        : [],
    [live, items],
  );
  const liveTotal = liveMatches.reduce((count, row) => count + row.jobs.length, 0);

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Startup Jobs — Hyderabad & Bengaluru"
        subtitle={`Research session ${RESEARCH_SESSION.date}: ${RESEARCH_SESSION.count} legitimate product companies hiring now for ${RESEARCH_SESSION.roles}. Ranked for a Python + AI profile.`}
        actions={
          <>
            {syncStatus?.last_synced_at && (
              <span className="text-xs font-semibold text-slate-400 dark:text-slate-500">
                Crawled {timeAgo(syncStatus.last_synced_at)}
              </span>
            )}
            {isAdmin && (
              <Button variant="outline" onClick={() => void runSync()} loading={syncing}>
                <RefreshCw className="h-4 w-4" /> Refresh openings
              </Button>
            )}
          </>
        }
      />

      <div className="flex flex-wrap items-center gap-2">
        {CITY_FILTERS.map((c) => (
          <button
            key={c}
            type="button"
            aria-pressed={city === c}
            onClick={() => setCity(c)}
            className={`rounded-xl px-3.5 py-2 text-sm font-semibold transition ${
              city === c
                ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            {c}
          </button>
        ))}
        <div className="relative ml-auto w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search company, role or skill (FastAPI, RAG, FDE...)"
            className="input pl-9"
          />
        </div>
      </div>

      <SectionHeader
        title="Ranked company table"
        subtitle={`${items.length} of ${STARTUP_JOBS.length} companies · ranked by job availability, Python/AI match, startup exposure, legitimacy and experience fit`}
      />

      {items.length ? (
        <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
          <table className="w-full min-w-[1500px] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-800/50">
                {HEADERS.map((h) => (
                  <th
                    key={h}
                    className="whitespace-nowrap px-3 py-2.5 text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map((job) => {
                const isOpen = expanded === job.rank;
                const hits = live?.[job.rank] ?? [];
                return (
                  <Fragment key={job.rank}>
                    <tr
                      onClick={() => setExpanded(isOpen ? null : job.rank)}
                      className={`cursor-pointer border-b border-slate-100 transition dark:border-slate-800 ${
                        isOpen
                          ? 'bg-brand-50/60 dark:bg-brand-500/10'
                          : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'
                      }`}
                    >
                      <td className="px-3 py-2.5">
                        <div className="flex items-center gap-2">
                          <ChevronDown
                            className={`h-3.5 w-3.5 shrink-0 text-slate-400 transition ${isOpen ? 'rotate-180' : ''}`}
                          />
                          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-brand-600 text-[11px] font-bold text-white">
                            {job.rank}
                          </span>
                          <a
                            href={job.website}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            className="font-bold text-slate-900 hover:text-brand-600 dark:text-white dark:hover:text-brand-400"
                          >
                            {job.company}
                          </a>
                          {hits.length > 0 && <Badge color="green">{hits.length} live</Badge>}
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-2.5">
                        <span className="inline-flex items-center gap-1 text-slate-600 dark:text-slate-300">
                          <MapPin className="h-3.5 w-3.5 text-brand-500" />
                          {job.city}
                        </span>
                      </td>
                      <td className="max-w-[220px] px-3 py-2.5 text-slate-600 dark:text-slate-300">
                        {job.industry}
                      </td>
                      <td className="px-3 py-2.5">
                        <a
                          href={job.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-brand-600 hover:underline dark:text-brand-400"
                        >
                          site <ExternalLink className="h-3 w-3" />
                        </a>
                      </td>
                      <td className="whitespace-nowrap px-3 py-2.5 text-slate-600 dark:text-slate-300">
                        {job.size}
                      </td>
                      <td className="max-w-[260px] px-3 py-2.5 text-xs text-slate-500 dark:text-slate-400">
                        {job.techStack}
                      </td>
                      <td className="max-w-[260px] px-3 py-2.5 text-xs text-slate-500 dark:text-slate-400">
                        {job.funding}
                      </td>
                      <td className="max-w-[220px] px-3 py-2.5 font-semibold text-slate-800 dark:text-slate-200">
                        {job.role}
                      </td>
                      <td className="whitespace-nowrap px-3 py-2.5 text-slate-600 dark:text-slate-300">
                        {job.experience}
                      </td>
                      <td className="whitespace-nowrap px-3 py-2.5 text-slate-600 dark:text-slate-300">
                        {job.salary}
                      </td>
                      <td className="px-3 py-2.5">
                        <a
                          href={job.jobLink}
                          target="_blank"
                          rel="noopener noreferrer"
                          onClick={(e) => e.stopPropagation()}
                          className="inline-flex items-center gap-1 rounded-lg bg-brand-600 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-brand-700"
                        >
                          Apply <ExternalLink className="h-3 w-3" />
                        </a>
                      </td>
                      <td className="whitespace-nowrap px-3 py-2.5 text-slate-500 dark:text-slate-400">
                        {job.recruiter}
                      </td>
                      <td className="whitespace-nowrap px-3 py-2.5">
                        <Badge color={VERIFICATION_COLOR[job.verification]}>
                          {job.verification}
                        </Badge>
                      </td>
                    </tr>
                    {isOpen && (
                      <tr
                        className="border-b border-slate-100 bg-brand-50/40 dark:border-slate-800 dark:bg-brand-500/5"
                      >
                        <td colSpan={HEADERS.length} className="px-5 py-4">
                          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                            <Detail label="Office location" value={job.office} />
                            <Detail label="Founded" value={job.founded} />
                            <Detail label="LinkedIn" value={job.linkedin} isLink={job.linkedin.startsWith('http')} linkHref={job.linkedin} />
                            <Detail label="Leadership" value={job.leadership} />
                            <Detail label="Required skills" value={job.skills} />
                            <Detail label="Posted / last verified" value={job.posted} />
                            <Detail label="Careers page" value={job.careers} isLink={job.careers.startsWith('http')} linkHref={job.careers} />
                            <Detail label="Industry" value={job.industry} />
                          </div>
                          <div className="mt-4 rounded-xl border border-brand-200 bg-white p-3 text-sm text-slate-600 dark:border-brand-500/30 dark:bg-slate-900 dark:text-slate-300">
                            <b className="text-brand-600 dark:text-brand-400">Research notes:</b>{' '}
                            {job.notes}
                          </div>
                          {hits.length > 0 && (
                            <div className="mt-4 rounded-xl border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-500/30 dark:bg-emerald-500/10">
                              <p className="text-[11px] font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-300">
                                Live openings from the latest crawl ({hits.length})
                              </p>
                              <ul className="mt-2 space-y-1.5">
                                {hits.map((hit) => (
                                  <li key={hit.id} className="flex flex-wrap items-center gap-2 text-sm">
                                    <span className="min-w-0 font-semibold text-slate-800 dark:text-slate-200">
                                      {hit.title}
                                    </span>
                                    <Badge color="slate">{hit.source}</Badge>
                                    {hit.posted_at && (
                                      <span className="text-xs text-slate-400">{timeAgo(hit.posted_at)}</span>
                                    )}
                                    <a
                                      href={hit.apply_link}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      onClick={(e) => e.stopPropagation()}
                                      className="ml-auto inline-flex items-center gap-1 rounded-lg bg-emerald-600 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-emerald-700"
                                    >
                                      Apply <ExternalLink className="h-3 w-3" />
                                    </a>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <EmptyState
          title="Nothing matched that search"
          description="Try a company name, a role keyword like FDE or RAG, or switch the city filter."
          action={
            <button
              type="button"
              onClick={() => {
                setQuery('');
                setCity('All');
              }}
              className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            >
              Clear filters
            </button>
          }
        />
      )}

      {items.length > 0 && (
        <>
          <SectionHeader
            title="Live openings from these companies"
            subtitle={
              live === null
                ? 'Fetching the latest crawled openings…'
                : `${liveTotal} live opening${liveTotal === 1 ? '' : 's'} across ${liveMatches.length} compan${
                    liveMatches.length === 1 ? 'y' : 'ies'
                  } · matched by company name from the crawled IT board · auto-sync daily 11:00 AM IST${
                    syncStatus?.last_synced_at ? ` · last crawl ${timeAgo(syncStatus.last_synced_at)}` : ''
                  }`
            }
          />
          {liveMatches.length ? (
            <Card className="space-y-4">
              {liveMatches.map(({ startup, jobs }) => (
                <div key={startup.rank} className="border-b border-slate-100 pb-4 last:border-0 last:pb-0">
                  <p className="flex flex-wrap items-center gap-2 font-bold text-slate-900 dark:text-white">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-brand-600 text-[11px] font-bold text-white">
                      {startup.rank}
                    </span>
                    {startup.company}
                    <Badge color="green">{jobs.length} live</Badge>
                    <span className="text-xs font-normal text-slate-400">{startup.city}</span>
                  </p>
                  <ul className="mt-2 space-y-1.5">
                    {jobs.map((hit) => (
                      <li key={hit.id} className="flex flex-wrap items-center gap-2 text-sm">
                        <span className="min-w-0 flex-1 text-slate-700 dark:text-slate-200">{hit.title}</span>
                        <span className="text-xs text-slate-400">
                          {hit.source}
                          {hit.posted_at ? ` · ${timeAgo(hit.posted_at)}` : ''}
                        </span>
                        <a
                          href={hit.apply_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 rounded-lg bg-brand-600 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-brand-700"
                        >
                          Apply <ExternalLink className="h-3 w-3" />
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </Card>
          ) : (
            <EmptyState
              title="No live matches yet"
              description={
                isAdmin
                  ? 'No crawled listings match these companies right now — hit "Refresh openings" above to run an Apify crawl, or wait for the daily 11:00 AM IST sync.'
                  : 'No crawled listings match these companies right now — the board re-syncs daily at 11:00 AM IST.'
              }
            />
          )}
        </>
      )}

      <SectionHeader
        title="Top 10 companies to apply to first"
        subtitle="Ranked on job availability, Python + AI match, startup/product exposure, legitimacy and fit for an early-to-mid Python/AI profile."
      />

      <div className="grid gap-4 sm:grid-cols-2">
        {TOP_TEN.map((pick) => (
          <Card key={pick.company} className="flex gap-3">
            <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-amber-100 text-sm font-extrabold text-amber-700 dark:bg-amber-500/20 dark:text-amber-300">
              {pick.rank}
            </span>
            <div className="min-w-0">
              <h3 className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white">
                <Trophy className="h-3.5 w-3.5 text-amber-500" />
                {pick.company}
              </h3>
              <p className="mt-1 text-sm leading-relaxed text-slate-500 dark:text-slate-400">
                {pick.why}
              </p>
            </div>
          </Card>
        ))}
      </div>

      <Card className="space-y-3">
        <h2 className="flex items-center gap-2 font-bold text-slate-900 dark:text-white">
          <ShieldCheck className="h-5 w-5 text-emerald-500" /> Research notes &
          methodology
        </h2>
        <ul className="space-y-2 text-sm text-slate-500 dark:text-slate-400">
          {RESEARCH_NOTES.map((note) => (
            <li key={note} className="flex items-start gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-brand-500" />
              {note}
            </li>
          ))}
        </ul>
        <p className="flex items-center gap-2 text-xs font-semibold text-slate-400">
          <Building2 className="h-3.5 w-3.5" />
          Next session: re-run this research weekly — postings rotate fast in this market.
        </p>
      </Card>
    </div>
  );
}

function Detail({
  label,
  value,
  isLink,
  linkHref,
}: {
  label: string;
  value: string;
  isLink?: boolean;
  linkHref?: string;
}) {
  return (
    <div>
      <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
        {label}
      </p>
      {isLink ? (
        <a
          href={linkHref}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-0.5 block break-words text-sm text-brand-600 hover:underline dark:text-brand-400"
        >
          {value}
        </a>
      ) : (
        <p className="mt-0.5 break-words text-sm text-slate-600 dark:text-slate-300">{value}</p>
      )}
    </div>
  );
}
