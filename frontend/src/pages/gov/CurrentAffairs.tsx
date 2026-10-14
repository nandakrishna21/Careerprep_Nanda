import { useCallback, useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowRight, CalendarDays, Newspaper, RefreshCw } from 'lucide-react';
import { errorMessage, get, post } from '../../lib/api';
import type { CurrentAffair } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { formatDate, toItems } from '../../components/helpers';

const PERIODS = [
  { key: 'daily', label: 'Daily' },
  { key: 'weekly', label: 'Weekly' },
  { key: 'monthly', label: 'Monthly' },
] as const;

type Period = (typeof PERIODS)[number]['key'];

interface SyncStatus {
  today: string;
  today_slug: string;
  today_exists: boolean;
  latest_date: string | null;
  counts: Record<string, number>;
  cooldown_remaining_seconds: number;
}

export default function CurrentAffairs() {
  const [period, setPeriod] = useState<Period>('daily');
  const [items, setItems] = useState<CurrentAffair[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState<SyncStatus | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const loadList = useCallback(async (p: Period, signal?: AbortSignal) => {
    const data = await get<unknown>('/current-affairs', { period: p }, { signal });
    return toItems<CurrentAffair>(data);
  }, []);

  const loadStatus = useCallback(async () => {
    try {
      const s = await get<SyncStatus>('/current-affairs/sync/status');
      setStatus(s);
      return s;
    } catch {
      return null;
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const [list] = await Promise.all([loadList(period, controller.signal), loadStatus()]);
        if (alive) setItems(list);
      } catch (err) {
        if (controller.signal.aborted) return;
        if (alive) {
          toast.error(errorMessage(err));
          setItems([]);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
      controller.abort();
    };
  }, [period, loadList, loadStatus]);

  useEffect(
    () => () => {
      if (pollRef.current) clearInterval(pollRef.current);
    },
    [],
  );

  const handleRefresh = async () => {
    if (refreshing) return;
    setRefreshing(true);
    try {
      const res = await post<{ started: boolean; reason?: string }>('/current-affairs/refresh', {});
      if (!res.started) {
        toast(res.reason ?? 'Refresh is on cooldown — try again shortly.');
        setRefreshing(false);
        return;
      }
      toast.success('Fetching today’s headlines — updating shortly…');
      // Poll status until today's edition lands (max ~90s), then reload list.
      let tries = 0;
      if (pollRef.current) clearInterval(pollRef.current);
      pollRef.current = setInterval(async () => {
        tries += 1;
        const s = await loadStatus();
        if (s?.today_exists) {
          if (pollRef.current) clearInterval(pollRef.current);
          try {
            const list = await loadList(period);
            setItems(list);
            toast.success('Current affairs are up to date.');
          } catch {
            /* keep old list */
          }
          setRefreshing(false);
        } else if (tries >= 18) {
          if (pollRef.current) clearInterval(pollRef.current);
          setRefreshing(false);
          toast('Still updating — check back in a minute.');
        }
      }, 5000);
    } catch (err) {
      toast.error(errorMessage(err));
      setRefreshing(false);
    }
  };

  const freshness = status
    ? status.today_exists
      ? `Updated today · ${formatDate(status.today)}`
      : status.latest_date
        ? `Latest: ${formatDate(status.latest_date)} — tap Refresh for today`
        : 'No editions yet'
    : undefined;

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <PageHeader
        title="Current Affairs"
        subtitle="Stay updated with daily, weekly and monthly round-ups — complete with revision notes and AI-powered MCQs."
        actions={
          <button
            type="button"
            onClick={handleRefresh}
            disabled={refreshing}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            {refreshing ? 'Updating…' : 'Refresh today'}
          </button>
        }
      />

      <div className="flex flex-wrap items-center gap-2" role="tablist" aria-label="Period">
        {PERIODS.map((p) => (
          <button
            key={p.key}
            type="button"
            role="tab"
            aria-selected={period === p.key}
            onClick={() => setPeriod(p.key)}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              period === p.key
                ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            {p.label}
          </button>
        ))}
        {freshness && (
          <span className="ml-auto text-xs font-medium text-slate-400">{freshness}</span>
        )}
      </div>

      <SectionHeader
        title={`${PERIODS.find((p) => p.key === period)?.label} updates`}
        subtitle={items ? `${items.length} edition${items.length === 1 ? '' : 's'}` : undefined}
      />

      {loading ? (
        <Spinner />
      ) : items && items.length ? (
        <div className="space-y-4">
          {items.map((ca) => (
            <Card
              key={ca.id}
              className="flex flex-col gap-3 transition hover:-translate-y-0.5 hover:border-brand-300 sm:flex-row sm:items-center sm:justify-between dark:hover:border-brand-500/40"
            >
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge color="brand">{ca.period}</Badge>
                  <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400">
                    <CalendarDays className="h-3.5 w-3.5" /> {formatDate(ca.date)}
                  </span>
                  {status?.today_slug === ca.slug && (
                    <Badge color="green">Today</Badge>
                  )}
                </div>
                <h3 className="mt-2 font-bold text-slate-900 dark:text-white">{ca.title}</h3>
                {ca.summary && (
                  <p className="mt-1 line-clamp-2 text-sm text-slate-500 dark:text-slate-400">
                    {ca.summary}
                  </p>
                )}
              </div>
              <Link
                to={`/gov/current-affairs/${ca.slug}`}
                className="inline-flex shrink-0 items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
              >
                <Newspaper className="h-4 w-4" /> Read <ArrowRight className="h-4 w-4" />
              </Link>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title={`No ${period} current affairs yet`}
          description="Tap Refresh today to fetch the latest headlines from free sources, or try another period."
          action={
            <div className="mt-2 flex items-center justify-center gap-3">
              <button
                type="button"
                onClick={handleRefresh}
                className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
              >
                <RefreshCw className="h-4 w-4" /> Refresh today
              </button>
              <button
                type="button"
                onClick={() => setPeriod(period === 'daily' ? 'weekly' : 'daily')}
                className="text-sm font-semibold text-brand-600 hover:underline dark:text-brand-400"
              >
                Try another period
              </button>
            </div>
          }
        />
      )}
    </div>
  );
}
