import { FormEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { CheckCircle2, KeyRound } from 'lucide-react';
import { Button, Input } from '../../components/ui';
import { AuthShell } from '../../components/AuthShell';
import { errorMessage, post } from '../../lib/api';

interface ForgotResponse {
  message?: string;
  reset_token?: string;
}

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState<ForgotResponse | null>(null);

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!email.trim()) {
      toast.error('Enter your email address.');
      return;
    }
    setLoading(true);
    try {
      const res = await post<ForgotResponse>('/auth/forgot-password', { email: email.trim() });
      setDone(res);
      toast.success(res.message || 'Reset instructions sent.');
    } catch (err) {
      toast.error(errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  if (done) {
    return (
      <AuthShell
        title="Check your inbox"
        footer={
          <Link to="/login" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Back to sign in
          </Link>
        }
      >
        <div className="space-y-4 text-center">
          <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-300">
            <CheckCircle2 className="h-6 w-6" />
          </span>
          <p className="text-sm text-slate-600 dark:text-slate-300">
            {done.message ||
              `If an account exists for ${email}, a password reset link has been sent.`}
          </p>
          {done.reset_token && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-left dark:border-amber-500/30 dark:bg-amber-500/10">
              <p className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-amber-700 dark:text-amber-300">
                <KeyRound className="h-3.5 w-3.5" /> Development mode â€” reset token
              </p>
              <code className="mt-2 block break-all rounded-lg bg-white/70 p-2 text-xs text-slate-700 dark:bg-slate-950/50 dark:text-slate-300">
                {done.reset_token}
              </code>
              <Link
                to={`/reset-password?token=${encodeURIComponent(done.reset_token)}`}
                className="mt-3 inline-flex items-center justify-center rounded-xl bg-amber-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-amber-700"
              >
                Continue to reset password
              </Link>
            </div>
          )}
        </div>
      </AuthShell>
    );
  }

  return (
    <AuthShell
      title="Forgot your password?"
      subtitle="Enter your email and we will send you a reset link."
      footer={
        <>
          Remembered it?{' '}
          <Link to="/login" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Sign in
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
        <Button type="submit" loading={loading} className="w-full">
          Send reset link
        </Button>
      </form>
    </AuthShell>
  );
}
