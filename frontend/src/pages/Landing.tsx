import { FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  BookOpen,
  Building2,
  CheckCircle2,
  ClipboardCheck,
  FileText,
  Monitor,
  Search,
  Sparkles,
  Trophy,
} from 'lucide-react';
import { Button } from '../components/ui';
import { LinkButton } from '../components/LinkButton';
import { useAuth } from '../stores/auth';

const features = [
  {
    icon: Sparkles,
    title: 'AI Quiz Generator',
    blurb: 'Turn any topic into a fresh practice quiz in seconds with AI.',
    to: '/ai/quiz-generator',
  },
  {
    icon: ClipboardCheck,
    title: 'Mock Tests',
    blurb: 'Full-length exam simulations with timers, sections and rankings.',
    to: '/gov/mock',
  },
  {
    icon: FileText,
    title: 'Resume Builder',
    blurb: 'ATS-friendly resumes with instant scoring and AI polish.',
    to: '/ai/resume',
  },
  {
    icon: Trophy,
    title: 'Leaderboard',
    blurb: 'Earn XP, unlock achievements and climb the weekly rankings.',
    to: '/leaderboard',
  },
];

const stats = [
  { value: '13+', label: 'Exams' },
  { value: '27', label: 'Subjects & Topics' },
  { value: 'AI-Powered', label: 'Adaptive Learning' },
  { value: '1000+', label: 'Questions' },
];

