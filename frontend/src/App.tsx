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
const VideoTutorials = lazy(() => import('./pages/gov/VideoTutorials'));

const ItDashboard = lazy(() => import('./pages/it/ItDashboard'));
const CareerPathDetail = lazy(() => import('./pages/it/CareerPathDetail'));
const LearningPath = lazy(() => import('./pages/it/LearningPath'));
const ItMockTests = lazy(() => import('./pages/it/ItMockTests'));

const DsaPrepWay = lazy(() => import('./pages/dsa/DsaPrepWay'));

const TrackRoadmap = lazy(() => import('./pages/tracks/TrackRoadmap'));
const TrackResources = lazy(() => import('./pages/tracks/TrackResources'));

const StartupJobs = lazy(() => import('./pages/startups/StartupJobs'));

const QuizRunner = lazy(() => import('./pages/quiz/QuizRunner'));

const AiQuizGenerator = lazy(() => import('./pages/ai/AiQuizGenerator'));
const AiInterview = lazy(() => import('./pages/ai/AiInterview'));
const AiPlanner = lazy(() => import('./pages/ai/AiPlanner'));
const AiResume = lazy(() => import('./pages/ai/AiResume'));
const AiResumeAnalyze = lazy(() => import('./pages/ai/AiResumeAnalyze'));
const GeminiChat = lazy(() => import('./pages/ai/GeminiChat'));

const Jobs = lazy(() => import('./pages/jobs/Jobs'));
const JobDetail = lazy(() => import('./pages/jobs/JobDetail'));
const MyJobsList = lazy(() => import('./pages/jobs/MyJobsList'));
const FreeResources = lazy(() => import('./pages/FreeResources'));
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

// Single-level layout wrappers — avoids the old nested <Routes> inside
// <Route path="*"> which forced a full remount + double match on every refresh.
function Public({ children }: { children: ReactNode }) {
  return <PublicLayout>{children}</PublicLayout>;
}

function Protected({ children }: { children: ReactNode }) {
  return (
    <RequireAuth>
      <AppLayout>{children}</AppLayout>
    </RequireAuth>
  );
}

function ProtectedAdmin({ children }: { children: ReactNode }) {
  return (
    <RequireAuth>
      <AppLayout>
        <RequireAdmin>{children}</RequireAdmin>
      </AppLayout>
    </RequireAuth>
  );
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
      {/* Flat route table: one matcher pass per refresh, layout stays mounted
          across navigations so refresh + navigation feel instant. */}
      <Routes>
        <Route path="/" element={<Public><Landing /></Public>} />
        <Route path="/login" element={<Public><Login /></Public>} />
        <Route path="/register" element={<Public><Register /></Public>} />
        <Route path="/pending-approval" element={<Public><PendingApproval /></Public>} />
        <Route path="/forgot-password" element={<Public><ForgotPassword /></Public>} />
        <Route path="/reset-password" element={<Public><ResetPassword /></Public>} />

        {/* Jobs are public so shared links open on any device, logged in or not. */}
        <Route path="/jobs" element={<AppLayout><Jobs /></AppLayout>} />
        <Route path="/jobs/:id" element={<AppLayout><JobDetail /></AppLayout>} />
        <Route path="/my-jobs" element={<Protected><MyJobsList /></Protected>} />
        <Route path="/resources" element={<Protected><FreeResources /></Protected>} />

        <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
        <Route path="/leaderboard" element={<Protected><Leaderboard /></Protected>} />
        <Route path="/search" element={<Protected><Search /></Protected>} />
        <Route path="/profile" element={<Protected><Profile /></Protected>} />

        <Route path="/gov" element={<Protected><GovDashboard /></Protected>} />
        <Route path="/gov/exam/:slug" element={<Protected><GovExamDetail /></Protected>} />
        <Route path="/gov/topic/:slug" element={<Protected><TopicDetail /></Protected>} />
        <Route path="/gov/mock" element={<Protected><MockTests /></Protected>} />
        <Route path="/gov/mock/:slug" element={<Protected><MockTestDetail /></Protected>} />
        <Route path="/gov/pyqs" element={<Protected><Pyqs /></Protected>} />
        <Route path="/gov/current-affairs" element={<Protected><CurrentAffairs /></Protected>} />
        <Route path="/gov/current-affairs/:slug" element={<Protected><CurrentAffairDetail /></Protected>} />
        <Route path="/gov/videos" element={<Protected><VideoTutorials /></Protected>} />
        <Route path="/gov/quizzes/:id" element={<Protected><QuizRunner /></Protected>} />

        <Route path="/it" element={<Protected><ItDashboard /></Protected>} />
        <Route path="/it/path/:slug" element={<Protected><CareerPathDetail /></Protected>} />
        <Route path="/it/learn/:slug" element={<Protected><LearningPath /></Protected>} />
        <Route path="/it/mock" element={<Protected><ItMockTests /></Protected>} />
        <Route path="/it/quizzes/:id" element={<Protected><QuizRunner /></Protected>} />

        <Route path="/dsa/prep-way" element={<Protected><DsaPrepWay /></Protected>} />

        <Route path="/tracks/:slug" element={<Protected><TrackRoadmap /></Protected>} />
        <Route path="/tracks/:slug/resources" element={<Protected><TrackResources /></Protected>} />

        <Route path="/startups" element={<Protected><StartupJobs /></Protected>} />

        <Route path="/ai/quiz-generator" element={<Protected><AiQuizGenerator /></Protected>} />
        <Route path="/ai/interview" element={<Protected><AiInterview /></Protected>} />
        <Route path="/ai/planner" element={<Protected><AiPlanner /></Protected>} />
        <Route path="/ai/resume" element={<Protected><AiResume /></Protected>} />
        <Route path="/ai/resume/analyze" element={<Protected><AiResumeAnalyze /></Protected>} />
        <Route path="/ai/chat" element={<Protected><GeminiChat /></Protected>} />

        <Route path="/admin/*" element={<ProtectedAdmin><Admin /></ProtectedAdmin>} />
        <Route path="*" element={<Protected><NotFound /></Protected>} />
      </Routes>
    </Suspense>
  );
}
