import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { Filter, GraduationCap, PlayCircle, Target } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Exam, QuizMeta } from '../../lib/types';
import { Card, EmptyState, Select, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { QuizCard } from '../../components/QuizCard';
import { toItems } from '../../components/helpers';

export default function Pyqs() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [exam, setExam] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [year, setYear] = useState('');
  const [items, setItems] = useState<QuizMeta[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const data = await get<unknown>('/exams');
        if (alive) setExams(toItems<Exam>(data));
      } catch (err) {
        if (alive) toast.error(errorMessage(err));
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const params: Record<string, unknown> = {};
        if (exam) params.exam = exam;
        if (difficulty) params.difficulty = difficulty;
        if (year) params.year = Number(year);
        const data = await get<unknown>('/pyqs', params);
        if (alive) setItems(toItems<QuizMeta>(data));
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
  }, [exam, difficulty, year]);

  const reset = () => {
    setExam('');
    setDifficulty('');
    setYear('');
  };

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
          <Select id="pyq-difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
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
            {[2026, 2025, 2024, 2023, 2022, 2021, 2020].map((y) => (
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

      <SectionHeader
        title="PYQ quizzes"
        subtitle={items ? `${items.length} question set${items.length === 1 ? '' : 's'} found` : undefined}
      />

      {loading ? (
        <Spinner />
      ) : items && items.length ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
          description="Try changing the filters — new PYQ sets are added regularly."
          action={
            <button
              type="button"
              onClick={reset}
              className="text-sm font-semibold text-brand-600 hover:underline dark:text-brand-400"
            >
              Clear filters
            </button>
          }
        />
      )}
    </div>
  );
}
