import { FormEvent, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { AlertTriangle } from 'lucide-react';
import { Button, Input } from '../../components/ui';
import { AuthShell } from '../../components/AuthShell';
import { errorMessage, post } from '../../lib/api';

interface ResetResponse {
  message?: string;
}

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token') ?? '';
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (password.length < 8) {
      toast.error('Password must be at least 8 characters.');
      return;
    }
    if (password !== confirm) {
      toast.error('Passwords do not match.');
      return;
    }
    setLoading(true);
    try {
      const res = await post<ResetResponse>('/auth/reset-password', { token, password });
      toast.success(res.message || 'Password updated. Please sign in.');
      navigate('/login', { replace: true });
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <AuthShell
        title="Invalid reset link"
        footer={
          <Link to="/forgot-password" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Request a new link
          </Link>
        }
      >
        <div className="flex flex-col items-center gap-3 text-center">
          <span className="flex h-12 w-12 items-center justify-center rounded-full bg-rose-100 text-rose-600 dark:bg-rose-500/15 dark:text-rose-300">
            <AlertTriangle className="h-6 w-6" />
          </span>
          <p className="text-sm text-slate-600 dark:text-slate-300">
            This password reset link is missing its token. Please request a new one.
          </p>
        </div>
      </AuthShell>
    );
  }

  return (
    <AuthShell
      title="Set a new password"
      subtitle="Choose a strong password of at least 8 characters."
      footer={
        <>
          Back to{' '}
          <Link to="/login" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            sign in
          </Link>
        </>
      }
    >
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="label" htmlFor="password">
            New password
          </label>
          <Input
            id="password"
            type="password"
            autoComplete="new-password"
            required
            minLength={8}
            placeholder="Minimum 8 characters"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label className="label" htmlFor="confirm">
            Confirm new password
          </label>
          <Input
            id="confirm"
            type="password"
            autoComplete="new-password"
            required
            minLength={8}
            placeholder="Repeat your new password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />
        </div>
        <Button type="submit" loading={loading} className="w-full">
          Update password
        </Button>
      </form>
    </AuthShell>
  );
}
