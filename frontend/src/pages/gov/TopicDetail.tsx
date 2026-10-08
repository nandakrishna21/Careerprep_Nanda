import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowLeft,
  BookOpen,
  ChevronRight,
  Clock,
  GraduationCap,
  ListChecks,
  PlayCircle,
} from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Course, QuizMeta, Topic } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { AccordionItem } from '../../components/Accordion';
import { AttemptLite, toItems } from '../../components/helpers';

interface LessonSummary {
  id: number;
  title: string;
  order?: number;
}

interface LessonContent {
  notes?: string;
  examples?: unknown;
  practice?: unknown;
  code?: string;
}

interface LessonDetail {
  id: number;
  title: string;
  content?: LessonContent | null;
}

interface TopicDetailData extends Topic {
  course?: Course;
  lessons?: LessonSummary[] | null;
  quizzes?: QuizMeta[] | null;
}

const DIFFICULTIES: { key: string; label: string; ring: string; badge: 'green' | 'amber' | 'rose' }[] = [
  { key: 'beginner', label: 'Beginner', ring: 'hover:border-emerald-400 dark:hover:border-emerald-500/50', badge: 'green' },
  { key: 'intermediate', label: 'Intermediate', ring: 'hover:border-amber-400 dark:hover:border-amber-500/50', badge: 'amber' },
  { key: 'advanced', label: 'Advanced', ring: 'hover:border-rose-400 dark:hover:border-rose-500/50', badge: 'rose' },
];

function asList(value: unknown): string[] {
  if (Array.isArray(value)) return value.map((v) => String(v));
  if (typeof value === 'string' && value.trim()) {
    return value
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean);
  }
  return [];
}

