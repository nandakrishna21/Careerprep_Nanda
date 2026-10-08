import { ReactNode } from 'react';
import { Clock, HelpCircle, MinusCircle } from 'lucide-react';
import { Badge, Card } from './ui';

export type BadgeColor = 'brand' | 'green' | 'amber' | 'rose' | 'slate' | 'violet';

export function difficultyColor(value?: string | null): BadgeColor {
  switch ((value ?? '').toLowerCase()) {
    case 'beginner':
      return 'green';
    case 'intermediate':
      return 'amber';
    case 'advanced':
      return 'rose';
    case 'easy':
      return 'green';
    case 'medium':
      return 'amber';
    case 'hard':
      return 'rose';
    default:
      return 'slate';
  }
}

export interface QuizCardData {
  id: number;
  title: string;
  difficulty?: string | null;
  duration_minutes?: number | null;
  total_questions?: number | null;
  negative_marks?: number | null;
  meta?: Record<string, unknown> | null;
}

export function QuizCard({
  quiz,
  badges,
  actions,
  footer,
  className = '',
}: {
  quiz: QuizCardData;
  badges?: ReactNode;
  actions?: ReactNode;
  footer?: ReactNode;
  className?: string;
}) {
  const meta = quiz.meta ?? {};
  const year = typeof meta.year === 'number' || typeof meta.year === 'string' ? String(meta.year) : null;
  const exam = typeof meta.exam === 'string' ? meta.exam : null;

  return (
    <Card className={`flex flex-col gap-3 ${className}`}>
      <div className="flex items-start justify-between gap-3">
        <h3 className="font-semibold leading-snug text-slate-900 dark:text-white">{quiz.title}</h3>
        <Badge color={difficultyColor(quiz.difficulty)}>{quiz.difficulty || 'Quiz'}</Badge>
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-slate-500 dark:text-slate-400">
        <span className="inline-flex items-center gap-1.5">
          <Clock className="h-3.5 w-3.5" /> {quiz.duration_minutes ?? 'â€”'} min
        </span>
        <span className="inline-flex items-center gap-1.5">
          <HelpCircle className="h-3.5 w-3.5" /> {quiz.total_questions ?? 'â€”'} questions
        </span>
        {typeof quiz.negative_marks === 'number' && quiz.negative_marks > 0 && (
          <span className="inline-flex items-center gap-1.5">
            <MinusCircle className="h-3.5 w-3.5" /> âˆ’{quiz.negative_marks} negative
          </span>
        )}
        {year && <Badge color="violet">{year}</Badge>}
        {exam && <Badge color="slate">{exam}</Badge>}
        {badges}
      </div>

      {actions && <div className="mt-auto flex flex-wrap gap-2 pt-1">{actions}</div>}
      {footer}
    </Card>
  );
}
