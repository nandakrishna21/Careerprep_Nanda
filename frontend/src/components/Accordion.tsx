import { ReactNode, useState } from 'react';
import { ChevronDown } from 'lucide-react';

export function AccordionItem({
  title,
  subtitle,
  right,
  open,
  defaultOpen = false,
  onOpenChange,
  children,
  className = '',
}: {
  title: ReactNode;
  subtitle?: ReactNode;
  right?: ReactNode;
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (next: boolean) => void;
  children?: ReactNode;
  className?: string;
}) {
  const [internal, setInternal] = useState(defaultOpen);
  const isControlled = open !== undefined;
  const isOpen = isControlled ? open : internal;

  const toggle = () => {
    const next = !isOpen;
    if (!isControlled) setInternal(next);
    onOpenChange?.(next);
  };

  return (
    <div
      className={`overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 ${className}`}
    >
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={toggle}
          aria-expanded={isOpen}
          className="flex min-w-0 flex-1 items-center gap-3 px-4 py-3.5 text-left transition hover:bg-slate-50 dark:hover:bg-slate-800/60"
        >
          <ChevronDown
            className={`h-4 w-4 shrink-0 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          />
          <span className="min-w-0 flex-1">
            <span className="block truncate text-sm font-semibold text-slate-800 dark:text-slate-100">
              {title}
            </span>
            {subtitle && (
              <span className="mt-0.5 block truncate text-xs text-slate-500 dark:text-slate-400">
                {subtitle}
              </span>
            )}
          </span>
        </button>
        {right && <div className="shrink-0 pr-4">{right}</div>}
      </div>
      {isOpen && (
        <div className="border-t border-slate-100 px-4 py-4 dark:border-slate-800">{children}</div>
      )}
    </div>
  );
}