export default function Landing() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const onSearch = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const q = new FormData(e.currentTarget).get('q') as string | null;
    if (q?.trim()) navigate(`/search?q=${encodeURIComponent(q.trim())}`);
  };

  return (
    <div className="min-h-screen">
      <section className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-brand-50/80 via-brand-50/20 to-transparent dark:from-brand-500/10 dark:via-brand-500/5" />
        <div className="relative mx-auto max-w-7xl px-4 pb-16 pt-14 sm:px-6 sm:pt-20">
          <div className="mx-auto max-w-3xl text-center">
            <span className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-white/70 px-3 py-1 text-xs font-semibold text-brand-700 dark:border-brand-500/30 dark:bg-slate-900/60 dark:text-brand-300">
              <Sparkles className="h-3.5 w-3.5" /> One platform for government exams &amp; IT careers
            </span>
            <h1 className="mt-5 text-3xl font-black leading-tight tracking-tight text-slate-900 sm:text-5xl dark:text-white">
              Crack Government Exams.{' '}
              <span className="bg-gradient-to-r from-brand-600 to-violet-600 bg-clip-text text-transparent">
                Build Your IT Career.
              </span>{' '}
              One Platform.
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-base text-slate-600 sm:text-lg dark:text-slate-300">
              Structured courses, previous year questions, AI-generated quizzes, timed mock tests
              and current affairs â€” everything you need to prepare smarter and get hired.
            </p>

            <form
              onSubmit={onSearch}
              className="mx-auto mt-8 flex w-full max-w-2xl items-center gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-lg shadow-slate-900/5 dark:border-slate-700 dark:bg-slate-900 dark:shadow-black/20"
            >
              <Search className="ml-2 h-5 w-5 shrink-0 text-slate-400" />
              <input
                name="q"
                aria-label="Search"
                placeholder="Search exams, topics, quizzes, jobs..."
                className="min-w-0 flex-1 border-0 bg-transparent px-1 py-2 text-sm outline-none placeholder:text-slate-400 dark:placeholder:text-slate-500"
              />
              <Button type="submit" className="shrink-0">
                Search
              </Button>
            </form>

            <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
              {user ? (
                <LinkButton to="/dashboard">
                  Go to Dashboard <ArrowRight className="h-4 w-4" />
                </LinkButton>
              ) : (
                <>
                  <LinkButton to="/register">Get started free</LinkButton>
                  <LinkButton to="/login" variant="outline">
                    Sign in
                  </LinkButton>
                </>
              )}
            </div>
          </div>
        </div>
      </section>

      <div className="mx-auto max-w-7xl space-y-12 px-4 pb-20 sm:px-6">
        <section className="grid gap-6 md:grid-cols-2">
          <TrackCard
            icon={Building2}
            iconClass="from-amber-500 to-orange-600"
            title="Government Jobs"
            description="Prepare for SSC, Banking, Railway and UPSC exams with structured subjects, topic quizzes, PYQs, mock tests and daily current affairs."
            bullets={[
              '13 exams with detailed patterns',
              'Quant, Reasoning, English & General Awareness',
              'Previous year questions & full mock tests',
            ]}
            cta="Explore"
            to={user ? '/gov' : '/login'}
          />
          <TrackCard
            icon={Monitor}
            iconClass="from-brand-500 to-violet-600"
            title="IT Career"
            description="Follow role-based career paths and hands-on learning paths â€” from Python and DSA to Full Stack, Data and DevOps â€” with lessons, practice and quizzes."
            bullets={[
              '9 career paths with clear roadmaps',
              'Notes, examples, practice & code per lesson',
              'IT mock tests to check your readiness',
            ]}
            cta="Explore"
            to={user ? '/it' : '/login'}
          />
        </section>

        <section>
          <div className="mx-auto mb-8 max-w-2xl text-center">
            <h2 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">
              Everything you need to prepare
            </h2>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
              Powerful tools that keep your preparation focused and measurable.
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((f) => (
              <Link
                key={f.title}
                to={f.to}
                className="group card p-5 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
              >
                <span className="inline-flex rounded-xl bg-brand-50 p-3 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                  <f.icon className="h-5 w-5" />
                </span>
                <h3 className="mt-4 font-bold text-slate-900 dark:text-white">{f.title}</h3>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{f.blurb}</p>
                <span className="mt-3 inline-flex items-center gap-1 text-xs font-semibold text-brand-600 opacity-0 transition group-hover:opacity-100 dark:text-brand-400">
                  Learn more <ArrowRight className="h-3.5 w-3.5" />
                </span>
              </Link>
            ))}
          </div>
        </section>

        <section className="rounded-3xl bg-slate-900 px-6 py-10 sm:px-10 dark:bg-slate-900/70">
          <div className="grid grid-cols-2 gap-8 text-center lg:grid-cols-4">
            {stats.map((s) => (
              <div key={s.label}>
                <p className="text-2xl font-extrabold text-white sm:text-3xl">{s.value}</p>
                <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-400">
                  {s.label}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="overflow-hidden rounded-3xl bg-gradient-to-r from-brand-600 to-violet-600 px-6 py-12 text-center sm:px-10">
          <h2 className="text-2xl font-extrabold text-white sm:text-3xl">
            Start preparing today â€” it is free to join
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-sm text-white/85">
            Create your account to unlock quizzes, mock tests, progress tracking and AI tools.
          </p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            <Link
              to="/register"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-brand-700 shadow-lg transition hover:bg-slate-50"
            >
              Register now <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              to="/login"
              className="inline-flex items-center gap-2 rounded-xl border border-white/40 px-5 py-3 text-sm font-bold text-white transition hover:bg-white/10"
            >
              I already have an account
            </Link>
          </div>
        </section>

        <footer className="border-t border-slate-200 pt-8 text-center text-xs text-slate-400 dark:border-slate-800">
          CareerPrep Hub â€” government exam preparation &amp; IT career readiness in one place.
        </footer>
      </div>
    </div>
  );
}

function TrackCard({
  icon: Icon,
  iconClass,
  title,
  description,
  bullets,
  cta,
  to,
}: {
  icon: typeof Building2;
  iconClass: string;
  title: string;
  description: string;
  bullets: string[];
  cta: string;
  to: string;
}) {
  return (
    <div className="card relative flex flex-col overflow-hidden p-6 sm:p-8">
      <div
        className={`pointer-events-none absolute -right-16 -top-16 h-48 w-48 rounded-full bg-gradient-to-br ${iconClass} opacity-10 blur-2xl`}
      />
      <span
        className={`inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${iconClass} text-white shadow-lg`}
      >
        <Icon className="h-6 w-6" />
      </span>
      <h2 className="mt-4 text-xl font-extrabold text-slate-900 dark:text-white">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{description}</p>
      <ul className="mt-4 space-y-2">
        {bullets.map((b) => (
          <li key={b} className="flex items-start gap-2 text-sm text-slate-500 dark:text-slate-400">
            <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />
            {b}
          </li>
        ))}
      </ul>
      <div className="mt-6 flex items-center gap-3 pt-2">
        <LinkButton to={to}>
          {cta} <ArrowRight className="h-4 w-4" />
        </LinkButton>
        <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400">
          <BookOpen className="h-3.5 w-3.5" /> Structured curriculum
        </span>
      </div>
    </div>
  );
}
