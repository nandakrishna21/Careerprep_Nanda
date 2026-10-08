import { ReactNode } from 'react';

export function AuthShell({
  title,
  subtitle,
  children,
  footer,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
  footer?: ReactNode;
}) {
  return (
    <div className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-md flex-col justify-center px-4 py-10">
      <div className="mb-6 flex flex-col items-center text-center">
        <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-violet-600 text-xl font-black text-white">
          C
        </span>
        <h1 className="mt-4 text-xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          {title}
        </h1>
        {subtitle && (
          <p className="mt-1.5 text-sm text-slate-500 dark:text-slate-400">{subtitle}</p>
        )}
      </div>
      <div className="card p-6 sm:p-7">{children}</div>
      {footer && (
        <div className="mt-5 text-center text-sm text-slate-500 dark:text-slate-400">{footer}</div>
      )}
    </div>
  );
}
