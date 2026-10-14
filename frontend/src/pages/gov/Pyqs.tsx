import { useEffect, useMemo, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { Filter, GraduationCap, PlayCircle, Target, X } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Exam, QuizMeta } from '../../lib/types';
import { Badge, Card, EmptyState, Select, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { QuizCard } from '../../components/QuizCard';
import { toItems } from '../../components/helpers';

const YEARS = [2026, 2025, 2024, 2023, 2022, 2021, 2020];
const DIFFICULTIES = ['beginner', 'intermediate', 'advanced'] as const;
const EXAMS_CACHE_KEY = 'cp_exams';
const EXAMS_CACHE_TTL = 24 * 60 * 60 * 1000;

function readCachedExams(): Exam[] | null {
  try {
    const raw = localStorage.getItem(EXAMS_CACHE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { at: number; items: Exam[] };
    if (Date.now() - parsed.at > EXAMS_CACHE_TTL) return null;
    return Array.isArray(parsed.items) ? parsed.items : null;
  } catch {
    return null;
  }
}

export default function Pyqs() {
  const [exams, setExams] = useState<Exam[]>(() => readCachedExams() ?? []);
  const [exam, setExam] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [year, setYear] = useState('');
  const [items, setItems] = useState<QuizMeta[] | null>(null);
  const [loading, setLoading] = useState(true);
  const abortRef = useRef<AbortController | null>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Exams rarely change — paint cache instantly, refresh in background.
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const data = await get<unknown>('/exams');
        if (!alive) return;
        const list = toItems<Exam>(data);
        setExams(list);
        try {
          localStorage.setItem(EXAMS_CACHE_KEY, JSON.stringify({ at: Date.now(), items: list }));
        } catch {
          /* ignore */
        }
      } catch (err) {
        // Keep cached list on failure; only toast when we have nothing to show.
        if (alive && exams.length === 0) toast.error(errorMessage(err));
      }
    })();
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Debounced + abortable PYQ fetch — rapid filter changes don't pile up
  // requests, and previous results stay visible (no full-screen flash).
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;
      let alive = true;
      (async () => {
        // Only full-spinner on first load; refetches keep old grid visible.
        setLoading(true);
        try {
          const params: Record<string, unknown> = {};
          if (exam) params.exam = exam;
          if (difficulty) params.difficulty = difficulty;
          if (year) params.year = Number(year);
          const data = await get<unknown>('/pyqs', params, { signal: controller.signal });
          if (alive) setItems(toItems<QuizMeta>(data));
        } catch (err) {
          if (controller.signal.aborted) return;
          if (alive) {
            toast.error(errorMessage(err));
            setItems((prev) => prev ?? []);
          }
        } finally {
          if (alive) setLoading(false);
        }
      })();
      return () => {
        alive = false;
      };
    }, 250);
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
      abortRef.current?.abort();
    };
  }, [exam, difficulty, year]);

  const reset = () => {
    setExam('');
    setDifficulty('');
    setYear('');
  };

  const selectedExamName = useMemo(() => {
    if (!exam) return '';
    const found = exams.find(
      (ex) => ex.slug === exam || ex.name === exam || String(ex.id) === exam,
    );
    return found?.name ?? exam;
  }, [exam, exams]);

  const activeFilters = useMemo(() => {
    const list: { key: string; label: string; clear: () => void }[] = [];
    if (exam)
      list.push({
        key: 'exam',
        label: `Exam: ${selectedExamName || exam}`,
        clear: () => setExam(''),
      });
    if (difficulty)
      list.push({
        key: 'difficulty',
        label: `Level: ${difficulty}`,
        clear: () => setDifficulty(''),
      });
    if (year)
      list.push({ key: 'year', label: `Year: ${year}`, clear: () => setYear('') });
    return list;
  }, [exam, difficulty, year, selectedExamName]);

  const hasFilters = activeFilters.length > 0;
  const isInitialLoad = items === null && loading;
  const isRefreshing = items !== null && loading;

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Previous Year Questions"
        subtitle="Real PYQs organised by exam and difficulty — practise in relaxed mode or under exam conditions."
        actions={
          <LinkButton to="/gov/mock" variant="outline">
            Full mock tests
          </LinkButton>
        }
      />

      <Card className="flex flex-col gap-3 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label className="label" htmlFor="pyq-exam">
            Exam
          </label>
          <Select id="pyq-exam" value={exam} onChange={(e) => setExam(e.target.value)}>
            <option value="">All exams</option>
            {exams.map((ex) => (
              <option key={ex.id} value={ex.slug || ex.name}>
                {ex.name}
              </option>
            ))}
          </Select>
        </div>
        <div className="flex-1">
          <label className="label" htmlFor="pyq-difficulty">
            Difficulty
          </label>
          <Select
            id="pyq-difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="">All difficulties</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </Select>
        </div>
        <div className="flex-1">
          <label className="label" htmlFor="pyq-year">
            Year
          </label>
          <Select id="pyq-year" value={year} onChange={(e) => setYear(e.target.value)}>
            <option value="">All years</option>
            {YEARS.map((y) => (
              <option key={y} value={String(y)}>
                {y}
              </option>
            ))}
          </Select>
        </div>
        <button
          type="button"
          onClick={reset}
          className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800"
        >
          <Filter className="h-4 w-4" /> Reset
        </button>
      </Card>

      {hasFilters && (
        <div className="flex flex-wrap items-center gap-2 text-sm">
          <span className="text-slate-500 dark:text-slate-400">Active filters:</span>
          {activeFilters.map((f) => (
            <button
              key={f.key}
              type="button"
              onClick={f.clear}
              title={`Clear ${f.key} filter`}
              className="inline-flex items-center gap-1.5 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700 transition hover:bg-brand-100 dark:bg-brand-500/10 dark:text-brand-300 dark:hover:bg-brand-500/20"
            >
              {f.label} <X className="h-3 w-3" />
            </button>
          ))}
          <button
            type="button"
            onClick={reset}
            className="text-xs font-semibold text-slate-500 underline hover:text-slate-700 dark:text-slate-400"
          >
            Clear all
          </button>
        </div>
      )}

      <SectionHeader
        title="PYQ quizzes"
        subtitle={
          items
            ? `${items.length} question set${items.length === 1 ? '' : 's'} found${
                hasFilters ? ' for the selected filters' : ' — 13 exams × 7 years (2020–2026) × 3 levels'
              }${isRefreshing ? ' · updating…' : ''}`
            : undefined
        }
      />

      {isInitialLoad ? (
        <Spinner />
      ) : items && items.length ? (
        <div
          className={`grid gap-4 sm:grid-cols-2 lg:grid-cols-3 transition-opacity ${
            isRefreshing ? 'opacity-60' : ''
          }`}
        >
          {items.map((quiz) => (
            <QuizCard
              key={quiz.id}
              quiz={quiz}
              badges={
                typeof quiz.meta?.year !== 'undefined' ? undefined : (
                  <span className="inline-flex items-center gap-1">
                    <GraduationCap className="h-3.5 w-3.5" /> PYQ
                  </span>
                )
              }
              actions={
                <>
                  <LinkButton
                    to={`/gov/quizzes/${quiz.id}?mode=practice`}
                    variant="outline"
                    className="flex-1"
                  >
                    <PlayCircle className="h-4 w-4" /> Practice Mode
                  </LinkButton>
                  <LinkButton to={`/gov/quizzes/${quiz.id}?mode=exam`} className="flex-1">
                    <Target className="h-4 w-4" /> Exam Mode
                  </LinkButton>
                </>
              }
            />
          ))}
        </div>
      ) : (
        <EmptyState
          title="No previous year questions found"
          description={
            hasFilters
              ? `No sets match ${activeFilters.map((f) => f.label).join(' · ')}. This usually means the backend hasn't been seeded yet, or the combination has no paper. Try removing one filter at a time — clearing all filters always shows the full bank.`
              : 'No PYQ sets are available right now. If you just deployed, the seeder runs on backend boot — give it a minute and refresh. Otherwise contact an admin.'
          }
          action={
            <div className="mt-3 flex flex-wrap items-center justify-center gap-2">
              {hasFilters && (
                <>
                  {exam && (
                    <button
                      type="button"
                      onClick={() => setExam('')}
                      className="rounded-full border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300"
                    >
                      Clear exam{selectedExamName ? ` (${selectedExamName})` : ''}
                    </button>
                  )}
                  {difficulty && (
                    <button
                      type="button"
                      onClick={() => setDifficulty('')}
                      className="rounded-full border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300"
                    >
                      Clear level ({difficulty})
                    </button>
                  )}
                  {year && (
                    <button
                      type="button"
                      onClick={() => setYear('')}
                      className="rounded-full border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300"
                    >
                      Clear year ({year})
                    </button>
                  )}
                </>
              )}
              <button
                type="button"
                onClick={reset}
                className="text-sm font-semibold text-brand-600 hover:underline dark:text-brand-400"
              >
                Clear filters
              </button>
            </div>
          }
        />
      )}

      {!isInitialLoad && items && items.length > 0 && items.length < 5 && hasFilters && (
        <div className="flex flex-wrap items-center gap-2 rounded-xl bg-slate-50 p-3 text-xs text-slate-500 dark:bg-slate-800/60 dark:text-slate-400">
          <Badge color="slate">Tip</Badge>
          <span>
            Only {items.length} set{items.length === 1 ? '' : 's'} match. Clear a filter to
            see more — the full bank covers every exam × year (2020–2026) ×{' '}
            {DIFFICULTIES.join(' / ')}.
          </span>
        </div>
      )}
    </div>
  );
}
