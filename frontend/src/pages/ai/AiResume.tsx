import { useCallback, useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ScanSearch,
  Download,
  FileText,
  Plus,
  Save,
  Sparkles,
  Trash2,
  X,
} from 'lucide-react';
import { errorMessage, get, post, put } from '../../lib/api';
import type { Resume, ResumeData } from '../../lib/types';
import { Badge, Button, Card, Input, Select, Spinner, Textarea } from '../../components/ui';
import { toItems } from '../../components/helpers';

type TemplateKey = 'modern' | 'classic' | 'minimal';

const TEMPLATES: { value: TemplateKey; label: string }[] = [
  { value: 'modern', label: 'Modern' },
  { value: 'classic', label: 'Classic' },
  { value: 'minimal', label: 'Minimal' },
];

const EMPTY_DATA: ResumeData = {
  personal: { name: '', email: '', phone: '', location: '', summary: '' },
  education: [],
  skills: [],
  projects: [],
  experience: [],
};

interface AnalysisResult {
  ats_score: number;
  missing_keywords: string[];
  suggestions: string[];
  job_recommendations: { title: string; reason: string }[];
}

function gaugeColor(score: number): string {
  if (score >= 80) return '#10b981';
  if (score >= 60) return '#f59e0b';
  return '#f43f5e';
}

