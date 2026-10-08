import { Link } from 'react-router-dom';
import { ArrowLeft, Compass, Home } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="mx-auto flex min-h-[60vh] max-w-7xl flex-col items-center justify-center space-y-6 text-center">
      <p className="text-7xl font-black tracking-tight text-brand-600 sm:text-9xl dark:text-brand-400">404</p>
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Page not found</h1>
        <p className="mx-auto max-w-md text-sm text-slate-500 dark:text-slate-400">
          The page you are looking for does not exist or may have been moved. Let's get you back on track.
        </p>
      </div>
      <div className="flex flex-wrap items-center justify-center gap-3">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-brand-600/25 transition hover:bg-brand-700"
        >
          <Compass className="h-4 w-4" /> Back to Dashboard
        </Link>
        <Link
          to="/"
          className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800"
        >
          <Home className="h-4 w-4" /> Home
        </Link>
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800"
        >
          <ArrowLeft className="h-4 w-4" /> Go back
        </Link>
      </div>
    </div>
  );
}
