import { DragEvent, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  ChevronDown,
  FileText,
  Sparkles,
  Target,
  UploadCloud,
  X,
} from 'lucide-react';
import api, { errorMessage } from '../../lib/api';
import { Badge, Button, Card, EmptyState, Spinner } from '../../components/ui';

const MAX_BYTES = 5 * 1024 * 1024;

interface AnalyzeResult {
  ats_score: number;
  missing_keywords: string[];
  suggestions: string[];
  job_recommendations: { title: string; reason: string }[];
  extracted_text: string;
}

function scoreColor(score: number): string {
  if (score >= 80) return '#10b981';
  if (score >= 60) return '#f59e0b';
  return '#f43f5e';
}

export default function AiResumeAnalyze() {
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [showText, setShowText] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const accept = (picked: File | null | undefined) => {
    if (!picked) return;
    if (picked.type !== 'application/pdf' && !picked.name.toLowerCase().endsWith('.pdf')) {
      toast.error('Only PDF files are supported.');
      return;
    }
    if (picked.size > MAX_BYTES) {
      toast.error('File is too large — maximum size is 5MB.');
      return;
    }
    setFile(picked);
    setResult(null);
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
    accept(e.dataTransfer.files?.[0]);
  };

  const analyze = async () => {
    if (!file) {
      toast.error('Choose a PDF resume first.');
      return;
    }
    setUploading(true);
    setResult(null);
    try {
      const form = new FormData();
      form.append('file', file);
      const res = await api.post<AnalyzeResult>('/resumes/analyze-file', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
      toast.success(`ATS score: ${res.data.ats_score}`);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 503) {
        toast.error('AI not configured — set GEMINI_API_KEY');
      } else {
        const msg = errorMessage(err);
        toast.error(/not configured/i.test(msg) ? 'AI not configured — set GEMINI_API_KEY' : msg);
      }
    } finally {
      setUploading(false);
    }
  };

  const score = result ? Math.max(0, Math.min(100, result.ats_score ?? 0)) : 0;
  const color = scoreColor(score);
  const radius = 56;
  const circumference = 2 * Math.PI * radius;

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Resume ATS Analyzer</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Upload a PDF resume to get an ATS score, missing keywords, suggestions and job matches.
          </p>
        </div>
        <Link
          to="/ai/resume"
          className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
        >
          <Sparkles className="h-4 w-4" /> Open resume builder
        </Link>
      </div>

      <Card>
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          className={`flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed px-6 py-12 text-center transition ${
            dragging
              ? 'border-brand-500 bg-brand-50 dark:bg-brand-500/10'
              : 'border-slate-300 bg-slate-50 dark:border-slate-700 dark:bg-slate-800/40'
          }`}
        >
          <span className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-100 text-brand-600 dark:bg-brand-500/15 dark:text-brand-300">
            <UploadCloud className="h-7 w-7" />
          </span>
          <div>
            <p className="text-sm font-bold text-slate-800 dark:text-slate-100">
              Drag & drop your resume here
            </p>
            <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">PDF only · up to 5MB</p>
          </div>
          <input
            ref={inputRef}
            type="file"
            accept="application/pdf,.pdf"
            className="hidden"
            onChange={(e) => accept(e.target.files?.[0])}
          />
          <Button variant="outline" onClick={() => inputRef.current?.click()}>
            <FileText className="h-4 w-4" /> Browse files
          </Button>

          {file && (
            <div className="mt-1 flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 dark:border-slate-700 dark:bg-slate-900">
              <FileText className="h-4 w-4 shrink-0 text-brand-500" />
              <span className="max-w-[220px] truncate text-xs font-semibold text-slate-700 dark:text-slate-200">
                {file.name}
              </span>
              <span className="text-[11px] text-slate-400">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
              <button
                type="button"
                aria-label="Remove file"
                onClick={() => setFile(null)}
                className="rounded p-0.5 text-slate-400 hover:text-rose-500"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            </div>
          )}
        </div>

        <div className="mt-4 flex justify-center">
          <Button onClick={() => void analyze()} loading={uploading} disabled={!file}>
            <Sparkles className="h-4 w-4" /> Analyze resume
          </Button>
        </div>
        {uploading && (
          <div className="mt-4 flex flex-col items-center gap-2">
            <Spinner className="py-2" />
            <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
              Extracting text and scoring with AI…
            </p>
          </div>
        )}
      </Card>

      {!result && !uploading && (
        <EmptyState
          title="No analysis yet"
          description="Upload a PDF resume above to receive a full ATS report."
        />
      )}

      {result && (
        <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
          <Card className="flex flex-col items-center gap-4 text-center">
            <div className="relative h-40 w-40">
              <svg viewBox="0 0 140 140" className="h-40 w-40 -rotate-90">
                <circle
                  cx="70"
                  cy="70"
                  r={radius}
                  fill="none"
                  strokeWidth="12"
                  className="stroke-slate-200 dark:stroke-slate-800"
                />
                <circle
                  cx="70"
                  cy="70"
                  r={radius}
                  fill="none"
                  stroke={color}
                  strokeWidth="12"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={circumference - (score / 100) * circumference}
                  className="transition-all duration-700"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-black" style={{ color }}>
                  {score}
                </span>
                <span className="text-xs font-bold uppercase tracking-wide text-slate-400">ATS score</span>
              </div>
            </div>
            <Badge color={score >= 80 ? 'green' : score >= 60 ? 'amber' : 'rose'}>
              {score >= 80 ? 'Great — ATS friendly' : score >= 60 ? 'Needs some work' : 'At risk of rejection'}
            </Badge>
            <Link
              to="/ai/resume"
              className="text-sm font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400"
            >
              Improve it in the builder →
            </Link>
          </Card>

          <div className="space-y-4">
            <Card>
              <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-rose-600 dark:text-rose-400">
                Missing keywords
              </h3>
              {result.missing_keywords?.length ? (
                <div className="flex flex-wrap gap-2">
                  {result.missing_keywords.map((k) => (
                    <span
                      key={k}
                      className="rounded-full bg-rose-100 px-3 py-1 text-xs font-semibold text-rose-700 dark:bg-rose-500/15 dark:text-rose-300"
                    >
                      {k}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-400">No notable keywords missing.</p>
              )}
            </Card>

            <Card>
              <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-brand-600 dark:text-brand-400">
                Suggestions
              </h3>
              {result.suggestions?.length ? (
                <ul className="space-y-2">
                  {result.suggestions.map((s, i) => (
                    <li key={i} className="flex gap-2.5 text-sm text-slate-600 dark:text-slate-300">
                      <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-brand-500" />
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-slate-400">No suggestions — looks tidy.</p>
              )}
            </Card>

            <Card>
              <h3 className="mb-3 flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-emerald-600 dark:text-emerald-400">
                <Target className="h-4 w-4" /> Recommended roles
              </h3>
              {result.job_recommendations?.length ? (
                <div className="grid gap-3 sm:grid-cols-2">
                  {result.job_recommendations.map((j, i) => (
                    <div
                      key={i}
                      className="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-800/40"
                    >
                      <p className="text-sm font-bold text-slate-900 dark:text-white">{j.title}</p>
                      <p className="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">{j.reason}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-400">No role recommendations yet.</p>
              )}
            </Card>

            <Card className="p-0">
              <button
                type="button"
                onClick={() => setShowText((v) => !v)}
                className="flex w-full items-center justify-between gap-2 px-5 py-4 text-left"
              >
                <span className="text-sm font-bold text-slate-900 dark:text-white">Extracted text</span>
                <ChevronDown
                  className={`h-4 w-4 shrink-0 text-slate-400 transition-transform ${showText ? 'rotate-180' : ''}`}
                />
              </button>
              {showText && (
                <div className="border-t border-slate-100 px-5 py-4 dark:border-slate-800">
                  <pre className="max-h-80 overflow-auto whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-xs leading-5 text-slate-600 dark:bg-slate-950 dark:text-slate-400">
                    {result.extracted_text || 'No text was extracted from this file.'}
                  </pre>
                </div>
              )}
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}