export default function AiResume() {
  const [searchParams, setSearchParams] = useSearchParams();
  const paramId = searchParams.get('id');

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [resumeId, setResumeId] = useState<number | null>(paramId ? Number(paramId) : null);
  const [title, setTitle] = useState('My Resume');
  const [template, setTemplate] = useState<TemplateKey>('modern');
  const [data, setData] = useState<ResumeData>(EMPTY_DATA);
  const [dirty, setDirty] = useState(false);
  const [loading, setLoading] = useState(Boolean(paramId));
  const [saving, setSaving] = useState(false);
  const [polishing, setPolishing] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [targetRole, setTargetRole] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [skillInput, setSkillInput] = useState('');

  const loadList = useCallback(async () => {
    try {
      const data = await get<unknown>('/resumes/mine');
      setResumes(toItems<Resume>(data));
    } catch {
      setResumes([]);
    }
  }, []);

  const loadResume = useCallback(async (id: number) => {
    setLoading(true);
    try {
      const r = await get<Resume>(`/resumes/${id}`);
      setResumeId(r.id);
      setTitle(r.title);
      setTemplate((r.template as TemplateKey) || 'modern');
      setData({ ...EMPTY_DATA, ...r.data, personal: { ...EMPTY_DATA.personal, ...(r.data?.personal ?? {}) } });
      setAnalysis(
        r.analysis && Object.keys(r.analysis).length
          ? (r.analysis as unknown as AnalysisResult)
          : null
      );
      setDirty(false);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadList();
  }, [loadList]);

  useEffect(() => {
    if (paramId) void loadResume(Number(paramId));
  }, [paramId, loadResume]);

  useEffect(() => {
    if (!dirty) return;
    const handler = (e: BeforeUnloadEvent) => {
      e.preventDefault();
      e.returnValue = '';
    };
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [dirty]);

  const patchData = (patch: Partial<ResumeData>) => {
    setData((prev) => ({ ...prev, ...patch }));
    setDirty(true);
  };

  const patchPersonal = (key: keyof ResumeData['personal'], value: string) => {
    setData((prev) => ({ ...prev, personal: { ...prev.personal, [key]: value } }));
    setDirty(true);
  };

  const guard = (): boolean => {
    if (!dirty) return true;
    return window.confirm('You have unsaved changes. Discard them?');
  };

  const newResume = () => {
    if (!guard()) return;
    setResumeId(null);
    setTitle('My Resume');
    setTemplate('modern');
    setData(EMPTY_DATA);
    setAnalysis(null);
    setDirty(false);
    setSearchParams({});
  };

  const pickResume = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    if (!value) {
      newResume();
      return;
    }
    if (!guard()) return;
    setSearchParams({ id: value });
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = { title: title.trim() || 'My Resume', template, data };
      if (resumeId) {
        const updated = await put<Resume>(`/resumes/${resumeId}`, payload);
        setResumes((prev) => prev.map((r) => (r.id === updated.id ? updated : r)));
        toast.success('Resume updated');
      } else {
        const created = await post<Resume>('/resumes', payload);
        setResumeId(created.id);
        setSearchParams({ id: String(created.id) });
        setResumes((prev) => [...prev, created]);
        toast.success('Resume saved');
      }
      setDirty(false);
      void loadList();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const polishSummary = async () => {
    if (!data.personal.summary.trim()) {
      toast.error('Write a summary first, then let AI polish it.');
      return;
    }
    setPolishing(true);
    try {
      const res = await post<{ content: string }>('/ai/resume/polish', {
        section: 'summary',
        content: data.personal.summary,
        target_role: targetRole.trim() || undefined,
      });
      patchPersonal('summary', res.content);
      toast.success('Summary polished');
    } catch (err) {
      const msg = errorMessage(err);
      toast.error(/not configured/i.test(msg) ? 'AI not configured â€” set GEMINI_API_KEY' : msg);
    } finally {
      setPolishing(false);
    }
  };

  const analyze = async () => {
    if (!resumeId) {
      toast.error('Save the resume before running ATS analysis.');
      return;
    }
    setAnalyzing(true);
    try {
      const res = await post<AnalysisResult>(`/resumes/${resumeId}/ScanSearch`);
      setAnalysis(res);
      toast.success(`ATS score: ${res.ats_score}`);
      void loadList();
    } catch (err) {
      const msg = errorMessage(err);
      toast.error(/not configured/i.test(msg) ? 'AI not configured â€” set GEMINI_API_KEY' : msg);
    } finally {
      setAnalyzing(false);
    }
  };

  const addSkill = () => {
    const value = skillInput.trim();
    if (!value) return;
    if (data.skills.includes(value)) {
      setSkillInput('');
      return;
    }
    patchData({ skills: [...data.skills, value] });
    setSkillInput('');
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl space-y-6">
        <Header />
        <Spinner />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="min-w-0">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Resume Builder</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Build a clean resume with a live preview, polish it with AI and check your ATS score.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {dirty && (
            <Badge color="amber">Unsaved changes</Badge>
          )}
          <Link
            to="/ai/resume/analyze"
            className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <ScanSearch className="h-4 w-4" /> Analyze PDF
          </Link>
          <Button variant="outline" onClick={newResume}>
            <Plus className="h-4 w-4" /> New
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <Card className="space-y-4">
            <div className="grid gap-3 sm:grid-cols-2">
              <div>
                <label className="label" htmlFor="resume-picker">
                  Saved resume
                </label>
                <Select id="resume-picker" value={resumeId ? String(resumeId) : ''} onChange={pickResume}>
                  <option value="">+ New resume</option>
                  {resumes.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.title}
                    </option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="label" htmlFor="resume-title">
                  Title
                </label>
                <Input
                  id="resume-title"
                  value={title}
                  onChange={(e) => {
                    setTitle(e.target.value);
                    setDirty(true);
                  }}
                />
              </div>
              <div className="sm:col-span-2">
                <label className="label" htmlFor="template">
                  Template
                </label>
                <Select
                  id="template"
                  value={template}
                  onChange={(e) => {
                    setTemplate(e.target.value as TemplateKey);
                    setDirty(true);
                  }}
                >
                  {TEMPLATES.map((t) => (
                    <option key={t.value} value={t.value}>
                      {t.label}
                    </option>
                  ))}
                </Select>
              </div>
            </div>
          </Card>

          <Card>
            <SectionTitle icon={<FileText className="h-4 w-4" />} title="Personal details" />
            <div className="grid gap-3 sm:grid-cols-2">
              <Field label="Full name" value={data.personal.name} onChange={(v) => patchPersonal('name', v)} placeholder="Jane Doe" />
              <Field label="Email" value={data.personal.email} onChange={(v) => patchPersonal('email', v)} placeholder="jane@example.com" />
              <Field label="Phone" value={data.personal.phone} onChange={(v) => patchPersonal('phone', v)} placeholder="+91 98765 43210" />
              <Field label="Location" value={data.personal.location} onChange={(v) => patchPersonal('location', v)} placeholder="Bengaluru, India" />
            </div>
            <div className="mt-3">
              <label className="label" htmlFor="summary">
                Summary
              </label>
              <Textarea
                id="summary"
                value={data.personal.summary}
                onChange={(e) => patchPersonal('summary', e.target.value)}
                placeholder="A short professional summary"
              />
            </div>
            <div className="mt-3 flex flex-wrap items-end gap-2">
              <div className="min-w-[180px] flex-1">
                <label className="label" htmlFor="target-role">
                  Target role <span className="text-xs text-slate-400">(for AI polish)</span>
                </label>
                <Input
                  id="target-role"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  placeholder="e.g. Backend Developer"
                />
              </div>
              <Button variant="secondary" onClick={() => void polishSummary()} loading={polishing}>
                <Sparkles className="h-4 w-4" /> AI Polish Summary
              </Button>
            </div>
          </Card>

          <Card>
            <SectionTitle
              icon={<Plus className="h-4 w-4" />}
              title="Education"
              action={
                <button
                  type="button"
                  className="text-xs font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400"
                  onClick={() => patchData({ education: [...data.education, { degree: '', school: '', year: '' }] })}
                >
                  + Add
                </button>
              }
            />
            {data.education.length === 0 && (
              <p className="text-sm text-slate-400">No education entries yet.</p>
            )}
            <div className="space-y-3">
              {data.education.map((row, i) => (
                <div key={i} className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
                  <div className="mb-2 flex justify-end">
                    <button
                      type="button"
                      aria-label="Remove education"
                      className="rounded-lg p-1 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                      onClick={() => patchData({ education: data.education.filter((_, idx) => idx !== i) })}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-3">
                    <Field label="Degree" value={row.degree} placeholder="B.Tech" onChange={(v) => patchData({ education: data.education.map((e2, idx) => (idx === i ? { ...e2, degree: v } : e2)) })} />
                    <Field label="School" value={row.school} placeholder="IIT Delhi" onChange={(v) => patchData({ education: data.education.map((e2, idx) => (idx === i ? { ...e2, school: v } : e2)) })} />
                    <Field label="Year" value={row.year} placeholder="2020â€“2024" onChange={(v) => patchData({ education: data.education.map((e2, idx) => (idx === i ? { ...e2, year: v } : e2)) })} />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <SectionTitle icon={<FileText className="h-4 w-4" />} title="Skills" />
            <div className="flex flex-wrap gap-2">
              {data.skills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 rounded-full bg-brand-100 px-3 py-1.5 text-xs font-semibold text-brand-700 dark:bg-brand-500/15 dark:text-brand-300"
                >
                  {skill}
                  <button
                    type="button"
                    aria-label={`Remove ${skill}`}
                    onClick={() => patchData({ skills: data.skills.filter((s) => s !== skill) })}
                    className="rounded-full p-0.5 hover:bg-brand-200 dark:hover:bg-brand-500/30"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              ))}
              {!data.skills.length && <p className="text-sm text-slate-400">No skills added yet.</p>}
            </div>
            <div className="mt-3 flex gap-2">
              <Input
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    addSkill();
                  }
                }}
                placeholder="Type a skill and press Enter"
              />
              <Button variant="outline" onClick={addSkill} type="button">
                Add
              </Button>
            </div>
          </Card>

          <Card>
            <SectionTitle
              icon={<Plus className="h-4 w-4" />}
              title="Experience"
              action={
                <button
                  type="button"
                  className="text-xs font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400"
                  onClick={() =>
                    patchData({ experience: [...data.experience, { role: '', company: '', period: '', description: '' }] })
                  }
                >
                  + Add
                </button>
              }
            />
            {data.experience.length === 0 && <p className="text-sm text-slate-400">No experience entries yet.</p>}
            <div className="space-y-3">
              {data.experience.map((row, i) => (
                <div key={i} className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
                  <div className="mb-2 flex justify-end">
                    <button
                      type="button"
                      aria-label="Remove experience"
                      className="rounded-lg p-1 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                      onClick={() => patchData({ experience: data.experience.filter((_, idx) => idx !== i) })}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-3">
                    <Field label="Role" value={row.role} placeholder="Backend Intern" onChange={(v) => patchData({ experience: data.experience.map((x, idx) => (idx === i ? { ...x, role: v } : x)) })} />
                    <Field label="Company" value={row.company} placeholder="Acme Corp" onChange={(v) => patchData({ experience: data.experience.map((x, idx) => (idx === i ? { ...x, company: v } : x)) })} />
                    <Field label="Period" value={row.period} placeholder="2023 â€“ 2024" onChange={(v) => patchData({ experience: data.experience.map((x, idx) => (idx === i ? { ...x, period: v } : x)) })} />
                  </div>
                  <div className="mt-3">
                    <label className="label">Description</label>
                    <Textarea
                      value={row.description}
                      onChange={(e) =>
                        patchData({
                          experience: data.experience.map((x, idx) => (idx === i ? { ...x, description: e.target.value } : x)),
                        })
                      }
                      placeholder="What did you achieve in this role?"
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <SectionTitle
              icon={<Plus className="h-4 w-4" />}
              title="Projects"
              action={
                <button
                  type="button"
                  className="text-xs font-semibold text-brand-600 hover:text-brand-700 dark:text-brand-400"
                  onClick={() => patchData({ projects: [...data.projects, { name: '', description: '', link: '' }] })}
                >
                  + Add
                </button>
              }
            />
            {data.projects.length === 0 && <p className="text-sm text-slate-400">No projects yet.</p>}
            <div className="space-y-3">
              {data.projects.map((row, i) => (
                <div key={i} className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
                  <div className="mb-2 flex justify-end">
                    <button
                      type="button"
                      aria-label="Remove project"
                      className="rounded-lg p-1 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                      onClick={() => patchData({ projects: data.projects.filter((_, idx) => idx !== i) })}
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <Field label="Name" value={row.name} placeholder="Job Tracker API" onChange={(v) => patchData({ projects: data.projects.map((x, idx) => (idx === i ? { ...x, name: v } : x)) })} />
                    <Field label="Link" value={row.link} placeholder="https://github.com/..." onChange={(v) => patchData({ projects: data.projects.map((x, idx) => (idx === i ? { ...x, link: v } : x)) })} />
                  </div>
                  <div className="mt-3">
                    <label className="label">Description</label>
                    <Textarea
                      value={row.description}
                      onChange={(e) =>
                        patchData({ projects: data.projects.map((x, idx) => (idx === i ? { ...x, description: e.target.value } : x)) })
                      }
                      placeholder="Stack, features and impact"
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <div className="flex flex-wrap gap-2">
            <Button onClick={() => void save()} loading={saving}>
              <Save className="h-4 w-4" /> {resumeId ? 'Update resume' : 'Save resume'}
            </Button>
            <Button variant="secondary" onClick={() => window.print()}>
              <Download className="h-4 w-4" /> Download PDF
            </Button>
            <Button variant="outline" onClick={() => void analyze()} loading={analyzing}>
              <ScanSearch className="h-4 w-4" /> Analyze ATS
            </Button>
          </div>

          {analysis && <AnalysisPanel analysis={analysis} />}
        </div>

        <div className="lg:sticky lg:top-24 lg:self-start">
          <div className="mb-2 flex items-center justify-between">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Live preview</p>
            <Badge color="slate">{TEMPLATES.find((t) => t.value === template)?.label}</Badge>
          </div>
          <ResumePreview template={template} data={data} />
        </div>
      </div>
    </div>
  );
}

function Header() {
  return (
    <div className="min-w-0">
      <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Resume Builder</h1>
      <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Loading your resumeâ€¦</p>
    </div>
  );
}

function SectionTitle({
  icon,
  title,
  action,
}: {
  icon: React.ReactNode;
  title: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="mb-3 flex items-center justify-between gap-2">
      <h3 className="flex items-center gap-2 text-sm font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        <span className="text-brand-500">{icon}</span>
        {title}
      </h3>
      {action}
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}) {
  const id = `f-${label.replace(/\s+/g, '-').toLowerCase()}`;
  return (
    <div>
      <label className="label" htmlFor={id}>
        {label}
      </label>
      <Input id={id} value={value} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} />
    </div>
  );
}

function AnalysisPanel({ analysis }: { analysis: AnalysisResult }) {
  const score = Math.max(0, Math.min(100, analysis.ats_score ?? 0));
  const color = gaugeColor(score);
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  return (
    <Card>
      <div className="flex items-center gap-4">
        <div className="relative h-28 w-28 shrink-0">
          <svg viewBox="0 0 120 120" className="h-28 w-28 -rotate-90">
            <circle cx="60" cy="60" r={radius} fill="none" strokeWidth="10" className="stroke-slate-200 dark:stroke-slate-800" />
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke={color}
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={circumference - (score / 100) * circumference}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-black" style={{ color }}>
              {score}
            </span>
            <span className="text-[10px] font-bold uppercase text-slate-400">ATS</span>
          </div>
        </div>
        <div className="min-w-0">
          <h4 className="text-base font-bold text-slate-900 dark:text-white">ATS analysis</h4>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            How well this resume parses for applicant tracking systems.
          </p>
        </div>
      </div>

      {analysis.missing_keywords?.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-rose-600 dark:text-rose-400">
            Missing keywords
          </p>
          <div className="flex flex-wrap gap-1.5">
            {analysis.missing_keywords.map((k) => (
              <span
                key={k}
                className="rounded-full bg-rose-100 px-2.5 py-1 text-xs font-semibold text-rose-700 dark:bg-rose-500/15 dark:text-rose-300"
              >
                {k}
              </span>
            ))}
          </div>
        </div>
      )}

      {analysis.suggestions?.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-brand-600 dark:text-brand-400">
            Suggestions
          </p>
          <ul className="space-y-1.5">
            {analysis.suggestions.map((s, i) => (
              <li key={i} className="text-sm text-slate-600 dark:text-slate-300">
                â€¢ {s}
              </li>
            ))}
          </ul>
        </div>
      )}

      {analysis.job_recommendations?.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-400">Roles to explore</p>
          <div className="grid gap-2 sm:grid-cols-2">
            {analysis.job_recommendations.map((j, i) => (
              <div key={i} className="rounded-xl bg-slate-50 p-3 dark:bg-slate-800/50">
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-100">{j.title}</p>
                <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{j.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}

function ResumePreview({ template, data }: { template: TemplateKey; data: ResumeData }) {
  const hasContent =
    data.personal.name ||
    data.personal.summary ||
    data.skills.length ||
    data.education.length ||
    data.experience.length ||
    data.projects.length;

  const base = 'print-area w-full rounded-2xl border p-6 sm:p-8 shadow-sm';
  const shell =
    template === 'classic'
      ? `${base} border-slate-300 bg-white font-serif text-slate-900`
      : template === 'minimal'
        ? `${base} border-slate-200 bg-white font-sans text-slate-800`
        : `${base} border-slate-200 bg-white font-sans text-slate-800`;

  const headingCls =
    template === 'classic'
      ? 'border-b-2 border-slate-800 pb-1 text-center text-sm font-bold uppercase tracking-[0.2em] text-slate-900'
      : template === 'minimal'
        ? 'border-b border-slate-200 pb-1 text-xs font-bold uppercase tracking-widest text-slate-500'
        : 'text-xs font-black uppercase tracking-widest text-white';

  const section = (title: string, body: React.ReactNode, key: string) => {
    if (template === 'modern') {
      return (
        <div key={key} className="mt-5">
          <div className="mb-2 rounded-md bg-brand-600 px-3 py-1">
            <h3 className="text-xs font-black uppercase tracking-widest text-white">{title}</h3>
          </div>
          {body}
        </div>
      );
    }
    return (
      <div key={key} className="mt-5">
        <h3 className={headingCls}>{title}</h3>
        <div className="mt-2">{body}</div>
      </div>
    );
  };

  return (
    <div className={shell}>
      <div className={template === 'modern' ? 'border-b-4 border-brand-500 pb-4' : 'pb-3'}>
        <h1
          className={`text-2xl font-black tracking-tight ${
            template === 'classic' ? 'text-center text-slate-900' : 'text-slate-900'
          }`}
        >
          {data.personal.name || 'Your Name'}
        </h1>
        <p
          className={`mt-1 text-sm ${
            template === 'classic' ? 'text-center text-slate-600' : 'text-brand-600'
          }`}
        >
          {[data.personal.email, data.personal.phone, data.personal.location]
            .filter(Boolean)
            .join('  Â·  ') || 'email Â· phone Â· location'}
        </p>
      </div>

      {data.personal.summary &&
        section(
          'Summary',
          <p className="whitespace-pre-wrap text-sm leading-6 text-slate-600">{data.personal.summary}</p>,
          'summary'
        )}

      {data.skills.length > 0 &&
        section(
          'Skills',
          <div className="flex flex-wrap gap-1.5">
            {data.skills.map((s) => (
              <span
                key={s}
                className={
                  template === 'modern'
                    ? 'rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700'
                    : template === 'classic'
                      ? 'rounded-sm border border-slate-400 px-2 py-0.5 text-xs font-medium text-slate-700'
                      : 'rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700'
                }
              >
                {s}
              </span>
            ))}
          </div>,
          'skills'
        )}

      {data.experience.length > 0 &&
        section(
          'Experience',
          <div className="space-y-3">
            {data.experience.map((x, i) => (
              <div key={i}>
                <div className="flex flex-wrap items-baseline justify-between gap-1">
                  <p className="text-sm font-bold text-slate-900">{x.role || 'Role'}</p>
                  <p className="text-xs font-medium text-slate-500">{x.period}</p>
                </div>
                <p className="text-xs font-semibold text-brand-600">{x.company}</p>
                {x.description && (
                  <p className="mt-1 whitespace-pre-wrap text-sm leading-6 text-slate-600">{x.description}</p>
                )}
              </div>
            ))}
          </div>,
          'experience'
        )}

      {data.education.length > 0 &&
        section(
          'Education',
          <div className="space-y-2">
            {data.education.map((e, i) => (
              <div key={i} className="flex flex-wrap items-baseline justify-between gap-1">
                <div>
                  <p className="text-sm font-bold text-slate-900">{e.degree || 'Degree'}</p>
                  <p className="text-xs text-slate-500">{e.school}</p>
                </div>
                <p className="text-xs font-medium text-slate-500">{e.year}</p>
              </div>
            ))}
          </div>,
          'education'
        )}

      {data.projects.length > 0 &&
        section(
          'Projects',
          <div className="space-y-2">
            {data.projects.map((p, i) => (
              <div key={i}>
                <p className="text-sm font-bold text-slate-900">{p.name || 'Project'}</p>
                {p.link && <p className="text-xs text-brand-600">{p.link}</p>}
                {p.description && <p className="mt-0.5 text-sm leading-6 text-slate-600">{p.description}</p>}
              </div>
            ))}
          </div>,
          'projects'
        )}

      {!hasContent && (
        <div className="mt-6 rounded-xl border border-dashed border-slate-300 p-8 text-center">
          <p className="text-sm text-slate-400">Start filling the form â€” your resume appears here live.</p>
        </div>
      )}
    </div>
  );
}

