import { create } from 'zustand';
import { get as apiGet, post as apiPost, errorMessage } from '../lib/api';
import type { AuthResponse, Profile, User } from '../lib/types';

interface AuthState {
  token: string | null;
  user: User | null;
  profile: Profile | null;
  hydrated: boolean;
  setSession: (token: string, user: User) => void;
  hydrate: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

export const useAuth = create<AuthState>((set, get) => ({
  token: localStorage.getItem('cp_token'),
  user: null,
  profile: null,
  hydrated: false,

  setSession: (token, user) => {
    localStorage.setItem('cp_token', token);
    set({ token, user });
  },

  hydrate: async () => {
    const token = get().token;
    if (!token) {
      set({ hydrated: true });
      return;
    }
    try {
      const data = await apiGet<{ user: User; profile: Profile }>('/auth/me');
      set({ user: data.user, profile: data.profile, hydrated: true });
    } catch {
      localStorage.removeItem('cp_token');
      set({ token: null, user: null, profile: null, hydrated: true });
    }
  },

  login: async (email, password) => {
    try {
      const data = await apiPost<AuthResponse>('/auth/login', { email, password });
      get().setSession(data.access_token, data.user);
      await get().hydrate();
    } catch (err) {
      throw new Error(errorMessage(err));
    }
  },

  register: async (full_name, email, password) => {
    try {
      const data = await apiPost<AuthResponse>('/auth/register', { full_name, email, password });
      get().setSession(data.access_token, data.user);
      await get().hydrate();
    } catch (err) {
      throw new Error(errorMessage(err));
    }
  },

  logout: () => {
    localStorage.removeItem('cp_token');
    set({ token: null, user: null, profile: null });
  },

  refreshProfile: async () => {
    if (!get().token) return;
    try {
      const data = await apiGet<{ user: User; profile: Profile }>('/auth/me');
      set({ user: data.user, profile: data.profile });
    } catch {
      /* ignore */
    }
  },
}));
