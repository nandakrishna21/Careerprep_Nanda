import { FormEvent, useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useSearchParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Button, Input } from '../../components/ui';
import { AuthShell } from '../../components/AuthShell';
import { useAuth } from '../../stores/auth';

const RESEND_WAIT_SECONDS = 60;

export default function VerifyOtp() {
  const [searchParams] = useSearchParams();
  const [email, setEmail] = useState(searchParams.get('email') ?? '');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [cooldown, setCooldown] = useState(0);
  const { verifyOtp, resendOtp, token } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (cooldown <= 0) return;
    const timer = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(timer);
  }, [cooldown]);

  if (token) return <Navigate to="/dashboard" replace />;

  const onVerify = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!email.trim()) {
      toast.error('Enter your email address.');
      return;
    }
    if (otp.trim().length < 4) {
      toast.error('Enter the 6-digit code from your email.');
      return;
    }
    setLoading(true);
    try {
      await verifyOtp(email.trim(), otp.trim());
      toast.success('Email verified - welcome aboard!');
      navigate('/dashboard', { replace: true });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Verification failed.';
      if (message.toLowerCase().includes('already verified')) {
        toast.success('Email already verified - please sign in.');
        navigate('/login', { replace: true });
        return;
      }
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const onResend = async () => {
    if (!email.trim()) {
      toast.error('Enter your email address first.');
      return;
    }
    if (cooldown > 0 || resending) return;
    setResending(true);
    try {
      await resendOtp(email.trim());
      toast.success('A fresh code is on its way to your inbox.');
      setCooldown(RESEND_WAIT_SECONDS);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : 'Unable to resend the code.');
    } finally {
      setResending(false);
    }
  };

  return (
    <AuthShell
      title="Verify your email"
      subtitle="Enter the 6-digit code we sent to your inbox to activate your account."
      footer={
        <>
          Wrong email?{' '}
          <Link to="/register" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Sign up again
          </Link>
        </>
      }
    >
      <form onSubmit={onVerify} className="space-y-4">
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
        <div>
          <label className="label" htmlFor="verify-otp">
            Verification code
          </label>
          <Input
            id="verify-otp"
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            required
            minLength={4}
            maxLength={12}
            placeholder="6-digit code"
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
            className="text-center text-2xl font-bold tracking-[0.5em]"
          />
          <p className="mt-1.5 text-xs text-slate-400">The code expires 10 minutes after it is sent.</p>
        </div>
        <Button type="submit" loading={loading} className="w-full">
          Verify and sign in
        </Button>
        <button
          type="button"
          onClick={() => void onResend()}
          disabled={resending || cooldown > 0}
          className="w-full text-center text-sm font-semibold text-brand-600 hover:underline disabled:cursor-not-allowed disabled:opacity-50 dark:text-brand-400"
        >
          {cooldown > 0 ? `Resend code in ${cooldown}s` : resending ? 'Sending…' : "Didn't get the code? Resend"}
        </button>
      </form>
    </AuthShell>
  );
}
