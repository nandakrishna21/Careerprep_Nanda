import { FormEvent, useEffect, useRef, useState } from 'react';
import { Bot, FileText, ImageIcon, Paperclip, Send, Sparkles, User as UserIcon, X } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import toast from 'react-hot-toast';
import api, { errorMessage } from '../../lib/api';
import { Card, Spinner } from '../../components/ui';
import { PageHeader } from '../../components/SectionHeader';

type AttachmentMeta = { name: string; isImage: boolean; url?: string };

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  attachments?: AttachmentMeta[];
};

const SUGGESTIONS = [
  'Explain recursion with a simple example',
  'Explain P&L and Balance Sheet for beginners',
  'How does OOP work in simple terms?',
  'Give me 5 MCQs on Indian Polity with answers',
];

const MAX_FILES = 5;
const MAX_FILE_BYTES = 10 * 1024 * 1024;
const MAX_TOTAL_BYTES = 18 * 1024 * 1024;
const ALLOWED_EXT = /\.(png|jpe?g|webp|heic|heif|pdf|txt|md|csv|json)$/i;
const CHAT_TIMEOUT_MS = 120_000;
const API_BASE = (import.meta.env.VITE_API_BASE_URL as string) || '/api';

async function streamChat(message: string, onDelta: (delta: string) => void): Promise<void> {
  const token = localStorage.getItem('cp_token');
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), CHAT_TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE}/ai/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ message }),
      signal: controller.signal,
    });
    if (res.status === 401) {
      localStorage.removeItem('cp_token');
      window.location.href = '/login';
      throw new Error('Session expired. Please sign in again.');
    }
    if (!res.ok || !res.body) {
      let detail = 'Could not reach the AI service. Please retry.';
      try {
        const data = (await res.json()) as { detail?: string };
        if (typeof data?.detail === 'string') detail = data.detail;
      } catch {
        /* non-JSON error body */
      }
      throw new Error(detail);
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      let boundary = buffer.indexOf('\n\n');
      while (boundary !== -1) {
        const event = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        for (const line of event.split('\n')) {
          if (!line.startsWith('data:')) continue;
          const payload = line.slice(5).trim();
          if (!payload) continue;
          if (payload === '[DONE]') return;
          let parsed: { delta?: string; error?: string };
          try {
            parsed = JSON.parse(payload) as { delta?: string; error?: string };
          } catch {
            continue;
          }
          if (parsed.error) throw new Error(parsed.error);
          if (parsed.delta) onDelta(parsed.delta);
        }
        boundary = buffer.indexOf('\n\n');
      }
    }
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new Error('The answer took too long. Please try a shorter question.');
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

