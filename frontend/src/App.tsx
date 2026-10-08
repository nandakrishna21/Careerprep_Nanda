import { ReactNode, useEffect } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { useAuth } from './stores/auth';
import PublicLayout from './layouts/PublicLayout';
import AppLayout from './layouts/AppLayout';
import { Spinner } from './components/ui';

import Landing from './pages/Landing';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';

import Dashboard from './pages/dashboard/Dashboard';
import Leaderboard from './pages/Leaderboard';
import Search from './pages/Search';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

import GovDashboard from './pages/gov/GovDashboard';
import GovExamDetail from './pages/gov/GovExamDetail';
import TopicDetail from './pages/gov/TopicDetail';
import MockTests from './pages/gov/MockTests';
import MockTestDetail from './pages/gov/MockTestDetail';
import Pyqs from './pages/gov/Pyqs';
import CurrentAffairs from './pages/gov/CurrentAffairs';
import CurrentAffairDetail from './pages/gov/CurrentAffairDetail';

import ItDashboard from './pages/it/ItDashboard';
import CareerPathDetail from './pages/it/CareerPathDetail';
import LearningPath from './pages/it/LearningPath';
import ItMockTests from './pages/it/ItMockTests';

import DsaPrepWay from './pages/dsa/DsaPrepWay';

import QuizRunner from './pages/quiz/QuizRunner';

import AiQuizGenerator from './pages/ai/AiQuizGenerator';
import AiInterview from './pages/ai/AiInterview';
import AiPlanner from './pages/ai/AiPlanner';
import AiResume from './pages/ai/AiResume';
import AiResumeAnalyze from './pages/ai/AiResumeAnalyze';

import Jobs from './pages/jobs/Jobs';
import Admin from './pages/admin/Admin';

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
  if (user?.role !== 'admin') return <Navigate to="/dashboard" replace />;
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
      <Route path="/forgot-password" element={<PublicLayout><ForgotPassword /></PublicLayout>} />
      <Route path="/reset-password" element={<PublicLayout><ResetPassword /></PublicLayout>} />

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

                <Route path="/jobs" element={<Jobs />} />
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
  );
}
