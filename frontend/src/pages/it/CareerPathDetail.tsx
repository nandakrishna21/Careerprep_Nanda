import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowLeft, ArrowRight, BookOpen, Clock, HelpCircle, Layers, ListChecks, PlayCircle } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Course, QuizMeta, Topic } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { AccordionItem } from '../../components/Accordion';

interface TopicDetailData extends Topic {
  lessons?: { id: number; title: string; order?: number }[] | null;
  quizzes?: QuizMeta[] | null;
}

interface CourseDetail extends Omit<Course, 'topics'> {
  topics?: Topic[] | null;
}

export default function CareerPathDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [expanded, setExpanded] = useState<string | null>(null);
  const [topicDetails, setTopicDetails] = useState<Record<string, TopicDetailData>>({});
  const [detailLoading, setDetailLoading] = useState<string | null>(null);
  const [siblings, setSiblings] = useState<Course[]>([]);

  useEffect(() => {
    if (!slug) return;
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await get<CourseDetail>(`/courses/${slug}`);
        if (!alive) return;
        setCourse(data);
        try {
          const all = await get<unknown>('/courses', { category: 'it' });
          if (!alive) return;
          const list = Array.isArray(all) ? (all as Course[]) : [];
          setSiblings(list.filter((c) => c.career_path !== true && c.slug !== slug));
        } catch {
          if (alive) setSiblings([]);
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

  const expand = async (topicSlug: string) => {
    const next = expanded === topicSlug ? null : topicSlug;
    setExpanded(next);
    if (!next || topicDetails[next]) return;
    setDetailLoading(next);
    try {
      const data = await get<TopicDetailData>(`/topics/${next}`);
      setTopicDetails((prev) => ({ ...prev, [next]: data }));
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setDetailLoading(null);
    }
  };

  if (loading) return <Spinner />;

  if (error || !course) {
    return (
      <div className="mx-auto max-w-5xl">
        <EmptyState
          title="Career path not found"
          description={error ?? 'This path may not be published yet.'}
          action={
            <LinkButton to="/it" variant="outline">
              <ArrowLeft className="h-4 w-4" /> Back to IT hub
            </LinkButton>
          }
        />
      </div>
    );
  }

  const topics = (course.topics ?? []).slice().sort((a, b) => a.order - b.order);
  const firstTopic = topics[0];

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-wrap items-center gap-2">
        <LinkButton to="/it" variant="ghost" className="!px-3 !py-1.5">
          <ArrowLeft className="h-4 w-4" /> IT Career Hub
        </LinkButton>
        <Badge color="violet">Career Path</Badge>
        <Badge color="slate">{course.level || 'All levels'}</Badge>
      </div>

      <PageHeader
        title={course.title}
        subtitle={course.description || undefined}
        actions={
          firstTopic && (
            <LinkButton to={`/it/learn/${course.slug}?topic=${encodeURIComponent(firstTopic.slug)}`}>
              <PlayCircle className="h-4 w-4" /> Start Learning
            </LinkButton>
          )
        }
      />

      <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-500 dark:text-slate-400">
        <span className="inline-flex items-center gap-1.5">
          <Layers className="h-4 w-4" /> {topics.length} topics
        </span>
        <span className="inline-flex items-center gap-1.5">
          <BookOpen className="h-4 w-4" /> Guided roadmap
        </span>
        <span className="inline-flex items-center gap-1.5">
          <ListChecks className="h-4 w-4" /> Quizzes after every topic
        </span>
      </div>

      <section>
        <SectionHeader
          title="Roadmap"
          subtitle="Follow the steps in order â€” expand a topic to preview its lessons and quizzes."
        />
        {topics.length ? (
          <div className="relative space-y-4">
            {topics.map((topic, index) => {
              const detail = topicDetails[topic.slug];
              const isLoading = detailLoading === topic.slug;
              return (
                <div key={topic.id} className="relative pl-11">
                  {index < topics.length - 1 && (
                    <span
                      aria-hidden
                      className="absolute left-[15px] top-9 h-[calc(100%-4px)] w-0.5 bg-slate-200 dark:bg-slate-800"
                    />
                  )}
                  <span className="absolute left-0 top-1 flex h-8 w-8 items-center justify-center rounded-full bg-brand-600 text-xs font-bold text-white shadow-sm shadow-brand-600/30">
                    {index + 1}
                  </span>
                  <AccordionItem
                    title={topic.title}
                    subtitle={
                      topic.description ||
                      `${topic.lesson_count ?? detail?.lessons?.length ?? 0} lessons Â· ${
                        topic.quiz_count ?? detail?.quizzes?.length ?? 0
                      } quizzes`
                    }
                    open={expanded === topic.slug}
                    onOpenChange={() => void expand(topic.slug)}
                    right={
                      isLoading ? <span className="text-xs text-slate-400">Loadingâ€¦</span> : undefined
                    }
                  >
                    {!detail ? (
                      <Spinner className="py-4" />
                    ) : (
                      <div className="space-y-4">
                        {detail.description && (
                          <p className="text-sm text-slate-600 dark:text-slate-300">
                            {detail.description}
                          </p>
                        )}
                        <div className="grid gap-4 sm:grid-cols-2">
                          <div>
                            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">
                              Lessons
                            </p>
                            {(detail.lessons ?? []).length ? (
                              <ul className="space-y-1.5">
                                {detail.lessons
                                  ?.slice()
                                  .sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
                                  .map((lesson) => (
                                    <li
                                      key={lesson.id}
                                      className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300"
                                    >
                                      <BookOpen className="h-3.5 w-3.5 shrink-0 text-brand-500" />
                                      {lesson.title}
                                    </li>
                                  ))}
                              </ul>
                            ) : (
                              <p className="text-sm text-slate-400">No lessons yet.</p>
                            )}
                          </div>
                          <div>
                            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">
                              Quizzes
                            </p>
                            {(detail.quizzes ?? []).length ? (
                              <ul className="space-y-1.5">
                                {detail.quizzes?.map((quiz) => (
                                  <li key={quiz.id}>
                                    <LinkButton
                                      to={`/it/quizzes/${quiz.id}`}
                                      variant="outline"
                                      className="w-full !justify-start !py-2"
                                    >
                                      <HelpCircle className="h-3.5 w-3.5" /> {quiz.title}
                                      <span className="ml-auto text-xs font-normal text-slate-400">
                                        {quiz.total_questions} Q Â· {quiz.duration_minutes} min
                                      </span>
                                    </LinkButton>
                                  </li>
                                ))}
                              </ul>
                            ) : (
                              <p className="text-sm text-slate-400">No quizzes yet.</p>
                            )}
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          <LinkButton
                            to={`/it/learn/${course.slug}?topic=${encodeURIComponent(topic.slug)}`}
                            className="!py-2"
                          >
                            Study this topic <ArrowRight className="h-4 w-4" />
                          </LinkButton>
                        </div>
                      </div>
                    )}
                  </AccordionItem>
                </div>
              );
            })}
          </div>
        ) : (
          <EmptyState
            title="No topics published yet"
            description="The roadmap for this career path will appear once topics are added."
          />
        )}
      </section>

      {siblings.length > 0 && (
        <section>
          <SectionHeader title="Related learning paths" subtitle="Build the underlying skills first." />
          <div className="flex flex-wrap gap-2">
            {siblings.map((s) => (
              <LinkButton key={s.id} to={`/it/learn/${s.slug}`} variant="outline" className="!py-2">
                <Clock className="h-3.5 w-3.5" /> {s.title}
              </LinkButton>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
