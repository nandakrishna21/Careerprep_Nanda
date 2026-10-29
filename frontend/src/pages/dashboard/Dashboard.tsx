import { Suspense, lazy, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
// Charts are lazy — recharts is ~380kB. Loading it only after first paint
// makes dashboard refresh feel instant instead of blocking on JS parse.
const DashboardCharts = lazy(() => import('./DashboardCharts'));
import {
  Award,
  BookOpen,
  Briefcase,
  ClipboardList,
  Flame,
  GraduationCap,
  Lock,
  MessageSquare,
  Sparkles,
  Target,
  TrendingUp,
  Trophy,
} from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Achievement, DashboardData } from '../../lib/types';
import { Card, EmptyState, Spinner, StatCard } from '../../components/ui';
import { asPercent } from '../../components/helpers';
import { useAuth } from '../../stores/auth';
import { useTheme } from '../../stores/theme';

function greeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
}

export default function Dashboard() {
  const { profile } = useAuth();
  const { theme } = useTheme();
  const [data, setData] = useState<DashboardData | null>(null);
  const [badges, setBadges] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const d = await get<DashboardData>('/progress/dashboard');
        if (alive) setData(d);
      } catch (err) {
        if (alive) toast.error(errorMessage(err));
      } finally {
        if (alive) setLoading(false);
      }
    })();
    (async () => {
      try {
        const list = await get<unknown>('/achievements');
        if (!alive) return;
        const items = Array.isArray(list)
          ? (list as Achievement[])
          : ((list as { items?: Achievement[] }).items ?? []);
        setBadges(items);
      } catch {
        if (alive) setBadges([]);
      }
    })();
    return () => {
      alive = false;
    };
  }, [reloadKey]);

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl space-y-6">
        <Header />
        <Spinner />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="mx-auto max-w-7xl space-y-6">
        <Header />
        <EmptyState
          title="Unable to load your progress"
          description="Something went wrong while fetching your dashboard data."
          action={
            <button
              type="button"
              onClick={() => setReloadKey((k) => k + 1)}
              className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            >
              Try again
            </button>
          }
        />
      </div>
    );
  }

  const unlockedCount = badges.filter((b) => b.unlocked).length;

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <Header
        pills={
          <>
            <Pill icon={<GraduationCap className="h-3.5 w-3.5" />} label={`Level ${data.level}`} tone="brand" />
            <Pill icon={<Trophy className="h-3.5 w-3.5" />} label={`${data.xp} XP`} tone="violet" />
            <Pill icon={<Flame className="h-3.5 w-3.5" />} label={`${data.streak_days} day streak`} tone="amber" />
            {profile && <Pill icon={<Award className="h-3.5 w-3.5" />} label={`${unlockedCount} badges`} tone="green" />}
          </>
        }
      />

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          label="Study Hours"
          value={data.total_study_hours}
          icon={<BookOpen className="h-5 w-5" />}
          hint="All time"
          to="/profile"
        />
        <StatCard
          label="Quizzes Taken"
          value={data.total_quizzes}
          icon={<Target className="h-5 w-5" />}
          hint="All time"
          to="/leaderboard"
        />
        <StatCard
          label="Average Score"
          value={`${asPercent(data.average_score)}%`}
          icon={<TrendingUp className="h-5 w-5" />}
          hint="Across all attempts"
          to="/leaderboard"
        />
        <StatCard
          label="Mock Tests Taken"
          value={data.mock_tests_taken}
          icon={<Sparkles className="h-5 w-5" />}
          hint="Full length exams"
          to="/gov/mock"
        />
        <StatCard
          label="Streak"
          value={`${data.streak_days} days`}
          icon={<Flame className="h-5 w-5" />}
          hint="Keep it alive"
          to="/leaderboard"
        />
        <StatCard
          label="Badges"
          value={`${data.badges_unlocked ?? unlockedCount}`}
          icon={<Award className="h-5 w-5" />}
          hint="Achievements unlocked"
          to="#badges"
        />
      </section>

      {/* Charts load lazily after stats paint — refresh feels instant. */}
      <Suspense
        fallback={
          <section className="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
            {[0, 1, 2].map((i) => (
              <Card key={i} className="animate-pulse">
                <div className="h-4 w-32 rounded bg-slate-200 dark:bg-slate-700" />
                <div className="mt-4 h-40 rounded-lg bg-slate-100 dark:bg-slate-800" />
              </Card>
            ))}
          </section>
        }
      >
        <DashboardCharts data={data} theme={theme} />
      </Suspense>

      <section className="grid gap-4 sm:grid-cols-2">
        <Card>
          <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-emerald-600 dark:text-emerald-400">
            Strong topics
          </h2>
          {data.strong_topics.length ? (
            <div className="flex flex-wrap gap-2">
              {data.strong_topics.map((t) => (
                <span
                  key={t.name}
                  className="inline-flex items-center gap-1.5 rounded-full bg-emerald-100 px-3 py-1.5 text-xs font-semibold text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300"
                >
                  {t.name} · {asPercent(t.accuracy)}%
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400">No strong topics recorded yet — take a few quizzes.</p>
          )}
        </Card>
        <Card>
          <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-rose-600 dark:text-rose-400">
            Weak topics
          </h2>
          {data.weak_topics.length ? (
            <div className="flex flex-wrap gap-2">
              {data.weak_topics.map((t) => (
                <span
                  key={t.name}
                  className="inline-flex items-center gap-1.5 rounded-full bg-rose-100 px-3 py-1.5 text-xs font-semibold text-rose-700 dark:bg-rose-500/15 dark:text-rose-300"
                >
                  {t.name} · {asPercent(t.accuracy)}%
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400">Nothing flagged — keep it up!</p>
          )}
        </Card>
      </section>

      <section id="badges" className="scroll-mt-24">
        <div className="mb-4 flex items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Badges</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              {badges.filter((b) => b.unlocked).length} of {badges.length} unlocked
            </p>
          </div>
        </div>
        {badges.length ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {badges.map((b) => (
              <div
                key={b.id}
                className={`card flex items-start gap-3 p-4 ${
                  b.unlocked ? '' : 'grayscale opacity-70'
                }`}
              >
                <span
                  className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                    b.unlocked
                      ? 'bg-amber-100 text-amber-600 dark:bg-amber-500/15 dark:text-amber-300'
                      : 'bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-500'
                  }`}
                >
                  {b.unlocked ? <Award className="h-5 w-5" /> : <Lock className="h-5 w-5" />}
                </span>
                <div className="min-w-0">
                  <p className="truncate text-sm font-bold text-slate-900 dark:text-white">{b.title}</p>
                  <p className="mt-0.5 line-clamp-2 text-xs text-slate-500 dark:text-slate-400">{b.description}</p>
                  <p className="mt-1 text-[11px] font-semibold text-brand-600 dark:text-brand-400">+{b.xp_reward} XP</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <EmptyState title="No badges yet" description="Complete quizzes, mock tests and interviews to unlock badges." />
        )}
      </section>

      <section>
        <div className="mb-4">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white">Quick actions</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">Jump straight into what matters.</p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <QuickAction to="/gov" icon={<Target className="h-5 w-5" />} title="Government Hub" blurb="Exams, mock tests, PYQs and current affairs." />
          <QuickAction to="/ai/planner" icon={<Sparkles className="h-5 w-5" />} title="AI Study Planner" blurb="Build a personalised day-by-day study plan." />
          <QuickAction to="/ai/interview" icon={<MessageSquare className="h-5 w-5" />} title="AI Mock Interview" blurb="Practice interviews with instant feedback." />
          <QuickAction to="/jobs" icon={<Briefcase className="h-5 w-5" />} title="Jobs Board" blurb="Government notifications and IT openings." />
          <QuickAction to="/my-jobs" icon={<ClipboardList className="h-5 w-5" />} title="My Applications" blurb="Track every application and its status." />
          <QuickAction to="/resources" icon={<BookOpen className="h-5 w-5" />} title="Free Resources" blurb="Official portals, free courses and practice sites." />
        </div>
      </section>
    </div>
  );
}

function Header({ pills }: { pills?: React.ReactNode }) {
  const { user } = useAuth();
  const firstName = (user?.full_name ?? 'there').split(' ')[0];
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div className="min-w-0">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
          {greeting()}, {firstName}!
        </h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Here is a snapshot of your preparation progress.
        </p>
      </div>
      {pills && <div className="flex flex-wrap items-center gap-2">{pills}</div>}
    </div>
  );
}

function Pill({
  icon,
  label,
  tone,
}: {
  icon: React.ReactNode;
  label: string;
  tone: 'brand' | 'violet' | 'amber' | 'green';
}) {
  const tones = {
    brand: 'bg-brand-100 text-brand-700 dark:bg-brand-500/15 dark:text-brand-300',
    violet: 'bg-violet-100 text-violet-700 dark:bg-violet-500/15 dark:text-violet-300',
    amber: 'bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300',
    green: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300',
  };
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-bold ${tones[tone]}`}
    >
      {icon}
      {label}
    </span>
  );
}

function QuickAction({
  to,
  icon,
  title,
  blurb,
}: {
  to: string;
  icon: React.ReactNode;
  title: string;
  blurb: string;
}) {
  return (
    <Link
      to={to}
      className="card group flex items-start gap-4 p-5 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
    >
      <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
        {icon}
      </span>
      <span className="min-w-0">
        <span className="block font-bold text-slate-900 dark:text-white">{title}</span>
        <span className="mt-0.5 block text-sm text-slate-500 dark:text-slate-400">{blurb}</span>
      </span>
    </Link>
  );
}
