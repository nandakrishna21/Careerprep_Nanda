import { ReactNode, Suspense, lazy, useEffect } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { useAuth } from './stores/auth';
import PublicLayout from './layouts/PublicLayout';
import AppLayout from './layouts/AppLayout';
import { Spinner } from './components/ui';

// Route pages are lazy-loaded so the first paint only downloads the
// framework + the current route instead of the whole 900 kB+ bundle.
const Landing = lazy(() => import('./pages/Landing'));
const Login = lazy(() => import('./pages/auth/Login'));
const Register = lazy(() => import('./pages/auth/Register'));
const PendingApproval = lazy(() => import('./pages/auth/PendingApproval'));
const ForgotPassword = lazy(() => import('./pages/auth/ForgotPassword'));
const ResetPassword = lazy(() => import('./pages/auth/ResetPassword'));

const Dashboard = lazy(() => import('./pages/dashboard/Dashboard'));
const Leaderboard = lazy(() => import('./pages/Leaderboard'));
const Search = lazy(() => import('./pages/Search'));
const Profile = lazy(() => import('./pages/Profile'));
const NotFound = lazy(() => import('./pages/NotFound'));

const GovDashboard = lazy(() => import('./pages/gov/GovDashboard'));
const GovExamDetail = lazy(() => import('./pages/gov/GovExamDetail'));
const TopicDetail = lazy(() => import('./pages/gov/TopicDetail'));
const MockTests = lazy(() => import('./pages/gov/MockTests'));
const MockTestDetail = lazy(() => import('./pages/gov/MockTestDetail'));
const Pyqs = lazy(() => import('./pages/gov/Pyqs'));
const CurrentAffairs = lazy(() => import('./pages/gov/CurrentAffairs'));
const CurrentAffairDetail = lazy(() => import('./pages/gov/CurrentAffairDetail'));

const ItDashboard = lazy(() => import('./pages/it/ItDashboard'));
const CareerPathDetail = lazy(() => import('./pages/it/CareerPathDetail'));
const LearningPath = lazy(() => import('./pages/it/LearningPath'));
const ItMockTests = lazy(() => import('./pages/it/ItMockTests'));

const DsaPrepWay = lazy(() => import('./pages/dsa/DsaPrepWay'));

const QuizRunner = lazy(() => import('./pages/quiz/QuizRunner'));

const AiQuizGenerator = lazy(() => import('./pages/ai/AiQuizGenerator'));
const AiInterview = lazy(() => import('./pages/ai/AiInterview'));
const AiPlanner = lazy(() => import('./pages/ai/AiPlanner'));
const AiResume = lazy(() => import('./pages/ai/AiResume'));
const AiResumeAnalyze = lazy(() => import('./pages/ai/AiResumeAnalyze'));

const Jobs = lazy(() => import('./pages/jobs/Jobs'));
const JobDetail = lazy(() => import('./pages/jobs/JobDetail'));
const Admin = lazy(() => import('./pages/admin/Admin'));

function RequireAuth({ children }: { children: ReactNode }) {
  const { token, hydrated } = useAuth();
  const location = useLocation();
  if (!hydrated) return <Spinner />;
  if (!token) return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  return <>{children}</>;
}

function RequireAdmin({ children }: { children: ReactNode }) {
  const { user, hydrated } = useAuth();
  if (!hydrated) return <Spinner />;
  if (user?.role !== 'admin' && user?.role !== 'superadmin') return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}

export default function App() {
  const { hydrate, hydrated } = useAuth();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  if (!hydrated) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center">
          <Spinner />
        </div>
      }
    >
    <Routes>
      <Route
        path="/"
        element={
          <PublicLayout>
            <Landing />
          </PublicLayout>
        }
      />
      <Route path="/login" element={<PublicLayout><Login /></PublicLayout>} />
      <Route path="/register" element={<PublicLayout><Register /></PublicLayout>} />
      <Route path="/pending-approval" element={<PublicLayout><PendingApproval /></PublicLayout>} />
      <Route path="/forgot-password" element={<PublicLayout><ForgotPassword /></PublicLayout>} />
      <Route path="/reset-password" element={<PublicLayout><ResetPassword /></PublicLayout>} />

      {/* Jobs are public so shared links open on any device, logged in or not. */}
      <Route path="/jobs" element={<AppLayout><Jobs /></AppLayout>} />
      <Route path="/jobs/:id" element={<AppLayout><JobDetail /></AppLayout>} />

      <Route
        path="*"
        element={
          <RequireAuth>
            <AppLayout>
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/leaderboard" element={<Leaderboard />} />
                <Route path="/search" element={<Search />} />
                <Route path="/profile" element={<Profile />} />

                <Route path="/gov" element={<GovDashboard />} />
                <Route path="/gov/exam/:slug" element={<GovExamDetail />} />
                <Route path="/gov/topic/:slug" element={<TopicDetail />} />
                <Route path="/gov/mock" element={<MockTests />} />
                <Route path="/gov/mock/:slug" element={<MockTestDetail />} />
                <Route path="/gov/pyqs" element={<Pyqs />} />
                <Route path="/gov/current-affairs" element={<CurrentAffairs />} />
                <Route path="/gov/current-affairs/:slug" element={<CurrentAffairDetail />} />
                <Route path="/gov/quizzes/:id" element={<QuizRunner />} />

                <Route path="/it" element={<ItDashboard />} />
                <Route path="/it/path/:slug" element={<CareerPathDetail />} />
                <Route path="/it/learn/:slug" element={<LearningPath />} />
                <Route path="/it/mock" element={<ItMockTests />} />
                <Route path="/it/quizzes/:id" element={<QuizRunner />} />

                <Route path="/dsa/prep-way" element={<DsaPrepWay />} />

                <Route path="/ai/quiz-generator" element={<AiQuizGenerator />} />
                <Route path="/ai/interview" element={<AiInterview />} />
                <Route path="/ai/planner" element={<AiPlanner />} />
                <Route path="/ai/resume" element={<AiResume />} />
                <Route path="/ai/resume/analyze" element={<AiResumeAnalyze />} />

                <Route
                  path="/admin/*"
                  element={
                    <RequireAdmin>
                      <Admin />
                    </RequireAdmin>
                  }
                />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </AppLayout>
          </RequireAuth>
        }
      />
    </Routes>
    </Suspense>
  );
}
