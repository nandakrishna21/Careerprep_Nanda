import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowRight,
  BookOpen,
  ChevronDown,
  FileText,
  Loader2,
  Newspaper,
  PlayCircle,
  Target,
} from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Course, Exam, Topic } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { AttemptLite, formatScore, patternHint, toItems } from '../../components/helpers';

export default function GovDashboard() {
  const [exams, setExams] = useState<Exam[] | null>(null);
  const [subjects, setSubjects] = useState<Course[] | null>(null);
  const [attempts, setAttempts] = useState<AttemptLite[] | null>(null);
  const [loading, setLoading] = useState(true);

  const [openSubject, setOpenSubject] = useState<string | null>(null);
  const [subjectTopics, setSubjectTopics] = useState<Record<string, Topic[]>>({});
  const [subjectLoading, setSubjectLoading] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const [ex, co] = await Promise.all([
          get<unknown>('/exams'),
          get<unknown>('/courses', { category: 'government' }),
        ]);
        if (!alive) return;
        setExams(toItems<Exam>(ex));
        setSubjects(toItems<Course>(co));
      } catch (err) {
        if (alive) toast.error(errorMessage(err));
        if (alive) {
          setExams([]);
          setSubjects([]);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();

    (async () => {
      try {
        const at = await get<unknown>('/attempts/mine');
        if (alive) setAttempts(toItems<AttemptLite>(at));
      } catch {
        if (alive) setAttempts([]);
      }
    })();

    return () => {
      alive = false;
    };
  }, []);

  const toggleSubject = async (slug: string) => {
    const next = openSubject === slug ? null : slug;
    setOpenSubject(next);
    if (!next || subjectTopics[slug]) return;
    setSubjectLoading(slug);
    try {
      const course = await get<Course>(`/courses/${slug}`);
      setSubjectTopics((prev) => ({ ...prev, [slug]: course.topics ?? [] }));
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSubjectLoading(null);
    }
  };

  const latest = attempts && attempts.length ? attempts[0] : null;

  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <PageHeader
        title="Government Exam Hub"
        subtitle="Explore exams, subjects, mock tests, previous year questions and daily current affairs."
        actions={
          <>
            <LinkButton to="/gov/mock" variant="outline">
              <FileText className="h-4 w-4" /> Mock Tests
            </LinkButton>
            <LinkButton to="/gov/pyqs" variant="outline">
              <Target className="h-4 w-4" /> PYQs
            </LinkButton>
          </>
        }
      />

      {loading ? (
        <Spinner />
      ) : (
        <>
          {latest && (
            <Card className="flex flex-col gap-4 border-brand-200 bg-brand-50/50 sm:flex-row sm:items-center sm:justify-between dark:border-brand-500/30 dark:bg-brand-500/10">
              <div className="min-w-0">
                <p className="text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-300">
                  Continue practicing
                </p>
                <h3 className="mt-1 truncate font-bold text-slate-900 dark:text-white">
                  {latest.quiz?.title || `Quiz #${latest.quiz_id}`}
                </h3>
                <p className="mt-0.5 text-sm text-slate-500 dark:text-slate-400">
                  Last score {formatScore(latest.score)}/{latest.total}
                  {latest.accuracy !== null && latest.accuracy !== undefined
                    ? ` Â· ${Math.round(latest.accuracy)}% accuracy`
                    : ''}
                  {latest.mode ? ` Â· ${latest.mode} mode` : ''}
                </p>
              </div>
              <LinkButton to={`/gov/quizzes/${latest.quiz_id}`}>
                Resume <ArrowRight className="h-4 w-4" />
              </LinkButton>
            </Card>
          )}

          <section>
            <SectionHeader
              title="13 Government Exams"
              subtitle="Pick an exam to see its pattern, related quizzes and preparation material."
            />
            {exams && exams.length ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {exams.map((exam) => {
                  const hint = patternHint(exam.pattern);
                  return (
                    <Card
                      key={exam.id}
                      className="flex flex-col gap-3 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="font-bold leading-snug text-slate-900 dark:text-white">
                          {exam.name}
                        </h3>
                        <Badge color="brand">{exam.category}</Badge>
                      </div>
                      {exam.description && (
                        <p className="line-clamp-2 text-sm text-slate-500 dark:text-slate-400">
                          {exam.description}
                        </p>
                      )}
                      {hint && (
                        <p className="text-xs font-medium text-slate-400 dark:text-slate-500">
                          {hint}
                        </p>
                      )}
                      <div className="mt-auto pt-1">
                        <LinkButton
                          to={`/gov/exam/${exam.slug}`}
                          variant="outline"
                          className="w-full"
                        >
                          View
                        </LinkButton>
                      </div>
                    </Card>
                  );
                })}
              </div>
            ) : (
              <EmptyState
                title="No exams found"
                description="Exam data will appear here once published by an administrator."
              />
            )}
          </section>

          <section>
            <SectionHeader
              title="Subjects"
              subtitle="Tap a subject to reveal its topics, then jump straight into a topic quiz."
            />
            {subjects && subjects.length ? (
              <div className="space-y-3">
                {subjects.map((subject) => {
                  const isOpen = openSubject === subject.slug;
                  const topics = subjectTopics[subject.slug];
                  const isLoading = subjectLoading === subject.slug;
                  return (
                    <div
                      key={subject.id}
                      className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900"
                    >
                      <button
                        type="button"
                        onClick={() => void toggleSubject(subject.slug)}
                        aria-expanded={isOpen}
                        className="flex w-full items-center gap-4 px-4 py-4 text-left transition hover:bg-slate-50 sm:px-5 dark:hover:bg-slate-800/60"
                      >
                        <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                          <BookOpen className="h-5 w-5" />
                        </span>
                        <span className="min-w-0 flex-1">
                          <span className="block font-bold text-slate-900 dark:text-white">
                            {subject.title}
                          </span>
                          {subject.description && (
                            <span className="mt-0.5 block truncate text-sm text-slate-500 dark:text-slate-400">
                              {subject.description}
                            </span>
                          )}
                        </span>
                        <Badge color="slate">{subject.topic_count ?? 0} topics</Badge>
                        {isLoading ? (
                          <Loader2 className="h-4 w-4 animate-spin text-slate-400" />
                        ) : (
                          <ChevronDown
                            className={`h-4 w-4 shrink-0 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
                          />
                        )}
                      </button>

                      {isOpen && (
                        <div className="border-t border-slate-100 px-4 py-4 sm:px-5 dark:border-slate-800">
                          {isLoading ? (
                            <Spinner className="py-6" />
                          ) : topics && topics.length ? (
                            <div className="flex flex-wrap gap-2">
                              {topics
                                .slice()
                                .sort((a, b) => a.order - b.order)
                                .map((topic) => (
                                  <Link
                                    key={topic.id}
                                    to={`/gov/topic/${topic.slug}`}
                                    className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:border-brand-400 hover:bg-brand-50 hover:text-brand-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:border-brand-500/50 dark:hover:bg-brand-500/10 dark:hover:text-brand-300"
                                  >
                                    {topic.title}
                                    <ArrowRight className="h-3 w-3" />
                                  </Link>
                                ))}
                            </div>
                          ) : (
                            <p className="text-sm text-slate-500 dark:text-slate-400">
                              No topics available for this subject yet.
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ) : (
              <EmptyState
                title="No subjects found"
                description="Subjects will appear once the curriculum is published."
              />
            )}
          </section>

          <section>
            <SectionHeader title="Quick links" />
            <div className="grid gap-4 sm:grid-cols-3">
              <QuickLink
                to="/gov/mock"
                icon={<FileText className="h-5 w-5" />}
                title="Mock Tests"
                blurb="Full-length timed exams with sectional analysis."
              />
              <QuickLink
                to="/gov/pyqs"
                icon={<Target className="h-5 w-5" />}
                title="Previous Year Questions"
                blurb="Practice real PYQs in practice or exam mode."
              />
              <QuickLink
                to="/gov/current-affairs"
                icon={<Newspaper className="h-5 w-5" />}
                title="Current Affairs"
                blurb="Daily, weekly and monthly updates with AI quizzes."
              />
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function QuickLink({
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
        <span className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white">
          {title}
          <PlayCircle className="h-4 w-4 text-brand-500 opacity-0 transition group-hover:opacity-100" />
        </span>
        <span className="mt-0.5 block text-sm text-slate-500 dark:text-slate-400">{blurb}</span>
      </span>
    </Link>
  );
}
