import { FormEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import { CheckCircle2, ExternalLink, RotateCcw, Sparkles, XCircle } from 'lucide-react';
import { errorMessage, post } from '../../lib/api';
import type { AiQuestion } from '../../lib/types';
import { Badge, Button, Card, EmptyState, Input, Select, Spinner } from '../../components/ui';

const LETTERS = ['A', 'B', 'C', 'D'];

function aiErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err) && err.response?.status === 503) {
    return 'AI not configured — set GEMINI_API_KEY';
  }
  const msg = errorMessage(err);
  if (/not configured/i.test(msg)) return 'AI not configured — set GEMINI_API_KEY';
  return msg;
}

interface GenerateResponse {
  questions: AiQuestion[];
  quiz_id?: number;
}

export default function AiQuizGenerator() {
  const [topic, setTopic] = useState('');
  const [difficulty, setDifficulty] = useState('intermediate');
  const [count, setCount] = useState(10);
  const [save, setSave] = useState(false);
  const [title, setTitle] = useState('');

  const [questions, setQuestions] = useState<AiQuestion[]>([]);
  const [quizId, setQuizId] = useState<number | null>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [loading, setLoading] = useState(false);
  const [hasGenerated, setHasGenerated] = useState(false);

  const generate = async (e?: FormEvent) => {
    e?.preventDefault();
    if (!topic.trim()) {
      toast.error('Enter a topic to generate questions from.');
      return;
    }
    const safeCount = Math.min(30, Math.max(1, Math.round(count) || 1));
    setLoading(true);
    setHasGenerated(true);
    try {
      const res = await post<GenerateResponse>('/ai/quiz-generate', {
        topic: topic.trim(),
        difficulty,
        count: safeCount,
        save,
        title: save ? title.trim() || undefined : undefined,
      });
      setQuestions(res.questions ?? []);
      setQuizId(res.quiz_id ?? null);
      setAnswers({});
      if (save && res.quiz_id) toast.success('Quiz saved to your library');
    } catch (err) {
      toast.error(aiErrorMessage(err));
      setQuestions([]);
      setQuizId(null);
    } finally {
      setLoading(false);
    }
  };

  const pick = (qIndex: number, optionIndex: number) => {
    setAnswers((prev) => (prev[qIndex] !== undefined ? prev : { ...prev, [qIndex]: optionIndex }));
  };

  const answeredCount = Object.keys(answers).length;
  const correctCount = questions.filter((q, i) => answers[i] === q.correct_index).length;
  const wrongCount = answeredCount - correctCount;

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Quiz Generator</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Generate a custom quiz on any topic, answer instantly and learn from explanations.
          </p>
        </div>
        <Link
          to="/ai/resume"
          className="text-sm font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400"
        >
          Try the resume builder →
        </Link>
      </div>

      <Card>
        <form onSubmit={generate} className="grid gap-4 lg:grid-cols-[2fr_1fr_1fr]">
          <div>
            <label className="label" htmlFor="topic">
              Topic
            </label>
            <Input
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Percentage, Python decorators, SQL joins"
            />
          </div>
          <div>
            <label className="label" htmlFor="difficulty">
              Difficulty
            </label>
            <Select id="difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </Select>
          </div>
          <div>
            <label className="label" htmlFor="count">
              Questions (1–30)
            </label>
            <Input
              id="count"
              type="number"
              min={1}
              max={30}
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
            />
          </div>

          <div className="lg:col-span-3 flex flex-wrap items-end gap-4">
            <label className="flex cursor-pointer items-center gap-2 text-sm font-medium text-slate-600 dark:text-slate-300">
              <input
                type="checkbox"
                checked={save}
                onChange={(e) => setSave(e.target.checked)}
                className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
              />
              Save to my quizzes
            </label>
            {save && (
              <div className="min-w-[220px] flex-1">
                <label className="label" htmlFor="save-title">
                  Quiz title
                </label>
                <Input
                  id="save-title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Saved quiz title"
                />
              </div>
            )}
            <Button type="submit" loading={loading}>
              <Sparkles className="h-4 w-4" /> Generate quiz
            </Button>
          </div>
        </form>
      </Card>

      {loading ? (
        <Card className="flex flex-col items-center gap-3 py-14">
          <Spinner className="py-0" />
          <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
            Generating your quiz with AI…
          </p>
        </Card>
      ) : !hasGenerated ? (
        <EmptyState
          title="No quiz yet"
          description="Pick a topic, choose a difficulty and hit Generate to create a fresh set of questions."
        />
      ) : questions.length === 0 ? (
        <EmptyState
          title="No questions returned"
          description="The AI did not return any questions. Try a broader topic or a different difficulty."
        />
      ) : (
        <>
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex flex-wrap gap-2">
              <Badge color="green">{correctCount} correct</Badge>
              <Badge color="rose">{wrongCount} wrong</Badge>
              <Badge color="slate">
                {answeredCount}/{questions.length} answered
              </Badge>
              <Badge color="brand">{difficulty}</Badge>
            </div>
            <div className="ml-auto flex flex-wrap gap-2">
              {quizId && (
                <Link
                  to={`/gov/quizzes/${quizId}`}
                  className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
                >
                  <ExternalLink className="h-4 w-4" /> Open saved quiz
                </Link>
              )}
              <Button variant="secondary" onClick={() => void generate()}>
                <RotateCcw className="h-4 w-4" /> Regenerate
              </Button>
            </div>
          </div>

          <div className="space-y-4">
            {questions.map((q, qi) => {
              const chosen = answers[qi];
              const revealed = chosen !== undefined;
              return (
                <Card key={qi}>
                  <div className="flex items-start gap-3">
                    <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-brand-600 text-xs font-bold text-white">
                      {qi + 1}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="font-semibold leading-6 text-slate-900 dark:text-white">{q.question_text}</p>
                      <div className="mt-3 grid gap-2">
                        {q.options.map((opt, oi) => {
                          const isCorrect = oi === q.correct_index;
                          const isChosen = chosen === oi;
                          let cls =
                            'border-slate-200 bg-white text-slate-700 hover:border-brand-300 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-brand-500/40';
                          if (revealed && isCorrect) {
                            cls =
                              'border-emerald-500 bg-emerald-50 text-emerald-800 dark:border-emerald-500/60 dark:bg-emerald-500/10 dark:text-emerald-200';
                          } else if (revealed && isChosen) {
                            cls =
                              'border-rose-500 bg-rose-50 text-rose-800 dark:border-rose-500/60 dark:bg-rose-500/10 dark:text-rose-200';
                          } else if (revealed) {
                            cls =
                              'border-slate-200 bg-white text-slate-400 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-500';
                          }
                          return (
                            <button
                              key={oi}
                              type="button"
                              disabled={revealed}
                              onClick={() => pick(qi, oi)}
                              className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-left text-sm transition ${cls}`}
                            >
                              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-current text-xs font-bold opacity-70">
                                {LETTERS[oi] ?? oi + 1}
                              </span>
                              <span className="min-w-0 flex-1">{opt}</span>
                              {revealed && isCorrect && <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-500" />}
                              {revealed && isChosen && !isCorrect && (
                                <XCircle className="h-4 w-4 shrink-0 text-rose-500" />
                              )}
                            </button>
                          );
                        })}
                      </div>
                      {revealed && q.explanation && (
                        <blockquote className="mt-3 border-l-2 border-brand-400 bg-brand-50/60 px-3 py-2 text-sm italic text-slate-600 dark:border-brand-500 dark:bg-brand-500/10 dark:text-slate-300">
                          {q.explanation}
                        </blockquote>
                      )}
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-slate-500 dark:text-slate-400">
              {answeredCount === questions.length
                ? 'All questions answered — regenerate for a fresh set.'
                : `${questions.length - answeredCount} questions left.`}
            </p>
            <Button variant="secondary" onClick={() => void generate()}>
              <RotateCcw className="h-4 w-4" /> Regenerate
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
