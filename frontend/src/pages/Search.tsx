import { FormEvent, useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  BookOpen,
  Briefcase,
  ClipboardList,
  FileText,
  HelpCircle,
  Layers,
  Newspaper,
  Search as SearchIcon,
} from 'lucide-react';
import { errorMessage, get } from '../lib/api';
import type { SearchResponse } from '../lib/types';
import { EmptyState, Spinner } from '../components/ui';

type SectionKey = keyof SearchResponse;

const SECTIONS: { key: SectionKey; label: string; icon: typeof BookOpen; hint: string }[] = [
  { key: 'courses', label: 'Courses', icon: BookOpen, hint: 'Learning paths and subjects' },
  { key: 'topics', label: 'Topics', icon: Layers, hint: 'Individual topics inside courses' },
  { key: 'lessons', label: 'Lessons', icon: FileText, hint: 'Notes, examples and practice' },
  { key: 'quizzes', label: 'Quizzes', icon: HelpCircle, hint: 'Topic, PYQ and AI quizzes' },
  { key: 'mock_tests', label: 'Mock Tests', icon: ClipboardList, hint: 'Full length timed exams' },
  { key: 'jobs', label: 'Jobs', icon: Briefcase, hint: 'Government and IT openings' },
  { key: 'current_affairs', label: 'Current Affairs', icon: Newspaper, hint: 'Daily, weekly and monthly' },
];

const EMPTY: SearchResponse = {
  courses: [],
  topics: [],
  lessons: [],
  quizzes: [],
  mock_tests: [],
  jobs: [],
  current_affairs: [],
};

export default function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const q = searchParams.get('q') ?? '';
  const [draft, setDraft] = useState(q);
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setDraft(q);
  }, [q]);

  useEffect(() => {
    let alive = true;
    if (!q.trim()) {
      setResults(null);
      setLoading(false);
      return;
    }
    (async () => {
      setLoading(true);
      try {
        const data = await get<SearchResponse>('/search', { q });
        if (alive) setResults(data);
      } catch (err) {
        if (alive) {
          toast.error(errorMessage(err));
          setResults(EMPTY);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [q]);

  const submit = (e: FormEvent) => {
    e.preventDefault();
    const next = draft.trim();
    setSearchParams(next ? { q: next } : {});
  };

  const data = results ?? EMPTY;
  const totalResults = SECTIONS.reduce((sum, s) => sum + (data[s.key]?.length ?? 0), 0);

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="min-w-0">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Search</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Find courses, lessons, quizzes, mock tests, jobs and current affairs in one place.
        </p>
      </div>

      <form onSubmit={submit} className="relative max-w-2xl">
        <SearchIcon className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Search for anything — e.g. percentage, SSC CGL, React, data analyst..."
          className="input pl-10 pr-24"
          autoFocus
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg bg-brand-600 px-3.5 py-1.5 text-sm font-semibold text-white transition hover:bg-brand-700"
        >
          Search
        </button>
      </form>

      {loading ? (
        <Spinner />
      ) : !q.trim() ? (
        <EmptyState
          title="Start searching"
          description="Type a topic, exam, course or job above. Results are grouped by content type."
        />
      ) : totalResults === 0 ? (
        <EmptyState
          title={`No results for “${q}”`}
          description="Try a different keyword — shorter queries usually work better."
        />
      ) : (
        <div className="space-y-6">
          {SECTIONS.map((section) => {
            const items = data[section.key] ?? [];
            if (!items.length) return null;
            const Icon = section.icon;
            return (
              <section key={section.key}>
                <div className="mb-3 flex items-center gap-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                    <Icon className="h-4 w-4" />
                  </span>
                  <div className="min-w-0">
                    <h2 className="text-base font-bold text-slate-900 dark:text-white">
                      {section.label}
                      <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-500 dark:bg-slate-800 dark:text-slate-400">
                        {items.length}
                      </span>
                    </h2>
                    <p className="text-xs text-slate-400">{section.hint}</p>
                  </div>
                </div>
                <div className="card divide-y divide-slate-100 overflow-hidden p-0 dark:divide-slate-800">
                  {items.map((item, i) => (
                    <Link
                      key={`${section.key}-${i}`}
                      to={item.url}
                      className="flex items-center gap-3 px-4 py-3 transition hover:bg-slate-50 dark:hover:bg-slate-800/60"
                    >
                      <span className="min-w-0 flex-1">
                        <span className="block truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                          {item.title}
                        </span>
                        {item.subtitle && (
                          <span className="mt-0.5 block truncate text-xs text-slate-500 dark:text-slate-400">
                            {item.subtitle}
                          </span>
                        )}
                      </span>
                      <span className="shrink-0 text-xs font-semibold uppercase tracking-wide text-brand-600 dark:text-brand-400">
                        Open
                      </span>
                    </Link>
                  ))}
                </div>
              </section>
            );
          })}
        </div>
      )}
    </div>
  );
}
