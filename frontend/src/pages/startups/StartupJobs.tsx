import { Fragment, useMemo, useState } from 'react';
import {
  Building2,
  ChevronDown,
  ExternalLink,
  Info,
  MapPin,
  Search,
  ShieldCheck,
  Trophy,
} from 'lucide-react';
import { Badge, Card, EmptyState } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import {
  RESEARCH_NOTES,
  RESEARCH_SESSION,
  STARTUP_JOBS,
  TOP_TEN,
  type VerificationStatus,
} from '../../lib/startupJobs';

const VERIFICATION_COLOR: Record<VerificationStatus, 'green' | 'amber' | 'rose'> = {
  Verified: 'green',
  Partial: 'amber',
  Unverified: 'rose',
};

const CITY_FILTERS = ['All', 'Hyderabad', 'Bengaluru'] as const;
type CityFilter = (typeof CITY_FILTERS)[number];

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
  const [city, setCity] = useState<CityFilter>('All');
  const [query, setQuery] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);

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

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Startup Jobs — Hyderabad & Bengaluru"
        subtitle={`Research session ${RESEARCH_SESSION.date}: ${RESEARCH_SESSION.count} legitimate product companies hiring now for ${RESEARCH_SESSION.roles}. Ranked for a Python + AI profile.`}
      />

      <Card className="flex items-start gap-3 border-amber-200 bg-amber-50/60 p-4 dark:border-amber-500/30 dark:bg-amber-500/10">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-300">
          <Info className="h-4 w-4" />
        </span>
        <div className="text-sm text-amber-900 dark:text-amber-100">
          <b>How to read this table.</b> Every field marked <i>Not verified</i> could not be
          confirmed from a public source — do not treat it as fact. Salaries tagged
          <i> estimate</i> come from job aggregators, not employers. Re-open the job link before
          applying to confirm the role is still live. Click any row for office, leadership, posting
          date, careers page and research notes.
        </div>
      </Card>

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