export default function TopicDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [topic, setTopic] = useState<TopicDetailData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [lessons, setLessons] = useState<Record<number, LessonDetail>>({});
  const [lessonLoading, setLessonLoading] = useState<number | null>(null);
  const [openLesson, setOpenLesson] = useState<number | null>(null);

  const [attempts, setAttempts] = useState<Record<number, AttemptLite | undefined>>({});

  useEffect(() => {
    if (!slug) return;
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await get<TopicDetailData>(`/topics/${slug}`);
        if (!alive) return;
        setTopic(data);
        const quizIds = (data.quizzes ?? []).map((q) => q.id);
        if (quizIds.length) {
          try {
            const results = await Promise.all(
              quizIds.map((id) =>
                get<unknown>('/attempts/mine', { quiz_id: id }).catch(() => null)
              )
            );
            if (!alive) return;
            const map: Record<number, AttemptLite | undefined> = {};
            quizIds.forEach((id, i) => {
              const items = toItems<AttemptLite>(results[i]);
              map[id] = items[0];
            });
            setAttempts(map);
          } catch {
          }
        }
      } catch (err) {
        if (alive) {
          const msg = errorMessage(err);
          setError(msg);
          toast.error(msg);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [slug]);

  const loadLesson = async (id: number) => {
    if (lessons[id] || lessonLoading === id) return;
    setLessonLoading(id);
    try {
      const data = await get<LessonDetail>(`/lessons/${id}`);
      setLessons((prev) => ({ ...prev, [id]: data }));
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setLessonLoading(null);
    }
  };

  if (loading) return <Spinner />;

  if (error || !topic) {
    return (
      <div className="mx-auto max-w-5xl">
        <EmptyState
          title="Topic not found"
          description={error ?? 'This topic may not be published yet.'}
          action={
            <LinkButton to="/gov" variant="outline">
              <ArrowLeft className="h-4 w-4" /> Back to Government Hub
            </LinkButton>
          }
        />
      </div>
    );
  }

  const course = topic.course;
  const lessonsList = (topic.lessons ?? []).slice().sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
  const quizzes = topic.quizzes ?? [];

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <nav className="flex flex-wrap items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400" aria-label="Breadcrumb">
        <Link to="/gov" className="inline-flex items-center gap-1 font-medium hover:text-brand-600 dark:hover:text-brand-400">
          <ArrowLeft className="h-4 w-4" /> Government Hub
        </Link>
        <ChevronRight className="h-3.5 w-3.5" />
        <span className="font-medium text-slate-600 dark:text-slate-300">
          {course?.title ?? 'Subject'}
        </span>
        <ChevronRight className="h-3.5 w-3.5" />
        <span className="font-semibold text-slate-900 dark:text-white">{topic.title}</span>
      </nav>

      <PageHeader
        title={topic.title}
        subtitle={topic.description || undefined}
        actions={
          course && (
            <LinkButton to="/gov" variant="outline">
              <BookOpen className="h-4 w-4" /> {course.title}
            </LinkButton>
          )
        }
      />

      <section>
        <SectionHeader
          title="Lessons"
          subtitle={
            lessonsList.length
              ? `${lessonsList.length} lesson${lessonsList.length === 1 ? '' : 's'} â€” expand to read notes, examples and practice.`
              : undefined
          }
        />
        {lessonsList.length ? (
          <div className="space-y-3">
            {lessonsList.map((lesson) => {
              const detail = lessons[lesson.id];
              const isLoading = lessonLoading === lesson.id;
              return (
                <AccordionItem
                  key={lesson.id}
                  title={lesson.title}
                  subtitle={detail ? 'Loaded â€” notes, examples and practice below' : 'Click to load lesson content'}
                  open={openLesson === lesson.id}
                  onOpenChange={(next) => {
                    setOpenLesson(next ? lesson.id : null);
                    if (next) void loadLesson(lesson.id);
                  }}
                  right={
                    isLoading ? (
                      <span className="text-xs text-slate-400">Loadingâ€¦</span>
                    ) : (
                      <PlayCircle className="h-4 w-4 text-brand-500" />
                    )
                  }
                >
                  {!detail ? (
                    <Spinner className="py-6" />
                  ) : (
                    <div className="space-y-5">
                      <div>
                        <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">
                          Notes
                        </p>
                        <p className="whitespace-pre-line text-sm leading-7 text-slate-600 dark:text-slate-300">
                          {detail.content?.notes?.trim() || 'No notes for this lesson yet.'}
                        </p>
                      </div>
                      <div>
                        <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">
                          Examples
                        </p>
                        <ListBlock items={asList(detail.content?.examples)} iconless />
                      </div>
                      <div>
                        <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">
                          Practice
                        </p>
                        <ListBlock items={asList(detail.content?.practice)} iconless />
                      </div>
                    </div>
                  )}
                </AccordionItem>
              );
            })}
          </div>
        ) : (
          <EmptyState
            title="No lessons yet"
            description="Lesson content for this topic will appear here once published."
          />
        )}
      </section>

      <section>
        <SectionHeader title="Topic quizzes" subtitle="Pick your difficulty and start practising." />
        {quizzes.length ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {DIFFICULTIES.map((d) => {
              const quiz = quizzes.find((q) => (q.difficulty ?? '').toLowerCase() === d.key);
              if (!quiz) return null;
              const last = attempts[quiz.id];
              return (
                <Card key={d.key} className={`flex flex-col gap-3 transition ${d.ring}`}>
                  <div className="flex items-center justify-between gap-2">
                    <h3 className="font-bold text-slate-900 dark:text-white">{quiz.title}</h3>
                    <Badge color={d.badge}>{d.label}</Badge>
                  </div>
                  <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
                    <span className="inline-flex items-center gap-1.5">
                      <Clock className="h-3.5 w-3.5" /> {quiz.duration_minutes} min
                    </span>
                    <span className="inline-flex items-center gap-1.5">
                      <ListChecks className="h-3.5 w-3.5" /> {quiz.total_questions} questions
                    </span>
                    {typeof quiz.negative_marks === 'number' && quiz.negative_marks > 0 && (
                      <span>âˆ’{quiz.negative_marks} negative</span>
                    )}
                  </div>
                  {last && (
                    <span className="inline-flex w-fit items-center gap-1.5 rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                      <GraduationCap className="h-3.5 w-3.5" /> Last attempt: {last.score}/
                      {last.total}
                      {typeof last.accuracy === 'number'
                        ? ` Â· ${Math.round(last.accuracy)}%`
                        : ''}
                    </span>
                  )}
                  <div className="mt-auto pt-1">
                    <LinkButton to={`/gov/quizzes/${quiz.id}`} className="w-full">
                      <PlayCircle className="h-4 w-4" /> Start
                    </LinkButton>
                  </div>
                </Card>
              );
            })}
            {quizzes.length < 3 && (
              <Card className="flex flex-col justify-center gap-2 border-dashed p-5 text-center">
                <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
                  More difficulty levels coming soon
                </p>
                <p className="text-xs text-slate-400">
                  Start with the levels available above.
                </p>
              </Card>
            )}
          </div>
        ) : (
          <EmptyState
            title="No quizzes for this topic yet"
            description="Quizzes will appear here as soon as an administrator publishes them."
          />
        )}
      </section>
    </div>
  );
}

function ListBlock({ items, iconless = false }: { items: string[]; iconless?: boolean }) {
  if (!items.length) {
    return <p className="text-sm text-slate-400">Nothing added yet.</p>;
  }
  return (
    <ol className="space-y-2">
      {items.map((item, i) => (
        <li key={i} className="flex gap-3 text-sm text-slate-600 dark:text-slate-300">
          <span
            className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[11px] font-bold ${
              iconless
                ? 'bg-brand-100 text-brand-700 dark:bg-brand-500/15 dark:text-brand-300'
                : 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400'
            }`}
          >
            {i + 1}
          </span>
          <span className="whitespace-pre-line">{item}</span>
        </li>
      ))}
    </ol>
  );
}
