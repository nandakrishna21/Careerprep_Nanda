import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowLeft,
  BookOpen,
  Check,
  CheckCircle2,
  Code2,
  FileText,
  HelpCircle,
  ListChecks,
  PlayCircle,
} from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Course, QuizMeta, Topic } from '../../lib/types';
import { Badge, Card, EmptyState, ProgressBar, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import MarkdownLite from '../../components/MarkdownLite';

interface TopicDetailData extends Topic {
  course?: Course;
  lessons?: { id: number; title: string; order?: number }[] | null;
  quizzes?: QuizMeta[] | null;
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

type TabKey = 'notes' | 'examples' | 'practice' | 'code';

const TABS: { key: TabKey; label: string; icon: typeof BookOpen }[] = [
  { key: 'notes', label: 'Notes', icon: BookOpen },
  { key: 'examples', label: 'Examples', icon: ListChecks },
  { key: 'practice', label: 'Practice', icon: FileText },
  { key: 'code', label: 'Code', icon: Code2 },
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

function readCompleted(slug: string): number[] {
  try {
    const raw = localStorage.getItem(`cp_learn_${slug}`);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.map((v) => Number(v)).filter((v) => Number.isFinite(v)) : [];
  } catch {
    return [];
  }
}

export default function LearningPath() {
  const { slug } = useParams<{ slug: string }>();
  const [searchParams, setSearchParams] = useSearchParams();

  const [course, setCourse] = useState<Course | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [activeTopic, setActiveTopic] = useState<string>('');
  const [topicDetail, setTopicDetail] = useState<TopicDetailData | null>(null);
  const [topicLoading, setTopicLoading] = useState(false);

  const [lessonId, setLessonId] = useState<number | null>(null);
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [lessonLoading, setLessonLoading] = useState(false);
  const [tab, setTab] = useState<TabKey>('notes');

  const [completed, setCompleted] = useState<number[]>([]);

  useEffect(() => {
    if (!slug) return;
    let alive = true;
    setCompleted(readCompleted(slug));
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await get<Course>(`/courses/${slug}`);
        if (!alive) return;
        const sorted = (data.topics ?? []).slice().sort((a, b) => a.order - b.order);
        setCourse(data);
        setTopics(sorted);
        const wanted = searchParams.get('topic');
        const initial = wanted && sorted.some((t) => t.slug === wanted) ? wanted : sorted[0]?.slug ?? '';
        setActiveTopic(initial);
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

  useEffect(() => {
    if (!activeTopic) {
      setTopicDetail(null);
      return;
    }
    let alive = true;
    (async () => {
      setTopicLoading(true);
      try {
        const data = await get<TopicDetailData>(`/topics/${activeTopic}`);
        if (!alive) return;
        setTopicDetail(data);
        const lessons = (data.lessons ?? []).slice().sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
        setLessonId(lessons[0]?.id ?? null);
        setTab('notes');
      } catch (err) {
        if (alive) toast.error(errorMessage(err));
      } finally {
        if (alive) setTopicLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [activeTopic]);

  useEffect(() => {
    if (lessonId === null) {
      setLesson(null);
      return;
    }
    let alive = true;
    (async () => {
      setLessonLoading(true);
      try {
        const data = await get<LessonDetail>(`/lessons/${lessonId}`);
        if (alive) setLesson(data);
      } catch (err) {
        if (alive) toast.error(errorMessage(err));
      } finally {
        if (alive) setLessonLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [lessonId]);

  const selectTopic = (topicSlug: string) => {
    setActiveTopic(topicSlug);
    setSearchParams({ topic: topicSlug }, { replace: true });
  };

  const toggleComplete = (topicId: number) => {
    setCompleted((prev) => {
      const next = prev.includes(topicId) ? prev.filter((id) => id !== topicId) : [...prev, topicId];
      if (slug) {
        try {
          localStorage.setItem(`cp_learn_${slug}`, JSON.stringify(next));
        } catch {
        }
      }
      return next;
    });
  };

  if (loading) return <Spinner />;

  if (error || !course) {
    return (
      <div className="mx-auto max-w-5xl">
        <EmptyState
          title="Learning path not found"
          description={error ?? 'This course may not be published yet.'}
          action={
            <LinkButton to="/it" variant="outline">
              <ArrowLeft className="h-4 w-4" /> Back to IT hub
            </LinkButton>
          }
        />
      </div>
    );
  }

  const active = topics.find((t) => t.slug === activeTopic) ?? null;
  const isDone = active ? completed.includes(active.id) : false;
  const lessons = (topicDetail?.lessons ?? [])
    .slice()
    .sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
  const content: LessonContent = lesson?.content ?? {};

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-wrap items-center gap-2">
        <LinkButton to="/it" variant="ghost" className="!px-3 !py-1.5">
          <ArrowLeft className="h-4 w-4" /> IT Career Hub
        </LinkButton>
        <Badge color="brand">Learning Path</Badge>
        <Badge color="slate">{course.level || 'All levels'}</Badge>
      </div>

      <PageHeader title={course.title} subtitle={course.description || undefined} />

      <Card className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0 flex-1">
          <div className="mb-1.5 flex items-center justify-between text-xs font-semibold text-slate-500 dark:text-slate-400">
            <span>Course progress</span>
            <span>
              {completed.length}/{topics.length} topics completed
            </span>
          </div>
          <ProgressBar
            value={completed.length}
            max={Math.max(1, topics.length)}
            color="bg-emerald-500"
          />
        </div>
        {active && (
          <button
            type="button"
            onClick={() => toggleComplete(active.id)}
            className={`inline-flex shrink-0 items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition ${
              isDone
                ? 'bg-emerald-600 text-white hover:bg-emerald-700'
                : 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800'
            }`}
          >
            {isDone ? <CheckCircle2 className="h-4 w-4" /> : <Check className="h-4 w-4" />}
            {isDone ? 'Completed' : 'Mark complete'}
          </button>
        )}
      </Card>

      <div className="flex flex-col gap-6 lg:flex-row">
        <aside className="lg:w-72 lg:shrink-0">
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-sm font-bold uppercase tracking-wide text-slate-400">Topics</h2>
            <span className="text-xs text-slate-400">{topics.length} total</span>
          </div>
          <nav
            className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-2 lg:mx-0 lg:flex-col lg:overflow-visible lg:px-0"
            aria-label="Topics"
          >
            {topics.map((topic, i) => {
              const isActive = topic.slug === activeTopic;
              const done = completed.includes(topic.id);
              return (
                <button
                  key={topic.id}
                  type="button"
                  onClick={() => selectTopic(topic.slug)}
                  aria-current={isActive ? 'true' : undefined}
                  className={`flex min-w-max items-center gap-2.5 whitespace-nowrap rounded-xl border px-3.5 py-2.5 text-left text-sm font-semibold transition lg:w-full ${
                    isActive
                      ? 'border-brand-500 bg-brand-50 text-brand-700 dark:bg-brand-500/15 dark:text-brand-300'
                      : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-slate-700'
                  }`}
                >
                  <span
                    className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold ${
                      done
                        ? 'bg-emerald-500 text-white'
                        : isActive
                          ? 'bg-brand-600 text-white'
                          : 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400'
                    }`}
                  >
                    {done ? <Check className="h-3 w-3" /> : i + 1}
                  </span>
                  {topic.title}
                </button>
              );
            })}
            {!topics.length && (
              <p className="text-sm text-slate-400">No topics published yet.</p>
            )}
          </nav>
        </aside>

        <div className="min-w-0 flex-1 space-y-6">
          {topicLoading ? (
            <Spinner />
          ) : !topicDetail ? (
            <EmptyState
              title="Select a topic"
              description="Choose a topic from the list to start reading lessons."
            />
          ) : (
            <>
              <section>
                <PageHeader
                  title={topicDetail.title}
                  subtitle={topicDetail.description || undefined}
                  actions={
                    (topicDetail.quizzes ?? []).length > 0 ? (
                      <LinkButton
                        to={`/it/quizzes/${topicDetail.quizzes![0].id}`}
                        variant="outline"
                      >
                        <HelpCircle className="h-4 w-4" /> Topic quiz
                      </LinkButton>
                    ) : undefined
                  }
                />
              </section>

              <section className="space-y-4">
                <SectionHeader
                  title="Lessons"
                  subtitle={
                    lessons.length
                      ? `${lessons.length} lesson${lessons.length === 1 ? '' : 's'} in this topic`
                      : undefined
                  }
                />
                {lessons.length ? (
                  <div className="flex flex-wrap gap-2">
                    {lessons.map((l) => (
                      <button
                        key={l.id}
                        type="button"
                        onClick={() => setLessonId(l.id)}
                        className={`inline-flex items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-xs font-semibold transition ${
                          lessonId === l.id
                            ? 'border-brand-500 bg-brand-600 text-white'
                            : 'border-slate-200 bg-white text-slate-600 hover:border-brand-300 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-brand-500/50'
                        }`}
                      >
                        <PlayCircle className="h-3.5 w-3.5" />
                        {l.title}
                      </button>
                    ))}
                  </div>
                ) : (
                  <EmptyState
                    title="No lessons yet"
                    description="Lesson content for this topic will appear here once published."
                  />
                )}

                {lessons.length > 0 && (
                  <Card>
                    <div className="mb-4 flex flex-wrap gap-2" role="tablist" aria-label="Lesson sections">
                      {TABS.map((t) => (
                        <button
                          key={t.key}
                          type="button"
                          role="tab"
                          aria-selected={tab === t.key}
                          onClick={() => setTab(t.key)}
                          className={`inline-flex items-center gap-1.5 rounded-xl px-3.5 py-2 text-sm font-semibold transition ${
                            tab === t.key
                              ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                              : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
                          }`}
                        >
                          <t.icon className="h-4 w-4" /> {t.label}
                        </button>
                      ))}
                    </div>

                    {lessonLoading ? (
                      <Spinner className="py-8" />
                    ) : !lesson ? (
                      <p className="text-sm text-slate-400">Select a lesson to view its content.</p>
                    ) : (
                      <div>
                        <p className="mb-4 text-sm font-semibold text-slate-400">
                          {lesson.title}
                        </p>
                        {tab === 'notes' && <MarkdownLite text={content.notes} />}

                        {tab === 'examples' && <NumberedList items={asList(content.examples)} />}

                        {tab === 'practice' && <NumberedList items={asList(content.practice)} />}

                        {tab === 'code' &&
                          (content.code && content.code.trim() ? (
                            <pre className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-950 p-4 text-[13px] leading-6 text-emerald-300">
                              <code>{content.code}</code>
                            </pre>
                          ) : (
                            <p className="text-sm text-slate-400">
                              No code snippet for this lesson yet.
                            </p>
                          ))}
                      </div>
                    )}
                  </Card>
                )}
              </section>

              <section>
                <SectionHeader
                  title="Topic quizzes"
                  subtitle="Check your understanding before moving on."
                />
                {(topicDetail.quizzes ?? []).length ? (
                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {topicDetail.quizzes!.map((quiz) => (
                      <Card key={quiz.id} className="flex flex-col gap-3">
                        <div className="flex items-start justify-between gap-2">
                          <h3 className="font-semibold text-slate-900 dark:text-white">
                            {quiz.title}
                          </h3>
                          <Badge
                            color={
                              quiz.difficulty === 'beginner'
                                ? 'green'
                                : quiz.difficulty === 'intermediate'
                                  ? 'amber'
                                  : 'rose'
                            }
                          >
                            {quiz.difficulty}
                          </Badge>
                        </div>
                        <p className="text-xs text-slate-400">
                          {quiz.total_questions} questions Â· {quiz.duration_minutes} min
                        </p>
                        <LinkButton
                          to={`/it/quizzes/${quiz.id}`}
                          className="mt-auto w-full"
                          variant="outline"
                        >
                          <PlayCircle className="h-4 w-4" /> Start
                        </LinkButton>
                      </Card>
                    ))}
                  </div>
                ) : (
                  <EmptyState
                    title="No quizzes for this topic"
                    description="Quizzes will appear here once published."
                  />
                )}
              </section>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function NumberedList({ items }: { items: string[] }) {
  if (!items.length) {
    return <p className="text-sm text-slate-400">Nothing added yet for this section.</p>;
  }
  return (
    <ol className="space-y-3">
      {items.map((item, i) => (
        <li key={i} className="flex gap-3 text-sm leading-6 text-slate-600 dark:text-slate-300">
          <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand-100 text-xs font-bold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300">
            {i + 1}
          </span>
          <span className="whitespace-pre-line">{item}</span>
        </li>
      ))}
    </ol>
  );
}
