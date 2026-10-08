import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArrowRight,
  BarChart3,
  Briefcase,
  Brain,
  Code2,
  Cpu,
  FileText,
  Headphones,
  Layers,
  Layout,
  Monitor,
  Rocket,
  Server,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Course } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { toItems } from '../../components/helpers';

const CAREER_ICONS: Record<string, LucideIcon> = {
  'Python Developer': Code2,
  'Backend Developer': Server,
  'Frontend Developer': Layout,
  'Full Stack Developer': Layers,
  'Data Analyst': BarChart3,
  'Data Scientist': Brain,
  'Technical Support Engineer': Headphones,
  'KPO Analyst': Briefcase,
  'DevOps Engineer': Rocket,
};

const CAREER_BLURBS: Record<string, string> = {
  'Python Developer': 'Master Python fundamentals, APIs and automation to land your first dev role.',
  'Backend Developer': 'Build fast, secure APIs with FastAPI, databases and authentication.',
  'Frontend Developer': 'Craft responsive interfaces with HTML, CSS, JavaScript and React.',
  'Full Stack Developer': 'Combine frontend and backend skills to ship complete products.',
  'Data Analyst': 'Turn raw data into insight with SQL, spreadsheets and visualisation.',
  'Data Scientist': 'Apply statistics, Python and ML techniques to solve real problems.',
  'Technical Support Engineer': 'Resolve incidents, network issues and customer escalations.',
  'KPO Analyst': 'Research, analyse and deliver business insights for global teams.',
  'DevOps Engineer': 'Automate delivery with CI/CD, containers, cloud and monitoring.',
};

const DEFAULT_ICON: LucideIcon = Cpu;

export default function ItDashboard() {
  const [courses, setCourses] = useState<Course[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const data = await get<unknown>('/courses', { category: 'it' });
        if (alive) setCourses(toItems<Course>(data));
      } catch (err) {
        if (alive) {
          toast.error(errorMessage(err));
          setCourses([]);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const all = courses ?? [];
  const careerPaths = all.filter((c) => c.career_path === true);
  const learningPaths = all.filter((c) => c.career_path !== true);

  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <section className="relative overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-br from-brand-600 via-brand-600 to-violet-600 p-6 sm:p-10 dark:border-slate-800">
        <div className="pointer-events-none absolute -right-10 -top-10 h-56 w-56 rounded-full bg-white/10 blur-2xl" />
        <div className="relative max-w-2xl">
          <span className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold text-white">
            <Monitor className="h-3.5 w-3.5" /> IT Career Hub
          </span>
          <h1 className="mt-4 text-3xl font-black tracking-tight text-white sm:text-4xl">
            Build Your IT Career
          </h1>
          <p className="mt-3 text-sm leading-6 text-white/85 sm:text-base">
            Pick a role, follow a structured roadmap of topics and lessons, and prove your skills
            with quizzes and mock tests â€” from Python basics to DevOps.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              to={learningPaths[0] ? `/it/learn/${learningPaths[0].slug}` : '/it'}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-brand-700 shadow-sm transition hover:bg-slate-100"
            >
              Start learning <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              to="/it/mock"
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/40 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-white/10"
            >
              <FileText className="h-4 w-4" /> IT Mock Tests
            </Link>
          </div>
        </div>
      </section>

      {loading ? (
        <Spinner />
      ) : (
        <>
          <section>
            <SectionHeader
              title="Career Paths"
              subtitle="Role-based roadmaps with the exact topics, lessons and quizzes you need."
            />
            {careerPaths.length ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {careerPaths.map((course) => {
                  const Icon = CAREER_ICONS[course.title] ?? DEFAULT_ICON;
                  return (
                    <Card
                      key={course.id}
                      className="flex flex-col gap-3 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
                    >
                      <div className="flex items-start gap-3">
                        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 text-white shadow-md shadow-brand-600/20">
                          <Icon className="h-5 w-5" />
                        </span>
                        <div className="min-w-0">
                          <h3 className="font-bold text-slate-900 dark:text-white">
                            {course.title}
                          </h3>
                          <Badge color="slate">{course.level || 'All levels'}</Badge>
                        </div>
                      </div>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        {CAREER_BLURBS[course.title] || course.description}
                      </p>
                      <div className="mt-auto flex items-center justify-between pt-2">
                        <span className="text-xs font-medium text-slate-400">
                          {course.topic_count ?? course.topics?.length ?? 0} topics
                        </span>
                        <LinkButton to={`/it/path/${course.slug}`} variant="outline">
                          Explore <ArrowRight className="h-4 w-4" />
                        </LinkButton>
                      </div>
                    </Card>
                  );
                })}
              </div>
            ) : (
              <EmptyState
                title="Career paths are being prepared"
                description="Role-based career paths will appear here as soon as they are published."
              />
            )}
          </section>

          <section>
            <SectionHeader
              title="Learning Paths"
              subtitle="Skill-focused tracks with notes, examples, practice problems and code."
            />
            {learningPaths.length ? (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
                {learningPaths.map((course) => (
                  <Card
                    key={course.id}
                    className="flex flex-col gap-3 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                        <Code2 className="h-4 w-4" />
                      </span>
                      <Badge color={course.level === 'beginner' ? 'green' : 'amber'}>
                        {course.level || 'All levels'}
                      </Badge>
                    </div>
                    <h3 className="font-bold text-slate-900 dark:text-white">{course.title}</h3>
                    {course.description && (
                      <p className="line-clamp-3 text-sm text-slate-500 dark:text-slate-400">
                        {course.description}
                      </p>
                    )}
                    <div className="mt-auto flex items-center justify-between pt-2">
                      <span className="text-xs font-medium text-slate-400">
                        {course.topic_count ?? course.topics?.length ?? 0} topics
                      </span>
                      <LinkButton
                        to={`/it/learn/${course.slug}`}
                        variant="outline"
                        className="!px-3 !py-2"
                      >
                        Learn
                      </LinkButton>
                    </div>
                  </Card>
                ))}
              </div>
            ) : (
              <EmptyState
                title="No learning paths yet"
                description="Skill tracks such as Python, SQL and DSA will appear here once published."
              />
            )}
          </section>

          <section className="flex flex-col items-start justify-between gap-4 rounded-3xl border border-slate-200 bg-white p-6 sm:flex-row sm:items-center sm:p-8 dark:border-slate-800 dark:bg-slate-900">
            <div>
              <h2 className="text-lg font-extrabold text-slate-900 dark:text-white">
                Ready to test your skills?
              </h2>
              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                Attempt IT mock tests to benchmark yourself against real interview expectations.
              </p>
            </div>
            <LinkButton to="/it/mock">
              Go to IT Mock Tests <ArrowRight className="h-4 w-4" />
            </LinkButton>
          </section>
        </>
      )}
    </div>
  );
}
