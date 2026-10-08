import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { Clock, FileText, HelpCircle, MinusCircle, Users } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { MockTest } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { toItems } from '../../components/helpers';
import type { BadgeColor } from '../../components/QuizCard';

const categoryColor: Record<string, BadgeColor> = {
  ssc: 'violet',
  chsl: 'violet',
  banking: 'green',
  rbi: 'amber',
  railway: 'rose',
};

export default function MockTests() {
  const [items, setItems] = useState<MockTest[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const data = await get<unknown>('/mock-tests');
        if (alive) setItems(toItems<MockTest>(data));
      } catch (err) {
        if (alive) {
          toast.error(errorMessage(err));
          setItems([]);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title="Mock Tests"
        subtitle="Full-length exam simulations with sectional breakdown, timers and all-India style ranking."
        actions={
          <LinkButton to="/gov/pyqs" variant="outline">
            Practice PYQs
          </LinkButton>
        }
      />

      <SectionHeader title="Available tests" subtitle="Choose a test to read its instructions before you begin." />

      {loading ? (
        <Spinner />
      ) : items && items.length ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((mock) => (
            <Card
              key={mock.id}
              className="flex flex-col gap-3 transition hover:-translate-y-0.5 hover:border-brand-300 dark:hover:border-brand-500/40"
            >
              <div className="flex items-start justify-between gap-2">
                <h3 className="font-bold leading-snug text-slate-900 dark:text-white">
                  {mock.title}
                </h3>
                <Badge color={categoryColor[mock.category] ?? 'slate'}>{mock.category}</Badge>
              </div>
              {mock.description && (
                <p className="line-clamp-2 text-sm text-slate-500 dark:text-slate-400">
                  {mock.description}
                </p>
              )}
              <div className="flex flex-wrap gap-x-4 gap-y-1.5 text-xs text-slate-500 dark:text-slate-400">
                <span className="inline-flex items-center gap-1.5">
                  <Clock className="h-3.5 w-3.5" /> {mock.duration_minutes} min
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <HelpCircle className="h-3.5 w-3.5" /> {mock.total_questions} questions
                </span>
                {mock.negative_marks > 0 && (
                  <span className="inline-flex items-center gap-1.5">
                    <MinusCircle className="h-3.5 w-3.5" /> âˆ’{mock.negative_marks}
                  </span>
                )}
                {typeof mock.attempts_count === 'number' && (
                  <span className="inline-flex items-center gap-1.5">
                    <Users className="h-3.5 w-3.5" /> {mock.attempts_count} attempts
                  </span>
                )}
              </div>
              {mock.sections && mock.sections.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {mock.sections.map((s) => (
                    <Badge key={s.name} color="slate">
                      {s.name}
                    </Badge>
                  ))}
                </div>
              )}
              <div className="mt-auto pt-1">
                <LinkButton to={`/gov/mock/${mock.slug}`} className="w-full">
                  <FileText className="h-4 w-4" /> View &amp; start
                </LinkButton>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No mock tests published yet"
          description="Mock tests seeded by an administrator will show up here."
          action={
            <LinkButton to="/gov" variant="outline">
              Back to Government Hub
            </LinkButton>
          }
        />
      )}
    </div>
  );
}
