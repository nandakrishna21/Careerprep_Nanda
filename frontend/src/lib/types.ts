export interface User {
  id: number;
  full_name: string;
  email: string;
  role: 'student' | 'admin';
  is_active?: boolean;
  created_at?: string;
}

export interface Profile {
  id: number;
  user_id: number;
  headline: string;
  bio: string;
  phone: string;
  education: string;
  skills: string[];
  target_exams: string[];
  avatar_color: string;
  xp: number;
  level: number;
  streak_days: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Topic {
  id: number;
  title: string;
  slug: string;
  description: string;
  order: number;
  lesson_count?: number;
  quiz_count?: number;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  category: 'government' | 'it';
  description: string;
  icon: string;
  level: string;
  order: number;
  career_path: boolean;
  topic_count?: number;
  topics?: Topic[];
}

export interface Exam {
  id: number;
  name: string;
  slug: string;
  category: string;
  description: string;
  pattern: Record<string, unknown>;
}

export interface QuizMeta {
  id: number;
  title: string;
  slug: string;
  quiz_type: string;
  difficulty: string;
  duration_minutes: number;
  total_questions: number;
  negative_marks: number;
  sections: { name: string; question_count: number; marks?: number }[] | null;
  meta: Record<string, unknown>;
  topic?: { id: number; title: string; slug?: string } | null;
  exam?: { id: number; name: string; slug?: string } | null;
}

export interface QuizQuestion {
  id: number;
  question_text: string;
  options: string[];
  order: number;
}

export interface AttemptQuestionReview {
  id: number;
  question_text: string;
  options: string[];
  your_answer: number | null;
  correct_index: number;
  explanation: string;
  is_correct: boolean;
}

export interface AttemptReport {
  attempt: {
    id: number;
    score: number;
    total: number;
    correct: number;
    wrong: number;
    skipped: number;
    accuracy: number;
    time_taken_seconds: number;
    rank: number | null;
    xp_awarded: number;
    created_at: string;
  };
  report: {
    weak_areas: { topic: string; accuracy: number }[];
    strong_areas: { topic: string; accuracy: number }[];
    topic_breakdown: { name: string; total: number; correct: number; accuracy: number }[];
    suggestions: string[];
    section_analysis?: { name: string; attempted: number; correct: number; accuracy: number }[];
    improvement_suggestions?: string[];
    questions: AttemptQuestionReview[];
  };
  achievements_unlocked: { code: string; title: string; icon: string; xp_reward: number }[];
}

export interface MockTest {
  id: number;
  title: string;
  slug: string;
  category: string;
  description: string;
  duration_minutes: number;
  total_questions: number;
  negative_marks: number;
  sections: { name: string; question_count: number; marks?: number }[];
  exam_pattern: Record<string, unknown>;
  quiz_id: number | null;
  attempts_count?: number;
}

export interface CurrentAffair {
  id: number;
  title: string;
  slug: string;
  period: string;
  date: string;
  summary: string;
  content?: string;
  ai_content?: {
    mcqs?: { question: string; options: string[]; correct_index: number; explanation: string }[];
    short_questions?: string[];
    revision_notes?: string;
    quiz_id?: number;
  };
}

export interface Job {
  id: number;
  title: string;
  company: string;
  type: 'government' | 'it';
  category: string;
  description: string;
  location: string;
  salary: string;
  apply_link: string;
  deadline: string | null;
  source: string;
  role?: string;
  city?: string;
  created_at: string;
  is_saved?: boolean;
  save_status?: string;
}

export interface Paged<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface FacetOption {
  value: string;
  label: string;
  count: number;
}

export interface JobFacetGroup {
  roles: FacetOption[];
  locations: FacetOption[];
  categories: FacetOption[];
}

export interface JobFacets {
  all: JobFacetGroup;
  government: JobFacetGroup;
  it: JobFacetGroup;
}

export interface DashboardData {
  total_study_hours: number;
  total_quizzes: number;
  average_score: number;
  strong_topics: { name: string; accuracy: number }[];
  weak_topics: { name: string; accuracy: number }[];
  streak_days: number;
  xp: number;
  level: number;
  weekly_xp: number;
  mock_tests_taken: number;
  badges_unlocked: number;
  daily_activity: { date: string; hours: number; quizzes: number }[];
  performance_trend: { date: string; score: number }[];
  mock_performance: { title: string; score: number; accuracy: number; date: string }[];
}

export interface LeaderboardEntry {
  rank: number;
  id: number;
  full_name: string;
  avatar_color: string;
  xp: number;
  streak_days: number;
  level: number;
}

export interface Achievement {
  id: number;
  code: string;
  title: string;
  description: string;
  icon: string;
  xp_reward: number;
  unlocked: boolean;
  unlocked_at?: string;
}

export interface SearchResult {
  type: string;
  title: string;
  subtitle: string;
  url: string;
}

export interface SearchResponse {
  courses: SearchResult[];
  topics: SearchResult[];
  lessons: SearchResult[];
  quizzes: SearchResult[];
  mock_tests: SearchResult[];
  jobs: SearchResult[];
  current_affairs: SearchResult[];
}

export interface ResumeData {
  personal: { name: string; email: string; phone: string; location: string; summary: string };
  education: { degree: string; school: string; year: string }[];
  skills: string[];
  projects: { name: string; description: string; link: string }[];
  experience: { role: string; company: string; period: string; description: string }[];
}

export interface Resume {
  id: number;
  title: string;
  template: string;
  data: ResumeData;
  ats_score: number | null;
  analysis: {
    ats_score?: number;
    missing_keywords?: string[];
    suggestions?: string[];
    job_recommendations?: { title: string; reason: string }[];
  } | null;
  created_at: string;
}

export interface StudyPlan {
  id: number;
  goal: string;
  exam: string;
  hours_per_day: number;
  duration_days: number;
  plan: {
    daily?: { day: string; items: { time: string; task: string; hours: number }[] }[];
    weekly?: { week: string; focus: string; tasks: string[] }[];
    monthly?: { month: string; milestones: string[] }[];
  };
  created_at: string;
}

export interface InterviewTurn {
  id: number;
  question: string;
  user_answer: string;
  score: number | null;
  strengths: string[];
  weaknesses: string[];
  improved_answer: string;
}

export interface InterviewSession {
  id: number;
  role: string;
  status: string;
  overall_score: number | null;
  summary: { strengths?: string[]; weaknesses?: string[] };
  created_at: string;
  turns?: InterviewTurn[];
}

export interface AiQuestion {
  question_text: string;
  options: string[];
  correct_index: number;
  explanation: string;
  difficulty: string;
}
