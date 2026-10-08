import { FormEvent, useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Award, Flame, GraduationCap, Mail, Pencil, Save, Trophy } from 'lucide-react';
import { errorMessage, get, put } from '../lib/api';
import type { Profile as ProfileType } from '../lib/types';
import { AttemptLite, asPercent, formatDate, formatScore, toItems } from '../components/helpers';
import { Avatar, Button, Card, EmptyState, Input, ProgressBar, Spinner, Textarea } from '../components/ui';
import { useAuth } from '../stores/auth';

const AVATAR_SWATCHES = ['indigo', 'emerald', 'rose', 'amber', 'violet', 'sky'];

const SWATCH_CLASSES: Record<string, string> = {
  indigo: 'bg-indigo-500',
  emerald: 'bg-emerald-500',
  rose: 'bg-rose-500',
  amber: 'bg-amber-500',
  violet: 'bg-violet-500',
  sky: 'bg-sky-500',
};

function splitList(value: string): string[] {
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

interface FormState {
  headline: string;
  bio: string;
  phone: string;
  education: string;
  skills: string;
  target_exams: string;
  avatar_color: string;
}

export default function Profile() {
  const { user, profile, refreshProfile } = useAuth();
  const [form, setForm] = useState<FormState | null>(null);
  const [attempts, setAttempts] = useState<AttemptLite[] | null>(null);
  const [badgeCount, setBadgeCount] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!profile) return;
    setForm({
      headline: profile.headline ?? '',
      bio: profile.bio ?? '',
      phone: profile.phone ?? '',
      education: profile.education ?? '',
      skills: (profile.skills ?? []).join(', '),
      target_exams: (profile.target_exams ?? []).join(', '),
      avatar_color: profile.avatar_color || 'indigo',
    });
  }, [profile]);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const data = await get<unknown>('/attempts/mine');
        if (alive) setAttempts(toItems<AttemptLite>(data));
      } catch {
        if (alive) setAttempts([]);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    (async () => {
      try {
        const data = await get<unknown>('/achievements');
        if (!alive) return;
        const items = Array.isArray(data)
          ? (data as { unlocked?: boolean }[])
          : ((data as { items?: { unlocked?: boolean }[] }).items ?? []);
        setBadgeCount(items.filter((a) => a.unlocked).length);
      } catch {
        if (alive) setBadgeCount(0);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const xpIntoLevel = profile ? profile.xp % 500 : 0;

  const recentAttempts = useMemo(() => (attempts ?? []).slice(0, 10), [attempts]);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form) return;
    setSaving(true);
    try {
      await put<ProfileType>('/profile', {
        headline: form.headline,
        bio: form.bio,
        phone: form.phone,
        education: form.education,
        skills: splitList(form.skills),
        target_exams: splitList(form.target_exams),
        avatar_color: form.avatar_color,
      });
      await refreshProfile();
      toast.success('Profile updated');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  if (!profile || !form) {
    return (
      <div className="mx-auto max-w-7xl space-y-6">
        <Header />
        <Spinner />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <Header />

      <div className="grid gap-6 lg:grid-cols-[340px_1fr]">
        <div className="space-y-6">
          <Card className="flex flex-col items-center gap-3 text-center">
            <Avatar name={user?.full_name ?? 'U'} color={profile.avatar_color} size="h-20 w-20" />
            <div className="min-w-0">
              <h2 className="truncate text-lg font-bold text-slate-900 dark:text-white">
                {user?.full_name}
              </h2>
              <p className="flex items-center justify-center gap-1.5 truncate text-sm text-slate-500 dark:text-slate-400">
                <Mail className="h-3.5 w-3.5 shrink-0" />
                {user?.email}
              </p>
              {profile.headline && (
                <p className="mt-1 text-sm font-medium text-brand-600 dark:text-brand-400">{profile.headline}</p>
              )}
            </div>

            <div className="mt-2 w-full">
              <div className="mb-1.5 flex items-center justify-between text-xs font-semibold text-slate-500 dark:text-slate-400">
                <span>Level {profile.level}</span>
                <span>
                  {xpIntoLevel} / 500 XP to next level
                </span>
              </div>
              <ProgressBar value={xpIntoLevel} max={500} color="bg-brand-500" />
              <p className="mt-1.5 text-center text-[11px] text-slate-400">{profile.xp} total XP</p>
            </div>

            <div className="grid w-full grid-cols-2 gap-2">
              <div className="rounded-xl bg-amber-50 p-3 dark:bg-amber-500/10">
                <p className="flex items-center justify-center gap-1 text-lg font-black text-amber-600 dark:text-amber-400">
                  <Flame className="h-4 w-4" /> {profile.streak_days}
                </p>
                <p className="text-[11px] font-semibold text-amber-700/70 dark:text-amber-300/70">Day streak</p>
              </div>
              <div className="rounded-xl bg-brand-50 p-3 dark:bg-brand-500/10">
                <p className="flex items-center justify-center gap-1 text-lg font-black text-brand-600 dark:text-brand-400">
                  <Award className="h-4 w-4" /> {badgeCount ?? '–'}
                </p>
                <p className="text-[11px] font-semibold text-brand-700/70 dark:text-brand-300/70">Badges</p>
              </div>
            </div>
          </Card>

          <Card>
            <h3 className="mb-4 flex items-center gap-2 text-base font-bold text-slate-900 dark:text-white">
              <Pencil className="h-4 w-4 text-brand-500" /> Edit profile
            </h3>
            <form onSubmit={submit} className="space-y-4">
              <div>
                <label className="label" htmlFor="headline">
                  Headline
                </label>
                <Input
                  id="headline"
                  value={form.headline}
                  onChange={(e) => setForm({ ...form, headline: e.target.value })}
                  placeholder="Aspiring SSC CGL aspirant"
                />
              </div>
              <div>
                <label className="label" htmlFor="bio">
                  Bio
                </label>
                <Textarea
                  id="bio"
                  value={form.bio}
                  onChange={(e) => setForm({ ...form, bio: e.target.value })}
                  placeholder="A short summary about you"
                />
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="label" htmlFor="phone">
                    Phone
                  </label>
                  <Input
                    id="phone"
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    placeholder="+91 98765 43210"
                  />
                </div>
                <div>
                  <label className="label" htmlFor="education">
                    Education
                  </label>
                  <Input
                    id="education"
                    value={form.education}
                    onChange={(e) => setForm({ ...form, education: e.target.value })}
                    placeholder="B.Tech, Computer Science"
                  />
                </div>
              </div>
              <div>
                <label className="label" htmlFor="skills">
                  Skills <span className="text-xs text-slate-400">(comma separated)</span>
                </label>
                <Input
                  id="skills"
                  value={form.skills}
                  onChange={(e) => setForm({ ...form, skills: e.target.value })}
                  placeholder="Python, SQL, Reasoning"
                />
              </div>
              <div>
                <label className="label" htmlFor="target_exams">
                  Target exams <span className="text-xs text-slate-400">(comma separated)</span>
                </label>
                <Input
                  id="target_exams"
                  value={form.target_exams}
                  onChange={(e) => setForm({ ...form, target_exams: e.target.value })}
                  placeholder="SSC CGL, IBPS PO"
                />
              </div>
              <div>
                <span className="label">Avatar colour</span>
                <div className="flex flex-wrap gap-2">
                  {AVATAR_SWATCHES.map((color) => (
                    <button
                      key={color}
                      type="button"
                      aria-label={`Avatar colour ${color}`}
                      onClick={() => setForm({ ...form, avatar_color: color })}
                      className={`h-9 w-9 rounded-full transition ${
                        SWATCH_CLASSES[color]
                      } ${
                        form.avatar_color === color
                          ? 'ring-2 ring-offset-2 ring-slate-400 dark:ring-offset-slate-900'
                          : 'opacity-70 hover:opacity-100'
                      }`}
                    />
                  ))}
                </div>
              </div>
              <Button type="submit" loading={saving} className="w-full">
                <Save className="h-4 w-4" /> Save changes
              </Button>
            </form>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Recent attempts</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Your last {recentAttempts.length} quiz and mock test attempts.
                </p>
              </div>
              <Link
                to="/dashboard"
                className="text-sm font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400"
              >
                View dashboard
              </Link>
            </div>

            {loading ? (
              <Spinner className="py-8" />
            ) : recentAttempts.length ? (
              <div className="space-y-2">
                {recentAttempts.map((a) => {
                  const content = (
                    <>
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                          {a.quiz?.title || `Quiz #${a.quiz_id}`}
                        </p>
                        <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">
                          {formatDate(a.created_at)}
                          {a.mode ? ` · ${a.mode} mode` : ''}
                        </p>
                      </div>
                      <div className="shrink-0 text-right">
                        <p className="text-sm font-bold tabular-nums text-slate-900 dark:text-white">
                          {formatScore(a.score)}/{a.total}
                        </p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          {a.accuracy !== null && a.accuracy !== undefined ? `${asPercent(a.accuracy)}% accuracy` : '—'}
                        </p>
                      </div>
                    </>
                  );
                  const cls =
                    'flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 transition hover:border-brand-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-brand-500/40';
                  return a.quiz_id ? (
                    <Link key={a.id} to={`/gov/quizzes/${a.quiz_id}`} className={cls}>
                      {content}
                    </Link>
                  ) : (
                    <div key={a.id} className={cls}>
                      {content}
                    </div>
                  );
                })}
              </div>
            ) : (
              <EmptyState
                title="No attempts yet"
                description="Take your first quiz to start building your attempt history."
                action={
                  <Link
                    to="/gov"
                    className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
                  >
                    Browse quizzes
                  </Link>
                }
              />
            )}
          </Card>

          <div className="grid gap-4 sm:grid-cols-2">
            <Card className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-600 dark:bg-violet-500/10 dark:text-violet-300">
                <GraduationCap className="h-5 w-5" />
              </span>
              <div className="min-w-0">
                <p className="text-xs text-slate-400">Target exams</p>
                <p className="truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                  {profile.target_exams?.length ? profile.target_exams.join(', ') : 'Not set'}
                </p>
              </div>
            </Card>
            <Card className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-300">
                <Trophy className="h-5 w-5" />
              </span>
              <div className="min-w-0">
                <p className="text-xs text-slate-400">Skills</p>
                <p className="truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                  {profile.skills?.length ? profile.skills.join(', ') : 'Not set'}
                </p>
              </div>
            </Card>
          </div>

          {profile.bio && (
            <Card>
              <h3 className="mb-2 text-base font-bold text-slate-900 dark:text-white">About</h3>
              <p className="whitespace-pre-wrap text-sm leading-6 text-slate-600 dark:text-slate-300">{profile.bio}</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

function Header() {
  return (
    <div className="min-w-0">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Profile</h1>
      <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
        Manage your personal details, goals and track your recent attempts.
      </p>
    </div>
  );
}
