import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { AlertTriangle, ArrowLeft, Clock, HelpCircle, MinusCircle, Trophy } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { MockTest } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { PatternTable } from '../../components/PatternTable';
import { AttemptLite, formatScore, toItems } from '../../components/helpers';
import type { BadgeColor } from '../../components/QuizCard';

const categoryColor: Record<string, BadgeColor> = {
  ssc: 'violet',
  chsl: 'violet',
  banking: 'green',
  rbi: 'amber',
  railway: 'rose',
};

export default function MockTestDetail() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [mock, setMock] = useState<MockTest | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [attempts, setAttempts] = useState<AttemptLite[]>([]);
  const [beginning, setBeginning] = useState(false);

  useEffect(() => {
    if (!slug) return;
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await get<MockTest>(`/mock-tests/${slug}`);
        if (!alive) return;
        setMock(data);
        try {
          const all = await get<unknown>('/attempts/mine');
          if (!alive) return;
          const mine = toItems<AttemptLite>(all).filter((a) => a.quiz_id === data.quiz_id);
          setAttempts(mine);
        } catch {
          if (alive) setAttempts([]);
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

  const begin = () => {
    if (!mock?.quiz_id) {
      toast.error('This mock test is not linked to a quiz yet. Please try again later.');
      return;
    }
    setBeginning(true);
    navigate(`/gov/quizzes/${mock.quiz_id}?mode=exam`);
  };

  if (loading) return <Spinner />;

  if (error || !mock) {
    return (
      <div className="mx-auto max-w-4xl">
        <EmptyState
          title="Mock test not found"
          description={error ?? 'This test may have been unpublished.'}
          action={
            <LinkButton to="/gov/mock" variant="outline">
              <ArrowLeft className="h-4 w-4" /> Back to mock tests
            </LinkButton>
          }
        />
      </div>
    );
  }

  const { sections, exam_pattern: pattern } = mock;
  const patternData: Record<string, unknown> = { ...(pattern ?? {}) };
  delete patternData.sections;
  const hasSections = Array.isArray(sections) && sections.length > 0;

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="flex flex-wrap items-center gap-2">
        <LinkButton to="/gov/mock" variant="ghost" className="!px-3 !py-1.5">
          <ArrowLeft className="h-4 w-4" /> All mock tests
        </LinkButton>
        <Badge color={categoryColor[mock.category] ?? 'slate'}>{mock.category}</Badge>
      </div>

      <PageHeader
        title={mock.title}
        subtitle={mock.description || 'Read the instructions carefully before you begin.'}
        actions={
          <button
            type="button"
            onClick={begin}
            disabled={!mock.quiz_id || beginning}
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-3 text-sm font-bold text-white shadow-sm shadow-brand-600/25 transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Trophy className="h-4 w-4" /> Begin Test
          </button>
        }
      />

      <Card>
        <SectionHeader title="Instructions" subtitle="Read before starting â€” the timer begins immediately." />
        <div className="grid gap-3 sm:grid-cols-3">
          <InfoTile icon={<Clock className="h-4 w-4" />} label="Duration" value={`${mock.duration_minutes} minutes`} />
          <InfoTile
            icon={<HelpCircle className="h-4 w-4" />}
            label="Total questions"
            value={String(mock.total_questions)}
          />
          <InfoTile
            icon={<MinusCircle className="h-4 w-4" />}
            label="Negative marking"
            value={mock.negative_marks > 0 ? `âˆ’${mock.negative_marks} per wrong answer` : 'None'}
          />
        </div>

        {hasSections && (
          <div className="mt-6 overflow-x-auto">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Sections</p>
            <table className="w-full min-w-[420px] text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-700">
                  <th className="py-2 pr-4 font-semibold">Section</th>
                  <th className="py-2 pr-4 font-semibold">Questions</th>
                  <th className="py-2 font-semibold">Marks</th>
                </tr>
              </thead>
              <tbody>
                {sections.map((s) => (
                  <tr
                    key={s.name}
                    className="border-b border-slate-100 text-slate-600 last:border-0 dark:border-slate-800 dark:text-slate-300"
                  >
                    <td className="py-2 pr-4 font-medium text-slate-800 dark:text-slate-100">
                      {s.name}
                    </td>
                    <td className="py-2 pr-4">{s.question_count}</td>
                    <td className="py-2">{s.marks ?? 'â€”'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {Object.keys(patternData).length > 0 && (
          <div className="mt-6 border-t border-slate-100 pt-5 dark:border-slate-800">
            <p className="mb-3 text-xs font-bold uppercase tracking-wide text-slate-400">
              Exam pattern
            </p>
            <PatternTable data={patternData} />
          </div>
        )}

        {!mock.quiz_id && (
          <div className="mt-6 flex items-start gap-2 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800 dark:border-amber-500/30 dark:bg-amber-500/10 dark:text-amber-200">
            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
            This test has not been linked to a quiz yet, so it cannot be started right now.
          </div>
        )}
      </Card>

      <section>
        <SectionHeader title="Your past attempts" subtitle="Scores from your previous runs of this test." />
        {attempts.length ? (
          <div className="space-y-3">
            {attempts.map((a) => (
              <Card key={a.id} className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex flex-wrap items-center gap-3">
                  <Badge color="brand">{a.mode || 'exam'} mode</Badge>
                  <span className="text-sm font-semibold text-slate-800 dark:text-slate-100">
                    {formatScore(a.score)}/{a.total}
                  </span>
                  {typeof a.accuracy === 'number' && (
                    <span className="text-sm text-slate-500 dark:text-slate-400">
                      {Math.round(a.accuracy)}% accuracy
                    </span>
                  )}
                  <span className="text-xs text-slate-400">{a.created_at ? new Date(a.created_at).toLocaleString() : ''}</span>
                </div>
                <LinkButton to={`/gov/quizzes/${a.quiz_id}`} variant="outline">
                  View report
                </LinkButton>
              </Card>
            ))}
          </div>
        ) : (
          <EmptyState
            title="No attempts yet"
            description="Finish this mock test and your scorecard will appear here."
          />
        )}
      </section>
    </div>
  );
}

function InfoTile({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-800/40">
      <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-brand-600 shadow-sm dark:bg-slate-900 dark:text-brand-300">
        {icon}
      </span>
      <span className="min-w-0">
        <span className="block text-xs text-slate-400">{label}</span>
        <span className="block truncate text-sm font-bold text-slate-800 dark:text-slate-100">
          {value}
        </span>
      </span>
    </div>
  );
}
