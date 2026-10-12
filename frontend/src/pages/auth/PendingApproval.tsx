import { Link } from 'react-router-dom';
import { Hourglass } from 'lucide-react';
import { AuthShell } from '../../components/AuthShell';

export default function PendingApproval() {
  return (
    <AuthShell
      title="Account created!"
      subtitle="Your account is awaiting approval by the super admin."
      footer={
        <>
          Approved already?{' '}
          <Link to="/login" className="font-semibold text-brand-600 hover:underline dark:text-brand-400">
            Sign in
          </Link>
        </>
      }
    >
      <div className="flex flex-col items-center gap-3 py-4 text-center">
        <Hourglass className="h-12 w-12 text-amber-500" />
        <p className="max-w-sm text-sm text-slate-500 dark:text-slate-400">
          The super admin has been notified about your signup. You will be able to
          log in as soon as your account is accepted — usually within a day.
        </p>
        <Link
          to="/login"
          className="mt-2 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
        >
          Back to sign in
        </Link>
      </div>
    </AuthShell>
  );
}
