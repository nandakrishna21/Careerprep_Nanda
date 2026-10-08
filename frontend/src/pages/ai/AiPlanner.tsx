import { FormEvent, useCallback, useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { CalendarDays, CheckSquare, ClipboardList, Loader2, Plus, Trash2 } from 'lucide-react';
import { del, errorMessage, get, post } from '../../lib/api';
import type { StudyPlan } from '../../lib/types';
import { AccordionItem } from '../../components/Accordion';
import { Button, Card, EmptyState, Input, Select, Spinner } from '../../components/ui';
import { formatDate, toItems } from '../../components/helpers';

const DURATIONS = [7, 14, 30, 60, 90];
const PERFORMANCES = [
  { value: 'excellent', label: 'Excellent — scoring above 85%' },
  { value: 'good', label: 'Good — scoring 65–85%' },
  { value: 'average', label: 'Average — scoring 45–65%' },
  { value: 'weak', label: 'Needs work — below 45%' },
];

export default function AiPlanner() {
  const [goal, setGoal] = useState('');
  const [exam, setExam] = useState('');
  const [hoursPerDay, setHoursPerDay] = useState(3);
  const [durationDays, setDurationDays] = useState(30);
  const [performance, setPerformance] = useState('average');

  const [current, setCurrent] = useState<StudyPlan | null>(null);
  const [generating, setGenerating] = useState(false);
  const [history, setHistory] = useState<StudyPlan[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [loadingPlanId, setLoadingPlanId] = useState<number | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const loadHistory = useCallback(async () => {
    setLoadingHistory(true);
    try {
      const data = await get<unknown>('/ai/study-plans');
      setHistory(toItems<StudyPlan>(data));
    } catch {
      setHistory([]);
    } finally {
      setLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    void loadHistory();
  }, [loadHistory]);

  const generate = async (e: FormEvent) => {
    e.preventDefault();
    if (!goal.trim() || !exam.trim()) {
      toast.error('Please fill in your goal and target exam.');
      return;
    }
    setGenerating(true);
    try {
      const res = await post<{ id?: number; plan: StudyPlan['plan'] }>('/ai/study-plan', {
        goal: goal.trim(),
        exam: exam.trim(),
        hours_per_day: hoursPerDay,
        duration_days: durationDays,
        performance,
      });
      setCurrent({
        id: res.id ?? 0,
        goal: goal.trim(),
        exam: exam.trim(),
        hours_per_day: hoursPerDay,
        duration_days: durationDays,
        plan: res.plan,
        created_at: new Date().toISOString(),
      });
      toast.success('Study plan created');
      void loadHistory();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setGenerating(false);
    }
  };

  const openPlan = async (id: number) => {
    setLoadingPlanId(id);
    try {
      const plan = await get<StudyPlan>(`/ai/study-plans/${id}`);
      setCurrent(plan);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setLoadingPlanId(null);
    }
  };

  const removePlan = async (id: number) => {
    setDeletingId(id);
    try {
      await del(`/ai/study-plans/${id}`);
      toast.success('Plan deleted');
      setHistory((prev) => prev.filter((p) => p.id !== id));
      if (current?.id === id) setCurrent(null);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setDeletingId(null);
    }
  };

  const daily = current?.plan?.daily ?? [];
  const weekly = current?.plan?.weekly ?? [];
  const monthly = current?.plan?.monthly ?? [];

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="min-w-0">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Study Planner</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Tell us your goal and availability — get a personalised daily, weekly and monthly plan.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <div className="min-w-0 space-y-6">
          <Card>
            <form onSubmit={generate} className="grid gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className="label" htmlFor="goal">
                  Goal
                </label>
                <Input
                  id="goal"
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  placeholder="e.g. Crack SSC CGL Tier 1 in 3 months"
                />
              </div>
              <div>
                <label className="label" htmlFor="exam">
                  Target exam
                </label>
                <Input
                  id="exam"
                  value={exam}
                  onChange={(e) => setExam(e.target.value)}
                  placeholder="e.g. SSC CGL / IBPS PO / Placement"
                />
              </div>
              <div>
                <label className="label" htmlFor="hours">
                  Hours per day ({hoursPerDay})
                </label>
                <input
                  id="hours"
                  type="range"
                  min={1}
                  max={12}
                  value={hoursPerDay}
                  onChange={(e) => setHoursPerDay(Number(e.target.value))}
                  className="mt-3 w-full accent-brand-600"
                />
              </div>
              <div>
                <label className="label" htmlFor="duration">
                  Duration
                </label>
                <Select
                  id="duration"
                  value={durationDays}
                  onChange={(e) => setDurationDays(Number(e.target.value))}
                >
                  {DURATIONS.map((d) => (
                    <option key={d} value={d}>
                      {d} days
                    </option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="label" htmlFor="perf">
                  Current performance
                </label>
                <Select id="perf" value={performance} onChange={(e) => setPerformance(e.target.value)}>
                  {PERFORMANCES.map((p) => (
                    <option key={p.value} value={p.value}>
                      {p.label}
                    </option>
                  ))}
                </Select>
              </div>
              <div className="sm:col-span-2">
                <Button type="submit" loading={generating}>
                  <CalendarDays className="h-4 w-4" /> Generate plan
                </Button>
              </div>
            </form>
          </Card>

          {generating ? (
            <Card className="flex flex-col items-center gap-3 py-14">
              <Spinner className="py-0" />
              <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
                Building your study plan…
              </p>
            </Card>
          ) : !current ? (
            <EmptyState
              title="No plan generated yet"
              description="Fill the form above and the AI will map out your preparation day by day."
            />
          ) : (
            <>
              <Card className="border-brand-200 bg-brand-50/50 dark:border-brand-500/30 dark:bg-brand-500/10">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-300">
                      Your plan
                    </p>
                    <h2 className="mt-1 text-lg font-bold text-slate-900 dark:text-white">{current.goal}</h2>
                    <p className="mt-0.5 text-sm text-slate-500 dark:text-slate-400">
                      {current.exam} · {current.hours_per_day}h/day · {current.duration_days} days
                    </p>
                  </div>
                </div>
              </Card>

              <section>
                <h3 className="mb-3 flex items-center gap-2 text-base font-bold text-slate-900 dark:text-white">
                  <CalendarDays className="h-4 w-4 text-brand-500" /> Daily schedule
                </h3>
                {daily.length ? (
                  <div className="space-y-2">
                    {daily.map((day, i) => (
                      <AccordionItem
                        key={i}
                        title={day.day}
                        subtitle={`${day.items?.length ?? 0} tasks`}
                        defaultOpen={i === 0}
                      >
                        <div className="space-y-2">
                          {(day.items ?? []).map((item, ii) => (
                            <div
                              key={ii}
                              className="flex flex-wrap items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm dark:border-slate-800 dark:bg-slate-800/40"
                            >
                              <span className="rounded-lg bg-white px-2 py-1 text-xs font-bold text-brand-600 shadow-sm dark:bg-slate-900 dark:text-brand-400">
                                {item.time}
                              </span>
                              <span className="min-w-0 flex-1 text-slate-700 dark:text-slate-200">{item.task}</span>
                              <span className="text-xs font-semibold text-slate-400">{item.hours}h</span>
                            </div>
                          ))}
                        </div>
                      </AccordionItem>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-slate-400">No daily breakdown in this plan.</p>
                )}
              </section>

              {weekly.length > 0 && (
                <section>
                  <h3 className="mb-3 flex items-center gap-2 text-base font-bold text-slate-900 dark:text-white">
                    <ClipboardList className="h-4 w-4 text-brand-500" /> Weekly focus
                  </h3>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {weekly.map((week, i) => (
                      <Card key={i} className="p-4">
                        <p className="text-sm font-bold text-slate-900 dark:text-white">{week.week}</p>
                        <p className="mt-0.5 text-xs font-semibold text-brand-600 dark:text-brand-400">
                          {week.focus}
                        </p>
                        <ul className="mt-2 space-y-1">
                          {(week.tasks ?? []).map((t, ti) => (
                            <li key={ti} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
                              <CheckSquare className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-500" />
                              <span>{t}</span>
                            </li>
                          ))}
                        </ul>
                      </Card>
                    ))}
                  </div>
                </section>
              )}

              {monthly.length > 0 && (
                <section>
                  <h3 className="mb-3 flex items-center gap-2 text-base font-bold text-slate-900 dark:text-white">
                    <CheckSquare className="h-4 w-4 text-brand-500" /> Monthly milestones
                  </h3>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {monthly.map((m, i) => (
                      <Card key={i} className="p-4">
                        <p className="text-sm font-bold text-slate-900 dark:text-white">{m.month}</p>
                        <ul className="mt-2 space-y-1">
                          {(m.milestones ?? []).map((ms, mi) => (
                            <li key={mi} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
                              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-brand-500" />
                              <span>{ms}</span>
                            </li>
                          ))}
                        </ul>
                      </Card>
                    ))}
                  </div>
                </section>
              )}
            </>
          )}
        </div>

        <aside>
          <Card className="p-4">
            <p className="mb-3 text-xs font-bold uppercase tracking-wide text-slate-400">Saved plans</p>
            {loadingHistory ? (
              <Spinner className="py-6" />
            ) : history.length === 0 ? (
              <p className="text-sm text-slate-400">Plans you generate are saved here for later.</p>
            ) : (
              <div className="space-y-2">
                {history.map((plan) => (
                  <div
                    key={plan.id}
                    className={`rounded-xl border p-3 transition ${
                      current?.id === plan.id
                        ? 'border-brand-400 bg-brand-50 dark:border-brand-500/50 dark:bg-brand-500/10'
                        : 'border-slate-200 dark:border-slate-800'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      <button
                        type="button"
                        onClick={() => void openPlan(plan.id)}
                        className="min-w-0 flex-1 text-left"
                      >
                        <span className="block truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                          {plan.goal || 'Study plan'}
                        </span>
                        <span className="mt-0.5 block text-xs text-slate-400">
                          {plan.exam} · {plan.duration_days}d · {formatDate(plan.created_at)}
                        </span>
                      </button>
                      {loadingPlanId === plan.id ? (
                        <Loader2 className="h-4 w-4 animate-spin text-brand-500" />
                      ) : (
                        <button
                          type="button"
                          aria-label="Delete plan"
                          onClick={() => void removePlan(plan.id)}
                          disabled={deletingId === plan.id}
                          className="rounded-lg p-1.5 text-slate-400 transition hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </aside>
      </div>
    </div>
  );
}
