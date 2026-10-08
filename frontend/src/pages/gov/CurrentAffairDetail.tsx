import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowLeft, BookOpen, CalendarDays, CheckCircle2, ListChecks, PlayCircle, Sparkles, XCircle } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { CurrentAffair } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { formatDate } from '../../components/helpers';

interface Mcq {
  question: string;
  options: string[];
  correct_index: number;
  explanation?: string;
}

type TabKey = 'notes' | 'questions' | 'mcqs';

export default function CurrentAffairDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [ca, setCa] = useState<CurrentAffair | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<TabKey>('notes');
  const [picked, setPicked] = useState<Record<number, number | null>>({});

  useEffect(() => {
    if (!slug) return;
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await get<CurrentAffair>(`/current-affairs/${slug}`);
        if (alive) setCa(data);
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

  const ai = ca?.ai_content;
  const tabs = useMemo(() => {
    const list: { key: TabKey; label: string; icon: typeof BookOpen }[] = [];
    if (ai?.revision_notes) list.push({ key: 'notes', label: 'Revision Notes', icon: BookOpen });
    if (ai?.short_questions?.length) list.push({ key: 'questions', label: 'Short Questions', icon: ListChecks });
    if (ai?.mcqs?.length) list.push({ key: 'mcqs', label: 'AI MCQs', icon: Sparkles });
    return list;
  }, [ai]);

  useEffect(() => {
    if (tabs.length && !tabs.some((t) => t.key === tab)) setTab(tabs[0].key);
  }, [tabs, tab]);

  if (loading) return <Spinner />;

  if (error || !ca) {
    return (
      <div className="mx-auto max-w-4xl">
        <EmptyState
          title="Current affair not found"
          description={error ?? 'This edition may have been unpublished.'}
          action={
            <LinkButton to="/gov/current-affairs" variant="outline">
              <ArrowLeft className="h-4 w-4" /> Back to current affairs
            </LinkButton>
          }
        />
      </div>
    );
  }

  const paragraphs = (ca.content ?? '')
    .split(/\n{2,}/)
    .map((p) => p.trim())
    .filter(Boolean);
  const mcqs = (ai?.mcqs ?? []) as Mcq[];

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="flex flex-wrap items-center gap-2">
        <LinkButton to="/gov/current-affairs" variant="ghost" className="!px-3 !py-1.5">
          <ArrowLeft className="h-4 w-4" /> All editions
        </LinkButton>
        <Badge color="brand">{ca.period}</Badge>
        <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400">
          <CalendarDays className="h-3.5 w-3.5" /> {formatDate(ca.date)}
        </span>
      </div>

      <PageHeader title={ca.title} subtitle={ca.summary || undefined} />

      <Card>
        <div className="space-y-4">
          {paragraphs.length ? (
            paragraphs.map((p, i) => (
              <p key={i} className="whitespace-pre-line text-sm leading-7 text-slate-600 dark:text-slate-300">
                {p}
              </p>
            ))
          ) : (
            <p className="text-sm text-slate-400">No article content available.</p>
          )}
        </div>
        {typeof ai?.quiz_id === 'number' && (
          <div className="mt-6 border-t border-slate-100 pt-5 dark:border-slate-800">
            <LinkButton to={`/gov/quizzes/${ai.quiz_id}`}>
              <PlayCircle className="h-4 w-4" /> Take the quiz
            </LinkButton>
          </div>
        )}
      </Card>

      {tabs.length > 0 && (
        <section>
          <SectionHeader title="Study kit" subtitle="AI-generated revision material for this edition." />
          <div className="mb-4 flex flex-wrap gap-2" role="tablist" aria-label="Study kit sections">
            {tabs.map((t) => (
              <button
                key={t.key}
                type="button"
                role="tab"
                aria-selected={tab === t.key}
                onClick={() => setTab(t.key)}
                className={`inline-flex items-center gap-1.5 rounded-xl px-4 py-2 text-sm font-semibold transition ${
                  tab === t.key
                    ? 'bg-brand-600 text-white shadow-sm shadow-brand-600/25'
                    : 'border border-slate-300 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
                }`}
              >
                <t.icon className="h-4 w-4" /> {t.label}
              </button>
            ))}
          </div>

          <Card>
            {tab === 'notes' && <p className="whitespace-pre-line text-sm leading-7 text-slate-600 dark:text-slate-300">{ai?.revision_notes}</p>}

            {tab === 'questions' && (
              <ol className="space-y-3">
                {(ai?.short_questions ?? []).map((q, i) => (
                  <li key={i} className="flex gap-3 text-sm text-slate-600 dark:text-slate-300">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand-100 text-xs font-bold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300">
                      {i + 1}
                    </span>
                    <span className="whitespace-pre-line">{q}</span>
                  </li>
                ))}
              </ol>
            )}

            {tab === 'mcqs' && (
              <div className="space-y-6">
                {mcqs.map((mcq, i) => {
                  const selected = picked[i] ?? null;
                  const answered = selected !== null;
                  return (
                    <div key={i} className="rounded-2xl border border-slate-200 p-4 dark:border-slate-800">
                      <p className="font-semibold text-slate-800 dark:text-slate-100">
                        <span className="mr-2 text-brand-600 dark:text-brand-400">Q{i + 1}.</span>
                        {mcq.question}
                      </p>
                      <div className="mt-3 grid gap-2">
                        {(mcq.options ?? []).map((opt, oi) => {
                          const isCorrect = oi === mcq.correct_index;
                          const isSelected = selected === oi;
                          let cls =
                            'border-slate-200 bg-white text-slate-700 hover:border-brand-400 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-brand-500/50';
                          if (answered && isCorrect) {
                            cls =
                              'border-emerald-500 bg-emerald-50 text-emerald-800 dark:border-emerald-500/60 dark:bg-emerald-500/10 dark:text-emerald-200';
                          } else if (answered && isSelected && !isCorrect) {
                            cls =
                              'border-rose-500 bg-rose-50 text-rose-800 dark:border-rose-500/60 dark:bg-rose-500/10 dark:text-rose-200';
                          }
                          return (
                            <button
                              key={oi}
                              type="button"
                              disabled={answered}
                              onClick={() => setPicked((prev) => ({ ...prev, [i]: oi }))}
                              className={`flex items-center gap-3 rounded-xl border px-3.5 py-2.5 text-left text-sm transition ${cls} disabled:cursor-default`}
                            >
                              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-current text-xs font-bold opacity-70">
                                {String.fromCharCode(65 + oi)}
                              </span>
                              <span className="min-w-0 flex-1">{opt}</span>
                              {answered && isCorrect && <CheckCircle2 className="h-4 w-4 shrink-0" />}
                              {answered && isSelected && !isCorrect && <XCircle className="h-4 w-4 shrink-0" />}
                            </button>
                          );
                        })}
                      </div>
                      {answered && mcq.explanation && (
                        <blockquote className="mt-3 border-l-2 border-brand-400 bg-brand-50/60 px-3 py-2 text-sm italic text-slate-600 dark:border-brand-500 dark:bg-brand-500/10 dark:text-slate-300">
                          {mcq.explanation}
                        </blockquote>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </Card>
        </section>
      )}

      {!tabs.length && (
        <EmptyState
          title="Study kit not generated yet"
          description="Revision notes, short questions and MCQs will appear here once AI content is generated for this edition."
        />
      )}
    </div>
  );
}
