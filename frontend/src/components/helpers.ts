export interface AttemptLite {
  id: number;
  quiz_id: number;
  score: number;
  total: number;
  correct?: number;
  wrong?: number;
  skipped?: number;
  accuracy?: number | null;
  mode?: string | null;
  xp_awarded?: number;
  created_at?: string | null;
  quiz?: { id?: number; title?: string; topic?: { title?: string } | null } | null;
}

export function toItems<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[];
  if (data && typeof data === 'object') {
    const items = (data as { items?: unknown }).items;
    if (Array.isArray(items)) return items as T[];
  }
  return [];
}

export function formatDate(value?: string | null): string {
  if (!value) return 'â€”';
  const dateOnly = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);
  const d = dateOnly
    ? new Date(Number(dateOnly[1]), Number(dateOnly[2]) - 1, Number(dateOnly[3]))
    : new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

export function formatClock(seconds: number): string {
  const safe = Math.max(0, Math.floor(seconds));
  const h = Math.floor(safe / 3600);
  const m = Math.floor((safe % 3600) / 60);
  const s = safe % 60;
  const pad = (n: number) => String(n).padStart(2, '0');
  return h > 0 ? `${h}:${pad(m)}:${pad(s)}` : `${pad(m)}:${pad(s)}`;
}

export function formatDurationLabel(minutes?: number | null): string {
  if (minutes === null || minutes === undefined) return 'â€”';
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m ? `${h}h ${m}m` : `${h}h`;
}

export function titleCase(value: string): string {
  return value
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function asPercent(value: number): number {
  if (!Number.isFinite(value)) return 0;
  const v = value > 0 && value <= 1 ? value * 100 : value;
  return Math.round(v * 10) / 10;
}

export function formatScore(value: number): string {
  if (!Number.isFinite(value)) return '0';
  return Number.isInteger(value) ? String(value) : value.toFixed(1);
}

export function patternHint(pattern?: Record<string, unknown> | null): string | null {
  if (!pattern) return null;
  const parts: string[] = [];
  for (const [key, value] of Object.entries(pattern)) {
    if (value === null || value === undefined) continue;
    if (typeof value === 'object') continue;
    parts.push(`${titleCase(key)}: ${String(value)}`);
    if (parts.length >= 2) break;
  }
  return parts.length ? parts.join(' Â· ') : null;
}

export function primitiveEntries(data?: Record<string, unknown> | null): [string, unknown][] {
  if (!data) return [];
  return Object.entries(data).filter(([, v]) => v === null || v === undefined || typeof v !== 'object');
}