export default function GeminiChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [pending, setPending] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const objectUrls = useRef<string[]>([]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(
    () => () => {
      objectUrls.current.forEach((url) => URL.revokeObjectURL(url));
    },
    [],
  );

  const addFiles = (list: FileList | null) => {
    const incoming = Array.from(list ?? []);
    if (!incoming.length) return;
    const next = [...pending];
    let total = next.reduce((sum, file) => sum + file.size, 0);
    for (const file of incoming) {
      if (next.length >= MAX_FILES) {
        toast.error(`You can attach up to ${MAX_FILES} files.`);
        break;
      }
      if (!ALLOWED_EXT.test(file.name) && !file.type.startsWith('image/')) {
        toast.error(`${file.name}: attach images, PDF, TXT, MD, CSV or JSON files.`);
        continue;
      }
      if (file.size > MAX_FILE_BYTES) {
        toast.error(`${file.name} is larger than 10 MB.`);
        continue;
      }
      if (total + file.size > MAX_TOTAL_BYTES) {
        toast.error('Attachments exceed 18 MB in total.');
        break;
      }
      next.push(file);
      total += file.size;
    }
    setPending(next);
  };

  const send = async (text: string) => {
    const message = text.trim();
    if (loading || (!message && pending.length === 0)) return;
    const filesToSend = pending;
    const attachments: AttachmentMeta[] = filesToSend.map((file) => {
      const isImage = file.type.startsWith('image/');
      let url: string | undefined;
      if (isImage) {
        url = URL.createObjectURL(file);
        objectUrls.current.push(url);
      }
      return { name: file.name, isImage, url };
    });
    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: 'user',
        content: message || 'Explain this attachment.',
        attachments: attachments.length ? attachments : undefined,
      },
    ]);
    setInput('');
    setPending([]);
    setLoading(true);
    try {
      if (filesToSend.length) {
        const form = new FormData();
        form.append('message', message);
        filesToSend.forEach((file) => form.append('files', file));
        const res = await api.post<{ response: string }>('/ai/chat/attachments', form, {
          timeout: CHAT_TIMEOUT_MS,
        });
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: res.data.response || 'No response from Gemini.',
          },
        ]);
      } else {
        const assistantId = crypto.randomUUID();
        let added = false;
        const ensureBubble = () => {
          if (added) return;
          added = true;
          setMessages((prev) => [
            ...prev,
            { id: assistantId, role: 'assistant', content: '' },
          ]);
        };
        const appendDelta = (delta: string) =>
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + delta } : m)),
          );
        try {
          await streamChat(message, (delta) => {
            ensureBubble();
            appendDelta(delta);
          });
          if (!added) {
            const res = await api.post<{ response: string }>(
              '/ai/chat',
              { message },
              { timeout: CHAT_TIMEOUT_MS },
            );
            setMessages((prev) => [
              ...prev,
              {
                id: crypto.randomUUID(),
                role: 'assistant',
                content: res.data.response || 'No response from Gemini.',
              },
            ]);
          }
        } catch (err) {
          if (!added) throw err;
          toast.error(
            err instanceof Error ? err.message : 'The answer was cut off. Please retry.',
          );
        }
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    void send(input);
  };

  return (
    <div className="mx-auto flex h-[calc(100dvh-8rem)] max-w-4xl flex-col gap-4">
      <PageHeader
        title="Gemini Chat"
        subtitle="Ask anything and get clear, step-by-step explanations — attach images or PDFs for help with problems, notes and diagrams."
      />

      <Card className="flex flex-1 flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          {messages.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center text-center">
              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-violet-600 text-white">
                <Sparkles className="h-6 w-6" />
              </div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white">
                What can I explain for you?
              </h2>
              <p className="mt-1 max-w-md text-sm text-slate-500 dark:text-slate-400">
                Ask a question, or attach a photo of a problem, PDF notes or a diagram — Gemini will
                read it and explain.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-2">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => void send(s)}
                    className="rounded-xl border border-slate-200 px-3 py-1.5 text-sm text-slate-600 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex items-start gap-3 ${m.role === 'user' ? 'justify-end' : ''}`}
                >
                  {m.role === 'assistant' && (
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 text-white">
                      <Bot className="h-4 w-4" />
                    </div>
                  )}
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                      m.role === 'user'
                        ? 'bg-brand-600 text-white'
                        : 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100'
                    }`}
                  >
                    {m.attachments && m.attachments.length > 0 && (
                      <div className="mb-2 flex flex-wrap gap-2">
                        {m.attachments.map((file) =>
                          file.isImage && file.url ? (
                            <img
                              key={`${m.id}-${file.name}`}
                              src={file.url}
                              alt={file.name}
                              className="h-24 w-24 rounded-lg object-cover"
                            />
                          ) : (
                            <span
                              key={`${m.id}-${file.name}`}
                              className="inline-flex max-w-[14rem] items-center gap-1.5 rounded-lg bg-white/20 px-2 py-1 text-xs font-medium"
                            >
                              <FileText className="h-3.5 w-3.5 shrink-0" />
                              <span className="truncate">{file.name}</span>
                            </span>
                          ),
                        )}
                      </div>
                    )}
                    {m.role === 'assistant' ? (
                      <div className="prose prose-sm max-w-none prose-slate dark:prose-invert prose-p:my-2 prose-pre:my-3">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                      </div>
                    ) : (
                      <p className="whitespace-pre-wrap">{m.content}</p>
                    )}
                  </div>
                  {m.role === 'user' && (
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-200 text-slate-600 dark:bg-slate-700 dark:text-slate-200">
                      <UserIcon className="h-4 w-4" />
                    </div>
                  )}
                </div>
              ))}
              {loading && messages[messages.length - 1]?.role !== 'assistant' && (
                <div className="flex items-start gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 text-white">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div className="flex items-center gap-2 rounded-2xl bg-slate-100 px-4 py-3 dark:bg-slate-800">
                    <Spinner className="h-4 w-4" />
                    <span className="text-sm text-slate-500 dark:text-slate-400">Thinking…</span>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        <div className="border-t border-slate-200 dark:border-slate-800">
          {pending.length > 0 && (
            <div className="flex flex-wrap gap-2 px-3 pt-3">
              {pending.map((file, index) => (
                <span
                  key={`${file.name}-${index}`}
                  className="inline-flex items-center gap-2 rounded-lg bg-slate-100 px-2.5 py-1.5 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                >
                  {file.type.startsWith('image/') ? (
                    <ImageIcon className="h-3.5 w-3.5 shrink-0" />
                  ) : (
                    <FileText className="h-3.5 w-3.5 shrink-0" />
                  )}
                  <span className="max-w-[12rem] truncate">{file.name}</span>
                  <button
                    type="button"
                    onClick={() => setPending((prev) => prev.filter((_, i) => i !== index))}
                    className="rounded p-0.5 hover:bg-slate-200 dark:hover:bg-slate-700"
                    aria-label={`Remove ${file.name}`}
                  >
                    <X className="h-3.5 w-3.5" />
                  </button>
                </span>
              ))}
            </div>
          )}
          <form onSubmit={handleSubmit} className="flex items-center gap-2 p-3">
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept="image/*,.pdf,.txt,.md,.csv,.json"
              className="hidden"
              onChange={(e) => {
                addFiles(e.target.files);
                e.target.value = '';
              }}
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={loading || pending.length >= MAX_FILES}
              className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-slate-300 text-slate-500 transition hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-800"
              title="Attach images or files"
              aria-label="Attach images or files"
            >
              <Paperclip className="h-4 w-4" />
            </button>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me to explain anything, or attach a file..."
              className="input flex-1"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || (!input.trim() && pending.length === 0)}
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:opacity-60"
            >
              <Send className="h-4 w-4" /> Send
            </button>
          </form>
        </div>
      </Card>
    </div>
  );
}
