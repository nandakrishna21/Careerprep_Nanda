import { FormEvent, useState } from 'react';
import { Link, Navigate, useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Button, Input } from '../../components/ui';
import { AuthShell } from '../../components/AuthShell';
import { useAuth } from '../../stores/auth';

interface LocationState {
  from?: { pathname?: string };
}

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, token } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();

  const next =
    searchParams.get('next') ||
    (location.state as LocationState | null)?.from?.pathname ||
    '/dashboard';

  if (token) return <Navigate to={next} replace />;

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      toast.error('Enter your email and password.');
      return;
    }
    setLoading(true);
    try {
      await login(email.trim(), password);
      toast.success('Welcome back!');
      navigate(next, { replace: true });
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Unable to sign in.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Welcome back"
      subtitle="Sign in to continue your preparation."
      footer={
        <>
          New here?{' '}
          <Link to="/register" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Create an account
          </Link>
        </>
      }
    >
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="label" htmlFor="email">
            Email address
          </label>
          <Input
            id="email"
            type="email"
            autoComplete="email"
            required
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <div className="flex items-center justify-between">
            <label className="label" htmlFor="password">
              Password
            </label>
            <Link
              to="/forgot-password"
              className="mb-1.5 text-xs font-semibold text-brand-600 hover:underline dark:text-brand-400"
            >
              Forgot password?
            </Link>
          </div>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button type="submit" loading={loading} className="w-full">
          Sign in
        </Button>
      </form>

      <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs text-slate-500 dark:border-slate-800 dark:bg-slate-800/40 dark:text-slate-400">
        Demo account:{' '}
        <span className="font-semibold text-slate-700 dark:text-slate-200">
          student@careerprep.com
        </span>{' '}
        / <span className="font-semibold text-slate-700 dark:text-slate-200">Student@123</span>
      </div>
    </AuthShell>
  );
}
