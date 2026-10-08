import { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  CheckCircle2,
  History,
  MessageSquare,
  RotateCcw,
  Send,
  Sparkles,
  XCircle,
} from 'lucide-react';
import { errorMessage, get, post } from '../../lib/api';
import type { InterviewSession, InterviewTurn } from '../../lib/types';
import { Badge, Button, Card, EmptyState, Select, Spinner, Textarea } from '../../components/ui';
import { formatDate, toItems } from '../../components/helpers';

const ROLES = [
  'Python Developer',
  'Backend Developer',
  'Full Stack Developer',
  'Data Analyst',
  'Technical Support',
  'KPO Analyst',
];

function aiErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err) && err.response?.status === 503) {
    return 'AI not configured — set GEMINI_API_KEY';
  }
  const msg = errorMessage(err);
  if (/not configured/i.test(msg)) return 'AI not configured — set GEMINI_API_KEY';
  return msg;
}

interface Evaluation {
  score: number;
  strengths: string[];
  weaknesses: string[];
  improved_answer: string;
  next_question: string | null;
  progress?: { answered: number; overall_score: number };
}

interface Exchange {
  question: string;
  answer: string;
  evaluation: Evaluation;
}

type Phase = 'setup' | 'active' | 'done';

export default function AiInterview() {
  const [phase, setPhase] = useState<Phase>('setup');
  const [role, setRole] = useState(ROLES[0]);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [question, setQuestion] = useState('');
  const [exchanges, setExchanges] = useState<Exchange[]>([]);
  const [answer, setAnswer] = useState('');
  const [evaluating, setEvaluating] = useState(false);
  const [overallScore, setOverallScore] = useState<number | null>(null);
  const [finalSummary, setFinalSummary] = useState<{ strengths: string[]; weaknesses: string[] } | null>(null);
  const [finalTurns, setFinalTurns] = useState<InterviewTurn[]>([]);

  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [expandedTurns, setExpandedTurns] = useState<Record<number, InterviewTurn[]>>({});
  const [loadingTurns, setLoadingTurns] = useState<number | null>(null);

  const loadSessions = useCallback(async () => {
    try {
      const data = await get<unknown>('/ai/interview/sessions');
      setSessions(toItems<InterviewSession>(data));
    } catch {
      setSessions([]);
    }
  }, []);

  useEffect(() => {
    void loadSessions();
  }, [loadSessions]);

  const start = async () => {
    setEvaluating(true);
    try {
      const res = await post<{ session_id: number; question: string; question_number: number }>(
        '/ai/interview/start',
        { role }
      );
      setSessionId(res.session_id);
      setQuestion(res.question);
      setExchanges([]);
      setAnswer('');
      setOverallScore(null);
      setFinalSummary(null);
      setFinalTurns([]);
      setPhase('active');
      void loadSessions();
    } catch (err) {
      toast.error(aiErrorMessage(err));
    } finally {
      setEvaluating(false);
    }
  };

  const submitAnswer = async () => {
    if (!sessionId || !answer.trim() || evaluating) return;
    const submitted = answer.trim();
    setEvaluating(true);
    setAnswer('');
    try {
      const res = await post<Evaluation>('/ai/interview/answer', {
        session_id: sessionId,
        answer: submitted,
      });
      setExchanges((prev) => [...prev, { question, answer: submitted, evaluation: res }]);
      if (res.next_question) {
        setQuestion(res.next_question);
        setOverallScore(res.progress?.overall_score ?? null);
      } else {
        setPhase('done');
        try {
          const detail = await get<InterviewSession>(`/ai/interview/sessions/${sessionId}`);
          setOverallScore(detail.overall_score);
          setFinalSummary({
            strengths: detail.summary?.strengths ?? [],
            weaknesses: detail.summary?.weaknesses ?? [],
          });
          setFinalTurns(detail.turns ?? []);
        } catch {
          setOverallScore(res.progress?.overall_score ?? null);
        }
        void loadSessions();
      }
    } catch (err) {
      toast.error(aiErrorMessage(err));
      setAnswer(submitted);
    } finally {
      setEvaluating(false);
    }
  };

  const restart = () => {
    setPhase('setup');
    setSessionId(null);
    setQuestion('');
    setExchanges([]);
    setAnswer('');
    setOverallScore(null);
    setFinalSummary(null);
    setFinalTurns([]);
    void loadSessions();
  };

  const toggleSession = async (id: number) => {
    if (expandedId === id) {
      setExpandedId(null);
      return;
    }
    setExpandedId(id);
    if (expandedTurns[id]) return;
    setLoadingTurns(id);
    try {
      const detail = await get<InterviewSession>(`/ai/interview/sessions/${id}`);
      setExpandedTurns((prev) => ({ ...prev, [id]: detail.turns ?? [] }));
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setLoadingTurns(null);
    }
  };

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Mock Interview</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Practice role-specific interviews and get scored feedback on every answer.
          </p>
        </div>
        {phase !== 'setup' && (
          <Button variant="outline" onClick={restart}>
            <RotateCcw className="h-4 w-4" /> New session
          </Button>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <div className="min-w-0 space-y-4">
          {phase === 'setup' && (
            <Card className="p-6 sm:p-8">
              <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-600 dark:bg-brand-500/10 dark:text-brand-300">
                <Sparkles className="h-6 w-6" />
              </span>
              <h2 className="mt-4 text-lg font-bold text-slate-900 dark:text-white">Choose your target role</h2>
              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                The interviewer will ask role-specific questions and score each answer out of 10.
              </p>
              <div className="mt-5 max-w-md">
                <label className="label" htmlFor="role">
                  Role
                </label>
                <Select id="role" value={role} onChange={(e) => setRole(e.target.value)}>
                  {ROLES.map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </Select>
              </div>
              <div className="mt-6">
                <Button onClick={() => void start()} loading={evaluating}>
                  <MessageSquare className="h-4 w-4" /> Start interview
                </Button>
              </div>
            </Card>
          )}

          {phase !== 'setup' && (
            <Card className="flex flex-col gap-4">
              <div className="flex flex-wrap items-center gap-2 border-b border-slate-100 pb-3 dark:border-slate-800">
                <Badge color="brand">{role}</Badge>
                <Badge color="slate">{exchanges.length} answered</Badge>
                {overallScore !== null && (
                  <Badge color="green">Avg {Math.round(overallScore * 10) / 10}/10</Badge>
                )}
                <span className="ml-auto text-xs text-slate-400">
                  {phase === 'done' ? 'Completed' : 'In progress'}
                </span>
              </div>

              <div className="max-h-[52vh] space-y-4 overflow-y-auto pr-1">
                {exchanges.map((ex, i) => (
                  <div key={i} className="space-y-3">
                    <Bubble side="ai">
                      <span className="text-xs font-bold uppercase tracking-wide text-brand-500">
                        Interviewer · Q{i + 1}
                      </span>
                      <p className="mt-1">{ex.question}</p>
                    </Bubble>
                    <Bubble side="user">{ex.answer}</Bubble>

                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-800/40">
                      <div className="flex items-center justify-between gap-2">
                        <p className="text-xs font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                          Evaluation
                        </p>
                        <span className="rounded-full bg-brand-100 px-2.5 py-0.5 text-xs font-black text-brand-700 dark:bg-brand-500/15 dark:text-brand-300">
                          {ex.evaluation.score}/10
                        </span>
                      </div>
                      <div className="mt-3 grid gap-3 sm:grid-cols-2">
                        <div>
                          <p className="mb-1 flex items-center gap-1 text-xs font-bold text-emerald-600 dark:text-emerald-400">
                            <CheckCircle2 className="h-3.5 w-3.5" /> Strengths
                          </p>
                          {ex.evaluation.strengths?.length ? (
                            <ul className="space-y-1">
                              {ex.evaluation.strengths.map((s, si) => (
                                <li key={si} className="text-xs text-slate-600 dark:text-slate-300">
                                  • {s}
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="text-xs text-slate-400">None listed</p>
                          )}
                        </div>
                        <div>
                          <p className="mb-1 flex items-center gap-1 text-xs font-bold text-rose-600 dark:text-rose-400">
                            <XCircle className="h-3.5 w-3.5" /> Weaknesses
                          </p>
                          {ex.evaluation.weaknesses?.length ? (
                            <ul className="space-y-1">
                              {ex.evaluation.weaknesses.map((w, wi) => (
                                <li key={wi} className="text-xs text-slate-600 dark:text-slate-300">
                                  • {w}
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="text-xs text-slate-400">None listed</p>
                          )}
                        </div>
                      </div>
                      {ex.evaluation.improved_answer && (
                        <blockquote className="mt-3 border-l-2 border-brand-400 bg-white px-3 py-2 text-xs italic leading-5 text-slate-600 dark:border-brand-500 dark:bg-slate-900 dark:text-slate-300">
                          <span className="not-italic font-semibold text-brand-600 dark:text-brand-400">
                            Improved answer:
                          </span>{' '}
                          {ex.evaluation.improved_answer}
                        </blockquote>
                      )}
                    </div>
                  </div>
                ))}

                {phase === 'active' && (
                  <Bubble side="ai">
                    <span className="text-xs font-bold uppercase tracking-wide text-brand-500">
                      Interviewer · Q{exchanges.length + 1}
                    </span>
                    <p className="mt-1">{question}</p>
                  </Bubble>
                )}

                {evaluating && phase === 'active' && exchanges.length > 0 && (
                  <div className="flex items-center gap-2 pl-1 text-sm font-semibold text-slate-500 dark:text-slate-400">
                    <Spinner className="py-0" />
                    Evaluating…
                  </div>
                )}
              </div>

              {phase === 'active' && (
                <div className="border-t border-slate-100 pt-4 dark:border-slate-800">
                  <label className="label" htmlFor="answer">
                    Your answer
                  </label>
                  <Textarea
                    id="answer"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Type your answer…"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) void submitAnswer();
                    }}
                  />
                  <div className="mt-3 flex items-center justify-between gap-3">
                    <p className="text-xs text-slate-400">Ctrl/Cmd + Enter to send</p>
                    <Button onClick={() => void submitAnswer()} loading={evaluating} disabled={!answer.trim()}>
                      <Send className="h-4 w-4" /> Submit answer
                    </Button>
                  </div>
                </div>
              )}
            </Card>
          )}

          {phase === 'done' && (
            <Card className="border-brand-200 bg-gradient-to-br from-brand-50 to-white dark:border-brand-500/30 dark:from-brand-500/10 dark:to-slate-900">
              <div className="flex flex-col items-center gap-4 text-center sm:flex-row sm:text-left">
                <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-violet-600 text-3xl font-black text-white shadow-lg shadow-brand-600/30">
                  {overallScore !== null ? Math.round(overallScore * 10) / 10 : '–'}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-300">
                    Interview complete · overall score
                  </p>
                  <p className="mt-1 text-2xl font-bold text-slate-900 dark:text-white">
                    {overallScore !== null ? `${Math.round(overallScore * 10) / 10} / 10` : 'Score unavailable'}
                  </p>
                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                    {role} · {exchanges.length} questions answered
                  </p>
                </div>
                <Button onClick={restart}>
                  <RotateCcw className="h-4 w-4" /> Restart
                </Button>
              </div>

              {(finalSummary?.strengths?.length || finalSummary?.weaknesses?.length) && (
                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-xl bg-emerald-50 p-4 dark:bg-emerald-500/10">
                    <p className="mb-1 text-xs font-bold uppercase tracking-wide text-emerald-600 dark:text-emerald-400">
                      Strengths
                    </p>
                    <ul className="space-y-1 text-sm text-slate-700 dark:text-slate-300">
                      {(finalSummary?.strengths ?? []).map((s, i) => (
                        <li key={i}>• {s}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="rounded-xl bg-rose-50 p-4 dark:bg-rose-500/10">
                    <p className="mb-1 text-xs font-bold uppercase tracking-wide text-rose-600 dark:text-rose-400">
                      Weaknesses
                    </p>
                    <ul className="space-y-1 text-sm text-slate-700 dark:text-slate-300">
                      {(finalSummary?.weaknesses ?? []).map((w, i) => (
                        <li key={i}>• {w}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {finalTurns.length > 0 && (
                <div className="mt-5">
                  <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Turn summary</p>
                  <div className="space-y-2">
                    {finalTurns.map((t, i) => (
                      <div
                        key={t.id}
                        className="flex items-start gap-3 rounded-xl border border-slate-200 bg-white p-3 text-sm dark:border-slate-800 dark:bg-slate-900"
                      >
                        <span className="shrink-0 text-xs font-bold text-brand-600 dark:text-brand-400">
                          Q{i + 1}
                        </span>
                        <span className="min-w-0 flex-1 text-slate-700 dark:text-slate-300">{t.question}</span>
                        <span className="shrink-0 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                          {t.score}/10
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          )}
        </div>

        <aside className="space-y-4">
          <Card className="p-4">
            <p className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-slate-400">
              <History className="h-4 w-4" /> Session history
            </p>
            {sessions.length === 0 ? (
              <p className="text-sm text-slate-400">No past sessions yet. Start your first interview above.</p>
            ) : (
              <div className="space-y-2">
                {sessions.map((s) => (
                  <div
                    key={s.id}
                    className="rounded-xl border border-slate-200 dark:border-slate-800"
                  >
                    <button
                      type="button"
                      onClick={() => void toggleSession(s.id)}
                      className="flex w-full items-center gap-2 px-3 py-2.5 text-left transition hover:bg-slate-50 dark:hover:bg-slate-800/60"
                    >
                      <span className="min-w-0 flex-1">
                        <span className="block truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                          {s.role}
                        </span>
                        <span className="block text-xs text-slate-400">{formatDate(s.created_at)}</span>
                      </span>
                      <Badge color={s.status === 'completed' ? 'green' : 'amber'}>{s.status}</Badge>
                      {s.overall_score !== null && s.overall_score !== undefined && (
                        <span className="text-xs font-black text-brand-600 dark:text-brand-400">
                          {Math.round(s.overall_score * 10) / 10}
                        </span>
                      )}
                    </button>
                    {expandedId === s.id && (
                      <div className="border-t border-slate-100 px-3 py-3 dark:border-slate-800">
                        {loadingTurns === s.id ? (
                          <Spinner className="py-4" />
                        ) : (expandedTurns[s.id] ?? []).length ? (
                          <ol className="space-y-2">
                            {(expandedTurns[s.id] ?? []).map((t, i) => (
                              <li key={t.id} className="text-xs">
                                <p className="font-semibold text-slate-700 dark:text-slate-200">
                                  Q{i + 1}. {t.question}
                                </p>
                                <p className="mt-0.5 line-clamp-2 text-slate-500 dark:text-slate-400">
                                  {t.user_answer}
                                </p>
                                <p className="mt-0.5 font-bold text-brand-600 dark:text-brand-400">
                                  Score {t.score}/10
                                </p>
                              </li>
                            ))}
                          </ol>
                        ) : (
                          <p className="text-xs text-slate-400">No recorded turns.</p>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card className="p-4">
            <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Tips</p>
            <ul className="space-y-1.5 text-xs leading-5 text-slate-500 dark:text-slate-400">
              <li>• Structure answers with situation, task, action and result.</li>
              <li>• Quantify impact wherever possible (%, time saved, scale).</li>
              <li>• Review the improved answer after each turn and iterate.</li>
            </ul>
          </Card>
        </aside>
      </div>

      {phase === 'setup' && sessions.length === 0 && !evaluating && (
        <EmptyState
          title="No interviews yet"
          description="Pick a role and start a session — you will get a score and feedback for every answer."
        />
      )}
    </div>
  );
}

function Bubble({ side, children }: { side: 'ai' | 'user'; children: React.ReactNode }) {
  if (side === 'ai') {
    return (
      <div className="flex gap-3">
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-100 text-brand-600 dark:bg-brand-500/15 dark:text-brand-300">
          <MessageSquare className="h-4 w-4" />
        </span>
        <div className="max-w-[85%] rounded-2xl rounded-tl-sm border border-slate-200 bg-white px-4 py-3 text-sm leading-6 text-slate-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
          {children}
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-end">
      <div className="max-w-[85%] rounded-2xl rounded-tr-sm bg-brand-600 px-4 py-3 text-sm leading-6 text-white shadow-sm">
        {children}
      </div>
    </div>
  );
}
