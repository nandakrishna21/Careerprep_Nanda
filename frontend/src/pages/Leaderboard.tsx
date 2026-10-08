import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { Flame, Medal } from 'lucide-react';
import { errorMessage, get } from '../lib/api';
import type { LeaderboardEntry } from '../lib/types';
import { EmptyState, Spinner } from '../components/ui';
import { useAuth } from '../stores/auth';

type Period = 'weekly' | 'monthly' | 'all_time';

const TABS: { key: Period; label: string }[] = [
  { key: 'weekly', label: 'Weekly' },
  { key: 'monthly', label: 'Monthly' },
  { key: 'all_time', label: 'All-Time' },
];

const MEDAL_TONES = [
  'bg-amber-400 text-amber-950 ring-amber-300',
  'bg-slate-300 text-slate-700 ring-slate-200 dark:bg-slate-500 dark:text-slate-100 dark:ring-slate-400',
  'bg-orange-400 text-orange-950 ring-orange-300',
];

function initials(name: string): string {
  return (
    name
      .split(' ')
      .map((p) => p[0])
      .filter(Boolean)
      .slice(0, 2)
      .join('')
      .toUpperCase() || '?'
  );
}

const AVATAR_COLORS: Record<string, string> = {
  indigo: 'bg-indigo-500',
  emerald: 'bg-emerald-500',
  rose: 'bg-rose-500',
  amber: 'bg-amber-500',
  violet: 'bg-violet-500',
  sky: 'bg-sky-500',
};

export default function Leaderboard() {
  const { user } = useAuth();
  const [period, setPeriod] = useState<Period>('weekly');
  const [entries, setEntries] = useState<LeaderboardEntry[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const data = await get<unknown>('/leaderboard', { period });
        if (!alive) return;
        const items = Array.isArray(data)
          ? (data as LeaderboardEntry[])
          : ((data as { items?: LeaderboardEntry[] }).items ?? []);
        setEntries(items);
      } catch (err) {
        if (alive) {
          toast.error(errorMessage(err));
          setEntries([]);
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
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Leaderboard</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Top performers ranked by experience points. Climb the board by learning every day.
          </p>
        </div>
        <div className="inline-flex w-fit rounded-xl border border-slate-200 bg-white p-1 dark:border-slate-700 dark:bg-slate-900">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              onClick={() => setPeriod(tab.key)}
              className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
                period === tab.key
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <Spinner />
      ) : !entries || entries.length === 0 ? (
        <EmptyState
          title="No rankings yet"
          description="The leaderboard fills up as learners earn XP from quizzes, mock tests and interviews."
        />
      ) : (
        <>
          <div className="grid gap-4 sm:grid-cols-3">
            {entries.slice(0, 3).map((entry, i) => (
              <div
                key={entry.id}
                className={`card relative flex flex-col items-center gap-2 p-5 text-center ${
                  i === 0 ? 'border-amber-300 dark:border-amber-500/40' : ''
                }`}
              >
                <span
                  className={`absolute -top-3 flex h-7 w-7 items-center justify-center rounded-full text-xs font-black ring-2 ${MEDAL_TONES[i]}`}
                >
                  {entry.rank || i + 1}
                </span>
                <span
                  className={`flex h-14 w-14 items-center justify-center rounded-full text-lg font-bold text-white ${
                    AVATAR_COLORS[entry.avatar_color] ?? AVATAR_COLORS.indigo
                  }`}
                >
                  {initials(entry.full_name)}
                </span>
                <p className="truncate font-bold text-slate-900 dark:text-white">{entry.full_name}</p>
                <div className="flex flex-wrap items-center justify-center gap-2 text-xs">
                  <span className="rounded-full bg-brand-100 px-2 py-0.5 font-bold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300">
                    Level {entry.level}
                  </span>
                  <span className="rounded-full bg-violet-100 px-2 py-0.5 font-bold text-violet-700 dark:bg-violet-500/15 dark:text-violet-300">
                    {entry.xp} XP
                  </span>
                  <span className="inline-flex items-center gap-1 rounded-full bg-amber-100 px-2 py-0.5 font-bold text-amber-700 dark:bg-amber-500/15 dark:text-amber-300">
                    <Flame className="h-3 w-3" /> {entry.streak_days}d
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="card overflow-x-auto p-0">
            <table className="w-full min-w-[560px] text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-800">
                  <th className="px-5 py-3 font-semibold">Rank</th>
                  <th className="px-5 py-3 font-semibold">Learner</th>
                  <th className="px-5 py-3 font-semibold">Level</th>
                  <th className="px-5 py-3 font-semibold">Streak</th>
                  <th className="px-5 py-3 text-right font-semibold">XP</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((entry) => {
                  const isMe = user?.id === entry.id;
                  return (
                    <tr
                      key={entry.id}
                      className={`border-b border-slate-100 last:border-0 dark:border-slate-800 ${
                        isMe
                          ? 'bg-brand-50/70 dark:bg-brand-500/10'
                          : 'transition hover:bg-slate-50 dark:hover:bg-slate-800/50'
                      }`}
                    >
                      <td className="px-5 py-3">
                        {entry.rank <= 3 ? (
                          <span
                            className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-black ${MEDAL_TONES[entry.rank - 1]}`}
                          >
                            {entry.rank}
                          </span>
                        ) : (
                          <span className="pl-2 text-sm font-bold tabular-nums text-slate-500 dark:text-slate-400">
                            {entry.rank}
                          </span>
                        )}
                      </td>
                      <td className="px-5 py-3">
                        <div className="flex items-center gap-3">
                          <span
                            className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-xs font-bold text-white ${
                              AVATAR_COLORS[entry.avatar_color] ?? AVATAR_COLORS.indigo
                            }`}
                          >
                            {initials(entry.full_name)}
                          </span>
                          <span className="min-w-0">
                            <span className="flex items-center gap-1.5 font-semibold text-slate-800 dark:text-slate-100">
                              <span className="truncate">{entry.full_name}</span>
                              {isMe && (
                                <span className="rounded-full bg-brand-600 px-2 py-0.5 text-[10px] font-bold uppercase text-white">
                                  You
                                </span>
                              )}
                            </span>
                          </span>
                        </div>
                      </td>
                      <td className="px-5 py-3 text-slate-600 dark:text-slate-300">{entry.level}</td>
                      <td className="px-5 py-3">
                        <span className="inline-flex items-center gap-1 font-semibold text-amber-600 dark:text-amber-400">
                          <Flame className="h-3.5 w-3.5" /> {entry.streak_days}d
                        </span>
                      </td>
                      <td className="px-5 py-3 text-right font-bold tabular-nums text-slate-900 dark:text-white">
                        {entry.xp}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}

      <div className="flex items-center justify-center gap-2 text-xs text-slate-400">
        <Medal className="h-4 w-4" />
        Rankings are recalculated from XP earned in
        {period === 'weekly' ? ' the last 7 days' : period === 'monthly' ? ' the last 30 days' : ' all time'}.
      </div>
    </div>
  );
}
