import axios, { AxiosError } from 'axios';

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_BASE_URL as string) || '/api',
  headers: { 'Content-Type': 'application/json' },
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
    const detail = err.response?.data as { detail?: string | { msg?: string }[] } | undefined;
    if (typeof detail?.detail === 'string') return detail.detail;
    if (Array.isArray(detail?.detail)) return detail.detail.map((d) => d.msg ?? '').join(', ');
    if (err.message === 'Network Error') return 'Cannot reach the server. Is the backend running?';
    return err.message;
  }
  return 'Something went wrong';
}

export async function get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  return (await api.get<T>(url, { params })).data;
}
export async function post<T>(url: string, data?: unknown): Promise<T> {
  return (await api.post<T>(url, data)).data;
}
export async function put<T>(url: string, data?: unknown): Promise<T> {
  return (await api.put<T>(url, data)).data;
}
export async function del<T>(url: string): Promise<T> {
  return (await api.delete<T>(url)).data;
}

export default api;
