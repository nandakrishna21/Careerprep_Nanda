import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, BookOpen, ExternalLink, GraduationCap, Newspaper, PlayCircle, Search, Sparkles, Terminal } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { Badge, Card, EmptyState } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import {
  CAREER_TRACKS,
  TRACK_LEVELS,
  type TrackLevel,
  type TrackResource,
} from '../../lib/careerTracks';

const KIND_ICON: Record<TrackResource['kind'], LucideIcon> = {
  Course: GraduationCap,
  Docs: BookOpen,
  Video: PlayCircle,
  Practice: Terminal,
  Reading: Newspaper,
};

const LEVEL_COLOR: Record<TrackLevel, 'green' | 'amber' | 'rose'> = {
  Beginner: 'green',
  Intermediate: 'amber',
  Advanced: 'rose',
};

export default function TrackResources() {
  const { slug = '' } = useParams();
  const track = CAREER_TRACKS[slug];
  const [level, setLevel] = useState<'all' | TrackLevel>('all');
  const [query, setQuery] = useState('');

  const items = useMemo(() => {
    if (!track) return [];
    const q = query.trim().toLowerCase();
    return track.resources.filter((r) => {
      if (level !== 'all' && r.level !== level) return false;
      if (!q) return true;
      return (
        r.name.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.tags.some((tag) => tag.toLowerCase().includes(q))
      );
    });
  }, [track, level, query]);

  if (!track) {
    return (
      <div className="mx-auto max-w-3xl pt-10">
        <EmptyState
          title="Unknown track"
          description="This learning track does not exist yet. Pick one from the left panel."
          action={
            <Link
              to="/dashboard"
              className="rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            >
              Back to dashboard
            </Link>
          }
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <PageHeader
        title={`${track.shortTitle} — Free Resources`}
        subtitle={`Every free website, course and docs link to learn ${track.title} from scratch to advance. Filter by level or search a skill.`}
        actions={
          <Link
            to={`/tracks/${track.slug}`}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <ArrowLeft className="h-4 w-4" /> Roadmap
          </Link>
        }
      />

      <Card className="flex items-start gap-3 border-emerald-200 bg-emerald-50/60 p-4 dark:border-emerald-500/30 dark:bg-emerald-500/10">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-300">
          <Sparkles className="h-4 w-4" />
        </span>
        <p className="text-sm text-emerald-800 dark:text-emerald-200">
          <b>100% free to use.</b> Every link opens a free resource — docs, courses and
          practice sites. Some offer optional paid certificates; you never need them to learn.
        </p>
      </Card>

      <div className="flex flex-wrap items-center gap-2">
        {TRACK_LEVELS.map((l) => (
          <button
            key={l}
            type="button"
            aria-pressed={level === l}
            onClick={() => setLevel(l)}
            className={`rounded-xl px-3.5 py-2 text-sm font-semibold transition ${
              level === l
                ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            {l === 'all' ? 'All levels' : l}
          </button>
        ))}
        <div className="relative ml-auto w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search skill, site or topic..."
            className="input pl-9"
          />
        </div>
      </div>

      <SectionHeader
        title="Free websites & courses"
        subtitle={`${items.length} of ${track.resources.length} resources`}
      />

      {items.length ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((r) => {
            const Icon = KIND_ICON[r.kind];
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
                  <div className="flex flex-wrap justify-end gap-1.5">
                    <Badge color={LEVEL_COLOR[r.level]}>{r.level}</Badge>
                    <Badge color="slate">{r.kind}</Badge>
                  </div>
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
          description="Try a broader keyword like RAG, SQL, Docker, prompting or system design."
          action={
            <button
              type="button"
              onClick={() => {
                setQuery('');
                setLevel('all');
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
