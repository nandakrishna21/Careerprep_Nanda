import { FormEvent, useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import {
  Bookmark,
  BookmarkCheck,
  Building2,
  CalendarClock,
  ExternalLink,
  MapPin,
  Search as SearchIcon,
  Wallet,
} from 'lucide-react';
import api, { errorMessage, get, post, del } from '../../lib/api';
import type { Job, JobFacets, Paged } from '../../lib/types';
import { Badge, Button, Card, EmptyState, Select, Spinner } from '../../components/ui';
import { titleCase } from '../../components/helpers';

type Tab = 'all' | 'government' | 'it' | 'saved';

const TABS: { key: Tab; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'government', label: 'Government' },
  { key: 'it', label: 'IT' },
  { key: 'saved', label: 'Saved' },
];

const STATUS_OPTIONS = ['saved', 'applied', 'interviewing', 'offer', 'rejected'];

function daysLeft(deadline: string | null): { label: string; tone: string } | null {
  if (!deadline) return null;
  const end = new Date(`${deadline.slice(0, 10)}T23:59:59`);
  const diff = Math.ceil((end.getTime() - Date.now()) / 86400000);
  if (Number.isNaN(diff)) return null;
  if (diff < 0) return { label: 'Closed', tone: 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400' };
  if (diff <= 3)
    return { label: `${diff}d left`, tone: 'bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300' };
  if (diff <= 10)
    return { label: `${diff}d left`, tone: 'bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300' };
  return { label: `${diff}d left`, tone: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300' };
}

export default function Jobs() {
  const [tab, setTab] = useState<Tab>('all');
  const [category, setCategory] = useState('');
  const [role, setRole] = useState('');
  const [location, setLocation] = useState('');
  const [draft, setDraft] = useState('');
  const [q, setQ] = useState('');
  const [page, setPage] = useState(1);
  const [items, setItems] = useState<Job[]>([]);
  const [total, setTotal] = useState(0);
  const [pageSize, setPageSize] = useState(12);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [facets, setFacets] = useState<JobFacets | null>(null);

  // Filter options come from the board itself so the UI never offers a value that
  // returns zero rows (seed values and crawled values differ).
  useEffect(() => {
    let alive = true;
    get<JobFacets>('/jobs/facets')
      .then((data) => {
        if (alive) setFacets(data ?? null);
      })
      .catch(() => undefined);
    return () => {
      alive = false;
    };
  }, []);

  const facetKey: 'all' | 'government' | 'it' = tab === 'saved' ? 'all' : tab;
  const group = facets?.[facetKey];
  const categoryOptions = (group?.categories ?? []).map((option) => option.value);
  const roleOptions = group?.roles ?? [];
  const locationOptions = group?.locations ?? [];
  const hasFilters = Boolean(category || role || location);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        if (tab === 'saved') {
          const data = await get<unknown>('/jobs/saved');
          if (!alive) return;
          const list = Array.isArray(data)
            ? (data as Job[])
            : ((data as { items?: Job[] }).items ?? []);
          setItems(list);
          setTotal(list.length);
          setPageSize(list.length || 12);
        } else {
          const params: Record<string, unknown> = { page, page_size: 12 };
          if (tab !== 'all') params.type = tab;
          if (category) params.category = category;
          if (role) params.role = role;
          if (location) params.location = location;
          if (q.trim()) params.q = q.trim();
          const res = await get<Paged<Job>>('/jobs', params);
          if (!alive) return;
          setItems(res.items ?? []);
          setTotal(res.total ?? 0);
          setPageSize(res.page_size || 12);
        }
      } catch (err) {
        if (alive) {
          toast.error(errorMessage(err));
          setItems([]);
          setTotal(0);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [tab, category, role, location, q, page]);

  const switchTab = (next: Tab) => {
    setTab(next);
    setCategory('');
    setRole('');
    setLocation('');
    setPage(1);
  };

  const clearFilters = () => {
    setCategory('');
    setRole('');
    setLocation('');
    setPage(1);
  };

  const search = (e: FormEvent) => {
    e.preventDefault();
    setPage(1);
    setQ(draft);
  };

  const toggleSave = async (job: Job) => {
    setBusyId(job.id);
    try {
      if (job.is_saved) {
        await del(`/jobs/${job.id}/save`);
        setItems((prev) => prev.map((j) => (j.id === job.id ? { ...j, is_saved: false, save_status: undefined } : j)));
        toast.success('Removed from saved jobs');
      } else {
        await post(`/jobs/${job.id}/save`);
        setItems((prev) =>
          prev.map((j) => (j.id === job.id ? { ...j, is_saved: true, save_status: 'saved' } : j))
        );
        toast.success('Job saved');
      }
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  const changeStatus = async (job: Job, status: string) => {
    setBusyId(job.id);
    try {
      await api.patch(`/jobs/${job.id}/save`, { status });
      setItems((prev) => prev.map((j) => (j.id === job.id ? { ...j, save_status: status } : j)));
      toast.success(`Marked as ${status}`);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  const totalPages = Math.max(1, Math.ceil(total / Math.max(1, pageSize)));

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Jobs & Opportunities</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Government notifications, exams and IT openings — save and track your applications.
          </p>
        </div>
        <div className="inline-flex w-fit flex-wrap rounded-xl border border-slate-200 bg-white p-1 dark:border-slate-700 dark:bg-slate-900">
          {TABS.map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => switchTab(t.key)}
              className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
                tab === t.key
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <form onSubmit={search} className="relative flex-1">
          <SearchIcon className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Search jobs by title, company or location…"
            className="input pl-10"
          />
        </form>
      </div>

      {tab !== 'saved' &&
        (categoryOptions.length > 0 || roleOptions.length > 0 || locationOptions.length > 0) && (
          <div className="flex flex-wrap items-center gap-3">
            {categoryOptions.length > 0 && (
              <div className="w-full sm:w-48">
                <Select
                  value={category}
                  onChange={(e) => {
                    setCategory(e.target.value);
                    setPage(1);
                  }}
                  aria-label="Category"
                >
                  <option value="">All categories</option>
                  {categoryOptions.map((c) => (
                    <option key={c} value={c}>
                      {titleCase(c)}
                    </option>
                  ))}
                </Select>
              </div>
            )}

            {roleOptions.length > 0 && (
              <div className="w-full sm:w-64">
                <Select
                  value={role}
                  onChange={(e) => {
                    setRole(e.target.value);
                    setPage(1);
                  }}
                  aria-label="Role"
                >
                  <option value="">All roles</option>
                  {roleOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label} ({option.count})
                    </option>
                  ))}
                </Select>
              </div>
            )}

            {locationOptions.length > 0 && (
              <div className="w-full sm:w-56">
                <Select
                  value={location}
                  onChange={(e) => {
                    setLocation(e.target.value);
                    setPage(1);
                  }}
                  aria-label="Location"
                >
                  <option value="">All locations</option>
                  {locationOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label} ({option.count})
                    </option>
                  ))}
                </Select>
              </div>
            )}

            {hasFilters && (
              <Button variant="outline" onClick={clearFilters}>
                Clear filters
              </Button>
            )}
          </div>
        )}

      {loading ? (
        <Spinner />
      ) : items.length === 0 ? (
        <EmptyState
          title={tab === 'saved' ? 'No saved jobs yet' : 'No jobs found'}
          description={
            tab === 'saved'
              ? 'Save jobs from the board to track your applications here.'
              : 'Try another tab, role, location or search term.'
          }
          action={
            tab === 'saved' ? (
              <Button onClick={() => switchTab('all')}>Browse all jobs</Button>
            ) : undefined
          }
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {items.map((job) => {
            const days = daysLeft(job.deadline);
            return (
              <Card key={job.id} className="flex flex-col gap-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0">
                    <h2 className="line-clamp-2 font-bold leading-snug text-slate-900 dark:text-white">
                      {job.title}
                    </h2>
                    <p className="mt-1 flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400">
                      <Building2 className="h-3.5 w-3.5 shrink-0" />
                      {job.company}
                    </p>
                  </div>
                  {days && (
                    <span
                      className={`shrink-0 inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-bold ${days.tone}`}
                    >
                      <CalendarClock className="h-3 w-3" />
                      {days.label}
                    </span>
                  )}
                </div>

                <div className="flex flex-wrap gap-1.5">
                  <Badge color={job.type === 'government' ? 'violet' : 'brand'}>
                    {job.type === 'government' ? 'Government' : 'IT'}
                  </Badge>
                  <Badge color="slate">{titleCase(job.category)}</Badge>
                  {job.role && <Badge color="brand">{job.role}</Badge>}
                  {job.is_saved && <Badge color="green">{titleCase(job.save_status ?? 'saved')}</Badge>}
                </div>

                <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
                  {job.location && (
                    <span className="inline-flex items-center gap-1">
                      <MapPin className="h-3.5 w-3.5" /> {job.location}
                    </span>
                  )}
                  {job.salary && (
                    <span className="inline-flex items-center gap-1">
                      <Wallet className="h-3.5 w-3.5" /> {job.salary}
                    </span>
                  )}
                </div>

                <p className="line-clamp-2 text-sm text-slate-500 dark:text-slate-400">{job.description}</p>

                <div className="mt-auto space-y-2 pt-1">
                  <div className="flex flex-wrap gap-2">
                    <a
                      href={job.apply_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
                    >
                      Apply <ExternalLink className="h-4 w-4" />
                    </a>
                    <Button
                      variant="outline"
                      onClick={() => void toggleSave(job)}
                      loading={busyId === job.id}
                      aria-label={job.is_saved ? 'Unsave job' : 'Save job'}
                    >
                      {job.is_saved ? <BookmarkCheck className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
                      {job.is_saved ? 'Saved' : 'Save'}
                    </Button>
                  </div>

                  {job.is_saved && (
                    <div className="flex items-center gap-2">
                      <label className="text-xs font-semibold text-slate-400" htmlFor={`status-${job.id}`}>
                        Status
                      </label>
                      <select
                        id={`status-${job.id}`}
                        value={job.save_status ?? 'saved'}
                        disabled={busyId === job.id}
                        onChange={(e) => void changeStatus(job, e.target.value)}
                        className="input py-1.5 text-xs"
                      >
                        {STATUS_OPTIONS.map((s) => (
                          <option key={s} value={s}>
                            {titleCase(s)}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {tab !== 'saved' && !loading && totalPages > 1 && (
        <div className="flex items-center justify-center gap-3">
          <Button variant="outline" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>
            Previous
          </Button>
          <span className="text-sm font-semibold text-slate-500 dark:text-slate-400">
            Page {page} of {totalPages} · {total} jobs
          </span>
          <Button variant="outline" disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)}>
            Next
          </Button>
        </div>
      )}
    </div>
  );
}
