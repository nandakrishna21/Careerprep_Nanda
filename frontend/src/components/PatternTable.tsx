import { titleCase } from './helpers';

function cellText(value: unknown): string {
  if (value === null || value === undefined) return 'â€”';
  if (Array.isArray(value)) return value.map((v) => (typeof v === 'object' ? JSON.stringify(v) : String(v))).join(', ');
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function isObjectArray(value: unknown): value is Record<string, unknown>[] {
  return (
    Array.isArray(value) &&
    value.length > 0 &&
    value.every((v) => v !== null && typeof v === 'object' && !Array.isArray(v))
  );
}

function columnsOf(rows: Record<string, unknown>[]): string[] {
  const cols: string[] = [];
  rows.forEach((row) => {
    Object.keys(row).forEach((k) => {
      if (!cols.includes(k)) cols.push(k);
    });
  });
  return cols;
}

export function PatternTable({
  data,
  emptyLabel = 'No information available.',
}: {
  data?: Record<string, unknown> | null;
  emptyLabel?: string;
}) {
  const entries = Object.entries(data ?? {}).filter(([, v]) => v !== null && v !== undefined);
  if (!entries.length) {
    return <p className="text-sm text-slate-500 dark:text-slate-400">{emptyLabel}</p>;
  }

  return (
    <div className="space-y-4">
      {entries.map(([key, value]) => {
        if (isObjectArray(value)) {
          const cols = columnsOf(value);
          return (
            <div key={key} className="overflow-x-auto">
              <p className="mb-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
                {titleCase(key)}
              </p>
              <table className="w-full min-w-[420px] text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400 dark:border-slate-700">
                    {cols.map((col) => (
                      <th key={col} className="py-2 pr-4 font-semibold">
                        {titleCase(col)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {value.map((row, i) => (
                    <tr
                      key={i}
                      className="border-b border-slate-100 text-slate-600 last:border-0 dark:border-slate-800 dark:text-slate-300"
                    >
                      {cols.map((col) => (
                        <td key={col} className="py-2 pr-4">
                          {cellText(row[col])}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        }

        if (Array.isArray(value)) {
          return (
            <div key={key} className="flex flex-col gap-1">
              <span className="text-xs font-bold uppercase tracking-wide text-slate-400">
                {titleCase(key)}
              </span>
              <span className="text-sm text-slate-600 dark:text-slate-300">
                {value.length ? value.map((v) => cellText(v)).join(', ') : 'â€”'}
              </span>
            </div>
          );
        }

        return (
          <div
            key={key}
            className="flex items-start justify-between gap-4 border-b border-dashed border-slate-200 pb-2 text-sm last:border-0 last:pb-0 dark:border-slate-800"
          >
            <span className="font-medium text-slate-500 dark:text-slate-400">{titleCase(key)}</span>
            <span className="text-right font-semibold text-slate-800 dark:text-slate-100">
              {cellText(value)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
