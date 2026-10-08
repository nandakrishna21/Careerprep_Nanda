import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowRight, CalendarDays, Newspaper } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
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

export default function CurrentAffairs() {
  const [period, setPeriod] = useState<Period>('daily');
  const [items, setItems] = useState<CurrentAffair[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const data = await get<unknown>('/current-affairs', { period });
        if (alive) setItems(toItems<CurrentAffair>(data));
      } catch (err) {
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
    };
  }, [period]);

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <PageHeader
        title="Current Affairs"
        subtitle="Stay updated with daily, weekly and monthly round-ups â€” complete with revision notes and AI-powered MCQs."
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
          description="New editions are published regularly â€” check back soon or try another period."
          action={
            <button
              type="button"
              onClick={() => setPeriod(period === 'daily' ? 'weekly' : 'daily')}
              className="text-sm font-semibold text-brand-600 hover:underline dark:text-brand-400"
            >
              Try another period
            </button>
          }
        />
      )}
    </div>
  );
}
