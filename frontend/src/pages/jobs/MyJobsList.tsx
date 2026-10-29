import { useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import {
  Award,
  BookOpen,
  Briefcase,
  CalendarDays,
  CheckCircle2,
  ClipboardList,
  ExternalLink,
  FileText,
  Globe,
  Map,
  Plus,
  RefreshCw,
  Search,
  Target,
  Trash2,
  X,
  Youtube,
} from 'lucide-react';
import { errorMessage, get, post, put, del } from '../../lib/api';
import type { MyJob, MyJobTemplateCard } from '../../lib/types';
import { Badge, Button, Card, EmptyState, Input, Spinner, Textarea } from '../../components/ui';
import { PageHeader } from '../../components/SectionHeader';
import { formatDate } from '../../components/helpers';

type TabKey = 'overview' | 'syllabus' | 'pattern' | 'strategy' | 'plan' | 'resources' | 'notes';
type StatusFilter = 'all' | MyJob['status'];

const STATUS_ORDER: MyJob['status'][] = [
  'wishlist',
  'applied',
  'preparing',
  'exam',
  'interview',
  'selected',
  'rejected',
];

const STATUS_COLOR: Record<MyJob['status'], 'brand' | 'green' | 'amber' | 'rose' | 'slate' | 'violet'> = {
  wishlist: 'slate',
  applied: 'brand',
  preparing: 'amber',
  exam: 'violet',
  interview: 'amber',
  selected: 'green',
  rejected: 'rose',
};

const TABS: { key: TabKey; label: string; icon: typeof BookOpen }[] = [
  { key: 'overview', label: 'Overview', icon: Briefcase },
  { key: 'syllabus', label: 'Syllabus', icon: BookOpen },
  { key: 'pattern', label: 'Exam Pattern', icon: FileText },
  { key: 'strategy', label: 'Strategy', icon: Target },
  { key: 'plan', label: 'Preparation', icon: Map },
  { key: 'resources', label: 'Free Resources', icon: Youtube },
  { key: 'notes', label: 'My Notes', icon: ClipboardList },
];

export default function MyJobsList() {
  const [items, setItems] = useState<MyJob[]>([]);
  const [templates, setTemplates] = useState<MyJobTemplateCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [tab, setTab] = useState<TabKey>('overview');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [query, setQuery] = useState('');
  const [busyKey, setBusyKey] = useState<string | null>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [editing, setEditing] = useState<MyJob | null>(null);
  const [deleting, setDeleting] = useState<MyJob | null>(null);
  const [syncing, setSyncing] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [list, tpl] = await Promise.all([
        get<{ items: MyJob[] }>(`/my-jobs`),
        get<{ items: MyJobTemplateCard[] }>(`/my-jobs/templates`).catch(() => ({ items: [] })),
      ]);
      setItems(list.items ?? []);
      setTemplates(tpl.items ?? []);
      setSelectedId((prev) => {
        if (prev && (list.items ?? []).some((j) => j.id === prev)) return prev;
        return (list.items ?? [])[0]?.id ?? null;
      });
    } catch (err) {
      toast.error(errorMessage(err));
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const selected = useMemo(
    () => items.find((j) => j.id === selectedId) ?? null,
    [items, selectedId],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return items.filter((j) => {
      if (statusFilter !== 'all' && j.status !== statusFilter) return false;
      if (!q) return true;
      return [j.title, j.organization, j.role_name].join(' ').toLowerCase().includes(q);
    });
  }, [items, statusFilter, query]);

  const stats = useMemo(() => {
    const count = (s: MyJob['status']) => items.filter((j) => j.status === s).length;
    return { total: items.length, applied: count('applied'), preparing: count('preparing'), interview: count('interview') + count('exam') };
  }, [items]);

  const addedKeys = useMemo(() => new Set(items.map((j) => j.template_key).filter(Boolean)), [items]);

  const addFromTemplate = async (key: string) => {
    setBusyKey(key);
    try {
      const job = await post<MyJob>(`/my-jobs/from-template/${key}`, {});
      setItems((prev) => (prev.some((j) => j.id === job.id) ? prev.map((j) => (j.id === job.id ? job : j)) : [job, ...prev]));
      setSelectedId(job.id);
      setTab('overview');
      toast.success('Added to My Applications');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyKey(null);
    }
  };

  const changeStatus = async (job: MyJob, status: MyJob['status']) => {
    try {
      const updated = await put<MyJob>(`/my-jobs/${job.id}`, { status });
      setItems((prev) => prev.map((j) => (j.id === job.id ? updated : j)));
      toast.success(`Marked as ${status}`);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const syncLatest = async () => {
    if (!selected?.template_key || syncing) return;
    setSyncing(true);
    try {
      const updated = await post<MyJob>(`/my-jobs/${selected.id}/refresh-template`, {});
      setItems((prev) => prev.map((j) => (j.id === updated.id ? updated : j)));
      toast.success('Synced latest syllabus, plan and free resources');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSyncing(false);
    }
  };

  const removeJob = async () => {
    if (!deleting) return;
    try {
      await del(`/my-jobs/${deleting.id}`);
      setItems((prev) => prev.filter((j) => j.id !== deleting.id));
      if (selectedId === deleting.id) setSelectedId(null);
      toast.success('Removed from My Applications');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="My Applications"
        subtitle="Every job you apply for — tracked with its syllabus, exam pattern, strategy, preparation plan and free resources in one place."
        actions={
          <Button onClick={() => setShowAdd(true)}>
            <Plus className="h-4 w-4" /> Add job
          </Button>
        }
      />

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {[
          { label: 'Tracked', value: stats.total, icon: Briefcase },
          { label: 'Applied', value: stats.applied, icon: CheckCircle2 },
          { label: 'Preparing', value: stats.preparing, icon: BookOpen },
          { label: 'Exam / Interview', value: stats.interview, icon: Award },
        ].map((s) => (
          <Card key={s.label} className="flex items-center gap-3 p-4">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
              <s.icon className="h-5 w-5" />
            </span>
            <span>
              <span className="block text-xl font-bold text-slate-900 dark:text-white">{s.value}</span>
              <span className="block text-xs text-slate-500">{s.label}</span>
            </span>
          </Card>
        ))}
      </div>

      {/* Starter templates */}
      {templates.length > 0 && (
        <Card className="space-y-3">
          <div>
            <h2 className="font-bold text-slate-900 dark:text-white">Starter pack — your applied roles</h2>
            <p className="text-sm text-slate-500">One-click add with full syllabus, strategy, preparation plan and free YouTube + practice links.</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {templates.map((t) => {
              const added = addedKeys.has(t.template_key);
              return (
                <div key={t.template_key} className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                  <p className="font-bold text-slate-900 dark:text-white">{t.title}</p>
                  <p className="mt-0.5 text-xs text-slate-500">{t.organization} · {t.role_name}</p>
                  <p className="mt-1 text-xs text-slate-400">{t.sections} syllabus sections · {t.phases} prep phases</p>
                  <Button
                    variant={added ? 'outline' : 'primary'}
                    className="mt-3 w-full"
                    loading={busyKey === t.template_key}
                    onClick={() => void addFromTemplate(t.template_key)}
                  >
                    {added ? <CheckCircle2 className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
                    {added ? 'Added — open it' : 'Add to My Applications'}
                  </Button>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {loading ? (
        <Spinner />
      ) : items.length === 0 ? (
        <EmptyState
          title="No jobs tracked yet"
          description="Add the roles you have applied for — start with the two starter templates above, or add a custom job."
          action={<Button onClick={() => setShowAdd(true)}><Plus className="h-4 w-4" /> Add your first job</Button>}
        />
      ) : (
        <div className="grid gap-4 lg:grid-cols-[340px_1fr]">
          {/* List */}
          <div className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search tracked jobs…" className="pl-9" />
            </div>
            <div className="flex flex-wrap gap-1.5">
              {(['all', ...STATUS_ORDER] as StatusFilter[]).map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setStatusFilter(s)}
                  className={`rounded-full px-3 py-1 text-xs font-bold transition ${statusFilter === s ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300'}`}
                >
                  {s === 'all' ? 'All' : s}
                </button>
              ))}
            </div>
            <div className="space-y-2">
              {filtered.map((j) => (
                <button
                  key={j.id}
                  type="button"
                  onClick={() => { setSelectedId(j.id); setTab('overview'); }}
                  className={`w-full rounded-xl border p-3 text-left transition ${selectedId === j.id ? 'border-brand-400 bg-brand-50/60 dark:border-brand-500/50 dark:bg-brand-500/10' : 'border-slate-200 bg-white hover:border-slate-300 dark:border-slate-700 dark:bg-slate-900'}`}
                >
                  <span className="flex items-center justify-between gap-2">
                    <Badge color={STATUS_COLOR[j.status]}>{j.status}</Badge>
                    {j.exam_date && <span className="text-[11px] text-slate-400">Exam {formatDate(j.exam_date)}</span>}
                  </span>
                  <span className="mt-1.5 block font-bold leading-snug text-slate-900 dark:text-white">{j.title}</span>
                  <span className="mt-0.5 block truncate text-xs text-slate-500">{j.organization}</span>
                </button>
              ))}
              {filtered.length === 0 && <p className="py-6 text-center text-sm text-slate-400">No jobs match.</p>}
            </div>
          </div>

          {/* Detail */}
          {selected ? (
            <div className="min-w-0 space-y-4">
              <Card>
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge color={STATUS_COLOR[selected.status]}>{selected.status}</Badge>
                      {selected.exam_date && <span className="inline-flex items-center gap-1 text-xs text-slate-400"><CalendarDays className="h-3.5 w-3.5" /> Exam {formatDate(selected.exam_date)}</span>}
                    </div>
                    <h2 className="mt-2 text-xl font-bold text-slate-900 dark:text-white">{selected.title}</h2>
                    <p className="mt-0.5 text-sm text-slate-500">{selected.organization}{selected.role_name ? ` · ${selected.role_name}` : ''}</p>
                  </div>
                  <div className="flex gap-2">
                    {selected.template_key && (
                      <Button variant="outline" onClick={() => void syncLatest()} loading={syncing} title="Pull the latest syllabus, plan and free resources">
                        <RefreshCw className="h-4 w-4" /> Sync latest
                      </Button>
                    )}
                    <Button variant="outline" onClick={() => setEditing(selected)}>Edit</Button>
                    <Button variant="outline" onClick={() => setDeleting(selected)} aria-label="Remove job"><Trash2 className="h-4 w-4" /></Button>
                  </div>
                </div>
                <div className="mt-3 flex flex-wrap items-center gap-2">
                  <label className="text-xs font-bold text-slate-400" htmlFor="myjob-status">Status</label>
                  <select id="myjob-status" value={selected.status} onChange={(e) => void changeStatus(selected, e.target.value as MyJob['status'])} className="input w-auto py-1.5 text-sm">
                    {STATUS_ORDER.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                  {(selected.notification_link || selected.apply_link) && (
                    <span className="ml-auto flex gap-2">
                      {selected.notification_link && <a href={selected.notification_link} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-xs font-bold text-brand-600 hover:underline">Notification <ExternalLink className="h-3 w-3" /></a>}
                      {selected.apply_link && <a href={selected.apply_link} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-xs font-bold text-brand-600 hover:underline">Apply <ExternalLink className="h-3 w-3" /></a>}
                    </span>
                  )}
                </div>
              </Card>

              <div className="flex flex-wrap gap-2" role="tablist" aria-label="Job sections">
                {TABS.map((t) => (
                  <button key={t.key} type="button" role="tab" aria-selected={tab === t.key} onClick={() => setTab(t.key)}
                    className={`inline-flex items-center gap-1.5 rounded-xl px-3.5 py-2 text-sm font-semibold transition ${tab === t.key ? 'bg-brand-600 text-white' : 'border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300'}`}>
                    <t.icon className="h-4 w-4" /> {t.label}
                  </button>
                ))}
              </div>

              <Card>
                {tab === 'overview' && <OverviewTab job={selected} />}
                {tab === 'syllabus' && <SyllabusTab job={selected} />}
                {tab === 'pattern' && <PatternTab job={selected} />}
                {tab === 'strategy' && <StrategyTab job={selected} />}
                {tab === 'plan' && <PlanTab job={selected} />}
                {tab === 'resources' && <ResourcesTab job={selected} />}
                {tab === 'notes' && <NotesTab job={selected} onSaved={(u) => setItems((prev) => prev.map((j) => (j.id === u.id ? u : j)))} />}
              </Card>
            </div>
          ) : (
            <EmptyState title="Select a job" description="Pick a tracked job on the left to see its syllabus and plan." />
          )}
        </div>
      )}

      {showAdd && <AddModal onClose={() => setShowAdd(false)} onCreated={(j) => { setItems((prev) => [j, ...prev]); setSelectedId(j.id); setShowAdd(false); }} />}
      {editing && <EditModal job={editing} onClose={() => setEditing(null)} onSaved={(u) => { setItems((prev) => prev.map((j) => (j.id === u.id ? u : j))); setEditing(null); }} />}
      {deleting && (
        <ModalShell title="Remove job?" onClose={() => setDeleting(null)}>
          <p className="text-sm text-slate-500">Remove <b>{deleting.title}</b> from My Applications? Its syllabus and notes will be deleted.</p>
          <div className="mt-4 flex justify-end gap-2">
            <Button variant="outline" onClick={() => setDeleting(null)}>Cancel</Button>
            <Button variant="danger" onClick={() => void removeJob()}>Remove</Button>
          </div>
        </ModalShell>
      )}
    </div>
  );
}

function OverviewTab({ job }: { job: MyJob }) {
  const rows: [string, string][] = [
    ['Organization', job.organization || '—'],
    ['Role', job.role_name || '—'],
    ['Status', job.status],
    ['Applied', job.applied_date ? formatDate(job.applied_date) : '—'],
    ['Exam', job.exam_date ? formatDate(job.exam_date) : '—'],
    ['Deadline', job.deadline ? formatDate(job.deadline) : '—'],
  ];
  return (
    <div className="space-y-4">
      <dl className="grid gap-2 sm:grid-cols-2">
        {rows.map(([k, v]) => (
          <div key={k} className="rounded-xl bg-slate-50 p-3 dark:bg-slate-800/60">
            <dt className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{k}</dt>
            <dd className="mt-0.5 text-sm font-semibold text-slate-800 dark:text-slate-100">{v}</dd>
          </div>
        ))}
      </dl>
      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { label: `${job.syllabus.length} syllabus sections`, icon: BookOpen },
          { label: `${job.exam_pattern.length} exam rows`, icon: FileText },
          { label: `${job.preparation_plan.length} prep phases`, icon: Map },
          { label: `${(job.resources ?? []).length} resource groups`, icon: Youtube },
        ].map((s) => (
          <div key={s.label} className="flex items-center gap-2 rounded-xl border border-slate-200 p-3 text-sm font-semibold text-slate-600 dark:border-slate-700 dark:text-slate-300">
            <s.icon className="h-4 w-4 text-brand-500" /> {s.label}
          </div>
        ))}
      </div>
    </div>
  );
}

function SyllabusTab({ job }: { job: MyJob }) {
  if (!job.syllabus.length) return <p className="text-sm text-slate-400">No syllabus added yet — edit the job to add one.</p>;
  return (
    <div className="space-y-4">
      {job.syllabus.map((s, i) => (
        <div key={i}>
          <h3 className="font-bold text-slate-900 dark:text-white">{i + 1}. {s.section}</h3>
          <ul className="mt-1.5 grid gap-1.5 sm:grid-cols-2">
            {(s.topics ?? []).map((t, j) => (
              <li key={j} className="flex items-start gap-2 rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600 dark:bg-slate-800/60 dark:text-slate-300">
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" /> {t}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

function PatternTab({ job }: { job: MyJob }) {
  if (!job.exam_pattern.length) return <p className="text-sm text-slate-400">No exam pattern added yet.</p>;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[560px] text-sm">
        <thead>
          <tr className="text-left text-[11px] uppercase tracking-wider text-slate-400">
            <th className="pb-2 pr-3">Section</th>
            <th className="pb-2 pr-3">Qs</th>
            <th className="pb-2 pr-3">Marks</th>
            <th className="pb-2 pr-3">Time</th>
            <th className="pb-2">Note</th>
          </tr>
        </thead>
        <tbody>
          {job.exam_pattern.map((r, i) => (
            <tr key={i} className="border-t border-slate-100 dark:border-slate-800">
              <td className="py-2.5 pr-3 font-semibold text-slate-800 dark:text-slate-100">{r.section}</td>
              <td className="py-2.5 pr-3 text-slate-500">{r.questions ?? '—'}</td>
              <td className="py-2.5 pr-3 text-slate-500">{r.marks ?? '—'}</td>
              <td className="py-2.5 pr-3 text-slate-500">{r.duration ?? '—'}{r.medium ? ` · ${r.medium}` : ''}</td>
              <td className="py-2.5 text-xs text-slate-400">{r.note ?? ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function StrategyTab({ job }: { job: MyJob }) {
  if (!job.strategy) return <p className="text-sm text-slate-400">No strategy added yet.</p>;
  return <p className="whitespace-pre-line text-sm leading-7 text-slate-600 dark:text-slate-300">{job.strategy}</p>;
}

function PlanTab({ job }: { job: MyJob }) {
  if (!job.preparation_plan.length) return <p className="text-sm text-slate-400">No preparation plan added yet.</p>;
  return (
    <div className="space-y-4">
      {job.preparation_plan.map((p, i) => (
        <div key={i} className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
          <h3 className="font-bold text-slate-900 dark:text-white">{p.phase}</h3>
          {p.weeks && <p className="text-xs text-slate-400">Weeks: {p.weeks}</p>}
          {(p.focus?.length ?? 0) > 0 && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {(p.focus ?? []).map((f, j) => <Badge key={j} color="brand">{f}</Badge>)}
            </div>
          )}
          {(p.tasks?.length ?? 0) > 0 && (
            <ul className="mt-2 space-y-1.5">
              {(p.tasks ?? []).map((t, j) => (
                <li key={j} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-300">
                  <Target className="mt-0.5 h-4 w-4 shrink-0 text-brand-500" /> {t}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

function ResourcesTab({ job }: { job: MyJob }) {
  const groups = job.resources ?? [];
  if (!groups.length)
    return (
      <p className="text-sm text-slate-400">
        No free resources yet. {job.template_key ? 'Tap “Sync latest” above to pull the newest YouTube channels and practice sites.' : 'Free YouTube and practice links appear here for template jobs.'}
      </p>
    );
  return (
    <div className="space-y-5">
      <p className="text-xs text-slate-400">100% free — YouTube classes and practice sites mapped to each syllabus subject. All links open in a new tab.</p>
      {groups.map((g, i) => (
        <div key={i}>
          <h3 className="font-bold text-slate-900 dark:text-white">{i + 1}. {g.subject}</h3>
          {(g.youtube?.length ?? 0) > 0 && (
            <div className="mt-2">
              <p className="mb-1.5 flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-rose-500">
                <Youtube className="h-3.5 w-3.5" /> YouTube — free classes
              </p>
              <div className="grid gap-2 sm:grid-cols-2">
                {(g.youtube ?? []).map((r, j) => (
                  <a key={j} href={r.url} target="_blank" rel="noopener noreferrer"
                    className="group flex items-start gap-3 rounded-xl border border-slate-200 p-3 transition hover:-translate-y-0.5 hover:border-rose-300 dark:border-slate-700 dark:hover:border-rose-500/50">
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-rose-600 text-white">
                      <Youtube className="h-4 w-4" />
                    </span>
                    <span className="min-w-0">
                      <span className="block truncate font-bold text-slate-900 group-hover:text-rose-600 dark:text-white">{r.title}</span>
                      {r.note && <span className="mt-0.5 block text-xs leading-snug text-slate-500 dark:text-slate-400">{r.note}</span>}
                      <span className="mt-1 inline-flex items-center gap-1 text-[11px] font-bold text-rose-600">Watch free <ExternalLink className="h-3 w-3" /></span>
                    </span>
                  </a>
                ))}
              </div>
            </div>
          )}
          {(g.websites?.length ?? 0) > 0 && (
            <div className="mt-2">
              <p className="mb-1.5 flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-brand-500">
                <Globe className="h-3.5 w-3.5" /> Websites — free practice
              </p>
              <div className="grid gap-2 sm:grid-cols-2">
                {(g.websites ?? []).map((r, j) => (
                  <a key={j} href={r.url} target="_blank" rel="noopener noreferrer"
                    className="group flex items-start gap-3 rounded-xl border border-slate-200 p-3 transition hover:-translate-y-0.5 hover:border-brand-300 dark:border-slate-700 dark:hover:border-brand-500/50">
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                      <Globe className="h-4 w-4" />
                    </span>
                    <span className="min-w-0">
                      <span className="block truncate font-bold text-slate-900 group-hover:text-brand-600 dark:text-white">{r.title}</span>
                      {r.note && <span className="mt-0.5 block text-xs leading-snug text-slate-500 dark:text-slate-400">{r.note}</span>}
                      <span className="mt-1 inline-flex items-center gap-1 text-[11px] font-bold text-brand-600">Practise free <ExternalLink className="h-3 w-3" /></span>
                    </span>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function NotesTab({ job, onSaved }: { job: MyJob; onSaved: (u: MyJob) => void }) {
  const [notes, setNotes] = useState(job.notes ?? '');
  const [saving, setSaving] = useState(false);
  useEffect(() => setNotes(job.notes ?? ''), [job.id, job.notes]);
  const save = async () => {
    setSaving(true);
    try {
      const updated = await put<MyJob>(`/my-jobs/${job.id}`, { notes });
      onSaved(updated);
      toast.success('Notes saved');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };
  return (
    <div className="space-y-3">
      <Textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Application ID, roll number, centre, revision reminders…" rows={8} />
      <Button onClick={() => void save()} loading={saving}>Save notes</Button>
    </div>
  );
}

function ModalShell({ title, children, onClose }: { title: string; children: React.ReactNode; onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" onClick={onClose}>
      <div className="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white p-6 shadow-xl dark:bg-slate-900" onClick={(e) => e.stopPropagation()}>
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">{title}</h3>
          <button onClick={onClose} className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800" aria-label="Close"><X className="h-5 w-5" /></button>
        </div>
        {children}
      </div>
    </div>
  );
}

function AddModal({ onClose, onCreated }: { onClose: () => void; onCreated: (j: MyJob) => void }) {
  const [title, setTitle] = useState('');
  const [organization, setOrganization] = useState('');
  const [roleName, setRoleName] = useState('');
  const [status, setStatus] = useState<MyJob['status']>('applied');
  const [saving, setSaving] = useState(false);
  const submit = async () => {
    if (!title.trim()) { toast.error('Title is required'); return; }
    setSaving(true);
    try {
      const job = await post<MyJob>('/my-jobs', { title: title.trim(), organization: organization.trim(), role_name: roleName.trim(), status });
      toast.success('Added to My Applications');
      onCreated(job);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };
  return (
    <ModalShell title="Add job" onClose={onClose}>
      <div className="space-y-3">
        <div><label className="label">Title *</label><Input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. UIICL Administrative Officer (Scale I)" /></div>
        <div className="grid gap-3 sm:grid-cols-2">
          <div><label className="label">Organization</label><Input value={organization} onChange={(e) => setOrganization(e.target.value)} placeholder="UIICL" /></div>
          <div><label className="label">Role</label><Input value={roleName} onChange={(e) => setRoleName(e.target.value)} placeholder="AO Scale I" /></div>
        </div>
        <div><label className="label">Status</label>
          <select value={status} onChange={(e) => setStatus(e.target.value as MyJob['status'])} className="input">
            {STATUS_ORDER.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div className="flex justify-end gap-2 pt-1">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={() => void submit()} loading={saving}>Add</Button>
        </div>
      </div>
    </ModalShell>
  );
}

function EditModal({ job, onClose, onSaved }: { job: MyJob; onClose: () => void; onSaved: (u: MyJob) => void }) {
  const [form, setForm] = useState({ title: job.title, organization: job.organization ?? '', role_name: job.role_name ?? '', status: job.status, applied_date: job.applied_date ?? '', exam_date: job.exam_date ?? '', deadline: job.deadline ?? '', notification_link: job.notification_link ?? '', apply_link: job.apply_link ?? '', notes: job.notes ?? '' });
  const [saving, setSaving] = useState(false);
  const set = (k: keyof typeof form, v: string) => setForm((p) => ({ ...p, [k]: v }));
  const submit = async () => {
    if (!form.title.trim()) { toast.error('Title is required'); return; }
    setSaving(true);
    try {
      const payload: Record<string, unknown> = { title: form.title.trim(), organization: form.organization.trim(), role_name: form.role_name.trim(), status: form.status, notification_link: form.notification_link.trim(), apply_link: form.apply_link.trim(), notes: form.notes };
      for (const k of ['applied_date', 'exam_date', 'deadline'] as const) payload[k] = form[k] ? form[k].slice(0, 10) : null;
      const updated = await put<MyJob>(`/my-jobs/${job.id}`, payload);
      toast.success('Saved');
      onSaved(updated);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };
  return (
    <ModalShell title="Edit job" onClose={onClose}>
      <div className="space-y-3">
        <div><label className="label">Title *</label><Input value={form.title} onChange={(e) => set('title', e.target.value)} /></div>
        <div className="grid gap-3 sm:grid-cols-2">
          <div><label className="label">Organization</label><Input value={form.organization} onChange={(e) => set('organization', e.target.value)} /></div>
          <div><label className="label">Role</label><Input value={form.role_name} onChange={(e) => set('role_name', e.target.value)} /></div>
        </div>
        <div className="grid gap-3 sm:grid-cols-3">
          <div><label className="label">Applied</label><Input type="date" value={form.applied_date} onChange={(e) => set('applied_date', e.target.value)} /></div>
          <div><label className="label">Exam</label><Input type="date" value={form.exam_date} onChange={(e) => set('exam_date', e.target.value)} /></div>
          <div><label className="label">Deadline</label><Input type="date" value={form.deadline} onChange={(e) => set('deadline', e.target.value)} /></div>
        </div>
        <div><label className="label">Status</label>
          <select value={form.status} onChange={(e) => set('status', e.target.value)} className="input">
            {STATUS_ORDER.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div><label className="label">Notification link</label><Input value={form.notification_link} onChange={(e) => set('notification_link', e.target.value)} placeholder="https://…" /></div>
        <div><label className="label">Apply link</label><Input value={form.apply_link} onChange={(e) => set('apply_link', e.target.value)} placeholder="https://…" /></div>
        <div className="flex justify-end gap-2 pt-1">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={() => void submit()} loading={saving}>Save</Button>
        </div>
      </div>
    </ModalShell>
  );
}
