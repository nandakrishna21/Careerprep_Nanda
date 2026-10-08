import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useParams, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Clock,
  LayoutGrid,
  PlayCircle,
  RotateCcw,
  Send,
  Trophy,
  XCircle,
} from 'lucide-react';
import { errorMessage, get, post } from '../../lib/api';
import type { AttemptReport, QuizQuestion } from '../../lib/types';
import { Badge, Button, Card, EmptyState, Modal, ProgressBar, Spinner } from '../../components/ui';
import { difficultyColor } from '../../components/QuizCard';
import { asPercent, formatClock, formatScore, toItems } from '../../components/helpers';

interface QuizDetail {
  id: number;
  title: string;
  quiz_type: string;
  difficulty: string;
  duration_minutes: number;
  total_questions: number;
  negative_marks: number;
  sections: { name: string; question_count: number; marks?: number }[] | null;
  topic?: { id: number; title: string; slug?: string } | null;
  exam?: { id: number; name: string; slug?: string } | null;
  meta?: Record<string, unknown> | null;
  mode_options?: { practice?: boolean; exam?: boolean } | null;
}

type Phase = 'start' | 'running' | 'submitting' | 'result';
type Mode = 'practice' | 'exam';

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

export default function QuizRunner() {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const base = location.pathname.startsWith('/it') ? '/it' : '/gov';

  const [quiz, setQuiz] = useState<QuizDetail | null>(null);
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  const [phase, setPhase] = useState<Phase>('start');
  const [mode, setMode] = useState<Mode>(searchParams.get('mode') === 'exam' ? 'exam' : 'practice');
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [current, setCurrent] = useState(0);
  const [remaining, setRemaining] = useState(0);
  const [showSubmit, setShowSubmit] = useState(false);
  const [result, setResult] = useState<AttemptReport | null>(null);
  const submittingRef = useRef(false);

  const totalSeconds = Math.max(0, Math.round((quiz?.duration_minutes ?? 0) * 60));
  const totalQuestions = questions.length;
  const answeredCount = useMemo(
    () => questions.filter((q) => answers[q.id] !== undefined).length,
    [questions, answers]
  );

  useEffect(() => {
    if (!id) return;
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      setPhase('start');
      setAnswers({});
      setCurrent(0);
      setResult(null);
      try {
        const [detail, qs] = await Promise.all([
          get<QuizDetail>(`/quizzes/${id}`),
          get<unknown>(`/quizzes/${id}/questions`),
        ]);
        if (!alive) return;
        setQuiz(detail);
        const list = toItems<QuizQuestion>(qs);
        setQuestions(list);
        setRemaining(Math.max(0, Math.round((detail.duration_minutes ?? 0) * 60)));
        setMode(
          searchParams.get('mode') === 'exam' && detail.mode_options?.exam !== false
            ? 'exam'
            : 'practice'
        );
      } catch (err) {
        if (!alive) return;
        const msg = errorMessage(err);
        setError(msg);
        toast.error(msg);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [id, reloadKey]);

  const submitAttempt = useCallback(
    async (auto = false) => {
      if (!quiz || !id || submittingRef.current) return;
      if (phase !== 'running') return;
      submittingRef.current = true;
      setPhase('submitting');
      setShowSubmit(false);
      const payload: Record<string, number> = {};
      Object.entries(answers).forEach(([qid, idx]) => {
        payload[qid] = idx;
      });
      const timeTaken = Math.max(0, totalSeconds - remaining);
      try {
        const res = await post<AttemptReport>(`/quizzes/${id}/attempt`, {
          answers: payload,
          time_taken_seconds: timeTaken,
          mode,
        });
        setResult(res);
        setPhase('result');
        if (auto) {
          toast('Time is up â€” your answers were submitted automatically.', { icon: 'â±ï¸' });
        } else {
          toast.success(
            `Submitted! Score ${formatScore(res.attempt.score)}/${res.attempt.total}`
          );
        }
        (res.achievements_unlocked ?? []).forEach((a) => {
          toast(`Achievement unlocked: ${a.title}`, { icon: 'ðŸ†' });
        });
      } catch (err) {
        toast.error(errorMessage(err));
        setPhase('running');
      } finally {
        submittingRef.current = false;
      }
    },
    [quiz, id, phase, answers, remaining, totalSeconds, mode]
  );

  useEffect(() => {
    if (phase !== 'running') return;
    const timer = window.setInterval(() => {
      setRemaining((r) => Math.max(0, r - 1));
    }, 1000);
    return () => window.clearInterval(timer);
  }, [phase]);

  useEffect(() => {
    if (phase === 'running' && remaining === 0 && totalSeconds > 0) {
      void submitAttempt(true);
    }
  }, [phase, remaining, totalSeconds, submitAttempt]);

  const pick = (optionIndex: number) => {
    const question = questions[current];
    if (!question) return;
    setAnswers((prev) => ({ ...prev, [question.id]: optionIndex }));
  };

  useEffect(() => {
    if (phase !== 'running') return;
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')) return;
      if (e.key === 'ArrowRight') setCurrent((c) => Math.min(totalQuestions - 1, c + 1));
      else if (e.key === 'ArrowLeft') setCurrent((c) => Math.max(0, c - 1));
      else {
        const n = Number(e.key);
        if (n >= 1 && n <= 4) pick(n - 1);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [phase, current, totalQuestions]);

  const start = () => {
    if (!totalQuestions) {
      toast.error('This quiz has no questions yet.');
      return;
    }
    setRemaining(totalSeconds);
    setCurrent(0);
    setAnswers({});
    setPhase('running');
  };

  const retake = () => {
    setAnswers({});
    setCurrent(0);
    setResult(null);
    setRemaining(totalSeconds);
    setPhase('start');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl">
        <Spinner />
      </div>
    );
  }

  if (error || !quiz) {
    return (
      <div className="mx-auto max-w-4xl">
        <EmptyState
          title="Unable to load quiz"
          description={error ?? 'This quiz may not be available.'}
          action={
            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setReloadKey((k) => k + 1)}>
                Try again
              </Button>
              <Link
                to={base}
                className="inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                <ArrowLeft className="h-4 w-4" /> Back
              </Link>
            </div>
          }
        />
      </div>
    );
  }

  const lowTime = totalSeconds > 0 && remaining <= totalSeconds * 0.1;
  const skipped = Math.max(0, totalQuestions - answeredCount);

  if (phase === 'start') {
    return (
      <div className="mx-auto max-w-3xl space-y-6">
        <Link
          to={base}
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 transition hover:text-brand-600 dark:hover:text-brand-400"
        >
          <ArrowLeft className="h-4 w-4" /> Back to {base === '/it' ? 'IT hub' : 'Government hub'}
        </Link>

        <Card className="p-6 sm:p-8">
          <div className="flex flex-wrap items-center gap-2">
            <Badge color={difficultyColor(quiz.difficulty)}>{quiz.difficulty}</Badge>
            <Badge color="slate">{quiz.quiz_type}</Badge>
            {quiz.topic && <Badge color="brand">{quiz.topic.title}</Badge>}
            {quiz.exam && <Badge color="violet">{quiz.exam.name}</Badge>}
          </div>
          <h1 className="mt-3 text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl dark:text-white">
            {quiz.title}
          </h1>

          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <Fact icon={<LayoutGrid className="h-4 w-4" />} label="Questions" value={String(totalQuestions)} />
            <Fact
              icon={<Clock className="h-4 w-4" />}
              label="Duration"
              value={quiz.duration_minutes ? `${quiz.duration_minutes} min` : 'Untimed'}
            />
            <Fact
              icon={<AlertTriangle className="h-4 w-4" />}
              label="Negative marking"
              value={quiz.negative_marks > 0 ? `âˆ’${quiz.negative_marks} per wrong` : 'None'}
            />
          </div>

          {quiz.sections && quiz.sections.length > 0 && (
            <div className="mt-5 flex flex-wrap gap-1.5">
              {quiz.sections.map((s) => (
                <Badge key={s.name} color="slate">
                  {s.name}: {s.question_count} Q
                  {typeof s.marks === 'number' ? ` Â· ${s.marks} marks` : ''}
                </Badge>
              ))}
            </div>
          )}

          <div className="mt-7">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">
              Choose your mode
            </p>
            <div className="grid gap-3 sm:grid-cols-2">
              <ModeCard
                selected={mode === 'practice'}
                disabled={quiz.mode_options?.practice === false}
                onSelect={() => setMode('practice')}
                title="Practice"
                description="Relaxed setup â€” review your answers and learn at your own pace."
              />
              <ModeCard
                selected={mode === 'exam'}
                disabled={quiz.mode_options?.exam === false}
                onSelect={() => setMode('exam')}
                title="Exam"
                description="Real exam conditions â€” strict countdown timer with negative marking."
              />
            </div>
          </div>

          <div className="mt-7 flex flex-wrap items-center gap-3">
            <Button onClick={start} className="px-6 py-3">
              <PlayCircle className="h-4 w-4" /> Start {mode === 'exam' ? 'exam' : 'practice'}
            </Button>
            <span className="text-xs text-slate-400">
              Tip: use arrow keys to move and 1â€“4 to select an option.
            </span>
          </div>
        </Card>
      </div>
    );
  }

  if (phase === 'result' && result) {
    const a = result.attempt;
    const r = result.report;
    const accuracy = asPercent(a.accuracy);
    const questionsReview = r.questions ?? [];
    const suggestions = Array.from(
      new Set([...(r.suggestions ?? []), ...(r.improvement_suggestions ?? [])])
    );

    return (
      <div className="mx-auto max-w-4xl space-y-6">
        <Card className="border-brand-200 bg-gradient-to-br from-brand-50 to-white dark:border-brand-500/30 dark:from-brand-500/10 dark:to-slate-900">
          <div className="flex flex-col items-center gap-4 text-center sm:flex-row sm:text-left">
            <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-violet-600 text-white shadow-lg shadow-brand-600/30">
              <Trophy className="h-8 w-8" />
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-300">
                {mode === 'exam' ? 'Exam' : 'Practice'} complete
              </p>
              <p className="mt-1 text-3xl font-black text-slate-900 dark:text-white">
                {formatScore(a.score)}
                <span className="text-lg font-bold text-slate-400"> / {a.total}</span>
              </p>
              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                {quiz.title}
              </p>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-2 sm:justify-end">
              <Badge color="green">{accuracy}% accuracy</Badge>
              <Badge color="brand">+{a.xp_awarded} XP</Badge>
              {a.rank !== null && a.rank !== undefined && <Badge color="violet">Rank #{a.rank}</Badge>}
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <MiniStat label="Correct" value={String(a.correct ?? 0)} tone="text-emerald-600 dark:text-emerald-400" />
            <MiniStat label="Wrong" value={String(a.wrong ?? 0)} tone="text-rose-600 dark:text-rose-400" />
            <MiniStat label="Skipped" value={String(a.skipped ?? 0)} tone="text-slate-500" />
            <MiniStat
              label="Time taken"
              value={formatClock(a.time_taken_seconds ?? 0)}
              tone="text-slate-600 dark:text-slate-300"
            />
          </div>
        </Card>

        {r.topic_breakdown && r.topic_breakdown.length > 0 && (
          <Card>
            <h2 className="mb-3 text-base font-bold text-slate-900 dark:text-white">
              Topic breakdown
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full min-w-[420px] text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-700">
                    <th className="py-2 pr-4 font-semibold">Topic</th>
                    <th className="py-2 pr-4 font-semibold">Correct</th>
                    <th className="py-2 pr-4 font-semibold">Accuracy</th>
                    <th className="py-2 font-semibold">Progress</th>
                  </tr>
                </thead>
                <tbody>
                  {r.topic_breakdown.map((row, i) => {
                    const pct = asPercent(row.accuracy);
                    return (
                      <tr
                        key={i}
                        className="border-b border-slate-100 last:border-0 dark:border-slate-800"
                      >
                        <td className="py-2.5 pr-4 font-medium text-slate-800 dark:text-slate-100">
                          {row.name}
                        </td>
                        <td className="py-2.5 pr-4 text-slate-600 dark:text-slate-300">
                          {row.correct}/{row.total}
                        </td>
                        <td className="py-2.5 pr-4 text-slate-600 dark:text-slate-300">{pct}%</td>
                        <td className="w-40 py-2.5">
                          <ProgressBar
                            value={pct}
                            color={pct >= 70 ? 'bg-emerald-500' : pct >= 40 ? 'bg-amber-500' : 'bg-rose-500'}
                          />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Card>
        )}

        <div className="grid gap-4 sm:grid-cols-2">
          <Card>
            <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-emerald-600 dark:text-emerald-400">
              Strong areas
            </h2>
            {r.strong_areas && r.strong_areas.length ? (
              <div className="flex flex-wrap gap-2">
                {r.strong_areas.map((s, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1.5 rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300"
                  >
                    {s.topic} Â· {asPercent(s.accuracy)}%
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">No strong areas recorded yet.</p>
            )}
          </Card>
          <Card>
            <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-rose-600 dark:text-rose-400">
              Weak areas
            </h2>
            {r.weak_areas && r.weak_areas.length ? (
              <div className="flex flex-wrap gap-2">
                {r.weak_areas.map((w, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1.5 rounded-full bg-rose-100 px-3 py-1 text-xs font-semibold text-rose-700 dark:bg-rose-500/15 dark:text-rose-300"
                  >
                    {w.topic} Â· {asPercent(w.accuracy)}%
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">Nothing flagged â€” keep it up!</p>
            )}
          </Card>
        </div>

        {r.section_analysis && r.section_analysis.length > 0 && (
          <Card>
            <h2 className="mb-3 text-base font-bold text-slate-900 dark:text-white">
              Section analysis
            </h2>
            <div className="space-y-3">
              {r.section_analysis.map((s, i) => (
                <div key={i}>
                  <div className="mb-1 flex items-center justify-between text-sm">
                    <span className="font-medium text-slate-700 dark:text-slate-200">{s.name}</span>
                    <span className="text-slate-500 dark:text-slate-400">
                      {s.correct}/{s.attempted} attempted Â· {asPercent(s.accuracy)}%
                    </span>
                  </div>
                  <ProgressBar value={asPercent(s.accuracy)} color="bg-brand-500" />
                </div>
              ))}
            </div>
          </Card>
        )}

        {suggestions.length > 0 && (
          <Card>
            <h2 className="mb-3 text-base font-bold text-slate-900 dark:text-white">
              Suggestions &amp; improvements
            </h2>
            <ul className="space-y-2">
              {suggestions.map((s, i) => (
                <li key={i} className="flex gap-2.5 text-sm text-slate-600 dark:text-slate-300">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-brand-500" />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </Card>
        )}

        <Card>
          <h2 className="mb-4 text-base font-bold text-slate-900 dark:text-white">
            Question review
          </h2>
          {questionsReview.length ? (
            <ol className="space-y-5">
              {questionsReview.map((q, i) => (
                <li key={q.id} className="rounded-2xl border border-slate-200 p-4 dark:border-slate-800">
                  <div className="flex items-start justify-between gap-3">
                    <p className="font-semibold text-slate-800 dark:text-slate-100">
                      <span className="mr-2 text-brand-600 dark:text-brand-400">Q{i + 1}.</span>
                      {q.question_text}
                    </p>
                    {q.is_correct ? (
                      <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-emerald-500" />
                    ) : (
                      <XCircle className="mt-0.5 h-5 w-5 shrink-0 text-rose-500" />
                    )}
                  </div>
                  <div className="mt-3 grid gap-2">
                    {q.options.map((opt, oi) => {
                      const isCorrect = oi === q.correct_index;
                      const isYours = q.your_answer === oi;
                      let cls =
                        'border-slate-200 bg-white text-slate-600 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300';
                      if (isCorrect) {
                        cls =
                          'border-emerald-500 bg-emerald-50 text-emerald-800 dark:border-emerald-500/60 dark:bg-emerald-500/10 dark:text-emerald-200';
                      } else if (isYours) {
                        cls =
                          'border-rose-500 bg-rose-50 text-rose-800 dark:border-rose-500/60 dark:bg-rose-500/10 dark:text-rose-200';
                      }
                      return (
                        <div
                          key={oi}
                          className={`flex items-center gap-3 rounded-xl border px-3.5 py-2.5 text-sm ${cls}`}
                        >
                          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-current text-xs font-bold opacity-70">
                            {LETTERS[oi] ?? oi + 1}
                          </span>
                          <span className="min-w-0 flex-1">{opt}</span>
                          {isYours && (
                            <span className="shrink-0 text-xs font-bold">
                              {isCorrect ? 'Your answer' : 'Your answer'}
                            </span>
                          )}
                          {isCorrect && !isYours && (
                            <span className="shrink-0 text-xs font-bold">Correct</span>
                          )}
                        </div>
                      );
                    })}
                    {q.your_answer === null && (
                      <p className="text-xs font-semibold text-slate-400">You skipped this question.</p>
                    )}
                  </div>
                  {q.explanation && (
                    <blockquote className="mt-3 border-l-2 border-brand-400 bg-brand-50/60 px-3 py-2 text-sm italic text-slate-600 dark:border-brand-500 dark:bg-brand-500/10 dark:text-slate-300">
                      {q.explanation}
                    </blockquote>
                  )}
                </li>
              ))}
            </ol>
          ) : (
            <p className="text-sm text-slate-400">Detailed review is unavailable for this attempt.</p>
          )}
        </Card>

        <div className="flex flex-wrap gap-3">
          <Button onClick={retake}>
            <RotateCcw className="h-4 w-4" /> Retake
          </Button>
          <Link
            to={base}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <ArrowLeft className="h-4 w-4" /> Back
          </Link>
        </div>
      </div>
    );
  }

  const question = questions[current];

  return (
    <div className="mx-auto max-w-5xl">
      <div className="sticky top-16 z-10 -mx-4 border-b border-slate-200 bg-white/95 px-4 py-3 backdrop-blur sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8 dark:border-slate-800 dark:bg-slate-950/95">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex min-w-0 items-center gap-2">
              <span className="truncate text-sm font-bold text-slate-800 dark:text-slate-100">
                {quiz.title}
              </span>
              <Badge color="slate">{mode === 'exam' ? 'Exam' : 'Practice'}</Badge>
              <span className="hidden text-xs text-slate-400 sm:inline">
                Question {current + 1} of {totalQuestions}
              </span>
            </div>
            <div
              className={`inline-flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-sm font-bold tabular-nums ${
                lowTime
                  ? 'bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300'
                  : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
              }`}
              aria-label="Time remaining"
            >
              <Clock className={`h-4 w-4 ${lowTime ? 'animate-pulse' : ''}`} />
              {formatClock(remaining)}
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-slate-400 sm:hidden">
              Q {current + 1}/{totalQuestions}
            </span>
            <div className="flex-1">
              <ProgressBar
                value={current + 1}
                max={Math.max(1, totalQuestions)}
                color={lowTime ? 'bg-rose-500' : 'bg-brand-500'}
              />
            </div>
            <span className="text-xs font-semibold text-slate-400">
              {answeredCount}/{totalQuestions} answered
            </span>
          </div>
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_260px]">
        <div className="min-w-0 space-y-4">
          {question ? (
            <Card className="p-5 sm:p-6">
              <div className="flex items-start gap-3">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-brand-600 text-xs font-bold text-white">
                  {current + 1}
                </span>
                <h2 className="text-base font-semibold leading-7 text-slate-900 sm:text-lg dark:text-white">
                  {question.question_text}
                </h2>
              </div>

              <div className="mt-5 grid gap-2.5" role="group" aria-label="Answer options">
                {question.options.map((opt, oi) => {
                  const selected = answers[question.id] === oi;
                  return (
                    <button
                      key={oi}
                      type="button"
                      onClick={() => pick(oi)}
                      aria-pressed={selected}
                      className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-left text-sm transition ${
                        selected
                          ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-500/30 dark:bg-brand-500/10'
                          : 'border-slate-200 bg-white text-slate-700 hover:border-brand-300 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-brand-500/40 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span
                        className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full border text-xs font-bold ${
                          selected
                            ? 'border-brand-500 bg-brand-600 text-white'
                            : 'border-slate-300 text-slate-500 dark:border-slate-600 dark:text-slate-400'
                        }`}
                      >
                        {LETTERS[oi] ?? oi + 1}
                      </span>
                      <span className="min-w-0 flex-1">{opt}</span>
                      {selected && <CheckCircle2 className="h-4 w-4 shrink-0 text-brand-600 dark:text-brand-400" />}
                    </button>
                  );
                })}
              </div>

              <div className="mt-6 flex flex-wrap items-center justify-between gap-3">
                <Button
                  variant="outline"
                  disabled={current === 0}
                  onClick={() => setCurrent((c) => Math.max(0, c - 1))}
                >
                  <ArrowLeft className="h-4 w-4" /> Previous
                </Button>
                {current < totalQuestions - 1 ? (
                  <Button
                    variant="secondary"
                    onClick={() => setCurrent((c) => Math.min(totalQuestions - 1, c + 1))}
                  >
                    Next <ArrowRight className="h-4 w-4" />
                  </Button>
                ) : (
                  <Button onClick={() => setShowSubmit(true)}>
                    <Send className="h-4 w-4" /> Submit test
                  </Button>
                )}
              </div>
            </Card>
          ) : (
            <EmptyState
              title="No questions"
              description="This quiz has no questions to display."
            />
          )}

          {current < totalQuestions - 1 && (
            <div className="flex justify-end">
              <Button variant="ghost" onClick={() => setShowSubmit(true)}>
                <Send className="h-4 w-4" /> Submit early
              </Button>
            </div>
          )}
        </div>

        <aside className="lg:sticky lg:top-40 lg:self-start">
          <Card className="p-4">
            <div className="mb-3 flex items-center gap-2">
              <LayoutGrid className="h-4 w-4 text-slate-400" />
              <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                Question palette
              </p>
            </div>
            <div className="grid grid-cols-8 gap-1.5 sm:grid-cols-10 lg:grid-cols-6">
              {questions.map((q, i) => {
                const answered = answers[q.id] !== undefined;
                const isCurrent = i === current;
                return (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => setCurrent(i)}
                    aria-label={`Go to question ${i + 1}`}
                    aria-current={isCurrent ? 'true' : undefined}
                    className={`flex h-8 items-center justify-center rounded-lg text-xs font-bold transition ${
                      isCurrent
                        ? 'bg-brand-600 text-white ring-2 ring-brand-400'
                        : answered
                          ? 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200 dark:bg-emerald-500/20 dark:text-emerald-300'
                          : 'bg-slate-100 text-slate-500 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:hover:bg-slate-700'
                    }`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>
            <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-slate-400">
              <span className="inline-flex items-center gap-1">
                <span className="h-2.5 w-2.5 rounded-sm bg-emerald-400" /> Answered
              </span>
              <span className="inline-flex items-center gap-1">
                <span className="h-2.5 w-2.5 rounded-sm bg-slate-300 dark:bg-slate-700" /> Skipped
              </span>
              <span className="inline-flex items-center gap-1">
                <span className="h-2.5 w-2.5 rounded-sm bg-brand-500" /> Current
              </span>
            </div>
            <div className="mt-4 border-t border-slate-100 pt-3 dark:border-slate-800">
              <p className="mb-2 text-xs text-slate-400">
                {answeredCount} answered Â· {skipped} skipped
              </p>
              <Button className="w-full" onClick={() => setShowSubmit(true)}>
                <Send className="h-4 w-4" /> Submit test
              </Button>
            </div>
          </Card>
        </aside>
      </div>

      <Modal open={showSubmit} onClose={() => setShowSubmit(false)} title="Submit your answers?">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl bg-emerald-50 p-3 text-center dark:bg-emerald-500/10">
              <p className="text-2xl font-black text-emerald-600 dark:text-emerald-300">
                {answeredCount}
              </p>
              <p className="text-xs font-semibold text-emerald-700 dark:text-emerald-400">
                Answered
              </p>
            </div>
            <div className="rounded-xl bg-slate-100 p-3 text-center dark:bg-slate-800">
              <p className="text-2xl font-black text-slate-600 dark:text-slate-300">{skipped}</p>
              <p className="text-xs font-semibold text-slate-500 dark:text-slate-400">Skipped</p>
            </div>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            {mode === 'exam'
              ? 'Once submitted you cannot change your answers. Your score and report will be generated immediately.'
              : 'Your report and question review will be generated as soon as you submit.'}
          </p>
          <div className="flex justify-end gap-2">
            <Button variant="ghost" onClick={() => setShowSubmit(false)}>
              Keep working
            </Button>
            <Button onClick={() => void submitAttempt(false)}>
              <Send className="h-4 w-4" /> Submit now
            </Button>
          </div>
        </div>
      </Modal>

      {phase === 'submitting' && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="flex flex-col items-center gap-3 rounded-2xl bg-white px-8 py-6 shadow-xl dark:bg-slate-900">
            <Spinner className="py-0" />
            <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
              Evaluating your answersâ€¦
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

function Fact({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-800/40">
      <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-brand-600 shadow-sm dark:bg-slate-900 dark:text-brand-300">
        {icon}
      </span>
      <span className="min-w-0">
        <span className="block text-xs text-slate-400">{label}</span>
        <span className="block truncate text-sm font-bold text-slate-800 dark:text-slate-100">
          {value}
        </span>
      </span>
    </div>
  );
}

function MiniStat({ label, value, tone }: { label: string; value: string; tone: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-3 text-center dark:border-slate-800 dark:bg-slate-900">
      <p className={`text-lg font-black ${tone}`}>{value}</p>
      <p className="text-xs font-medium text-slate-400">{label}</p>
    </div>
  );
}

function ModeCard({
  selected,
  disabled,
  onSelect,
  title,
  description,
}: {
  selected: boolean;
  disabled?: boolean;
  onSelect: () => void;
  title: string;
  description: string;
}) {
  return (
    <label
      className={`relative flex cursor-pointer flex-col gap-1 rounded-2xl border p-4 transition ${
        selected
          ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-500/25 dark:bg-brand-500/10'
          : 'border-slate-200 bg-white hover:border-slate-300 dark:border-slate-700 dark:bg-slate-900 dark:hover:border-slate-600'
      } ${disabled ? 'cursor-not-allowed opacity-50' : ''}`}
    >
      <input
        type="radio"
        name="quiz-mode"
        className="sr-only"
        checked={selected}
        disabled={disabled}
        onChange={onSelect}
      />
      <span className="text-sm font-bold text-slate-900 dark:text-white">{title}</span>
      <span className="text-xs leading-5 text-slate-500 dark:text-slate-400">{description}</span>
    </label>
  );
}
