import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ArrowLeft, FileText, Target } from 'lucide-react';
import { errorMessage, get } from '../../lib/api';
import type { Course, Exam, QuizMeta } from '../../lib/types';
import { Badge, Card, EmptyState, Spinner } from '../../components/ui';
import { PageHeader, SectionHeader } from '../../components/SectionHeader';
import { LinkButton } from '../../components/LinkButton';
import { QuizCard } from '../../components/QuizCard';
import { PatternTable } from '../../components/PatternTable';

interface ExamDetail extends Exam {
  quizzes?: QuizMeta[] | null;
  courses?: Course[] | null;
}

export default function GovExamDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [exam, setExam] = useState<ExamDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await get<ExamDetail>(`/exams/${slug}`);
        if (alive) setExam(data);
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

  if (loading) return <Spinner />;

  if (error || !exam) {
    return (
      <div className="mx-auto max-w-7xl space-y-6">
        <EmptyState
          title="Exam not found"
          description={error ?? 'This exam may have been removed or is not published yet.'}
          action={
            <LinkButton to="/gov" variant="outline">
              <ArrowLeft className="h-4 w-4" /> Back to Government Hub
            </LinkButton>
          }
        />
      </div>
    );
  }

  const quizzes = exam.quizzes ?? [];

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <PageHeader
        title={exam.name}
        subtitle={exam.description || undefined}
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

      <div className="flex flex-wrap items-center gap-2">
        <LinkButton to="/gov" variant="ghost" className="!px-3 !py-1.5">
          <ArrowLeft className="h-4 w-4" /> All exams
        </LinkButton>
        <Badge color="brand">{exam.category}</Badge>
        {exam.courses && exam.courses.length > 0 && (
          <span className="text-xs text-slate-400">
            Related: {exam.courses.map((c) => c.title).join(', ')}
          </span>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <SectionHeader title="Exam pattern" subtitle="Key details straight from the syllabus." />
          <PatternTable data={exam.pattern} />
        </Card>

        <Card>
          <SectionHeader title="Prepare for this exam" />
          <div className="space-y-3 text-sm text-slate-600 dark:text-slate-300">
            <p>
              Attempt full-length mock tests under real exam conditions, then review the
              section-wise analysis to find weak areas.
            </p>
            <div className="flex flex-col gap-2">
              <LinkButton to="/gov/mock" className="w-full">
                <FileText className="h-4 w-4" /> Start a mock test
              </LinkButton>
              <LinkButton to="/gov/pyqs" variant="outline" className="w-full">
                <Target className="h-4 w-4" /> Practice PYQs
              </LinkButton>
              <LinkButton to="/gov/current-affairs" variant="outline" className="w-full">
                Daily current affairs
              </LinkButton>
            </div>
          </div>
        </Card>
      </div>

      <section>
        <SectionHeader
          title="Related quizzes"
          subtitle={`${quizzes.length} quiz${quizzes.length === 1 ? '' : 'zes'} linked to ${exam.name}.`}
        />
        {quizzes.length ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {quizzes.map((quiz) => (
              <QuizCard key={quiz.id} quiz={quiz} />
            ))}
          </div>
        ) : (
          <EmptyState
            title="No quizzes yet"
            description="Quizzes for this exam will appear as soon as they are published."
          />
        )}
      </section>
    </div>
  );
}
