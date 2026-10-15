import axios, { AxiosError } from 'axios';

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_BASE_URL as string) || '/api',
  headers: { 'Content-Type': 'application/json' },
  // Free-tier backends sleep: fail fast with a clear message instead of an
  // endless spinner, so get() can retry once (usually the wake-up call).
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cp_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    const url = error.config?.url ?? '';
    if (error.response?.status === 401 && !url.includes('/auth/login') && !url.includes('/auth/register')) {
      localStorage.removeItem('cp_token');
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export function errorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    if (err.code === 'ECONNABORTED')
      return 'Server is waking up (free tier sleeps when idle) — please retry in a few seconds.';
    const detail = err.response?.data as { detail?: string | { msg?: string }[] } | undefined;
    if (typeof detail?.detail === 'string') return detail.detail;
    if (Array.isArray(detail?.detail)) return detail.detail.map((d) => d.msg ?? '').join(', ');
    if (err.message === 'Network Error') return 'Cannot reach the server. Is the backend running?';
    return err.message;
  }
  return 'Something went wrong';
}

// ---------------------------------------------------------------------------
// Tiny stale-while-instant GET cache: hopping between left-panel sections
// reuses data fetched <45s ago instead of refetching + flashing spinners.
// Mutations invalidate their section below, so edits never show stale data.
// ---------------------------------------------------------------------------

const SWR_TTL_MS = 45_000;
// Auth identity must stay live (401 handling depends on it) — never cache it.
const NO_CACHE_PREFIXES = ['/auth/me'];

const swr = new Map<string, { at: number; data: unknown }>();

function swrKey(url: string, params?: Record<string, unknown>): string {
  if (!params) return url;
  const sorted = Object.keys(params)
    .filter((k) => params[k] !== undefined)
    .sort()
    .map((k) => `${k}=${JSON.stringify(params[k])}`);
  return sorted.length ? `${url}?${sorted.join('&')}` : url;
}

function cacheable(url: string): boolean {
  return !NO_CACHE_PREFIXES.some((p) => url === p || url.startsWith(`${p}/`));
}

export function invalidateCache(urlOrPrefix?: string): void {
  if (!urlOrPrefix) {
    swr.clear();
    return;
  }
  const segment = `/${urlOrPrefix.split('/').filter(Boolean)[0] ?? ''}`;
  for (const key of swr.keys()) {
    if (key === urlOrPrefix || key.startsWith(`${segment}/`) || key.startsWith(`${segment}?`) || key === segment) {
      swr.delete(key);
    }
  }
}

function shouldRetry(err: unknown, signal?: AbortSignal): boolean {
  if (signal?.aborted) return false;
  if (!axios.isAxiosError(err)) return false;
  // No response at all (cold start / sleep / dropped connection) or timeout —
  // safe to retry once for idempotent GETs.
  return !err.response || err.code === 'ECONNABORTED';
}

export async function get<T>(
  url: string,
  params?: Record<string, unknown>,
  opts?: { signal?: AbortSignal },
): Promise<T> {
  const key = swrKey(url, params);
  if (cacheable(url)) {
    const hit = swr.get(key);
    if (hit && Date.now() - hit.at < SWR_TTL_MS) return hit.data as T;
  }
  try {
    const data = (await api.get<T>(url, { params, signal: opts?.signal })).data;
    if (cacheable(url) && !opts?.signal?.aborted) swr.set(key, { at: Date.now(), data });
    return data;
  } catch (err) {
    if (shouldRetry(err, opts?.signal)) {
      // One retry: the first call often just wakes the sleeping backend.
      const data = (await api.get<T>(url, { params, signal: opts?.signal })).data;
      if (cacheable(url) && !opts?.signal?.aborted) swr.set(key, { at: Date.now(), data });
      return data;
    }
    throw err;
  }
}
export async function post<T>(url: string, data?: unknown): Promise<T> {
  const res = (await api.post<T>(url, data)).data;
  invalidateCache(url);
  return res;
}
export async function put<T>(url: string, data?: unknown): Promise<T> {
  const res = (await api.put<T>(url, data)).data;
  invalidateCache(url);
  return res;
}
export async function del<T>(url: string): Promise<T> {
  const res = (await api.delete<T>(url)).data;
  invalidateCache(url);
  return res;
}

export default api;
