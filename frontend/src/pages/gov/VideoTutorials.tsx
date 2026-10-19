import { useMemo, useState } from 'react';
import { ExternalLink, Search, Youtube } from 'lucide-react';
import { Badge, Card, EmptyState } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { GOVT_TUTORIALS, type GovtTutorial } from '../../lib/govtTutorials';

const LANGS = [
  { key: 'all', label: 'All' },
  { key: 'telugu', label: 'తెలుగు · Telugu' },
  { key: 'english', label: 'English' },
] as const;

type LangFilter = (typeof LANGS)[number]['key'];

const LANG_BADGE: Record<GovtTutorial['language'], { label: string; color: 'violet' | 'brand' | 'green' }> = {
  telugu: { label: 'Telugu', color: 'violet' },
  english: { label: 'English', color: 'brand' },
  both: { label: 'Telugu + English', color: 'green' },
};

export default function VideoTutorials() {
  const [lang, setLang] = useState<LangFilter>('all');
  const [query, setQuery] = useState('');

  const items = useMemo(() => {
    const q = query.trim().toLowerCase();
    return GOVT_TUTORIALS.filter((t) => {
      const langOk = lang === 'all' || t.language === lang || t.language === 'both';
      if (!langOk) return false;
      if (!q) return true;
      return (
        t.title.toLowerCase().includes(q) ||
        t.channel.toLowerCase().includes(q) ||
        t.tags.some((tag) => tag.toLowerCase().includes(q))
      );
    });
  }, [lang, query]);

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <PageHeader
        title="Video Tutorials"
        subtitle="Free YouTube explanation classes for government exams — curated channels and playlists in Telugu and English."
      />

      <div className="flex flex-wrap items-center gap-2">
        {LANGS.map((l) => (
          <button
            key={l.key}
            type="button"
            aria-pressed={lang === l.key}
            onClick={() => setLang(l.key)}
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              lang === l.key
                ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
            }`}
          >
            {l.label}
          </button>
        ))}
        <div className="relative ml-auto w-full sm:w-64">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search channel or exam..."
            className="input pl-9"
          />
        </div>
      </div>

      <SectionHeader
        title="Channels & playlists"
        subtitle={`${items.length} of ${GOVT_TUTORIALS.length} resources`}
      />

      {items.length ? (
        <div className="grid gap-4 sm:grid-cols-2">
          {items.map((t) => (
            <Card
              key={t.id}
              className="flex flex-col gap-3 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
            >
              <div className="flex flex-wrap items-center gap-2">
                <Badge color={LANG_BADGE[t.language].color}>{LANG_BADGE[t.language].label}</Badge>
                <Badge color="slate">{t.kind === 'playlist' ? 'Playlist' : 'Channel'}</Badge>
              </div>
              <div>
                <h3 className="font-bold text-slate-900 dark:text-white">{t.title}</h3>
                <p className="text-xs font-medium text-slate-400">{t.channel}</p>
              </div>
              <p className="line-clamp-3 text-sm text-slate-500 dark:text-slate-400">{t.description}</p>
              <div className="flex flex-wrap gap-1.5">
                {t.tags.map((tag) => (
                  <span
                    key={tag}
                    className="rounded-lg bg-slate-100 px-2 py-0.5 text-[11px] font-semibold text-slate-500 dark:bg-slate-800 dark:text-slate-400"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <a
                href={t.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-auto inline-flex items-center justify-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-rose-700"
              >
                <Youtube className="h-4 w-4" /> Watch on YouTube
                <ExternalLink className="h-3.5 w-3.5" />
              </a>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No matching tutorials"
          description="Try a different language tab or clear the search — for example “SSC”, “Banking” or “TSPSC”."
          action={
            <button
              type="button"
              onClick={() => {
                setLang('all');
                setQuery('');
              }}
              className="mt-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-brand-700"
            >
              Show all
            </button>
          }
        />
      )}
    </div>
  );
}
