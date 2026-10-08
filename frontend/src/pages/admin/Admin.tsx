import { FormEvent, useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  BookOpen,
  ChevronDown,
  ChevronRight,
  FileText,
  ImageIcon,
  LayoutGrid,
  ListChecks,
  Pencil,
  Plus,
  RefreshCw,
  Shield,
  Trash2,
  Users,
} from 'lucide-react';
import api, { del, errorMessage, get, post, put } from '../../lib/api';
import type { Course, CurrentAffair, Job, Topic } from '../../lib/types';
import {
  Badge,
  Button,
  Card,
  EmptyState,
  Input,
  Modal,
  Select,
  Spinner,
  StatCard,
  Textarea,
} from '../../components/ui';
import { formatDate, titleCase, toItems } from '../../components/helpers';
import { useAuth } from '../../stores/auth';
import { useTheme } from '../../stores/theme';

type TabKey = 'analytics' | 'courses' | 'quizzes' | 'content' | 'jobs' | 'users';

const TABS: { key: TabKey; label: string; to: string; icon: typeof LayoutGrid }[] = [
  { key: 'analytics', label: 'Analytics', to: '/admin', icon: LayoutGrid },
  { key: 'courses', label: 'Courses', to: '/admin/courses', icon: BookOpen },
  { key: 'quizzes', label: 'Quizzes', to: '/admin/quizzes', icon: ListChecks },
  { key: 'content', label: 'Content', to: '/admin/content', icon: FileText },
  { key: 'jobs', label: 'Jobs', to: '/admin/jobs', icon: ImageIcon },
  { key: 'users', label: 'Users', to: '/admin/users', icon: Users },
];

interface AnalyticsData {
  users_total: number;
  users_new_7d: number;
  quizzes_total: number;
  attempts_total: number;
  jobs_total: number;
  courses_total: number;
  top_quizzes: { title: string; attempts: number }[];
  signups_by_day: { date: string; count: number }[];
  avg_score_by_day: { date: string; avg: number }[];
}

interface LessonItem {
  id: number;
  title: string;
  order: number;
  content?: unknown;
}

interface CourseDetail extends Course {
  topics?: Topic[];
}

interface TopicDetail extends Topic {
  lessons?: LessonItem[];
}

interface AdminQuiz {
  id: number;
  title: string;
  slug: string;
  quiz_type: string;
  difficulty: string;
  duration_minutes: number;
  negative_marks: number;
  topic_id: number | null;
  exam_id: number | null;
  meta: Record<string, unknown> | null;
  is_published: boolean;
  total_questions?: number;
}

interface AdminQuestion {
  id: number;
  question_text: string;
  options: string[];
  correct_index: number;
  explanation: string;
  difficulty: string;
}

interface AdminUser {
  id: number;
  full_name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
  profile?: { xp?: number; level?: number } | null;
}

interface CaDetail extends CurrentAffair {
  content?: string;
}

function parseJson(text: string, label: string): Record<string, unknown> | null {
  const trimmed = text.trim();
  if (!trimmed) return {};
  try {
    const parsed: unknown = JSON.parse(trimmed);
    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
      return parsed as Record<string, unknown>;
    }
    toast.error(`${label} must be a JSON object`);
    return null;
  } catch {
    toast.error(`${label} is not valid JSON`);
    return null;
  }
}

function Labeled({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <span className="label">{label}</span>
      {children}
    </div>
  );
}

