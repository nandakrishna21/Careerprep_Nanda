import { ReactNode } from 'react';
import { Link, To } from 'react-router-dom';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';

const styles: Record<ButtonVariant, string> = {
  primary:
    'bg-brand-600 text-white hover:bg-brand-700 shadow-sm shadow-brand-600/25 disabled:bg-brand-400',
  secondary:
    'bg-slate-800 text-white hover:bg-slate-900 dark:bg-slate-200 dark:text-slate-900 dark:hover:bg-white',
  outline:
    'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800',
  ghost:
    'bg-transparent text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800',
  danger: 'bg-rose-600 text-white hover:bg-rose-700',
};

export function LinkButton({
  to,
  children,
  variant = 'primary',
  className = '',
  title,
}: {
  to: To;
  children: ReactNode;
  variant?: ButtonVariant;
  className?: string;
  title?: string;
}) {
  return (
    <Link
      to={to}
      title={title}
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition ${styles[variant]} ${className}`}
    >
      {children}
    </Link>
  );
}
