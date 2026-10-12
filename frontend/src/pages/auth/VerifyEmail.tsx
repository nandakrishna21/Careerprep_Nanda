import { FormEvent, useEffect, useRef, useState } from 'react';
import { Link, Navigate, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { CheckCircle2, MailOpen, XCircle } from 'lucide-react';
import { Button, Input, Spinner } from '../../components/ui';
import { AuthShell } from '../../components/AuthShell';
import { useAuth } from '../../stores/auth';

const RESEND_WAIT_SECONDS = 60;

type Status = 'verifying' | 'done' | 'pending' | 'error' | 'idle';

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token') ?? '';
  const [email, setEmail] = useState(searchParams.get('email') ?? '');
  const [status, setStatus] = useState<Status>(token ? 'verifying' : 'idle');
  const [error, setError] = useState('');
  const [resending, setResending] = useState(false);
  const [cooldown, setCooldown] = useState(0);
  const { verifyEmailToken, resendOtp, token: session } = useAuth();
  const navigate = useNavigate();
  const attempted = useRef(false);

  useEffect(() => {
    if (cooldown <= 0) return;
    const timer = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(timer);
  }, [cooldown]);

  useEffect(() => {
    if (!token || attempted.current) return;
    attempted.current = true;
    (async () => {
      try {
        const result = await verifyEmailToken(token);
        if (result.approved) {
          setStatus('done');
          toast.success('Email verified - welcome aboard!');
          setTimeout(() => navigate('/dashboard', { replace: true }), 1200);
        } else {
          setStatus('pending');
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Verification failed.';
        if (message.toLowerCase().includes('already verified')) {
          toast.success('Email already verified - please sign in.');
          navigate('/login', { replace: true });
          return;
        }
        setError(message);
        setStatus('error');
      }
    })();
  }, [token, verifyEmailToken, navigate]);

  if (session) return <Navigate to="/dashboard" replace />;

  const onResend = async (e?: FormEvent) => {
    e?.preventDefault();
    if (!email.trim()) {
      toast.error('Enter your email address first.');
      return;
    }
    if (cooldown > 0 || resending) return;
    setResending(true);
    try {
      await resendOtp(email.trim());
      toast.success('A fresh verification link is on its way to your inbox.');
      setCooldown(RESEND_WAIT_SECONDS);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Unable to resend the link.');
    } finally {
      setResending(false);
    }
  };

  return (
    <AuthShell
      title="Verify your email"
      subtitle="Open the verification link we emailed you to activate your account."
      footer={
        <>
          Wrong email?{' '}
          <Link to="/register" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Sign up again
          </Link>
        </>
      }
    >
      {status === 'verifying' && (
        <div className="flex flex-col items-center gap-3 py-6">
          <Spinner />
          <p className="text-sm text-slate-500 dark:text-slate-400">Verifying your link…</p>
        </div>
      )}

      {status === 'done' && (
        <div className="flex flex-col items-center gap-2 py-6 text-center">
          <CheckCircle2 className="h-12 w-12 text-emerald-500" />
          <p className="font-bold text-slate-900 dark:text-white">Email verified!</p>
          <p className="text-sm text-slate-500 dark:text-slate-400">Taking you to your dashboard…</p>
        </div>
      )}

      {status === 'pending' && (
        <div className="flex flex-col items-center gap-2 py-6 text-center">
          <MailOpen className="h-12 w-12 text-amber-500" />
          <p className="font-bold text-slate-900 dark:text-white">Almost there!</p>
          <p className="max-w-sm text-sm text-slate-500 dark:text-slate-400">
            Your email is verified. Your account is now awaiting approval by the super admin —
            you will be able to log in as soon as it is accepted.
          </p>
          <Link
            to="/login"
            className="mt-2 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
          >
            Back to sign in
          </Link>
        </div>
      )}

      {(status === 'error' || status === 'idle') && (
        <div className="space-y-4">
          {status === 'error' ? (
            <div className="flex items-start gap-2 rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700 dark:border-rose-500/30 dark:bg-rose-500/10 dark:text-rose-300">
              <XCircle className="mt-0.5 h-4 w-4 shrink-0" />
              {error}
            </div>
          ) : (
            <div className="flex items-start gap-2 rounded-xl border border-brand-200 bg-brand-50 p-3 text-sm text-brand-700 dark:border-brand-500/30 dark:bg-brand-500/10 dark:text-brand-300">
              <MailOpen className="mt-0.5 h-4 w-4 shrink-0" />
              We sent a verification link to your inbox. Open it within 24 hours to activate your account.
            </div>
          )}
          <form onSubmit={(e) => void onResend(e)} className="space-y-4">
            <div>
              <label className="label" htmlFor="verify-email">
                Email address
              </label>
              <Input
                id="verify-email"
                type="email"
                autoComplete="email"
                required
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <Button type="submit" loading={resending} className="w-full" disabled={cooldown > 0}>
              {cooldown > 0 ? `Resend link in ${cooldown}s` : "Didn't get it? Resend link"}
            </Button>
          </form>
        </div>
      )}
    </AuthShell>
  );
}