export default function Admin() {
  const location = useLocation();
  const segment = location.pathname.split('/')[2] ?? '';
  const tab: TabKey = (['courses', 'quizzes', 'content', 'jobs', 'users'] as string[]).includes(segment)
    ? (segment as TabKey)
    : 'analytics';

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="min-w-0">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Admin Panel</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Manage content, quizzes, jobs, users and review platform analytics.
        </p>
      </div>

      <nav className="flex flex-wrap gap-2 border-b border-slate-200 pb-2 dark:border-slate-800">
        {TABS.map((t) => {
          const active = t.key === tab;
          const Icon = t.icon;
          return (
            <Link
              key={t.key}
              to={t.to}
              className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition ${
                active
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200'
              }`}
            >
              <Icon className="h-4 w-4" />
              {t.label}
            </Link>
          );
        })}
      </nav>

      {tab === 'analytics' && <AnalyticsPanel />}
      {tab === 'courses' && <CoursesPanel />}
      {tab === 'quizzes' && <QuizzesPanel />}
      {tab === 'content' && <ContentPanel />}
      {tab === 'jobs' && <JobsPanel />}
      {tab === 'users' && <UsersPanel />}
    </div>
  );
}

function PageNote({ children }: { children: React.ReactNode }) {
  return <p className="text-sm text-slate-500 dark:text-slate-400">{children}</p>;
}

/* ---------------------------------- Analytics --------------------------------- */

function AnalyticsPanel() {
  const { theme } = useTheme();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      try {
        const res = await get<AnalyticsData>('/admin/analytics');
        if (alive) setData(res);
      } catch (err) {
        if (alive) toast.error(errorMessage(err));
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  if (loading) return <Spinner />;
  if (!data) return <EmptyState title="No analytics" description="Analytics data could not be loaded." />;

  const tickColor = theme === 'dark' ? '#94a3b8' : '#64748b';
  const gridColor = theme === 'dark' ? '#1e293b' : '#e2e8f0';
  const tooltipStyle = {
    background: theme === 'dark' ? '#0f172a' : '#ffffff',
    border: `1px solid ${theme === 'dark' ? '#334155' : '#e2e8f0'}`,
    borderRadius: 12,
    color: theme === 'dark' ? '#e2e8f0' : '#0f172a',
    fontSize: 12,
  } as const;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard label="Total users" value={data.users_total} icon={<Users className="h-5 w-5" />} />
        <StatCard label="New users (7d)" value={data.users_new_7d} icon={<Shield className="h-5 w-5" />} />
        <StatCard label="Quizzes" value={data.quizzes_total} icon={<ListChecks className="h-5 w-5" />} />
        <StatCard label="Attempts" value={data.attempts_total} icon={<FileText className="h-5 w-5" />} />
        <StatCard label="Jobs" value={data.jobs_total} icon={<LayoutGrid className="h-5 w-5" />} />
        <StatCard label="Courses" value={data.courses_total} icon={<BookOpen className="h-5 w-5" />} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <h3 className="mb-4 text-base font-bold text-slate-900 dark:text-white">Signups by day</h3>
          {data.signups_by_day.length ? (
            <div className="h-56 text-slate-500 dark:text-slate-400">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.signups_by_day} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: tickColor, fontSize: 11 }}
                    tickLine={false}
                    axisLine={{ stroke: gridColor }}
                    tickFormatter={(v: string) => String(v).slice(5)}
                    minTickGap={20}
                  />
                  <YAxis tick={{ fill: tickColor, fontSize: 11 }} tickLine={false} axisLine={false} width={40} />
                  <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: tickColor }} />
                  <Bar dataKey="count" fill="#6366f1" radius={[6, 6, 0, 0]} maxBarSize={28} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <PageNote>No signups recorded in this period.</PageNote>
          )}
        </Card>

        <Card>
          <h3 className="mb-4 text-base font-bold text-slate-900 dark:text-white">Average score by day</h3>
          {data.avg_score_by_day.length ? (
            <div className="h-56 text-slate-500 dark:text-slate-400">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.avg_score_by_day} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: tickColor, fontSize: 11 }}
                    tickLine={false}
                    axisLine={{ stroke: gridColor }}
                    tickFormatter={(v: string) => String(v).slice(5)}
                    minTickGap={20}
                  />
                  <YAxis tick={{ fill: tickColor, fontSize: 11 }} tickLine={false} axisLine={false} width={40} />
                  <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: tickColor }} />
                  <Bar dataKey="avg" fill="#6366f1" radius={[6, 6, 0, 0]} maxBarSize={28} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <PageNote>No attempt data in this period.</PageNote>
          )}
        </Card>
      </div>

      <Card>
        <h3 className="mb-4 text-base font-bold text-slate-900 dark:text-white">Top quizzes</h3>
        {data.top_quizzes.length ? (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[420px] text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-800">
                  <th className="py-2 pr-4 font-semibold">Quiz</th>
                  <th className="py-2 text-right font-semibold">Attempts</th>
                </tr>
              </thead>
              <tbody>
                {data.top_quizzes.map((q, i) => (
                  <tr key={i} className="border-b border-slate-100 last:border-0 dark:border-slate-800">
                    <td className="py-2.5 pr-4 font-medium text-slate-800 dark:text-slate-100">{q.title}</td>
                    <td className="py-2.5 text-right font-bold text-brand-600 dark:text-brand-400">{q.attempts}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <PageNote>No quiz attempts yet.</PageNote>
        )}
      </Card>
    </div>
  );
}

/* ----------------------------------- Courses ---------------------------------- */

interface CourseFormState {
  id?: number;
  title: string;
  slug: string;
  category: 'government' | 'it';
  description: string;
  icon: string;
  level: string;
  order: number;
  career_path: boolean;
  is_published: boolean;
}

const EMPTY_COURSE: CourseFormState = {
  title: '',
  slug: '',
  category: 'government',
  description: '',
  icon: '',
  level: 'beginner',
  order: 0,
  career_path: false,
  is_published: true,
};

function CoursesPanel() {
  const [courses, setCourses] = useState<Course[] | null>(null);
  const [modal, setModal] = useState<CourseFormState | null>(null);
  const [saving, setSaving] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);
  const [topicsByCourse, setTopicsByCourse] = useState<Record<number, Topic[]>>({});
  const [topicsLoading, setTopicsLoading] = useState<number | null>(null);
  const [topicForm, setTopicForm] = useState({ title: '', slug: '', description: '', order: 0 });
  const [addingTopicFor, setAddingTopicFor] = useState<number | null>(null);
  const [editingTopicId, setEditingTopicId] = useState<number | null>(null);
  const [expandedTopicId, setExpandedTopicId] = useState<number | null>(null);
  const [lessonsByTopic, setLessonsByTopic] = useState<Record<number, LessonItem[]>>({});
  const [lessonsLoading, setLessonsLoading] = useState<number | null>(null);
  const [lessonForm, setLessonForm] = useState({
    title: '',
    order: 0,
    content: '{\n  "notes": "",\n  "examples": [],\n  "practice": []\n}',
  });
  const [editingLesson, setEditingLesson] = useState<LessonItem | null>(null);

  const load = async () => {
    try {
      const data = await get<unknown>('/admin/courses');
      setCourses(toItems<Course>(data));
    } catch (err) {
      toast.error(errorMessage(err));
      setCourses([]);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const openCreate = () => setModal({ ...EMPTY_COURSE });

  const openEdit = (course: Course) => {
    setModal({
      id: course.id,
      title: course.title,
      slug: course.slug,
      category: course.category,
      description: course.description ?? '',
      icon: course.icon ?? '',
      level: course.level ?? 'beginner',
      order: course.order ?? 0,
      career_path: Boolean(course.career_path),
      is_published: true,
    });
  };

  const saveCourse = async (e: FormEvent) => {
    e.preventDefault();
    if (!modal) return;
    if (!modal.title.trim() || !modal.slug.trim()) {
      toast.error('Title and slug are required.');
      return;
    }
    setSaving(true);
    try {
      if (modal.id) {
        await put(`/admin/courses/${modal.id}`, modal);
        toast.success('Course updated');
      } else {
        await post('/admin/courses', modal);
        toast.success('Course created');
      }
      setModal(null);
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const removeCourse = async (course: Course) => {
    if (!window.confirm(`Delete course "${course.title}"?`)) return;
    try {
      await del(`/admin/courses/${course.id}`);
      toast.success('Course deleted');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const toggleTopics = async (course: Course) => {
    if (expanded === course.id) {
      setExpanded(null);
      return;
    }
    setExpanded(course.id);
    setExpandedTopicId(null);
    setEditingTopicId(null);
    if (topicsByCourse[course.id]) return;
    setTopicsLoading(course.id);
    try {
      const detail = await get<CourseDetail>(`/courses/${course.slug}`);
      setTopicsByCourse((prev) => ({ ...prev, [course.id]: detail.topics ?? [] }));
    } catch (err) {
      toast.error(errorMessage(err));
      setTopicsByCourse((prev) => ({ ...prev, [course.id]: [] }));
    } finally {
      setTopicsLoading(null);
    }
  };

  const refreshTopics = async (courseId: number, slug: string) => {
    try {
      const detail = await get<CourseDetail>(`/courses/${slug}`);
      setTopicsByCourse((prev) => ({ ...prev, [courseId]: detail.topics ?? [] }));
    } catch {
      /* ignore */
    }
  };

  const addTopic = async (course: Course, e: FormEvent) => {
    e.preventDefault();
    if (!topicForm.title.trim() || !topicForm.slug.trim()) {
      toast.error('Topic title and slug are required.');
      return;
    }
    try {
      await post('/admin/topics', { course_id: course.id, ...topicForm });
      toast.success('Topic added');
      setTopicForm({ title: '', slug: '', description: '', order: 0 });
      setAddingTopicFor(null);
      await refreshTopics(course.id, course.slug);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const saveTopic = async (course: Course, topic: Topic, e: FormEvent) => {
    e.preventDefault();
    try {
      await put(`/admin/topics/${topic.id}`, {
        course_id: course.id,
        title: topic.title,
        slug: topic.slug,
        description: topic.description ?? '',
        order: topic.order ?? 0,
      });
      toast.success('Topic updated');
      setEditingTopicId(null);
      await refreshTopics(course.id, course.slug);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const removeTopic = async (course: Course, topic: Topic) => {
    if (!window.confirm(`Delete topic "${topic.title}"?`)) return;
    try {
      await del(`/admin/topics/${topic.id}`);
      toast.success('Topic deleted');
      await refreshTopics(course.id, course.slug);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const toggleLessons = async (topic: Topic) => {
    if (expandedTopicId === topic.id) {
      setExpandedTopicId(null);
      setEditingLesson(null);
      return;
    }
    setExpandedTopicId(topic.id);
    setEditingLesson(null);
    if (lessonsByTopic[topic.id]) return;
    setLessonsLoading(topic.id);
    try {
      const detail = await get<TopicDetail>(`/topics/${topic.slug}`);
      setLessonsByTopic((prev) => ({ ...prev, [topic.id]: detail.lessons ?? [] }));
    } catch (err) {
      toast.error(errorMessage(err));
      setLessonsByTopic((prev) => ({ ...prev, [topic.id]: [] }));
    } finally {
      setLessonsLoading(null);
    }
  };

  const refreshLessons = async (topic: Topic) => {
    try {
      const detail = await get<TopicDetail>(`/topics/${topic.slug}`);
      setLessonsByTopic((prev) => ({ ...prev, [topic.id]: detail.lessons ?? [] }));
    } catch {
      /* ignore */
    }
  };

  const addLesson = async (topic: Topic, e: FormEvent) => {
    e.preventDefault();
    if (!lessonForm.title.trim()) {
      toast.error('Lesson title is required.');
      return;
    }
    const parsed = parseJson(lessonForm.content, 'Lesson content');
    if (parsed === null) return;
    try {
      await post('/admin/lessons', {
        topic_id: topic.id,
        title: lessonForm.title.trim(),
        order: lessonForm.order,
        content: parsed,
      });
      toast.success('Lesson added');
      setLessonForm({
        title: '',
        order: 0,
        content: '{\n  "notes": "",\n  "examples": [],\n  "practice": []\n}',
      });
      await refreshLessons(topic);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const saveLesson = async (topic: Topic, lesson: LessonItem, contentText: string, e: FormEvent) => {
    e.preventDefault();
    const parsed = parseJson(contentText, 'Lesson content');
    if (parsed === null) return;
    try {
      await put(`/admin/lessons/${lesson.id}`, {
        topic_id: topic.id,
        title: lesson.title,
        order: lesson.order,
        content: parsed,
      });
      toast.success('Lesson updated');
      setEditingLesson(null);
      await refreshLessons(topic);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const removeLesson = async (topic: Topic, lesson: LessonItem) => {
    if (!window.confirm(`Delete lesson "${lesson.title}"?`)) return;
    try {
      await del(`/admin/lessons/${lesson.id}`);
      toast.success('Lesson deleted');
      await refreshLessons(topic);
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  if (!courses) return <Spinner />;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <PageNote>{courses.length} courses</PageNote>
        <Button onClick={openCreate}>
          <Plus className="h-4 w-4" /> New course
        </Button>
      </div>

      {courses.length === 0 ? (
        <EmptyState title="No courses yet" description="Create the first course to get started." />
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-800">
                <th className="px-4 py-3 font-semibold"></th>
                <th className="px-4 py-3 font-semibold">Title</th>
                <th className="px-4 py-3 font-semibold">Category</th>
                <th className="px-4 py-3 font-semibold">Level</th>
                <th className="px-4 py-3 font-semibold">Order</th>
                <th className="px-4 py-3 font-semibold">Flags</th>
                <th className="px-4 py-3 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((course) => {
                const isOpen = expanded === course.id;
                const topics = topicsByCourse[course.id];
                return (
                  <>
                    <tr
                      key={course.id}
                      className="border-b border-slate-100 dark:border-slate-800"
                    >
                      <td className="px-4 py-3">
                        <button
                          type="button"
                          aria-label="Expand topics"
                          onClick={() => void toggleTopics(course)}
                          className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                        >
                          {topicsLoading === course.id ? (
                            <Spinner className="py-0" />
                          ) : isOpen ? (
                            <ChevronDown className="h-4 w-4" />
                          ) : (
                            <ChevronRight className="h-4 w-4" />
                          )}
                        </button>
                      </td>
                      <td className="px-4 py-3">
                        <p className="font-semibold text-slate-800 dark:text-slate-100">{course.title}</p>
                        <p className="text-xs text-slate-400">/{course.slug}</p>
                      </td>
                      <td className="px-4 py-3">
                        <Badge color={course.category === 'government' ? 'violet' : 'brand'}>
                          {course.category}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{course.level}</td>
                      <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{course.order}</td>
                      <td className="px-4 py-3">
                        <div className="flex flex-wrap gap-1">
                          {course.career_path && <Badge color="green">career path</Badge>}
                          <Badge color="slate">pub</Badge>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex justify-end gap-1">
                          <button
                            type="button"
                            aria-label="Edit course"
                            onClick={() => openEdit(course)}
                            className="rounded-lg p-1.5 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-500/10"
                          >
                            <Pencil className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            aria-label="Delete course"
                            onClick={() => void removeCourse(course)}
                            className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                    {isOpen && (
                      <tr key={`${course.id}-topics`}>
                        <td colSpan={7} className="bg-slate-50 px-4 py-4 dark:bg-slate-950/50">
                          {topics === undefined ? (
                            <Spinner className="py-4" />
                          ) : (
                            <div className="space-y-3">
                              <div className="flex flex-wrap items-center justify-between gap-2">
                                <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                                  Topics ({topics.length})
                                </p>
                                <Button
                                  variant="outline"
                                  onClick={() => setAddingTopicFor(addingTopicFor === course.id ? null : course.id)}
                                >
                                  <Plus className="h-4 w-4" /> Add topic
                                </Button>
                              </div>

                              {addingTopicFor === course.id && (
                                <form
                                  onSubmit={(e) => void addTopic(course, e)}
                                  className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900 sm:grid-cols-2"
                                >
                                  <Labeled label="Title">
                                    <Input
                                      value={topicForm.title}
                                      onChange={(e) => setTopicForm({ ...topicForm, title: e.target.value })}
                                    />
                                  </Labeled>
                                  <Labeled label="Slug">
                                    <Input
                                      value={topicForm.slug}
                                      onChange={(e) => setTopicForm({ ...topicForm, slug: e.target.value })}
                                    />
                                  </Labeled>
                                  <Labeled label="Description">
                                    <Input
                                      value={topicForm.description}
                                      onChange={(e) => setTopicForm({ ...topicForm, description: e.target.value })}
                                    />
                                  </Labeled>
                                  <Labeled label="Order">
                                    <Input
                                      type="number"
                                      value={topicForm.order}
                                      onChange={(e) => setTopicForm({ ...topicForm, order: Number(e.target.value) })}
                                    />
                                  </Labeled>
                                  <div className="sm:col-span-2">
                                    <Button type="submit">Save topic</Button>
                                  </div>
                                </form>
                              )}

                              {topics.length === 0 && <PageNote>No topics yet for this course.</PageNote>}

                              {topics.map((topic) => (
                                <div
                                  key={topic.id}
                                  className="rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900"
                                >
                                  {editingTopicId === topic.id ? (
                                    <form
                                      onSubmit={(e) => void saveTopic(course, topic, e)}
                                      className="grid gap-3 p-4 sm:grid-cols-2"
                                    >
                                      <Labeled label="Title">
                                        <Input
                                          value={topic.title}
                                          onChange={(e) =>
                                            setTopicsByCourse((prev) => ({
                                              ...prev,
                                              [course.id]: (prev[course.id] ?? []).map((t) =>
                                                t.id === topic.id ? { ...t, title: e.target.value } : t
                                              ),
                                            }))
                                          }
                                        />
                                      </Labeled>
                                      <Labeled label="Slug">
                                        <Input
                                          value={topic.slug}
                                          onChange={(e) =>
                                            setTopicsByCourse((prev) => ({
                                              ...prev,
                                              [course.id]: (prev[course.id] ?? []).map((t) =>
                                                t.id === topic.id ? { ...t, slug: e.target.value } : t
                                              ),
                                            }))
                                          }
                                        />
                                      </Labeled>
                                      <Labeled label="Description">
                                        <Input
                                          value={topic.description ?? ''}
                                          onChange={(e) =>
                                            setTopicsByCourse((prev) => ({
                                              ...prev,
                                              [course.id]: (prev[course.id] ?? []).map((t) =>
                                                t.id === topic.id ? { ...t, description: e.target.value } : t
                                              ),
                                            }))
                                          }
                                        />
                                      </Labeled>
                                      <Labeled label="Order">
                                        <Input
                                          type="number"
                                          value={topic.order ?? 0}
                                          onChange={(e) =>
                                            setTopicsByCourse((prev) => ({
                                              ...prev,
                                              [course.id]: (prev[course.id] ?? []).map((t) =>
                                                t.id === topic.id ? { ...t, order: Number(e.target.value) } : t
                                              ),
                                            }))
                                          }
                                        />
                                      </Labeled>
                                      <div className="flex gap-2 sm:col-span-2">
                                        <Button type="submit">Save</Button>
                                        <Button type="button" variant="ghost" onClick={() => setEditingTopicId(null)}>
                                          Cancel
                                        </Button>
                                      </div>
                                    </form>
                                  ) : (
                                    <>
                                      <div className="flex flex-wrap items-center gap-2 px-4 py-3">
                                        <button
                                          type="button"
                                          onClick={() => void toggleLessons(topic)}
                                          className="flex min-w-0 flex-1 items-center gap-2 text-left"
                                        >
                                          {expandedTopicId === topic.id ? (
                                            <ChevronDown className="h-4 w-4 shrink-0 text-slate-400" />
                                          ) : (
                                            <ChevronRight className="h-4 w-4 shrink-0 text-slate-400" />
                                          )}
                                          <span className="min-w-0">
                                            <span className="block truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
                                              {topic.title}
                                            </span>
                                            <span className="block text-xs text-slate-400">/{topic.slug}</span>
                                          </span>
                                        </button>
                                        <button
                                          type="button"
                                          aria-label="Edit topic"
                                          onClick={() => setEditingTopicId(topic.id)}
                                          className="rounded-lg p-1.5 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-500/10"
                                        >
                                          <Pencil className="h-4 w-4" />
                                        </button>
                                        <button
                                          type="button"
                                          aria-label="Delete topic"
                                          onClick={() => void removeTopic(course, topic)}
                                          className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                                        >
                                          <Trash2 className="h-4 w-4" />
                                        </button>
                                      </div>

                                      {expandedTopicId === topic.id && (
                                        <div className="border-t border-slate-100 p-4 dark:border-slate-800">
                                          {lessonsLoading === topic.id ? (
                                            <Spinner className="py-4" />
                                          ) : (
                                            <div className="space-y-3">
                                              <form
                                                onSubmit={(e) => void addLesson(topic, e)}
                                                className="grid gap-3 rounded-xl border border-dashed border-slate-300 p-3 dark:border-slate-700 sm:grid-cols-3"
                                              >
                                                <Labeled label="Lesson title">
                                                  <Input
                                                    value={lessonForm.title}
                                                    onChange={(e) =>
                                                      setLessonForm({ ...lessonForm, title: e.target.value })
                                                    }
                                                  />
                                                </Labeled>
                                                <Labeled label="Order">
                                                  <Input
                                                    type="number"
                                                    value={lessonForm.order}
                                                    onChange={(e) =>
                                                      setLessonForm({ ...lessonForm, order: Number(e.target.value) })
                                                    }
                                                  />
                                                </Labeled>
                                                <div className="flex items-end">
                                                  <Button type="submit" variant="secondary">
                                                    <Plus className="h-4 w-4" /> Add lesson
                                                  </Button>
                                                </div>
                                                <div className="sm:col-span-3">
                                                  <Labeled label="Content (JSON)">
                                                    <Textarea
                                                      className="font-mono text-xs"
                                                      value={lessonForm.content}
                                                      onChange={(e) =>
                                                        setLessonForm({ ...lessonForm, content: e.target.value })
                                                      }
                                                    />
                                                  </Labeled>
                                                </div>
                                              </form>

                                              {(lessonsByTopic[topic.id] ?? []).length === 0 && (
                                                <PageNote>No lessons yet.</PageNote>
                                              )}

                                              {(lessonsByTopic[topic.id] ?? []).map((lesson) =>
                                                editingLesson?.id === lesson.id ? (
                                                  <LessonEditForm
                                                    key={lesson.id}
                                                    lesson={lesson}
                                                    topic={topic}
                                                    onCancel={() => setEditingLesson(null)}
                                                    onSave={saveLesson}
                                                  />
                                                ) : (
                                                  <div
                                                    key={lesson.id}
                                                    className="flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 dark:border-slate-800"
                                                  >
                                                    <span className="text-xs font-bold text-slate-400">
                                                      #{lesson.order}
                                                    </span>
                                                    <span className="min-w-0 flex-1 truncate text-sm font-medium text-slate-700 dark:text-slate-200">
                                                      {lesson.title}
                                                    </span>
                                                    <button
                                                      type="button"
                                                      aria-label="Edit lesson"
                                                      onClick={() =>
                                                        setEditingLesson({
                                                          ...lesson,
                                                          content: JSON.stringify(lesson.content ?? {}, null, 2),
                                                        })
                                                      }
                                                      className="rounded-lg p-1.5 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-500/10"
                                                    >
                                                      <Pencil className="h-4 w-4" />
                                                    </button>
                                                    <button
                                                      type="button"
                                                      aria-label="Delete lesson"
                                                      onClick={() => void removeLesson(topic, lesson)}
                                                      className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                                                    >
                                                      <Trash2 className="h-4 w-4" />
                                                    </button>
                                                  </div>
                                                )
                                              )}
                                            </div>
                                          )}
                                        </div>
                                      )}
                                    </>
                                  )}
                                </div>
                              ))}
                            </div>
                          )}
                        </td>
                      </tr>
                    )}
                  </>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      <Modal
        open={modal !== null}
        onClose={() => setModal(null)}
        title={modal?.id ? 'Edit course' : 'New course'}
        wide
      >
        {modal && (
          <form onSubmit={saveCourse} className="grid gap-4 sm:grid-cols-2">
            <Labeled label="Title">
              <Input value={modal.title} onChange={(e) => setModal({ ...modal, title: e.target.value })} />
            </Labeled>
            <Labeled label="Slug">
              <Input value={modal.slug} onChange={(e) => setModal({ ...modal, slug: e.target.value })} />
            </Labeled>
            <Labeled label="Category">
              <Select
                value={modal.category}
                onChange={(e) => setModal({ ...modal, category: e.target.value as 'government' | 'it' })}
              >
                <option value="government">government</option>
                <option value="it">it</option>
              </Select>
            </Labeled>
            <Labeled label="Level">
              <Select value={modal.level} onChange={(e) => setModal({ ...modal, level: e.target.value })}>
                <option value="beginner">beginner</option>
                <option value="intermediate">intermediate</option>
                <option value="advanced">advanced</option>
              </Select>
            </Labeled>
            <div className="sm:col-span-2">
              <Labeled label="Description">
                <Textarea
                  value={modal.description}
                  onChange={(e) => setModal({ ...modal, description: e.target.value })}
                />
              </Labeled>
            </div>
            <Labeled label="Icon (lucide name)">
              <Input value={modal.icon} onChange={(e) => setModal({ ...modal, icon: e.target.value })} />
            </Labeled>
            <Labeled label="Order">
              <Input
                type="number"
                value={modal.order}
                onChange={(e) => setModal({ ...modal, order: Number(e.target.value) })}
              />
            </Labeled>
            <label className="flex items-center gap-2 text-sm font-medium text-slate-600 dark:text-slate-300">
              <input
                type="checkbox"
                checked={modal.career_path}
                onChange={(e) => setModal({ ...modal, career_path: e.target.checked })}
                className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
              />
              Career path
            </label>
            <label className="flex items-center gap-2 text-sm font-medium text-slate-600 dark:text-slate-300">
              <input
                type="checkbox"
                checked={modal.is_published}
                onChange={(e) => setModal({ ...modal, is_published: e.target.checked })}
                className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
              />
              Published
            </label>
            <div className="flex justify-end gap-2 sm:col-span-2">
              <Button type="button" variant="ghost" onClick={() => setModal(null)}>
                Cancel
              </Button>
              <Button type="submit" loading={saving}>
                {modal.id ? 'Save changes' : 'Create course'}
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}

function LessonEditForm({
  lesson,
  topic,
  onCancel,
  onSave,
}: {
  lesson: LessonItem & { content?: unknown };
  topic: Topic;
  onCancel: () => void;
  onSave: (topic: Topic, lesson: LessonItem, contentText: string, e: FormEvent) => void | Promise<void>;
}) {
  const [title, setTitle] = useState(lesson.title);
  const [order, setOrder] = useState(lesson.order ?? 0);
  const [content, setContent] = useState(() =>
    typeof lesson.content === 'string' ? lesson.content : JSON.stringify(lesson.content ?? {}, null, 2)
  );
  return (
    <form
      onSubmit={(e) => {
        void onSave(topic, { ...lesson, title, order }, content, e);
      }}
      className="grid gap-3 rounded-xl border border-brand-300 p-3 dark:border-brand-500/40 sm:grid-cols-3"
    >
      <Labeled label="Lesson title">
        <Input value={title} onChange={(e) => setTitle(e.target.value)} />
      </Labeled>
      <Labeled label="Order">
        <Input type="number" value={order} onChange={(e) => setOrder(Number(e.target.value))} />
      </Labeled>
      <div className="flex items-end gap-2">
        <Button type="submit">Save</Button>
        <Button type="button" variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
      </div>
      <div className="sm:col-span-3">
        <Labeled label="Content (JSON)">
          <Textarea className="font-mono text-xs" value={content} onChange={(e) => setContent(e.target.value)} />
        </Labeled>
      </div>
    </form>
  );
}

/* ----------------------------------- Quizzes ---------------------------------- */

interface QuizFormState {
  id?: number;
  title: string;
  slug: string;
  quiz_type: string;
  difficulty: string;
  duration_minutes: number;
  negative_marks: number;
  topic_id: string;
  exam_id: string;
  meta: string;
  is_published: boolean;
}

const EMPTY_QUIZ: QuizFormState = {
  title: '',
  slug: '',
  quiz_type: 'topic',
  difficulty: 'beginner',
  duration_minutes: 15,
  negative_marks: 0,
  topic_id: '',
  exam_id: '',
  meta: '{}',
  is_published: true,
};

const EMPTY_QUESTION = {
  question_text: '',
  options: ['', '', '', ''],
  correct_index: 0,
  explanation: '',
  difficulty: 'beginner',
};

function QuizzesPanel() {
  const [quizzes, setQuizzes] = useState<AdminQuiz[] | null>(null);
  const [modal, setModal] = useState<QuizFormState | null>(null);
  const [saving, setSaving] = useState(false);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [questions, setQuestions] = useState<Record<number, AdminQuestion[]>>({});
  const [questionsLoading, setQuestionsLoading] = useState<number | null>(null);
  const [qForm, setQForm] = useState({ ...EMPTY_QUESTION });
  const [editingQuestion, setEditingQuestion] = useState<AdminQuestion | null>(null);
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = async () => {
    try {
      const data = await get<unknown>('/admin/quizzes');
      setQuizzes(toItems<AdminQuiz>(data));
    } catch (err) {
      toast.error(errorMessage(err));
      setQuizzes([]);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const openCreate = () => setModal({ ...EMPTY_QUIZ });

  const openEdit = (quiz: AdminQuiz) => {
    setModal({
      id: quiz.id,
      title: quiz.title,
      slug: quiz.slug,
      quiz_type: quiz.quiz_type,
      difficulty: quiz.difficulty,
      duration_minutes: quiz.duration_minutes,
      negative_marks: quiz.negative_marks,
      topic_id: quiz.topic_id ? String(quiz.topic_id) : '',
      exam_id: quiz.exam_id ? String(quiz.exam_id) : '',
      meta: JSON.stringify(quiz.meta ?? {}, null, 2),
      is_published: quiz.is_published,
    });
  };

  const saveQuiz = async (e: FormEvent) => {
    e.preventDefault();
    if (!modal) return;
    const meta = parseJson(modal.meta, 'Meta');
    if (meta === null) return;
    const payload = {
      title: modal.title.trim(),
      slug: modal.slug.trim(),
      quiz_type: modal.quiz_type,
      difficulty: modal.difficulty,
      duration_minutes: modal.duration_minutes,
      negative_marks: modal.negative_marks,
      topic_id: modal.topic_id ? Number(modal.topic_id) : null,
      exam_id: modal.exam_id ? Number(modal.exam_id) : null,
      meta,
      is_published: modal.is_published,
    };
    if (!payload.title || !payload.slug) {
      toast.error('Title and slug are required.');
      return;
    }
    setSaving(true);
    try {
      if (modal.id) {
        await put(`/admin/quizzes/${modal.id}`, payload);
        toast.success('Quiz updated');
      } else {
        await post('/admin/quizzes', payload);
        toast.success('Quiz created');
      }
      setModal(null);
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const removeQuiz = async (quiz: AdminQuiz) => {
    if (!window.confirm(`Delete quiz "${quiz.title}"?`)) return;
    try {
      await del(`/admin/quizzes/${quiz.id}`);
      toast.success('Quiz deleted');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const togglePublish = async (quiz: AdminQuiz) => {
    setBusyId(quiz.id);
    try {
      await post(`/admin/quizzes/${quiz.id}/publish`);
      toast.success(quiz.is_published ? 'Quiz unpublished' : 'Quiz published');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  const loadQuestions = async (quiz: AdminQuiz) => {
    if (expandedId === quiz.id) {
      setExpandedId(null);
      setEditingQuestion(null);
      return;
    }
    setExpandedId(quiz.id);
    setEditingQuestion(null);
    setQForm({ ...EMPTY_QUESTION });
    setQuestionsLoading(quiz.id);
    try {
      const data = await get<unknown>(`/quizzes/${quiz.id}/questions`);
      setQuestions((prev) => ({ ...prev, [quiz.id]: toItems<AdminQuestion>(data) }));
    } catch (err) {
      toast.error(errorMessage(err));
      setQuestions((prev) => ({ ...prev, [quiz.id]: [] }));
    } finally {
      setQuestionsLoading(null);
    }
  };

  const addQuestion = async (quiz: AdminQuiz, e: FormEvent) => {
    e.preventDefault();
    if (!qForm.question_text.trim()) {
      toast.error('Question text is required.');
      return;
    }
    if (qForm.options.some((o) => !o.trim())) {
      toast.error('All four options are required.');
      return;
    }
    try {
      await post('/admin/questions', {
        quiz_id: quiz.id,
        question_text: qForm.question_text.trim(),
        options: qForm.options.map((o) => o.trim()),
        correct_index: qForm.correct_index,
        explanation: qForm.explanation,
        difficulty: qForm.difficulty,
      });
      toast.success('Question added');
      setQForm({ ...EMPTY_QUESTION });
      const data = await get<unknown>(`/quizzes/${quiz.id}/questions`);
      setQuestions((prev) => ({ ...prev, [quiz.id]: toItems<AdminQuestion>(data) }));
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const saveQuestion = async (quiz: AdminQuiz, question: AdminQuestion, e: FormEvent) => {
    e.preventDefault();
    try {
      await put(`/admin/questions/${question.id}`, {
        quiz_id: quiz.id,
        question_text: question.question_text,
        options: question.options,
        correct_index: question.correct_index,
        explanation: question.explanation,
        difficulty: question.difficulty,
      });
      toast.success('Question updated');
      setEditingQuestion(null);
      const data = await get<unknown>(`/quizzes/${quiz.id}/questions`);
      setQuestions((prev) => ({ ...prev, [quiz.id]: toItems<AdminQuestion>(data) }));
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const removeQuestion = async (quiz: AdminQuiz, question: AdminQuestion) => {
    if (!window.confirm('Delete this question?')) return;
    try {
      await del(`/admin/questions/${question.id}`);
      toast.success('Question deleted');
      setQuestions((prev) => ({
        ...prev,
        [quiz.id]: (prev[quiz.id] ?? []).filter((q) => q.id !== question.id),
      }));
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  if (!quizzes) return <Spinner />;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <PageNote>{quizzes.length} quizzes</PageNote>
        <Button onClick={openCreate}>
          <Plus className="h-4 w-4" /> New quiz
        </Button>
      </div>

      {quizzes.length === 0 ? (
        <EmptyState title="No quizzes yet" description="Create a quiz to start collecting attempts." />
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-800">
                <th className="px-4 py-3 font-semibold"></th>
                <th className="px-4 py-3 font-semibold">Title</th>
                <th className="px-4 py-3 font-semibold">Type</th>
                <th className="px-4 py-3 font-semibold">Difficulty</th>
                <th className="px-4 py-3 font-semibold">Questions</th>
                <th className="px-4 py-3 font-semibold">Status</th>
                <th className="px-4 py-3 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {quizzes.map((quiz) => (
                <>
                  <tr key={quiz.id} className="border-b border-slate-100 dark:border-slate-800">
                    <td className="px-4 py-3">
                      <button
                        type="button"
                        aria-label="Expand questions"
                        onClick={() => void loadQuestions(quiz)}
                        className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                      >
                        {questionsLoading === quiz.id ? (
                          <Spinner className="py-0" />
                        ) : expandedId === quiz.id ? (
                          <ChevronDown className="h-4 w-4" />
                        ) : (
                          <ChevronRight className="h-4 w-4" />
                        )}
                      </button>
                    </td>
                    <td className="px-4 py-3">
                      <p className="font-semibold text-slate-800 dark:text-slate-100">{quiz.title}</p>
                      <p className="text-xs text-slate-400">/{quiz.slug}</p>
                    </td>
                    <td className="px-4 py-3">
                      <Badge color="brand">{quiz.quiz_type}</Badge>
                    </td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{quiz.difficulty}</td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-300">
                      {quiz.total_questions ?? questions[quiz.id]?.length ?? '—'}
                    </td>
                    <td className="px-4 py-3">
                      <Badge color={quiz.is_published ? 'green' : 'slate'}>
                        {quiz.is_published ? 'published' : 'draft'}
                      </Badge>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex justify-end gap-1">
                        <button
                          type="button"
                          onClick={() => void togglePublish(quiz)}
                          disabled={busyId === quiz.id}
                          className="rounded-lg px-2 py-1.5 text-xs font-semibold text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
                        >
                          {quiz.is_published ? 'Unpublish' : 'Publish'}
                        </button>
                        <button
                          type="button"
                          aria-label="Edit quiz"
                          onClick={() => openEdit(quiz)}
                          className="rounded-lg p-1.5 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-500/10"
                        >
                          <Pencil className="h-4 w-4" />
                        </button>
                        <button
                          type="button"
                          aria-label="Delete quiz"
                          onClick={() => void removeQuiz(quiz)}
                          className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                  {expandedId === quiz.id && (
                    <tr key={`${quiz.id}-q`}>
                      <td colSpan={7} className="bg-slate-50 px-4 py-4 dark:bg-slate-950/50">
                        {questions[quiz.id] === undefined ? (
                          <Spinner className="py-4" />
                        ) : (
                          <div className="space-y-3">
                            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                              Questions ({questions[quiz.id].length})
                            </p>

                            <form
                              onSubmit={(e) => void addQuestion(quiz, e)}
                              className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
                            >
                              <Labeled label="Question text">
                                <Textarea
                                  value={qForm.question_text}
                                  onChange={(e) => setQForm({ ...qForm, question_text: e.target.value })}
                                />
                              </Labeled>
                              <div className="grid gap-3 sm:grid-cols-2">
                                {qForm.options.map((opt, i) => (
                                  <Labeled key={i} label={`Option ${i + 1}`}>
                                    <Input
                                      value={opt}
                                      onChange={(e) => {
                                        const next = [...qForm.options];
                                        next[i] = e.target.value;
                                        setQForm({ ...qForm, options: next });
                                      }}
                                    />
                                  </Labeled>
                                ))}
                              </div>
                              <div className="flex flex-wrap items-center gap-4">
                                <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                                  Correct option
                                </span>
                                {qForm.options.map((_, i) => (
                                  <label key={i} className="flex items-center gap-1.5 text-sm text-slate-600 dark:text-slate-300">
                                    <input
                                      type="radio"
                                      name={`correct-${quiz.id}`}
                                      checked={qForm.correct_index === i}
                                      onChange={() => setQForm({ ...qForm, correct_index: i })}
                                      className="h-4 w-4 border-slate-300 text-brand-600 focus:ring-brand-500"
                                    />
                                    {i + 1}
                                  </label>
                                ))}
                              </div>
                              <div className="grid gap-3 sm:grid-cols-2">
                                <Labeled label="Explanation">
                                  <Textarea
                                    value={qForm.explanation}
                                    onChange={(e) => setQForm({ ...qForm, explanation: e.target.value })}
                                  />
                                </Labeled>
                                <Labeled label="Difficulty">
                                  <Select
                                    value={qForm.difficulty}
                                    onChange={(e) => setQForm({ ...qForm, difficulty: e.target.value })}
                                  >
                                    <option value="beginner">beginner</option>
                                    <option value="intermediate">intermediate</option>
                                    <option value="advanced">advanced</option>
                                  </Select>
                                </Labeled>
                              </div>
                              <div>
                                <Button type="submit">Add question</Button>
                              </div>
                            </form>

                            {questions[quiz.id].length === 0 && <PageNote>No questions yet.</PageNote>}

                            <div className="space-y-2">
                              {questions[quiz.id].map((question, index) =>
                                editingQuestion?.id === question.id ? (
                                  <form
                                    key={question.id}
                                    onSubmit={(e) => void saveQuestion(quiz, question, e)}
                                    className="grid gap-3 rounded-xl border border-brand-300 bg-white p-4 dark:border-brand-500/40 dark:bg-slate-900"
                                  >
                                    <Labeled label="Question text">
                                      <Textarea
                                        value={question.question_text}
                                        onChange={(e) =>
                                          setEditingQuestion({ ...editingQuestion, question_text: e.target.value })
                                        }
                                      />
                                    </Labeled>
                                    <div className="grid gap-3 sm:grid-cols-2">
                                      {question.options.map((opt, i) => (
                                        <Labeled key={i} label={`Option ${i + 1}`}>
                                          <Input
                                            value={opt}
                                            onChange={(e) => {
                                              const next = [...editingQuestion.options];
                                              next[i] = e.target.value;
                                              setEditingQuestion({ ...editingQuestion, options: next });
                                            }}
                                          />
                                        </Labeled>
                                      ))}
                                    </div>
                                    <div className="flex flex-wrap items-center gap-4">
                                      <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                                        Correct option
                                      </span>
                                      {question.options.map((_, i) => (
                                        <label
                                          key={i}
                                          className="flex items-center gap-1.5 text-sm text-slate-600 dark:text-slate-300"
                                        >
                                          <input
                                            type="radio"
                                            name={`edit-correct-${question.id}`}
                                            checked={editingQuestion.correct_index === i}
                                            onChange={() => setEditingQuestion({ ...editingQuestion, correct_index: i })}
                                            className="h-4 w-4 border-slate-300 text-brand-600 focus:ring-brand-500"
                                          />
                                          {i + 1}
                                        </label>
                                      ))}
                                    </div>
                                    <Labeled label="Explanation">
                                      <Textarea
                                        value={editingQuestion.explanation ?? ''}
                                        onChange={(e) =>
                                          setEditingQuestion({ ...editingQuestion, explanation: e.target.value })
                                        }
                                      />
                                    </Labeled>
                                    <div className="flex gap-2">
                                      <Button type="submit">Save question</Button>
                                      <Button type="button" variant="ghost" onClick={() => setEditingQuestion(null)}>
                                        Cancel
                                      </Button>
                                    </div>
                                  </form>
                                ) : (
                                  <div
                                    key={question.id}
                                    className="rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-900"
                                  >
                                    <div className="flex items-start gap-3">
                                      <span className="text-xs font-black text-brand-600 dark:text-brand-400">
                                        Q{index + 1}
                                      </span>
                                      <p className="min-w-0 flex-1 text-sm font-medium text-slate-700 dark:text-slate-200">
                                        {question.question_text}
                                      </p>
                                      <button
                                        type="button"
                                        aria-label="Edit question"
                                        onClick={() => setEditingQuestion(question)}
                                        className="rounded-lg p-1.5 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-500/10"
                                      >
                                        <Pencil className="h-4 w-4" />
                                      </button>
                                      <button
                                        type="button"
                                        aria-label="Delete question"
                                        onClick={() => void removeQuestion(quiz, question)}
                                        className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                                      >
                                        <Trash2 className="h-4 w-4" />
                                      </button>
                                    </div>
                                    <ul className="mt-2 grid gap-1 sm:grid-cols-2">
                                      {question.options.map((opt, oi) => (
                                        <li
                                          key={oi}
                                          className={`rounded-lg px-2 py-1 text-xs ${
                                            oi === question.correct_index
                                              ? 'bg-emerald-50 font-semibold text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-300'
                                              : 'text-slate-500 dark:text-slate-400'
                                          }`}
                                        >
                                          {String.fromCharCode(65 + oi)}. {opt}
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal
        open={modal !== null}
        onClose={() => setModal(null)}
        title={modal?.id ? 'Edit quiz' : 'New quiz'}
        wide
      >
        {modal && (
          <form onSubmit={saveQuiz} className="grid gap-4 sm:grid-cols-2">
            <Labeled label="Title">
              <Input value={modal.title} onChange={(e) => setModal({ ...modal, title: e.target.value })} />
            </Labeled>
            <Labeled label="Slug">
              <Input value={modal.slug} onChange={(e) => setModal({ ...modal, slug: e.target.value })} />
            </Labeled>
            <Labeled label="Quiz type">
              <Select value={modal.quiz_type} onChange={(e) => setModal({ ...modal, quiz_type: e.target.value })}>
                <option value="topic">topic</option>
                <option value="pyq">pyq</option>
                <option value="mock">mock</option>
                <option value="current_affair">current_affair</option>
                <option value="ai">ai</option>
              </Select>
            </Labeled>
            <Labeled label="Difficulty">
              <Select value={modal.difficulty} onChange={(e) => setModal({ ...modal, difficulty: e.target.value })}>
                <option value="beginner">beginner</option>
                <option value="intermediate">intermediate</option>
                <option value="advanced">advanced</option>
              </Select>
            </Labeled>
            <Labeled label="Duration (minutes)">
              <Input
                type="number"
                value={modal.duration_minutes}
                onChange={(e) => setModal({ ...modal, duration_minutes: Number(e.target.value) })}
              />
            </Labeled>
            <Labeled label="Negative marks">
              <Input
                type="number"
                step="0.25"
                value={modal.negative_marks}
                onChange={(e) => setModal({ ...modal, negative_marks: Number(e.target.value) })}
              />
            </Labeled>
            <Labeled label="Topic ID (optional)">
              <Input
                value={modal.topic_id}
                onChange={(e) => setModal({ ...modal, topic_id: e.target.value })}
                placeholder="leave empty"
              />
            </Labeled>
            <Labeled label="Exam ID (optional)">
              <Input
                value={modal.exam_id}
                onChange={(e) => setModal({ ...modal, exam_id: e.target.value })}
                placeholder="leave empty"
              />
            </Labeled>
            <div className="sm:col-span-2">
              <Labeled label="Meta (JSON)">
                <Textarea
                  className="font-mono text-xs"
                  value={modal.meta}
                  onChange={(e) => setModal({ ...modal, meta: e.target.value })}
                />
              </Labeled>
            </div>
            <label className="flex items-center gap-2 text-sm font-medium text-slate-600 dark:text-slate-300">
              <input
                type="checkbox"
                checked={modal.is_published}
                onChange={(e) => setModal({ ...modal, is_published: e.target.checked })}
                className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
              />
              Published
            </label>
            <div className="flex justify-end gap-2 sm:col-span-2">
              <Button type="button" variant="ghost" onClick={() => setModal(null)}>
                Cancel
              </Button>
              <Button type="submit" loading={saving}>
                {modal.id ? 'Save changes' : 'Create quiz'}
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}

/* ----------------------------------- Content ---------------------------------- */

interface CaFormState {
  id?: number;
  title: string;
  slug: string;
  period: string;
  date: string;
  summary: string;
  content: string;
  ai_content: string;
}

const EMPTY_CA: CaFormState = {
  title: '',
  slug: '',
  period: 'daily',
  date: new Date().toISOString().slice(0, 10),
  summary: '',
  content: '',
  ai_content: '{\n  "mcqs": [],\n  "short_questions": [],\n  "revision_notes": ""\n}',
};

function ContentPanel() {
  const [items, setItems] = useState<CaDetail[] | null>(null);
  const [modal, setModal] = useState<CaFormState | null>(null);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = async () => {
    try {
      const data = await get<unknown>('/current-affairs');
      setItems(toItems<CaDetail>(data));
    } catch (err) {
      toast.error(errorMessage(err));
      setItems([]);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const openCreate = () => setModal({ ...EMPTY_CA });

  const openEdit = async (item: CaDetail) => {
    setBusyId(item.id);
    try {
      const detail = await get<CaDetail>(`/current-affairs/${item.slug}`);
      setModal({
        id: detail.id,
        title: detail.title,
        slug: detail.slug,
        period: detail.period,
        date: (detail.date ?? '').slice(0, 10),
        summary: detail.summary ?? '',
        content: detail.content ?? '',
        ai_content: JSON.stringify(detail.ai_content ?? {}, null, 2),
      });
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  const saveItem = async (e: FormEvent) => {
    e.preventDefault();
    if (!modal) return;
    const ai = parseJson(modal.ai_content, 'AI content');
    if (ai === null) return;
    if (!modal.title.trim() || !modal.slug.trim()) {
      toast.error('Title and slug are required.');
      return;
    }
    setSaving(true);
    const payload = {
      title: modal.title.trim(),
      slug: modal.slug.trim(),
      period: modal.period,
      date: modal.date,
      summary: modal.summary,
      content: modal.content,
      ai_content: ai,
      is_published: true,
    };
    try {
      if (modal.id) {
        await put(`/admin/current-affairs/${modal.id}`, payload);
        toast.success('Current affair updated');
      } else {
        await post('/admin/current-affairs', payload);
        toast.success('Current affair created');
      }
      setModal(null);
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const removeItem = async (item: CaDetail) => {
    if (!window.confirm(`Delete "${item.title}"?`)) return;
    try {
      await del(`/admin/current-affairs/${item.id}`);
      toast.success('Deleted');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  const generateQuiz = async (item: CaDetail) => {
    setBusyId(item.id);
    try {
      const quiz = await post<{ id?: number; title?: string }>(`/current-affairs/${item.id}/generate-quiz`);
      toast.success(`Quiz created${quiz?.title ? `: ${quiz.title}` : ''}`);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  if (!items) return <Spinner />;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <PageNote>{items.length} current affairs</PageNote>
        <Button onClick={openCreate}>
          <Plus className="h-4 w-4" /> New entry
        </Button>
      </div>

      {items.length === 0 ? (
        <EmptyState title="No content yet" description="Create the first current affairs entry." />
      ) : (
        <div className="space-y-3">
          {items.map((item) => {
            const mcqs = item.ai_content?.mcqs ?? [];
            const hasMcqs = mcqs.length > 0;
            return (
              <Card key={item.id} className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="font-bold text-slate-900 dark:text-white">{item.title}</h3>
                    <Badge color={item.period === 'daily' ? 'brand' : item.period === 'weekly' ? 'violet' : 'amber'}>
                      {item.period}
                    </Badge>
                    <Badge color="slate">{formatDate(item.date)}</Badge>
                  </div>
                  <p className="mt-1 line-clamp-2 text-sm text-slate-500 dark:text-slate-400">{item.summary}</p>
                </div>
                <div className="flex shrink-0 flex-wrap gap-2">
                  {hasMcqs && (
                    <Button
                      variant="secondary"
                      onClick={() => void generateQuiz(item)}
                      loading={busyId === item.id}
                    >
                      Generate quiz ({mcqs.length})
                    </Button>
                  )}
                  <Button variant="outline" onClick={() => void openEdit(item)} loading={busyId === item.id}>
                    <Pencil className="h-4 w-4" /> Edit
                  </Button>
                  <Button variant="danger" onClick={() => void removeItem(item)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <Modal
        open={modal !== null}
        onClose={() => setModal(null)}
        title={modal?.id ? 'Edit current affair' : 'New current affair'}
        wide
      >
        {modal && (
          <form onSubmit={saveItem} className="grid gap-4 sm:grid-cols-2">
            <Labeled label="Title">
              <Input value={modal.title} onChange={(e) => setModal({ ...modal, title: e.target.value })} />
            </Labeled>
            <Labeled label="Slug">
              <Input value={modal.slug} onChange={(e) => setModal({ ...modal, slug: e.target.value })} />
            </Labeled>
            <Labeled label="Period">
              <Select value={modal.period} onChange={(e) => setModal({ ...modal, period: e.target.value })}>
                <option value="daily">daily</option>
                <option value="weekly">weekly</option>
                <option value="monthly">monthly</option>
              </Select>
            </Labeled>
            <Labeled label="Date">
              <Input
                type="date"
                value={modal.date}
                onChange={(e) => setModal({ ...modal, date: e.target.value })}
              />
            </Labeled>
            <div className="sm:col-span-2">
              <Labeled label="Summary">
                <Textarea value={modal.summary} onChange={(e) => setModal({ ...modal, summary: e.target.value })} />
              </Labeled>
            </div>
            <div className="sm:col-span-2">
              <Labeled label="Content">
                <Textarea
                  className="min-h-[140px]"
                  value={modal.content}
                  onChange={(e) => setModal({ ...modal, content: e.target.value })}
                />
              </Labeled>
            </div>
            <div className="sm:col-span-2">
              <Labeled label="AI content (JSON)">
                <Textarea
                  className="font-mono text-xs"
                  value={modal.ai_content}
                  onChange={(e) => setModal({ ...modal, ai_content: e.target.value })}
                />
              </Labeled>
            </div>
            <div className="flex justify-end gap-2 sm:col-span-2">
              <Button type="button" variant="ghost" onClick={() => setModal(null)}>
                Cancel
              </Button>
              <Button type="submit" loading={saving}>
                {modal.id ? 'Save changes' : 'Create entry'}
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}

/* ------------------------------------ Jobs ------------------------------------ */

interface JobFormState {
  id?: number;
  title: string;
  company: string;
  type: string;
  category: string;
  description: string;
  location: string;
  salary: string;
  apply_link: string;
  deadline: string;
  source: string;
  is_published: boolean;
}

const EMPTY_JOB: JobFormState = {
  title: '',
  company: '',
  type: 'government',
  category: 'notification',
  description: '',
  location: '',
  salary: '',
  apply_link: '',
  deadline: '',
  source: '',
  is_published: true,
};

interface SyncSource {
  key: string;
  label: string;
  job_type: string;
}

interface SyncRun {
  key?: string;
  label?: string;
  job_type?: string;
  ok?: boolean;
  fetched?: number;
  error?: string;
}

interface SyncStatus {
  token_configured: boolean;
  last_synced_at: string | null;
  seed_jobs_remaining?: number;
  max_items_per_source?: number;
  sources: SyncSource[];
  by_source: { source: string; job_type: string; count: number; last_synced_at: string | null }[];
}

interface SyncResult {
  ok: boolean;
  duration_seconds: number;
  created: number;
  updated: number;
  purged_seed_jobs: number;
  retired_expired: number;
  synced_total: number;
  jobs_total: number;
  sources: SyncRun[];
}

function JobsPanel() {
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [modal, setModal] = useState<JobFormState | null>(null);
  const [saving, setSaving] = useState(false);
  const [syncStatus, setSyncStatus] = useState<SyncStatus | null>(null);
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null);
  const [syncing, setSyncing] = useState(false);

  const load = async () => {
    try {
      const data = await get<unknown>('/admin/jobs');
      setJobs(toItems<Job>(data));
    } catch (err) {
      toast.error(errorMessage(err));
      setJobs([]);
    }
  };

  const loadStatus = async () => {
    try {
      setSyncStatus(await get<SyncStatus>('/admin/jobs/sync/status'));
    } catch {
      setSyncStatus(null);
    }
  };

  useEffect(() => {
    void load();
    void loadStatus();
  }, []);

  const runSync = async () => {
    if (syncing) return;
    if (syncStatus && !syncStatus.token_configured) {
      toast.error('Set APIFY_TOKEN in .env before syncing live jobs.');
      return;
    }
    setSyncing(true);
    toast.loading('Crawling job boards — this can take a few minutes…', { id: 'job-sync' });
    try {
      const result = await post<SyncResult>('/admin/jobs/sync');
      setSyncResult(result);
      const failed = result.sources.filter((run) => !run.ok);
      if (failed.length) {
        toast.error(
          `Synced ${result.jobs_total} jobs, but ${failed.length} source(s) failed: ${failed
            .map((run) => run.key ?? 'source')
            .join(', ')}`,
          { id: 'job-sync', duration: 8000 }
        );
      } else {
        toast.success(
          `Synced ${result.synced_total} listings · ${result.created} new · ${result.updated} updated`,
          { id: 'job-sync', duration: 6000 }
        );
      }
      await Promise.all([load(), loadStatus()]);
    } catch (err) {
      toast.error(errorMessage(err), { id: 'job-sync', duration: 8000 });
    } finally {
      setSyncing(false);
    }
  };

  const saveJob = async (e: FormEvent) => {
    e.preventDefault();
    if (!modal) return;
    if (!modal.title.trim() || !modal.company.trim()) {
      toast.error('Title and company are required.');
      return;
    }
    setSaving(true);
    const payload = { ...modal, deadline: modal.deadline || null };
    try {
      if (modal.id) {
        await put(`/admin/jobs/${modal.id}`, payload);
        toast.success('Job updated');
      } else {
        await post('/admin/jobs', payload);
        toast.success('Job created');
      }
      setModal(null);
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const removeJob = async (job: Job) => {
    if (!window.confirm(`Delete job "${job.title}"?`)) return;
    try {
      await del(`/admin/jobs/${job.id}`);
      toast.success('Job deleted');
      await load();
    } catch (err) {
      toast.error(errorMessage(err));
    }
  };

  if (!jobs) return <Spinner />;

  const categories = modal?.type === 'it' ? CATEGORIES.it : CATEGORIES.government;
  const crawled = (syncStatus?.by_source ?? []).filter((row) => row.source && row.source !== 'manual');

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <PageNote>
          {jobs.length} jobs
          {syncStatus?.last_synced_at
            ? ` · last sync ${formatDate(syncStatus.last_synced_at)}`
            : ' · never synced'}
        </PageNote>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={() => void runSync()} loading={syncing}>
            <RefreshCw className="h-4 w-4" /> Sync now
          </Button>
          <Button onClick={() => setModal({ ...EMPTY_JOB })}>
            <Plus className="h-4 w-4" /> New job
          </Button>
        </div>
      </div>

      {crawled.length > 0 && (
        <div className="card flex flex-wrap items-center gap-2 text-xs">
          <span className="font-semibold text-slate-500 dark:text-slate-400">Live sources:</span>
          {crawled.map((row) => (
            <span
              key={`${row.source}-${row.job_type}`}
              className="inline-flex items-center gap-1.5 rounded-full bg-slate-100 px-2.5 py-1 font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300"
            >
              {titleCase(row.source)} · {row.job_type === 'government' ? 'Gov' : 'IT'}
              <span className="text-brand-600 dark:text-brand-400">{row.count}</span>
            </span>
          ))}
          {syncResult && (
            <span className="ml-auto text-slate-400">
              +{syncResult.created} new · {syncResult.updated} refreshed ·{' '}
              {syncResult.duration_seconds}s
            </span>
          )}
        </div>
      )}

      {jobs.length === 0 ? (
        <EmptyState title="No jobs yet" description="Post the first opportunity for your learners." />
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-800">
                <th className="px-4 py-3 font-semibold">Title</th>
                <th className="px-4 py-3 font-semibold">Company</th>
                <th className="px-4 py-3 font-semibold">Type</th>
                <th className="px-4 py-3 font-semibold">Category</th>
                <th className="px-4 py-3 font-semibold">Deadline</th>
                <th className="px-4 py-3 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr
                  key={job.id}
                  className="border-b border-slate-100 last:border-0 dark:border-slate-800"
                >
                  <td className="px-4 py-3 font-semibold text-slate-800 dark:text-slate-100">{job.title}</td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{job.company}</td>
                  <td className="px-4 py-3">
                    <Badge color={job.type === 'government' ? 'violet' : 'brand'}>{job.type}</Badge>
                  </td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{titleCase(job.category)}</td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-300">
                    {job.deadline ? formatDate(job.deadline) : '—'}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-1">
                      <button
                        type="button"
                        aria-label="Edit job"
                        onClick={() =>
                          setModal({
                            id: job.id,
                            title: job.title,
                            company: job.company,
                            type: job.type,
                            category: job.category,
                            description: job.description ?? '',
                            location: job.location ?? '',
                            salary: job.salary ?? '',
                            apply_link: job.apply_link ?? '',
                            deadline: (job.deadline ?? '').slice(0, 10),
                            source: job.source ?? '',
                            is_published: true,
                          })
                        }
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-brand-50 hover:text-brand-600 dark:hover:bg-brand-500/10"
                      >
                        <Pencil className="h-4 w-4" />
                      </button>
                      <button
                        type="button"
                        aria-label="Delete job"
                        onClick={() => void removeJob(job)}
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600 dark:hover:bg-rose-500/10"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal
        open={modal !== null}
        onClose={() => setModal(null)}
        title={modal?.id ? 'Edit job' : 'New job'}
        wide
      >
        {modal && (
          <form onSubmit={saveJob} className="grid gap-4 sm:grid-cols-2">
            <Labeled label="Title">
              <Input value={modal.title} onChange={(e) => setModal({ ...modal, title: e.target.value })} />
            </Labeled>
            <Labeled label="Company">
              <Input value={modal.company} onChange={(e) => setModal({ ...modal, company: e.target.value })} />
            </Labeled>
            <Labeled label="Type">
              <Select
                value={modal.type}
                onChange={(e) => setModal({ ...modal, type: e.target.value, category: '' })}
              >
                <option value="government">government</option>
                <option value="it">it</option>
              </Select>
            </Labeled>
            <Labeled label="Category">
              <Select value={modal.category} onChange={(e) => setModal({ ...modal, category: e.target.value })}>
                <option value="">select…</option>
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </Select>
            </Labeled>
            <div className="sm:col-span-2">
              <Labeled label="Description">
                <Textarea
                  value={modal.description}
                  onChange={(e) => setModal({ ...modal, description: e.target.value })}
                />
              </Labeled>
            </div>
            <Labeled label="Location">
              <Input value={modal.location} onChange={(e) => setModal({ ...modal, location: e.target.value })} />
            </Labeled>
            <Labeled label="Salary">
              <Input value={modal.salary} onChange={(e) => setModal({ ...modal, salary: e.target.value })} />
            </Labeled>
            <Labeled label="Apply link">
              <Input
                value={modal.apply_link}
                onChange={(e) => setModal({ ...modal, apply_link: e.target.value })}
                placeholder="https://…"
              />
            </Labeled>
            <Labeled label="Deadline">
              <Input
                type="date"
                value={modal.deadline}
                onChange={(e) => setModal({ ...modal, deadline: e.target.value })}
              />
            </Labeled>
            <Labeled label="Source">
              <Input value={modal.source} onChange={(e) => setModal({ ...modal, source: e.target.value })} />
            </Labeled>
            <label className="flex items-center gap-2 text-sm font-medium text-slate-600 dark:text-slate-300">
              <input
                type="checkbox"
                checked={modal.is_published}
                onChange={(e) => setModal({ ...modal, is_published: e.target.checked })}
                className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
              />
              Published
            </label>
            <div className="flex justify-end gap-2 sm:col-span-2">
              <Button type="button" variant="ghost" onClick={() => setModal(null)}>
                Cancel
              </Button>
              <Button type="submit" loading={saving}>
                {modal.id ? 'Save changes' : 'Create job'}
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
}

const CATEGORIES = {
  government: ['notification', 'admit-card', 'upcoming', 'result'],
  it: ['fulltime', 'internship', 'fresher', 'remote', 'contract'],
};

/* ------------------------------------ Users ----------------------------------- */

function UsersPanel() {
  const { user } = useAuth();
  const [users, setUsers] = useState<AdminUser[] | null>(null);
  const [q, setQ] = useState('');
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = async (query: string) => {
    try {
      const data = await get<unknown>('/admin/users', query ? { q: query } : undefined);
      setUsers(toItems<AdminUser>(data));
    } catch (err) {
      toast.error(errorMessage(err));
      setUsers([]);
    }
  };

  useEffect(() => {
    const timer = window.setTimeout(() => void load(q), 250);
    return () => window.clearTimeout(timer);
  }, [q]);

  const patch = async (target: AdminUser, payload: { role?: string; is_active?: boolean }) => {
    setBusyId(target.id);
    try {
      await api.patch(`/admin/users/${target.id}`, payload);
      toast.success('User updated');
      await load(q);
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  const remove = async (target: AdminUser) => {
    if (!window.confirm(`Delete user ${target.email}? This cannot be undone.`)) return;
    setBusyId(target.id);
    try {
      await del(`/admin/users/${target.id}`);
      toast.success('User deleted');
      setUsers((prev) => (prev ?? []).filter((u) => u.id !== target.id));
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setBusyId(null);
    }
  };

  if (!users) return <Spinner />;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="w-full max-w-sm">
          <Input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search by name or email…"
            aria-label="Search users"
          />
        </div>
        <PageNote>{users.length} users</PageNote>
      </div>

      {users.length === 0 ? (
        <EmptyState title="No users found" description="Try a different search term." />
      ) : (
        <div className="card overflow-x-auto p-0">
          <table className="w-full min-w-[760px] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-800">
                <th className="px-4 py-3 font-semibold">Name</th>
                <th className="px-4 py-3 font-semibold">Email</th>
                <th className="px-4 py-3 font-semibold">Role</th>
                <th className="px-4 py-3 font-semibold">XP</th>
                <th className="px-4 py-3 font-semibold">Level</th>
                <th className="px-4 py-3 font-semibold">Joined</th>
                <th className="px-4 py-3 font-semibold">Active</th>
                <th className="px-4 py-3 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const isSelf = u.id === user?.id;
                return (
                  <tr key={u.id} className="border-b border-slate-100 last:border-0 dark:border-slate-800">
                    <td className="px-4 py-3">
                      <span className="font-semibold text-slate-800 dark:text-slate-100">{u.full_name}</span>
                      {isSelf && <Badge color="brand">you</Badge>}
                    </td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{u.email}</td>
                    <td className="px-4 py-3">
                      <select
                        value={u.role}
                        disabled={isSelf || busyId === u.id}
                        onChange={(e) => void patch(u, { role: e.target.value })}
                        aria-label={`Role for ${u.full_name}`}
                        className="input py-1.5 text-xs disabled:opacity-60"
                      >
                        <option value="student">student</option>
                        <option value="admin">admin</option>
                      </select>
                      {isSelf && <p className="mt-0.5 text-[10px] text-slate-400">own role is locked</p>}
                    </td>
                    <td className="px-4 py-3 tabular-nums text-slate-600 dark:text-slate-300">
                      {u.profile?.xp ?? 0}
                    </td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{u.profile?.level ?? 1}</td>
                    <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{formatDate(u.created_at)}</td>
                    <td className="px-4 py-3">
                      <button
                        type="button"
                        disabled={busyId === u.id}
                        onClick={() => void patch(u, { is_active: !u.is_active })}
                        className={`rounded-full px-2.5 py-1 text-xs font-bold transition ${
                          u.is_active
                            ? 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200 dark:bg-emerald-500/15 dark:text-emerald-300'
                            : 'bg-rose-100 text-rose-700 hover:bg-rose-200 dark:bg-rose-500/15 dark:text-rose-300'
                        }`}
                      >
                        {u.is_active ? 'active' : 'blocked'}
                      </button>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        type="button"
                        aria-label="Delete user"
                        disabled={isSelf || busyId === u.id}
                        onClick={() => void remove(u)}
                        className="rounded-lg p-1.5 text-slate-400 transition hover:bg-rose-50 hover:text-rose-600 disabled:opacity-40 dark:hover:bg-rose-500/10"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
