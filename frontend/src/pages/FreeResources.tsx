import { useMemo, useState } from 'react';
import {
  BookOpen,
  Code2,
  ExternalLink,
  GraduationCap,
  Landmark,
  MessagesSquare,
  Search,
  Sparkles,
  Target,
} from 'lucide-react';
import { Badge, Card, EmptyState } from '../components/ui';
import { PageHeader, SectionHeader } from '../components/SectionHeader';
import {
  CATEGORY_LABEL,
  FREE_RESOURCES,
  RESOURCE_CATEGORIES,
  type ResourceCategory,
} from '../lib/freeResources';

type CategoryFilter = 'all' | ResourceCategory;

const CATEGORY_ICON: Record<ResourceCategory, typeof Landmark> = {
  government: Landmark,
  practice: Target,
  courses: GraduationCap,
  coding: Code2,
  interview: MessagesSquare,
  books: BookOpen,
};

const CATEGORY_COLOR: Record<ResourceCategory, 'brand' | 'green' | 'amber' | 'violet' | 'rose' | 'slate'> = {
  government: 'brand',
  practice: 'green',
  courses: 'amber',
  coding: 'violet',
  interview: 'rose',
  books: 'slate',
};

export default function FreeResources() {
  const [category, setCategory] = useState<CategoryFilter>('all');
  const [query, setQuery] = useState('');

  const items = useMemo(() => {
    const q = query.trim().toLowerCase();
    return FREE_RESOURCES.filter((r) => {
      if (category !== 'all' && r.category !== category) return false;
      if (!q) return true;
      return (
        r.name.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.tags.some((tag) => tag.toLowerCase().includes(q))
      );
    });
  }, [category, query]);

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <PageHeader
        title="Free Resources"
        subtitle="Hand-picked websites that cost nothing — official government portals, practice tests, free courses and interview material. No paywalls, no hidden sign-ups."
      />

      <Card className="flex items-start gap-3 border-emerald-200 bg-emerald-50/60 p-4 dark:border-emerald-500/30 dark:bg-emerald-500/10">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300">
          <Sparkles className="h-4 w-4" />
        </span>
        <p className="text-sm text-emerald-800 dark:text-emerald-200">
          <b>100% free to use.</b> Every link here opens a free resource. A few sites offer optional
          paid courses — you never need them to practise or apply.
        </p>
      </Card>

      <div className="flex flex-wrap items-center gap-2">
        {RESOURCE_CATEGORIES.map((c) => (
          <button
            key={c.key}
            type="button"
            aria-pressed={category === c.key}
            onClick={() => setCategory(c.key)}
            className={`rounded-xl px-3.5 py-2 text-sm font-semibold transition ${
              category === c.key
                ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            {c.label}
          </button>
        ))}
        <div className="relative ml-auto w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search exam, skill or site..."
            className="input pl-9"
          />
        </div>
      </div>

      <SectionHeader
        title="Free websites"
        subtitle={`${items.length} of ${FREE_RESOURCES.length} resources`}
      />

      {items.length ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((r) => {
            const Icon = CATEGORY_ICON[r.category];
            return (
              <a
                key={r.url}
                href={r.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group"
              >
                <Card className="flex h-full flex-col gap-3 transition group-hover:-translate-y-0.5 group-hover:border-brand-300 dark:group-hover:border-brand-500/40">
                  <div className="flex items-start justify-between gap-2">
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                      <Icon className="h-5 w-5" />
                    </span>
                    <Badge color={CATEGORY_COLOR[r.category]}>{CATEGORY_LABEL[r.category]}</Badge>
                  </div>
                  <div className="flex-1">
                    <h3 className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white">
                      {r.name}
                      <ExternalLink className="h-3.5 w-3.5 shrink-0 text-slate-400 transition group-hover:text-brand-500" />
                    </h3>
                    <p className="mt-1 text-sm leading-relaxed text-slate-500 dark:text-slate-400">
                      {r.description}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {r.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-md bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-500 dark:bg-slate-800 dark:text-slate-400"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </Card>
              </a>
            );
          })}
        </div>
      ) : (
        <EmptyState
          title="Nothing matched that search"
          description="Try a broader keyword like SSC, banking, DSA or resume."
          action={
            <button
              type="button"
              onClick={() => {
                setQuery('');
                setCategory('all');
              }}
              className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            >
              Clear filters
            </button>
          }
        />
      )}
    </div>
  );
}
